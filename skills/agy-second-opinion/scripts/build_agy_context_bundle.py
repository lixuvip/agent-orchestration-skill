#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


DEFAULT_MAX_BYTES = 2 * 1024 * 1024
MAX_BYTES = 10 * 1024 * 1024
BLOCKED_NAMES = {
    ".env",
    ".git",
    ".npmrc",
    ".pypirc",
    "credentials",
    "credentials.json",
    "id_rsa",
    "id_ed25519",
    "secrets",
    "secrets.json",
}
BLOCKED_SUFFIXES = {".key", ".p12", ".pem", ".pfx"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an allowlisted, read-only source bundle for agy review or research."
    )
    parser.add_argument("--project-root", required=True, help="Target project root.")
    parser.add_argument("--output-dir", required=True, help="New bundle directory to create.")
    parser.add_argument(
        "--include",
        action="append",
        required=True,
        help="Relative file or directory to include. Repeat as needed.",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=DEFAULT_MAX_BYTES,
        help=f"Maximum total source bytes. Default: {DEFAULT_MAX_BYTES}.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and print the manifest only.")
    return parser.parse_args()


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def blocked(path: Path) -> bool:
    lowered_parts = [part.lower() for part in path.parts]
    if any(part in BLOCKED_NAMES or part.startswith(".env.") for part in lowered_parts):
        return True
    return path.suffix.lower() in BLOCKED_SUFFIXES


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def collect_files(project_root: Path, includes: list[str]) -> list[Path]:
    files: dict[str, Path] = {}
    for raw in includes:
        relative = Path(raw)
        if relative.is_absolute():
            raise ValueError(f"include must be relative: {raw}")
        candidate_unresolved = project_root / relative
        if candidate_unresolved.is_symlink():
            raise ValueError(f"refusing to include symlink: {raw}")
        candidate = candidate_unresolved.resolve()
        if not is_within(candidate, project_root):
            raise ValueError(f"include escapes project root: {raw}")
        if not candidate.exists():
            raise ValueError(f"include does not exist: {raw}")
        candidates = [candidate] if candidate.is_file() else sorted(candidate.rglob("*"))
        for path in candidates:
            if path.is_symlink():
                raise ValueError(f"refusing to include symlink: {path.relative_to(project_root)}")
            if not path.is_file():
                continue
            resolved = path.resolve()
            if not is_within(resolved, project_root):
                raise ValueError(f"included file escapes project root: {path}")
            relative_path = resolved.relative_to(project_root)
            if blocked(relative_path):
                raise ValueError(f"refusing to include sensitive path: {relative_path}")
            files[relative_path.as_posix()] = resolved
    return [files[key] for key in sorted(files)]


def build_manifest(project_root: Path, files: list[Path], max_bytes: int) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    total = 0
    for path in files:
        size = path.stat().st_size
        total += size
        if total > max_bytes:
            raise ValueError(f"bundle exceeds max-bytes limit: {max_bytes}")
        entries.append(
            {
                "path": path.relative_to(project_root).as_posix(),
                "sha256": digest(path),
                "size": size,
            }
        )
    if not entries:
        raise ValueError("bundle contains no files")
    return {
        "bundle_schema": "agy-context-v1",
        "project_name": project_root.name,
        "project_root_sha256": hashlib.sha256(str(project_root).encode("utf-8")).hexdigest(),
        "total_bytes": total,
        "files": entries,
    }


def write_bundle(project_root: Path, output_dir: Path, files: list[Path], manifest: dict[str, Any]) -> None:
    if output_dir.exists() or output_dir.is_symlink():
        raise ValueError(f"output-dir already exists: {output_dir}")
    output_parent = output_dir.parent.resolve()
    output_parent.mkdir(parents=True, exist_ok=True)
    if is_within(output_dir.resolve(), project_root):
        raise ValueError("output-dir must be outside project-root")

    stage = Path(tempfile.mkdtemp(prefix=".agy-context-stage-", dir=output_parent))
    try:
        for source in files:
            relative = source.relative_to(project_root)
            destination = stage / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            destination.chmod(destination.stat().st_mode & 0o555)
        (stage / ".agy-context-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.replace(stage, output_dir)
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def main() -> int:
    args = parse_args()
    try:
        if args.max_bytes <= 0 or args.max_bytes > MAX_BYTES:
            raise ValueError(f"max-bytes must be between 1 and {MAX_BYTES}")
        project_root = Path(args.project_root).expanduser().resolve()
        if not project_root.is_dir():
            raise ValueError(f"project root is not a directory: {project_root}")
        output_dir = Path(args.output_dir).expanduser()
        output_dir = output_dir if output_dir.is_absolute() else Path.cwd() / output_dir
        files = collect_files(project_root, args.include)
        manifest = build_manifest(project_root, files, args.max_bytes)
        if args.dry_run:
            print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
            return 0
        write_bundle(project_root, output_dir, files, manifest)
    except (OSError, ValueError) as exc:
        print(f"AGY_CONTEXT_NOT_WRITTEN {exc}", file=sys.stderr)
        return 2

    print(f"AGY_CONTEXT_WRITTEN {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
