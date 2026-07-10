#!/usr/bin/env python3
"""Compute monotonic heartbeat-monitor lifecycle transitions."""

from __future__ import annotations

import json
import sys
from typing import Any, Mapping


LIFECYCLE_STATES = frozenset({"ACTIVE", "DRAINING", "CLOSED"})
ROLE_STATES = frozenset(
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
TERMINAL_ROLE_STATES = frozenset(
    {"DONE", "DONE_WITH_CONCERNS", "BLOCKED", "NEEDS_CONTEXT", "CANCELLED"}
)


class LifecycleError(ValueError):
    """Raised when heartbeat state is malformed or contradictory."""


def evaluate(state: Mapping[str, object]) -> dict[str, object]:
    if not isinstance(state, Mapping):
        raise LifecycleError("heartbeat state must be a JSON object")
    lifecycle_state = state.get("lifecycle_state")
    if lifecycle_state not in LIFECYCLE_STATES:
        raise LifecycleError("lifecycle_state must be ACTIVE, DRAINING, or CLOSED")
    role_states = state.get("role_states")
    if not isinstance(role_states, list) or not role_states:
        raise LifecycleError("role_states must be a non-empty list")
    invalid = [value for value in role_states if value not in ROLE_STATES]
    if invalid:
        raise LifecycleError(f"unsupported role state: {invalid[0]}")
    final_summary_posted = state.get("final_summary_posted")
    cleanup_confirmed = state.get("cleanup_confirmed")
    if not isinstance(final_summary_posted, bool) or not isinstance(cleanup_confirmed, bool):
        raise LifecycleError("final_summary_posted and cleanup_confirmed must be booleans")
    if cleanup_confirmed and not final_summary_posted:
        raise LifecycleError("cleanup cannot be confirmed before the final summary is posted")
    if lifecycle_state == "CLOSED" and not (final_summary_posted and cleanup_confirmed):
        raise LifecycleError("CLOSED requires a posted final summary and confirmed cleanup")

    all_terminal = all(value in TERMINAL_ROLE_STATES for value in role_states)
    result: dict[str, object] = {
        "previous_state": lifecycle_state,
        "all_roles_terminal": all_terminal,
        "terminal_role_count": sum(value in TERMINAL_ROLE_STATES for value in role_states),
        "tracked_role_count": len(role_states),
    }

    if lifecycle_state == "CLOSED":
        result.update(next_state="CLOSED", action="NOOP", coordinator_action="NONE")
        return result

    if lifecycle_state == "ACTIVE" and not all_terminal:
        result.update(
            next_state="ACTIVE",
            action="KEEP_ACTIVE",
            coordinator_action="WAIT_FOR_ROLES",
        )
        return result

    if not all_terminal:
        result.update(
            next_state="DRAINING",
            action="RECONCILE_ROLE_STATE",
            coordinator_action="REVIEW_TERMINAL_RESULTS",
        )
        return result

    if not final_summary_posted:
        result.update(
            next_state="DRAINING",
            action="POST_FINAL_SUMMARY",
            coordinator_action="REVIEW_TERMINAL_RESULTS",
        )
        return result
    if not cleanup_confirmed:
        result.update(
            next_state="DRAINING",
            action="CLOSE_HEARTBEAT",
            coordinator_action="REVIEW_TERMINAL_RESULTS",
        )
        return result

    result.update(next_state="CLOSED", action="NOOP", coordinator_action="REVIEW_TERMINAL_RESULTS")
    return result


def main() -> int:
    try:
        state: Any = json.load(sys.stdin)
        result = evaluate(state)
        print(
            "HEARTBEAT_TRANSITION "
            + json.dumps(result, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        )
        return 0
    except (json.JSONDecodeError, LifecycleError) as exc:
        print(f"HEARTBEAT_REJECTED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
