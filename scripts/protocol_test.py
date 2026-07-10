#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_SCRIPT = ROOT / "skills" / "agent-orchestration" / "scripts" / "orchestration_event.py"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_protocol() -> ModuleType:
    if not PROTOCOL_SCRIPT.exists():
        fail(f"Missing protocol helper: {PROTOCOL_SCRIPT.relative_to(ROOT)}")
    spec = importlib.util.spec_from_file_location("orchestration_event", PROTOCOL_SCRIPT)
    if spec is None or spec.loader is None:
        fail("Could not load orchestration event helper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def event(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "protocol_version": "ORCHESTRATION_EVENT_V1",
        "goal_id": "GOAL-001",
        "task_id": "TASK-001",
        "attempt": 2,
        "dispatch_nonce": "dispatch-2-abc",
        "coordinator_epoch": "coordinator-epoch-7",
        "event_id": "event-task-001-2-done",
        "event_timestamp": "2026-07-10T10:00:00+08:00",
        "role": "QA Tester",
        "coordinator_thread_id": "thread-coordinator",
        "role_thread_id": "thread-qa",
        "base_sha": "0123456789abcdef0123456789abcdef01234567",
        "expected_head_sha": "1111111111111111111111111111111111111111",
        "observed_head_sha": "1111111111111111111111111111111111111111",
        "execution_status": "DONE",
        "gate_verdict": "PASS",
        "coordinator_state": "IN_REVIEW",
    }
    value.update(overrides)
    return value


def expectation(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "goal_id": "GOAL-001",
        "task_id": "TASK-001",
        "attempt": 2,
        "dispatch_nonce": "dispatch-2-abc",
        "coordinator_epoch": "coordinator-epoch-7",
        "expected_head_sha": "1111111111111111111111111111111111111111",
    }
    value.update(overrides)
    return value


def main() -> int:
    protocol = load_protocol()

    current = event()
    protocol.validate_event(current)
    if protocol.classify_event(current, expectation(), set()) != "ACCEPT":
        fail("current callback was not accepted")
    if protocol.classify_event(current, expectation(), {current["event_id"]}) != "DUPLICATE":
        fail("duplicate event_id was not deduplicated")
    if protocol.classify_event(event(attempt=1), expectation(), set()) != "STALE":
        fail("older attempt was not classified as stale")
    if protocol.classify_event(event(dispatch_nonce="old-nonce"), expectation(), set()) != "STALE":
        fail("old dispatch nonce was not classified as stale")
    if protocol.classify_event(event(coordinator_epoch="old-epoch"), expectation(), set()) != "STALE":
        fail("old coordinator epoch was not classified as stale")
    if protocol.classify_event(
        event(observed_head_sha="2222222222222222222222222222222222222222"),
        expectation(),
        set(),
    ) != "STALE":
        fail("QA evidence from the wrong head SHA was not classified as stale")
    producer = event(
        expected_head_sha="UNKNOWN",
        observed_head_sha="2222222222222222222222222222222222222222",
        gate_verdict="PENDING",
    )
    if protocol.classify_event(
        producer,
        expectation(expected_head_sha="UNKNOWN"),
        set(),
    ) != "ACCEPT":
        fail("a producer callback could not report a newly created concrete head SHA")
    if protocol.accepted_delivery(producer):
        fail("a producer callback with UNKNOWN expected SHA was treated as delivery")

    failed_gate = event(gate_verdict="FAIL", coordinator_state="ACCEPTED")
    if protocol.accepted_delivery(failed_gate):
        fail("DONE + FAIL was treated as accepted delivery")
    pending_acceptance = event(coordinator_state="IN_REVIEW")
    if protocol.accepted_delivery(pending_acceptance):
        fail("role DONE was treated as coordinator acceptance")
    accepted = event(coordinator_state="ACCEPTED")
    if not protocol.accepted_delivery(accepted):
        fail("coordinator-accepted PASS evidence was not deliverable")
    accepted_without_git = event(
        base_sha="NONE",
        expected_head_sha="NONE",
        observed_head_sha="NONE",
        coordinator_state="ACCEPTED",
    )
    protocol.validate_event(accepted_without_git)
    if not protocol.accepted_delivery(accepted_without_git):
        fail("a non-Git task with matching NONE artifact identity was not deliverable")

    cancelled = event(
        execution_status="CANCELLED",
        gate_verdict="NOT_APPLICABLE",
        coordinator_state="CANCELLED",
    )
    protocol.validate_event(cancelled)
    if protocol.accepted_delivery(cancelled):
        fail("cancelled work was treated as accepted delivery")

    print("Protocol test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
