#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH_DIR = ROOT / "skills" / "agent-orchestration"
AGY_DIR = ROOT / "skills" / "agy-second-opinion"
ORCH = (ORCH_DIR / "SKILL.md").read_text(encoding="utf-8")
AGY = (AGY_DIR / "SKILL.md").read_text(encoding="utf-8")


def route(*, owners: int = 1, bounded_subagent: bool = False, recurring: bool = False) -> str:
    if recurring:
        return "AUTOMATION"
    if owners > 1:
        return "COORDINATION"
    if bounded_subagent:
        return "CORE"
    return "CURRENT_TASK"


cases = [
    ({"owners": 1}, "CURRENT_TASK"),
    ({"bounded_subagent": True}, "CORE"),
    ({"owners": 2}, "COORDINATION"),
    ({"recurring": True}, "AUTOMATION"),
]
for kwargs, expected in cases:
    actual = route(**kwargs)
    if actual != expected:
        print(f"ROUTING_TEST_FAILED {kwargs}: {actual} != {expected}", file=sys.stderr)
        raise SystemExit(1)

for token in (
    "Keep one-owner work in the current task",
    "one internal subagent",
    "COORDINATION.md",
    "AUTOMATION.md",
    "required read, write, execute, network, browser, and connector capabilities",
    "Keep delegation flat by default",
    "replace, add, or status",
):
    if token not in ORCH:
        print(f"ROUTING_TEST_FAILED main skill missing {token}", file=sys.stderr)
        raise SystemExit(1)
if "agy" in ORCH.lower() or "Gemini" in ORCH or "agent-orchestration" in AGY:
    print("ROUTING_TEST_FAILED external second opinion is not isolated", file=sys.stderr)
    raise SystemExit(1)
if (ORCH_DIR / "scripts" / "route_orchestration.py").exists():
    print("ROUTING_TEST_FAILED deterministic router still installed", file=sys.stderr)
    raise SystemExit(1)

print(f"ROUTING_TEST_OK cases={len(cases)} separate_agy=true")
