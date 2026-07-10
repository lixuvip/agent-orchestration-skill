#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path


START_MARKER = "<!-- agent-orchestration:agy-gemini-review:start -->"
END_MARKER = "<!-- agent-orchestration:agy-gemini-review:end -->"

SNIPPET = f"""\
{START_MARKER}
## Codex Agy/Gemini External Review And Research

- When a Codex thread in this repo is asked to use `agy`, `Gemini`, `Antigravity`, or an external model for review or research, immediately use the installed `$agent-orchestration` skill before running shell commands.
- Use `python3 ~/.codex/skills/agent-orchestration/scripts/run_agy_print.py` for every `agy --print` external review or research call so the prompt is passed immediately after `--print`.
- In this workflow, `Gemini` always means a Gemini model invoked through local `agy`. Do not invoke the standalone `gemini` CLI as a substitute execution surface.
- Capability discovery for this workflow is `command -v agy` and `agy models` only. Do not use `command -v gemini`, `gemini --version`, or `gemini --help`.
- Wrong first moves to avoid: do not probe standalone `gemini` CLI, do not open `gemini` auth/login flows, do not modify repository guidance merely to prepare a read-only pass, and do not expand context silently.
- For diff-only work, attach no repository. When source context is required, build an allowlisted directory with `build_agy_context_bundle.py` and pass that directory through `--add-dir`. Whole-repository disclosure requires explicit approval.
- If `agy` exits 0 but prints no stdout, treat that run as failed. Zero-byte stdout is not a successful review or research pass.
- For health checks, use `--expect-substring "READY"`. For structured review or research prompts, keep `--expect-substring` as the default parser guard. Add `--expect-first-line "AGY_REVIEW_V2"` / `--expect-first-line "AGY_RESEARCH_V1"` only when you explicitly want a stricter machine-parseable check and have verified that the chosen model actually emits the schema token on the first non-empty line.
- If invoking `agy` manually, the valid source-backed shape is `agy --add-dir "<ALLOWLISTED_CONTEXT>" --print "<PROMPT>" --model "<MODEL>" --sandbox`; never put `--model` or other flags between `--print` and the prompt.
- If a process accidentally opens the standalone `gemini` CLI or reports a `403` from that CLI, classify it as `WRONG_EXECUTION_SURFACE`, not as a model-quality problem, and rerun the task through `agy`.
- Keep external passes read-only: do not use `--mode accept-edits`, do not use `--dangerously-skip-permissions`, and do not ask agy to modify files.
- Do not claim tests, builds, commands, or current external facts are verified unless their exact evidence is included in the prompt context.
- Keep quality logs outside the repository by default. `append_agy_review_quality_log.py` writes to the Codex external-review ledger unless a project-local log was explicitly authorized.
{END_MARKER}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ensure target AGENTS.md contains stable agy/Gemini external-task guidance."
    )
    parser.add_argument("--project-root", required=True, help="Target repository/project root.")
    parser.add_argument(
        "--agents-file",
        help="Optional AGENTS.md path. Defaults to <project-root>/AGENTS.md.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview the explicit write without changing files.")
    parser.add_argument("--check", action="store_true", help="Check only. This is also the default behavior.")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Explicitly write or refresh stable guidance in the target repository.",
    )
    return parser.parse_args()


def ensure_trailing_newline(text: str) -> str:
    if not text:
        return ""
    return text if text.endswith("\n") else text + "\n"


def replace_existing_guidance(existing: str) -> tuple[str, bool]:
    start_count = existing.count(START_MARKER)
    end_count = existing.count(END_MARKER)
    if start_count != end_count or start_count > 1:
        raise ValueError("guidance markers are missing, duplicated, or unbalanced")
    start = existing.find(START_MARKER)
    end = existing.find(END_MARKER)
    if start == -1 or end == -1:
        updated = ensure_trailing_newline(existing)
        if updated:
            updated += "\n"
        updated += SNIPPET
        return updated, False

    if end < start:
        raise ValueError("guidance markers are out of order")
    end += len(END_MARKER)
    if end < len(existing) and existing[end:end + 1] == "\n":
        end += 1
    updated = existing[:start] + SNIPPET
    if end < len(existing):
        updated += existing[end:]
    return ensure_trailing_newline(updated), True


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise ValueError("refusing to replace a symlinked AGENTS.md")
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        temp_path.chmod(mode)
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def main() -> int:
    args = parse_args()
    try:
        project_root = Path(args.project_root).expanduser().resolve()
        if not project_root.is_dir():
            raise ValueError(f"project root is not a directory: {project_root}")
        raw_agents_path = (
            Path(args.agents_file).expanduser() if args.agents_file else project_root / "AGENTS.md"
        )
        candidate = raw_agents_path if raw_agents_path.is_absolute() else project_root / raw_agents_path
        if candidate.is_symlink():
            raise ValueError("refusing to use a symlinked AGENTS.md")
        agents_path = candidate.resolve()
        if not is_within(agents_path, project_root):
            raise ValueError("agents-file must remain inside project-root")

        existing = agents_path.read_text(encoding="utf-8") if agents_path.exists() else ""
        has_guidance = START_MARKER in existing and END_MARKER in existing
        updated, had_existing_block = replace_existing_guidance(existing)
        is_current = ensure_trailing_newline(existing) == updated

        if is_current:
            print(f"AGENTS_GUIDANCE_PRESENT {agents_path}")
            return 0
        if args.dry_run:
            action = (
                "AGENTS_GUIDANCE_WOULD_UPDATE"
                if had_existing_block
                else "AGENTS_GUIDANCE_WOULD_WRITE"
            )
            print(f"{action} {agents_path}")
            print(SNIPPET)
            return 0
        if not args.write:
            state = "AGENTS_GUIDANCE_STALE" if has_guidance else "AGENTS_GUIDANCE_MISSING"
            print(f"{state} {agents_path}")
            return 1

        atomic_write(agents_path, updated)
    except (OSError, ValueError) as exc:
        print(f"AGENTS_GUIDANCE_NOT_WRITTEN {exc}", file=sys.stderr)
        return 2

    print(f"AGENTS_GUIDANCE_WRITTEN {agents_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
