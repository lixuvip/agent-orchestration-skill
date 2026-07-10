#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


SKILL_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install one Codex skill with provenance, staged replacement, and rollback."
    )
    parser.add_argument("--source-dir", help="Skill source directory. Required unless --restore is used.")
    parser.add_argument("--target-root", required=True, help="Codex skills root directory.")
    parser.add_argument("--skill-name", required=True, help="Skill directory name.")
    parser.add_argument("--source-commit", default="unknown", help="Source git commit.")
    parser.add_argument("--source-dirty", action="store_true", help="Mark the source skill as dirty.")
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Explicitly allow installing a dirty development source.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and print the planned action.")
    parser.add_argument("--restore", action="store_true", help="Swap the current and previous installs.")
    return parser.parse_args()


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def reject_symlinks(root: Path) -> None:
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"source skill contains a symlink: {path.relative_to(root)}")


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def paths_for(target_root: Path, skill_name: str) -> dict[str, Path]:
    return {
        "target": target_root / skill_name,
        "previous": target_root / f".{skill_name}.previous",
        "manifest": target_root / f".{skill_name}.install-manifest.json",
        "previous_manifest": target_root / f".{skill_name}.previous-manifest.json",
    }


def validate_name(skill_name: str) -> None:
    if not SKILL_NAME_RE.fullmatch(skill_name):
        raise ValueError("skill-name must use lowercase letters, digits, and hyphens")


def install(args: argparse.Namespace) -> None:
    if not args.source_dir:
        raise ValueError("--source-dir is required unless --restore is used")
    if args.source_dirty and not args.allow_dirty:
        raise ValueError("dirty source refused; pass --allow-dirty for an explicit development install")

    source_dir = Path(args.source_dir).expanduser().resolve()
    target_root = Path(args.target_root).expanduser().resolve()
    if not source_dir.is_dir() or not (source_dir / "SKILL.md").is_file():
        raise ValueError(f"invalid skill source: {source_dir}")
    reject_symlinks(source_dir)

    target_root.mkdir(parents=True, exist_ok=True)
    paths = paths_for(target_root, args.skill_name)
    try:
        paths["target"].relative_to(source_dir)
    except ValueError:
        pass
    else:
        raise ValueError("target directory must not be inside the source skill")

    source_hash = tree_sha256(source_dir)
    manifest_data = {
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "skill_name": args.skill_name,
        "source_commit": args.source_commit,
        "source_dirty": bool(args.source_dirty),
        "source_path": str(source_dir),
        "source_tree_sha256": source_hash,
    }

    if args.dry_run:
        print("INSTALL_WOULD_COMPLETE")
        print(json.dumps(manifest_data, ensure_ascii=False, sort_keys=True))
        return

    stage_root = Path(tempfile.mkdtemp(prefix=f".{args.skill_name}.stage-", dir=target_root))
    stage_target = stage_root / args.skill_name
    stage_manifest = stage_root / "install-manifest.json"
    target_moved = False
    manifest_moved = False
    try:
        shutil.copytree(source_dir, stage_target)
        staged_hash = tree_sha256(stage_target)
        if staged_hash != source_hash:
            raise RuntimeError("staged skill hash does not match source hash")
        stage_manifest.write_text(
            json.dumps(manifest_data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        remove_path(paths["previous"])
        remove_path(paths["previous_manifest"])
        if paths["target"].exists() or paths["target"].is_symlink():
            os.replace(paths["target"], paths["previous"])
            target_moved = True
        if paths["manifest"].exists() or paths["manifest"].is_symlink():
            os.replace(paths["manifest"], paths["previous_manifest"])
            manifest_moved = True

        os.replace(stage_target, paths["target"])
        os.replace(stage_manifest, paths["manifest"])
    except Exception:
        if paths["target"].exists() or paths["target"].is_symlink():
            remove_path(paths["target"])
        if target_moved and paths["previous"].exists():
            os.replace(paths["previous"], paths["target"])
        if paths["manifest"].exists() or paths["manifest"].is_symlink():
            remove_path(paths["manifest"])
        if manifest_moved and paths["previous_manifest"].exists():
            os.replace(paths["previous_manifest"], paths["manifest"])
        raise
    finally:
        remove_path(stage_root)

    print(
        "INSTALL_COMPLETE "
        f"target={paths['target']} manifest={paths['manifest']} "
        f"source_commit={args.source_commit} source_dirty={str(bool(args.source_dirty)).lower()} "
        f"tree_sha256={source_hash}"
    )


def restore(args: argparse.Namespace) -> None:
    target_root = Path(args.target_root).expanduser().resolve()
    paths = paths_for(target_root, args.skill_name)
    if not paths["previous"].exists():
        raise ValueError(f"no previous installation exists for {args.skill_name}")
    if args.dry_run:
        print(f"INSTALL_WOULD_RESTORE target={paths['target']} previous={paths['previous']}")
        return

    swap = target_root / f".{args.skill_name}.restore-swap-{uuid4().hex}"
    manifest_swap = target_root / f".{args.skill_name}.manifest-swap-{uuid4().hex}"
    try:
        if paths["target"].exists() or paths["target"].is_symlink():
            os.replace(paths["target"], swap)
        os.replace(paths["previous"], paths["target"])
        if swap.exists() or swap.is_symlink():
            os.replace(swap, paths["previous"])

        if paths["manifest"].exists() or paths["manifest"].is_symlink():
            os.replace(paths["manifest"], manifest_swap)
        if paths["previous_manifest"].exists() or paths["previous_manifest"].is_symlink():
            os.replace(paths["previous_manifest"], paths["manifest"])
        if manifest_swap.exists() or manifest_swap.is_symlink():
            os.replace(manifest_swap, paths["previous_manifest"])
    except Exception:
        if not paths["target"].exists() and swap.exists():
            os.replace(swap, paths["target"])
        if not paths["manifest"].exists() and manifest_swap.exists():
            os.replace(manifest_swap, paths["manifest"])
        raise

    print(f"INSTALL_RESTORED target={paths['target']} previous={paths['previous']}")


def main() -> int:
    args = parse_args()
    try:
        validate_name(args.skill_name)
        if args.restore:
            restore(args)
        else:
            install(args)
    except Exception as exc:
        print(f"INSTALL_FAILED {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
