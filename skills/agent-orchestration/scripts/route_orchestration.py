#!/usr/bin/env python3
"""Choose the minimum safe orchestration mode from task characteristics."""

from __future__ import annotations

import json
import sys
from typing import Any, Mapping


MODES = ("LITE", "STANDARD", "DURABLE")
MODE_RANK = {mode: index for index, mode in enumerate(MODES)}
BOOLEAN_FIELDS = (
    "asynchronous",
    "recurring",
    "cross_repository",
    "merge_or_release_gate",
    "long_running",
    "user_visible_threads",
    "requires_durable_memory",
    "external_model",
    "parallel_shared_edit_scope",
)


class RoutingError(ValueError):
    """Raised when routing input is malformed."""


def _boolean(request: Mapping[str, object], field: str) -> bool:
    value = request.get(field, False)
    if not isinstance(value, bool):
        raise RoutingError(f"{field} must be a boolean")
    return value


def route(request: Mapping[str, object]) -> dict[str, object]:
    if not isinstance(request, Mapping):
        raise RoutingError("routing request must be a JSON object")
    role_count = request.get("role_count", 1)
    if isinstance(role_count, bool) or not isinstance(role_count, int) or not 1 <= role_count <= 32:
        raise RoutingError("role_count must be an integer from 1 to 32")
    features = {field: _boolean(request, field) for field in BOOLEAN_FIELDS}
    requested_mode = request.get("requested_mode", "AUTO")
    if requested_mode not in {"AUTO", *MODES}:
        raise RoutingError("requested_mode must be AUTO, LITE, STANDARD, or DURABLE")

    reasons: list[str] = []
    if features["recurring"]:
        reasons.append("recurring execution requires durable state")
    if features["requires_durable_memory"]:
        reasons.append("task explicitly requires durable memory")

    if features["recurring"] or features["requires_durable_memory"]:
        minimum_mode = "DURABLE"
    elif (
        role_count >= 2
        or features["asynchronous"]
        or features["cross_repository"]
        or features["merge_or_release_gate"]
        or features["long_running"]
        or features["user_visible_threads"]
        or features["parallel_shared_edit_scope"]
    ):
        minimum_mode = "STANDARD"
        if role_count >= 2:
            reasons.append("multiple roles require explicit ownership and handoff")
        if features["asynchronous"] or features["user_visible_threads"]:
            reasons.append("asynchronous or user-visible threads require callbacks")
        if features["cross_repository"]:
            reasons.append("cross-repository work requires a tracked task board")
        if features["merge_or_release_gate"]:
            reasons.append("merge or release work requires explicit gates")
        if features["long_running"]:
            reasons.append("long-running work requires recoverable monitoring")
    else:
        minimum_mode = "LITE"
        reasons.append("one-shot current-context work does not need durable coordination")

    if requested_mode == "AUTO":
        selected_mode = minimum_mode
        requested_mode_honored = True
    elif MODE_RANK[requested_mode] < MODE_RANK[minimum_mode]:
        selected_mode = minimum_mode
        requested_mode_honored = False
        reasons.append(f"requested {requested_mode} cannot bypass {minimum_mode} safety requirements")
    else:
        selected_mode = requested_mode
        requested_mode_honored = True
        if requested_mode != minimum_mode:
            reasons.append(f"user explicitly upgraded orchestration to {requested_mode}")

    if selected_mode == "DURABLE":
        monitoring = "CRON"
    elif selected_mode == "STANDARD" and (
        features["asynchronous"] or features["long_running"] or features["user_visible_threads"]
    ):
        monitoring = "HEARTBEAT"
    else:
        monitoring = "NONE"

    modifiers: list[str] = []
    if features["external_model"]:
        modifiers.append("EXTERNAL_MODEL_SECOND_OPINION")

    warnings: list[str] = []
    if features["parallel_shared_edit_scope"] and role_count >= 2:
        warnings.append("ISOLATE_OR_SERIALIZE_SHARED_EDITS")

    return {
        "minimum_mode": minimum_mode,
        "selected_mode": selected_mode,
        "requested_mode": requested_mode,
        "requested_mode_honored": requested_mode_honored,
        "monitoring": monitoring,
        "requires_event_protocol": bool(
            features["asynchronous"] or features["user_visible_threads"] or role_count >= 2
        ),
        "requires_task_board": selected_mode in {"STANDARD", "DURABLE"},
        "requires_goal_contract": selected_mode == "DURABLE",
        "requires_durable_memory": selected_mode == "DURABLE",
        "requires_lease": monitoring in {"HEARTBEAT", "CRON"},
        "requires_heartbeat_lifecycle": monitoring == "HEARTBEAT",
        "requires_isolation_or_serialization": bool(warnings),
        "modifiers": modifiers,
        "warnings": warnings,
        "reasons": reasons,
    }


def main() -> int:
    try:
        request: Any = json.load(sys.stdin)
        result = route(request)
        print(
            "ORCHESTRATION_ROUTE "
            + json.dumps(result, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        )
        return 0
    except (json.JSONDecodeError, RoutingError) as exc:
        print(f"ORCHESTRATION_ROUTE_REJECTED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
