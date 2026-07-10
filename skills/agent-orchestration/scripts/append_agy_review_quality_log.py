#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


DEFAULT_RELATIVE_LOG = Path(".codex") / "agent-orchestration" / "agy-review-quality.jsonl"
TASK_TYPES = {"review", "research"}

LIST_FIELDS = [
    "strong_points",
    "weak_points",
    "unsupported_claims",
    "scope_drift",
    "omissions",
    "accepted_findings",
    "rejected_findings",
    "needs_human_check",
    "agreed_points",
    "external_only_points",
    "codex_only_points",
    "valuable_takeaways",
    "follow_up_questions",
    "coordinator_notes",
    "template_tuning_suggestions",
]

SENSITIVE_KEY_RE = re.compile(
    r"(secret|token|cookie|credential|password|private[_-]?key|full[_-]?diff|raw[_-]?diff)",
    re.IGNORECASE,
)
SENSITIVE_VALUE_RE = re.compile(
    r"(-----BEGIN [A-Z ]*PRIVATE KEY-----|sk-[A-Za-z0-9_-]{16,}|xox[baprs]-[A-Za-z0-9-]{16,}|AKIA[0-9A-Z]{16})"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append one sanitized agy/Gemini external-task quality entry to a project JSONL log."
    )
    parser.add_argument("--project-root", required=True, help="Target repository/project root.")
    parser.add_argument(
        "--log-path",
        help="Optional explicit log path. Defaults to <project-root>/.codex/agent-orchestration/agy-review-quality.jsonl.",
    )
    parser.add_argument("--entry-file", help="JSON object file to append. Defaults to stdin.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print the normalized JSON without writing.")
    return parser.parse_args()


def load_entry(args: argparse.Namespace) -> dict[str, Any]:
    if args.entry_file:
        raw = Path(args.entry_file).read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()

    if not raw.strip():
        raise ValueError("entry JSON is empty")

    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("entry JSON must be an object")
    return data


def iter_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(iter_values(item))
        return result
    if isinstance(value, dict):
        result = []
        for nested in value.values():
            result.extend(iter_values(nested))
        return result
    return []


def reject_sensitive_content(entry: dict[str, Any]) -> None:
    for key in entry:
        if SENSITIVE_KEY_RE.search(str(key)):
            raise ValueError(f"refusing to log sensitive or oversized field: {key}")

    for value in iter_values(entry):
        if SENSITIVE_VALUE_RE.search(value):
            raise ValueError("refusing to log value that looks like a secret")


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def normalize_entry(entry: dict[str, Any], project_root: Path) -> dict[str, Any]:
    normalized = dict(entry)
    normalized.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    normalized.setdefault("repository", str(project_root))
    normalized.setdefault("review_id", f"agy-task-{uuid4().hex[:12]}")
    task_type = str(normalized.get("task_type") or "review").strip().lower()
    if task_type not in TASK_TYPES:
        raise ValueError("task_type must be one of: review, research")
    normalized["task_type"] = task_type

    score = normalized.get("quality_score")
    if score == "":
        score = None
    if score is not None:
        try:
            score = int(score)
        except (TypeError, ValueError) as exc:
            raise ValueError("quality_score must be an integer from 1 to 5 or null") from exc
        if score < 1 or score > 5:
            raise ValueError("quality_score must be an integer from 1 to 5 or null")
    normalized["quality_score"] = score

    for field in LIST_FIELDS:
        normalized[field] = normalize_list(normalized.get(field))

    return normalized


def compact_json(entry: dict[str, Any]) -> str:
    return json.dumps(entry, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    log_path = Path(args.log_path).expanduser() if args.log_path else project_root / DEFAULT_RELATIVE_LOG
    if not log_path.is_absolute():
        log_path = project_root / log_path

    try:
        entry = load_entry(args)
        reject_sensitive_content(entry)
        normalized = normalize_entry(entry, project_root)
        reject_sensitive_content(normalized)
    except Exception as exc:
        print(f"LOG_NOT_WRITTEN {exc}", file=sys.stderr)
        return 2

    line = compact_json(normalized)
    if args.dry_run:
        print(line)
        return 0

    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except OSError as exc:
        print(f"LOG_NOT_WRITTEN {exc}", file=sys.stderr)
        return 1

    print(f"LOG_WRITTEN {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
