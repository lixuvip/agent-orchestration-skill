#!/usr/bin/env python3
"""Validate and classify versioned orchestration callback envelopes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping


PROTOCOL_VERSION = "ORCHESTRATION_EVENT_V1"

EXECUTION_STATUSES = frozenset(
    {
        "TODO",
        "IN_PROGRESS",
        "DONE",
        "DONE_WITH_CONCERNS",
        "BLOCKED",
        "NEEDS_CONTEXT",
        "CANCELLED",
    }
)
GATE_VERDICTS = frozenset(
    {"PENDING", "PASS", "FAIL", "BLOCKED", "WAIVED", "NOT_APPLICABLE"}
)
COORDINATOR_STATES = frozenset(
    {
        "TODO",
        "DISPATCHED",
        "IN_PROGRESS",
        "IN_REVIEW",
        "RETURNED",
        "ACCEPTED",
        "ESCALATED",
        "CANCELLED",
    }
)

REQUIRED_FIELDS = (
    "protocol_version",
    "goal_id",
    "task_id",
    "attempt",
    "dispatch_nonce",
    "coordinator_epoch",
    "event_id",
    "event_timestamp",
    "role",
    "coordinator_thread_id",
    "role_thread_id",
    "base_sha",
    "expected_head_sha",
    "observed_head_sha",
    "execution_status",
    "gate_verdict",
    "coordinator_state",
)

EXPECTATION_FIELDS = (
    "goal_id",
    "task_id",
    "attempt",
    "dispatch_nonce",
    "coordinator_epoch",
    "expected_head_sha",
)

_IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")
_SHA_RE = re.compile(r"^(?:NONE|UNKNOWN|[0-9a-fA-F]{7,64})$")


class ProtocolError(ValueError):
    """Raised when an orchestration event does not satisfy the protocol."""


def _require_string(value: object, field: str, *, identifier: bool = False) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProtocolError(f"{field} must be a non-empty string")
    if len(value) > 256:
        raise ProtocolError(f"{field} exceeds 256 characters")
    if identifier and not _IDENTIFIER_RE.fullmatch(value):
        raise ProtocolError(f"{field} contains unsupported characters")
    return value


def _require_sha(value: object, field: str) -> str:
    text = _require_string(value, field)
    if not _SHA_RE.fullmatch(text):
        raise ProtocolError(f"{field} must be NONE, UNKNOWN, or a 7-64 digit hex SHA")
    return text


def _require_timestamp(value: object) -> str:
    text = _require_string(value, "event_timestamp")
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ProtocolError("event_timestamp must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ProtocolError("event_timestamp must include a timezone")
    return text


def _require_enum(value: object, field: str, allowed: frozenset[str]) -> str:
    text = _require_string(value, field)
    if text not in allowed:
        choices = ", ".join(sorted(allowed))
        raise ProtocolError(f"{field} must be one of: {choices}")
    return text


def validate_event(event: Mapping[str, object]) -> None:
    """Raise ProtocolError when *event* is not a valid V1 callback envelope."""

    if not isinstance(event, Mapping):
        raise ProtocolError("event must be a JSON object")
    missing = [field for field in REQUIRED_FIELDS if field not in event]
    if missing:
        raise ProtocolError(f"missing required fields: {', '.join(missing)}")

    if event["protocol_version"] != PROTOCOL_VERSION:
        raise ProtocolError(f"protocol_version must be {PROTOCOL_VERSION}")

    for field in (
        "goal_id",
        "task_id",
        "dispatch_nonce",
        "coordinator_epoch",
        "event_id",
        "coordinator_thread_id",
        "role_thread_id",
    ):
        _require_string(event[field], field, identifier=True)
    _require_string(event["role"], "role")

    attempt = event["attempt"]
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 1:
        raise ProtocolError("attempt must be a positive integer")

    _require_timestamp(event["event_timestamp"])
    base_sha = _require_sha(event["base_sha"], "base_sha")
    expected_sha = _require_sha(event["expected_head_sha"], "expected_head_sha")
    observed_sha = _require_sha(event["observed_head_sha"], "observed_head_sha")
    execution_status = _require_enum(
        event["execution_status"], "execution_status", EXECUTION_STATUSES
    )
    gate_verdict = _require_enum(event["gate_verdict"], "gate_verdict", GATE_VERDICTS)
    coordinator_state = _require_enum(
        event["coordinator_state"], "coordinator_state", COORDINATOR_STATES
    )

    if base_sha == "NONE" and expected_sha not in {"NONE", "UNKNOWN"}:
        raise ProtocolError("expected_head_sha cannot name a commit when base_sha is NONE")
    if execution_status == "CANCELLED" and coordinator_state != "CANCELLED":
        raise ProtocolError("CANCELLED execution requires CANCELLED coordinator_state")
    if coordinator_state == "CANCELLED" and execution_status != "CANCELLED":
        raise ProtocolError("CANCELLED coordinator_state requires CANCELLED execution_status")
    if coordinator_state == "ACCEPTED":
        if execution_status not in {"DONE", "DONE_WITH_CONCERNS"}:
            raise ProtocolError("ACCEPTED requires a completed execution_status")
        if expected_sha == "UNKNOWN" or observed_sha != expected_sha:
            raise ProtocolError("ACCEPTED requires evidence pinned to expected_head_sha")
        if expected_sha == "NONE" and base_sha != "NONE":
            raise ProtocolError("ACCEPTED may use NONE only when no Git repository applies")


def validate_expectation(expectation: Mapping[str, object]) -> None:
    """Validate the coordinator's active dispatch identity."""

    if not isinstance(expectation, Mapping):
        raise ProtocolError("expectation must be a JSON object")
    missing = [field for field in EXPECTATION_FIELDS if field not in expectation]
    if missing:
        raise ProtocolError(f"missing expectation fields: {', '.join(missing)}")
    for field in (
        "goal_id",
        "task_id",
        "dispatch_nonce",
        "coordinator_epoch",
    ):
        _require_string(expectation[field], field, identifier=True)
    attempt = expectation["attempt"]
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 1:
        raise ProtocolError("expectation attempt must be a positive integer")
    _require_sha(expectation["expected_head_sha"], "expected_head_sha")


