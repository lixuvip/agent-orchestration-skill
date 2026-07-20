#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH = (ROOT / "skills" / "agent-orchestration" / "SKILL.md").read_text(encoding="utf-8")
COORD = (ROOT / "skills" / "agent-orchestration" / "references" / "COORDINATION.md").read_text(encoding="utf-8")
AUTO = (ROOT / "skills" / "agent-orchestration" / "references" / "AUTOMATION.md").read_text(encoding="utf-8")
AGY = (ROOT / "skills" / "agy-second-opinion" / "SKILL.md").read_text(encoding="utf-8")
DOC = (ROOT / "docs" / "forward-tests.md").read_text(encoding="utf-8")


def fail(message: str) -> None:
    print(f"FORWARD_TEST_FAILED {message}", file=sys.stderr)
    raise SystemExit(1)


SCENARIOS = {
    "bounded_subagent": (
        ORCH,
        ["one internal subagent", "Do not create task boards", "result returns"],
    ),
    "visible_user_task": (
        ORCH,
        ["user-owned thread", "new sidebar task", "follow-up"],
    ),
    "formal_gate": (
        COORD,
        ["Formal Gates", "exact candidate commit", "full relevant suite once"],
    ),
    "recurring_work": (
        AUTO,
        ["product's automation tools", "quiet no-op", "stop conditions"],
    ),
    "explicit_external_pass": (
        AGY,
        ["explicit request", "Load exactly one reference", "untrusted advice"],
    ),
    "capability_preflight": (
        COORD,
        ["Preflight required read, write, execute, network, browser, and connector capabilities", "parent's plan/read-only state", "change the surface or scope before dispatch"],
    ),
    "midflight_steering": (
        COORD,
        ["replace", "add", "status/question", "superseded scope is stale"],
    ),
    "correction_vs_review": (
        COORD,
        ["Corrections normally return to the same owner", "fresh context", "raw evidence"],
    ),
    "requirement_closure": (
        COORD,
        ["closure checklist", "follow-ups and corrections", "done`, `waived`, or `blocked"],
    ),
    "active_work_audit": (
        COORD,
        ["Before final delivery", "background commands", "Never imply the whole objective is complete"],
    ),
    "bounded_retry": (
        COORD,
        ["Retries are bounded", "add evidence", "same blocker repeats"],
    ),
    "recovery_capsule": (
        COORD,
        ["recovery capsule", "active background work", "exact next action"],
    ),
    "optional_best_of_n": (
        COORD,
        ["Optional Best Of N", "2-3 isolated candidates", "allow rejecting every candidate"],
    ),
}

for name, (text, tokens) in SCENARIOS.items():
    missing = [token for token in tokens if token not in text]
    if missing:
        fail(f"{name} missing {missing}")
    if name not in DOC:
        fail(f"docs missing scenario {name}")

if "agy" in ORCH.lower() or "agent-orchestration" in AGY:
    fail("forward route still couples orchestration and agy")

print(f"FORWARD_TEST_OK scenarios={len(SCENARIOS)}")
