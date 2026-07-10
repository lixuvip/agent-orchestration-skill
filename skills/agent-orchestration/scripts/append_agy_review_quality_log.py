#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


LEDGER_DIRECTORY = "external-review-ledger"
TASK_TYPES = {"review", "research"}
MAX_INPUT_BYTES = 64 * 1024
MAX_LOG_BYTES = 128 * 1024
MAX_TEXT_LENGTH = 4_000

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
REQUIRED_FIELDS = {"project", "model", "mode", "timeout", "scope", "status"}
OPTIONAL_FIELDS = {
    "timestamp",
    "repository",
    "review_id",
    "task_type",
    "context_summary",
    "quality_score",
    "command_shape",
    "repo_attached",
    "template_version",
    "output_schema",
    "duration_ms",
    "exit_code",
    "failure_state",
    "thread_id",
    "coordinator_thread_id",
    "diff_summary",
}
ALLOWED_FIELDS = REQUIRED_FIELDS | OPTIONAL_FIELDS | set(LIST_FIELDS)

SENSITIVE_KEY_RE = re.compile(
    r"(secret|token|cookie|credential|password|private[_-]?key|full[_-]?diff|raw[_-]?diff)",
    re.IGNORECASE,
)
SENSITIVE_VALUE_RE = re.compile(
    r"(-----BEGIN [A-Z ]*PRIVATE KEY-----|sk-[A-Za-z0-9_-]{16,}|xox[baprs]-[A-Za-z0-9-]{16,}|AKIA[0-9A-Z]{16})"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append one sanitized agy/Gemini external-task quality entry to a Codex ledger."
    )
    parser.add_argument("--project-root", required=True, help="Target repository/project root.")
    parser.add_argument(
        "--log-path",
        help="Optional log path. Project-local paths require --allow-project-write.",
    )
    parser.add_argument(
        "--allow-project-write",
        action="store_true",
        help="Explicitly allow the log path to be inside project-root.",
    )
    parser.add_argument("--entry-file", help="JSON object file to append. Defaults to stdin.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print the normalized JSON without writing.")
    return parser.parse_args()


def load_entry(args: argparse.Namespace) -> dict[str, Any]:
    if args.entry_file:
        raw = Path(args.entry_file).read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()

    if len(raw.encode("utf-8")) > MAX_INPUT_BYTES:
        raise ValueError(f"entry JSON exceeds {MAX_INPUT_BYTES} bytes")
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


def iter_keys(value: Any) -> list[str]:
    if isinstance(value, dict):
        result: list[str] = []
        for key, nested in value.items():
            result.append(str(key))
            result.extend(iter_keys(nested))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(iter_keys(item))
        return result
    return []


def reject_sensitive_content(entry: dict[str, Any]) -> None:
    for key in iter_keys(entry):
        if SENSITIVE_KEY_RE.search(str(key)):
            raise ValueError(f"refusing to log sensitive or oversized field: {key}")

    for value in iter_values(entry):
        if len(value) > MAX_TEXT_LENGTH:
            raise ValueError(f"refusing to log text longer than {MAX_TEXT_LENGTH} characters")
        if SENSITIVE_VALUE_RE.search(value):
            raise ValueError("refusing to log value that looks like a secret")


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        if any(not isinstance(item, str) for item in value):
            raise ValueError("quality-log list fields must contain strings only")
        return [item for item in value if item.strip()]
    text = str(value).strip()
    return [text] if text else []


def normalize_entry(entry: dict[str, Any], project_root: Path) -> dict[str, Any]:
    unknown_fields = sorted(set(entry) - ALLOWED_FIELDS)
    if unknown_fields:
        raise ValueError(f"unsupported quality-log fields: {', '.join(unknown_fields)}")
    missing_fields = sorted(field for field in REQUIRED_FIELDS if not str(entry.get(field, "")).strip())
    if missing_fields:
        raise ValueError(f"missing required quality-log fields: {', '.join(missing_fields)}")

    normalized = dict(entry)
    normalized.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    normalized["repository"] = str(project_root)
    normalized.setdefault("review_id", f"agy-task-{uuid4().hex[:12]}")
    review_id = str(normalized["review_id"])
    if not re.fullmatch(r"[A-Za-z0-9._:-]{1,128}", review_id):
        raise ValueError("review_id contains unsupported characters or is too long")
    normalized["review_id"] = review_id
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


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def ledger_root() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser()
    return (codex_home / LEDGER_DIRECTORY).resolve()


def default_log_path(project_root: Path, root: Path) -> Path:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", project_root.name).strip("-") or "project"
    fingerprint = hashlib.sha256(str(project_root).encode("utf-8")).hexdigest()[:12]
    return root / f"{slug}-{fingerprint}" / "agy-review-quality.jsonl"


def select_log_path(args: argparse.Namespace, project_root: Path) -> Path:
    root = ledger_root()
    if not args.log_path:
        return default_log_path(project_root, root)

    raw = Path(args.log_path).expanduser()
    candidate = raw if raw.is_absolute() else project_root / raw
    if candidate.is_symlink():
        raise ValueError("refusing to write a symlinked quality log")
    resolved = candidate.resolve()
    if is_within(resolved, root):
        return resolved
    if args.allow_project_write and is_within(resolved, project_root):
        return resolved
    raise ValueError(
        "log path must stay in the Codex external-review ledger; "
        "use --allow-project-write for an explicitly authorized project-local log"
    )


def append_once(log_path: Path, line: str, review_id: str) -> bool:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if log_path.is_symlink():
        raise ValueError("refusing to write a symlinked quality log")
    with log_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.seek(0)
        for existing_line in handle:
            try:
                existing = json.loads(existing_line)
            except json.JSONDecodeError:
                raise ValueError(f"existing quality log is not valid JSONL: {log_path}")
            if existing.get("review_id") == review_id:
                return False
        handle.seek(0, os.SEEK_END)
        handle.write(line + "\n")
        handle.flush()
        os.fsync(handle.fileno())
        return True


def main() -> int:
    args = parse_args()
    try:
        project_root = Path(args.project_root).expanduser().resolve()
        if not project_root.is_dir():
            raise ValueError(f"project root is not a directory: {project_root}")
        log_path = select_log_path(args, project_root)
        entry = load_entry(args)
        reject_sensitive_content(entry)
        normalized = normalize_entry(entry, project_root)
        reject_sensitive_content(normalized)
    except Exception as exc:
        print(f"LOG_NOT_WRITTEN {exc}", file=sys.stderr)
        return 2

    line = compact_json(normalized)
    if len(line.encode("utf-8")) > MAX_LOG_BYTES:
        print(f"LOG_NOT_WRITTEN normalized entry exceeds {MAX_LOG_BYTES} bytes", file=sys.stderr)
        return 2
    if args.dry_run:
        print(line)
        return 0

    try:
        written = append_once(log_path, line, normalized["review_id"])
    except (OSError, ValueError) as exc:
        print(f"LOG_NOT_WRITTEN {exc}", file=sys.stderr)
        return 1

    if not written:
        print(f"LOG_ALREADY_PRESENT {log_path}")
        return 0

    print(f"LOG_WRITTEN {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
