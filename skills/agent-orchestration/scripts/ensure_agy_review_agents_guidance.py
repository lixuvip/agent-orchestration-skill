#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


START_MARKER = "<!-- agent-orchestration:agy-gemini-review:start -->"
END_MARKER = "<!-- agent-orchestration:agy-gemini-review:end -->"

SNIPPET = f"""\
{START_MARKER}
## Codex Agy/Gemini External Review And Research

- When a Codex thread in this repo is asked to use `agy`, `Gemini`, `Antigravity`, or an external model for review or research, immediately use the installed `$agent-orchestration` skill before running shell commands.
- If this checkout does not already contain this block and writes are allowed, run `python3 ~/.codex/skills/agent-orchestration/scripts/ensure_agy_review_agents_guidance.py --project-root "$PWD"` before any `agy` health check or model discovery. The workflow is not ready until it prints `AGENTS_GUIDANCE_PRESENT` or `AGENTS_GUIDANCE_WRITTEN`.
- Use `python3 ~/.codex/skills/agent-orchestration/scripts/run_agy_print.py` for every `agy --print` external review or research call so the prompt is passed immediately after `--print`.
- In this workflow, `Gemini` always means a Gemini model invoked through local `agy`. Do not invoke the standalone `gemini` CLI as a substitute execution surface.
- Capability discovery for this workflow is `command -v agy` and `agy models` only. Do not use `command -v gemini`, `gemini --version`, or `gemini --help`.
- Wrong first moves to avoid: do not probe standalone `gemini` CLI, do not open `gemini` auth/login flows, do not treat a missing repo attachment as a model-quality failure, and do not continue the external path after the guidance gate fails.
- When the target repository is not already the active agy project, attach it explicitly with `--add-dir "$PWD"` from the repo root or `--add-dir "/absolute/path/to/repo"`; otherwise `agy --print` may inspect the scratch workspace instead of project files.
- If `agy` exits 0 but prints no stdout, treat that run as failed. Zero-byte stdout is not a successful review or research pass.
- For health checks, use `--expect-substring "READY"`. For structured review or research prompts, keep `--expect-substring` as the default parser guard. Add `--expect-first-line "AGY_REVIEW_V2"` / `--expect-first-line "AGY_RESEARCH_V1"` only when you explicitly want a stricter machine-parseable check and have verified that the chosen model actually emits the schema token on the first non-empty line.
- If invoking `agy` manually, the valid repo-review or repo-research shape is `agy --add-dir "$PWD" --print "<PROMPT>" --model "<MODEL>" --sandbox`; never put `--model` or other flags between `--print` and the prompt.
- If a process accidentally opens the standalone `gemini` CLI or reports a `403` from that CLI, classify it as `WRONG_EXECUTION_SURFACE`, not as a model-quality problem, and rerun the task through `agy`.
- Keep external passes read-only: do not use `--mode accept-edits`, do not use `--dangerously-skip-permissions`, and do not ask agy to modify files.
- Do not claim tests, builds, commands, or current external facts are verified unless their exact evidence is included in the prompt context.
- After each external review or research pass, run `python3 ~/.codex/skills/agent-orchestration/scripts/append_agy_review_quality_log.py --project-root "$PWD"` and set `task_type` to `review` or `research`; only claim the quality log was written when stdout contains `LOG_WRITTEN`.
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
    parser.add_argument("--dry-run", action="store_true", help="Print the action without writing.")
    parser.add_argument("--check", action="store_true", help="Exit 0 if guidance exists, 1 otherwise.")
    return parser.parse_args()


def ensure_trailing_newline(text: str) -> str:
    if not text:
        return ""
    return text if text.endswith("\n") else text + "\n"


def replace_existing_guidance(existing: str) -> tuple[str, bool]:
    start = existing.find(START_MARKER)
    end = existing.find(END_MARKER)
    if start == -1 or end == -1:
        updated = ensure_trailing_newline(existing)
        if updated:
            updated += "\n"
        updated += SNIPPET
        return updated, False

    end += len(END_MARKER)
    if end < len(existing) and existing[end:end + 1] == "\n":
        end += 1
    updated = existing[:start] + SNIPPET
    if end < len(existing):
        updated += existing[end:]
    return ensure_trailing_newline(updated), True


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    agents_path = Path(args.agents_file).expanduser() if args.agents_file else project_root / "AGENTS.md"
    if not agents_path.is_absolute():
        agents_path = project_root / agents_path

    existing = agents_path.read_text(encoding="utf-8") if agents_path.exists() else ""
    has_guidance = START_MARKER in existing and END_MARKER in existing
    updated, had_existing_block = replace_existing_guidance(existing)
    is_current = ensure_trailing_newline(existing) == updated

    if args.check:
        if is_current:
            print(f"AGENTS_GUIDANCE_PRESENT {agents_path}")
            return 0
        if has_guidance:
            print(f"AGENTS_GUIDANCE_STALE {agents_path}")
            return 1
        print(f"AGENTS_GUIDANCE_MISSING {agents_path}")
        return 1

    if is_current:
        print(f"AGENTS_GUIDANCE_PRESENT {agents_path}")
        return 0

    if args.dry_run:
        action = "AGENTS_GUIDANCE_WOULD_UPDATE" if had_existing_block else "AGENTS_GUIDANCE_WOULD_WRITE"
        print(f"{action} {agents_path}")
        print(SNIPPET)
        return 0

    try:
        agents_path.parent.mkdir(parents=True, exist_ok=True)
        agents_path.write_text(updated, encoding="utf-8")
    except OSError as exc:
        print(f"AGENTS_GUIDANCE_NOT_WRITTEN {exc}", file=sys.stderr)
        return 2

    print(f"AGENTS_GUIDANCE_WRITTEN {agents_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
