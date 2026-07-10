#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "skills" / "agent-orchestration" / "scripts" / "route_orchestration.py"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def route(**overrides: object) -> dict[str, object]:
    request: dict[str, object] = {
        "role_count": 1,
        "asynchronous": False,
        "recurring": False,
        "cross_repository": False,
        "merge_or_release_gate": False,
        "long_running": False,
        "user_visible_threads": False,
        "requires_durable_memory": False,
        "external_model": False,
        "parallel_shared_edit_scope": False,
        "requested_mode": "AUTO",
    }
    request.update(overrides)
    completed = subprocess.run(
        [sys.executable, str(ROUTER)],
        input=json.dumps(request),
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"router rejected valid request: {completed.stderr}")
    if not completed.stdout.startswith("ORCHESTRATION_ROUTE "):
        fail(f"router returned unexpected output: {completed.stdout!r}")
    return json.loads(completed.stdout.split(" ", 1)[1])


def require(value: bool, message: str) -> None:
    if not value:
        fail(message)


def main() -> int:
    if not ROUTER.exists():
        fail(f"Missing orchestration router: {ROUTER.relative_to(ROOT)}")

    lite = route()
    require(lite["selected_mode"] == "LITE", "one-shot current-thread task was not LITE")
    require(lite["monitoring"] == "NONE", "LITE task created monitoring")
    require(not lite["requires_task_board"], "LITE task required a task board")
    require(not lite["requires_lease"], "LITE task required a concurrency lease")

    standard = route(role_count=2, asynchronous=True, user_visible_threads=True)
    require(standard["selected_mode"] == "STANDARD", "two async roles were not STANDARD")
    require(standard["monitoring"] == "HEARTBEAT", "async STANDARD did not choose heartbeat")
    require(standard["requires_event_protocol"], "async STANDARD omitted event protocol")
    require(standard["requires_task_board"], "STANDARD omitted task board")
    require(standard["requires_lease"], "recurring STANDARD heartbeat omitted fenced lease")

    durable = route(
        role_count=2,
        recurring=True,
        asynchronous=True,
        requires_durable_memory=True,
    )
    require(durable["selected_mode"] == "DURABLE", "recurring workspace task was not DURABLE")
    require(durable["monitoring"] == "CRON", "DURABLE task did not choose cron")
    require(durable["requires_goal_contract"], "DURABLE omitted goal contract")
    require(durable["requires_durable_memory"], "DURABLE omitted automation memory")
    require(durable["requires_lease"], "DURABLE omitted fenced lease")

    external = route(external_model=True)
    require(external["selected_mode"] == "LITE", "one-shot external review was over-orchestrated")
    require("EXTERNAL_MODEL_SECOND_OPINION" in external["modifiers"], "external review modifier missing")
    require(external["monitoring"] == "NONE", "one-shot external review created recurring monitoring")

    shared_scope = route(role_count=3, asynchronous=True, parallel_shared_edit_scope=True)
    require(shared_scope["selected_mode"] == "STANDARD", "parallel shared edit task routing changed")
    require(
        "ISOLATE_OR_SERIALIZE_SHARED_EDITS" in shared_scope["warnings"],
        "shared edit scope lacked isolation warning",
    )

    refused_downgrade = route(recurring=True, requested_mode="LITE")
    require(refused_downgrade["selected_mode"] == "DURABLE", "requested LITE downgraded recurring safety")
    require(not refused_downgrade["requested_mode_honored"], "unsafe requested downgrade was marked honored")

    explicit_upgrade = route(requested_mode="DURABLE")
    require(explicit_upgrade["selected_mode"] == "DURABLE", "explicit DURABLE upgrade was ignored")
    require(explicit_upgrade["requested_mode_honored"], "explicit safe upgrade was not honored")

    print("Orchestration routing behavior test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