def classify_event(
    event: Mapping[str, object],
    expectation: Mapping[str, object],
    seen_event_ids: Iterable[str],
) -> str:
    """Return ACCEPT, DUPLICATE, or STALE for a valid callback envelope."""

    validate_event(event)
    validate_expectation(expectation)
    if event["event_id"] in set(seen_event_ids):
        return "DUPLICATE"

    for field in EXPECTATION_FIELDS:
        if event[field] != expectation[field]:
            return "STALE"
    expected_sha = expectation["expected_head_sha"]
    if expected_sha != "UNKNOWN" and event["observed_head_sha"] != expected_sha:
        return "STALE"
    return "ACCEPT"


def accepted_delivery(event: Mapping[str, object]) -> bool:
    """Return whether the coordinator can treat this event as delivered."""

    try:
        validate_event(event)
    except ProtocolError:
        return False
    return bool(
        event["coordinator_state"] == "ACCEPTED"
        and event["execution_status"] in {"DONE", "DONE_WITH_CONCERNS"}
        and event["gate_verdict"] in {"PASS", "WAIVED", "NOT_APPLICABLE"}
        and event["expected_head_sha"] != "UNKNOWN"
        and event["observed_head_sha"] == event["expected_head_sha"]
        and (
            event["expected_head_sha"] != "NONE"
            or event["base_sha"] == "NONE"
        )
    )


def _read_json(path: str | None) -> Any:
    if path:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return json.load(sys.stdin)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and classify an ORCHESTRATION_EVENT_V1 callback."
    )
    parser.add_argument("--event-file", help="JSON event file; stdin is used when omitted")
    parser.add_argument("--expectation-file", help="active coordinator expectation JSON")
    parser.add_argument(
        "--seen-event-id",
        action="append",
        default=[],
        help="previously processed event ID; repeat as needed",
    )
    parser.add_argument(
        "--require-accepted-delivery",
        action="store_true",
        help="fail unless the event is coordinator-accepted and gate-passing",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        event = _read_json(args.event_file)
        validate_event(event)
        classification = "ACCEPT"
        if args.expectation_file:
            expectation = json.loads(Path(args.expectation_file).read_text(encoding="utf-8"))
            classification = classify_event(event, expectation, args.seen_event_id)
        if classification == "DUPLICATE":
            print("EVENT_DUPLICATE")
            return 0
        if classification == "STALE":
            print("EVENT_STALE")
            return 3
        if args.require_accepted_delivery and not accepted_delivery(event):
            print("EVENT_NOT_DELIVERABLE")
            return 4
        print("EVENT_ACCEPTED")
        return 0
    except (OSError, json.JSONDecodeError, ProtocolError) as exc:
        print(f"EVENT_REJECTED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
