#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "agent-orchestration"
SKILL = SKILL_DIR / "SKILL.md"
REFERENCES = SKILL_DIR / "references"

CANONICAL_PACKS = [
    REFERENCES / "COORDINATION_RUNBOOK.md",
    REFERENCES / "COORDINATION_RUNBOOK.zh-CN.md",
    REFERENCES / "PROJECT_AUTOPILOT.md",
    REFERENCES / "PROJECT_AUTOPILOT.zh-CN.md",
]

LEGACY_CORE_FILES = [
    "ORCHESTRATION_INTAKE.md",
    "ORCHESTRATION_ROUTING.md",
    "ORCHESTRATION_ROUTING.zh-CN.md",
    "ORCHESTRATION_PROTOCOL.md",
    "ORCHESTRATION_PROTOCOL.zh-CN.md",
    "COMMUNICATION_PROTOCOL.md",
    "CONTROLLER_LOOP.md",
    "STATE_MACHINE.md",
    "AUTOMATION_MONITORING.md",
    "AUTOMATION_TOOLING.md",
    "AUTOMATION_CONCURRENCY.md",
    "AUTOMATION_CONCURRENCY.zh-CN.md",
    "PROJECT_INSTRUCTIONS_DISCOVERY.md",
    "WORKFLOWS.md",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    text = SKILL.read_text(encoding="utf-8")
    body = text.split("---", 2)[-1]
    line_count = len(text.splitlines())
    word_count = len(body.split())
    if line_count > 70:
        fail(f"SKILL.md exceeds 70-line context budget: {line_count}")
    if word_count > 900:
        fail(f"SKILL.md exceeds 900-word context budget: {word_count}")

    for path in CANONICAL_PACKS:
        if not path.exists():
            fail(f"missing canonical capability pack: {path.relative_to(ROOT)}")
    if len((REFERENCES / "COORDINATION_RUNBOOK.md").read_text(encoding="utf-8").splitlines()) > 180:
        fail("COORDINATION_RUNBOOK.md exceeds 180-line budget")
    if len((REFERENCES / "PROJECT_AUTOPILOT.md").read_text(encoding="utf-8").splitlines()) > 200:
        fail("PROJECT_AUTOPILOT.md exceeds 200-line budget")

    for name in LEGACY_CORE_FILES:
        if (REFERENCES / name).exists():
            fail(f"legacy overlapping reference still exists: {name}")

    required_tokens = [
        "LITE: load no core reference",
        "STANDARD: load one language version of `COORDINATION_RUNBOOK.md`",
        "DURABLE: load the same runbook plus one language version of `PROJECT_AUTOPILOT.md`",
        "Never load both language versions",
        "External-model review/research is an independent modifier",
    ]
    for token in required_tokens:
        if token not in text:
            fail(f"SKILL.md is missing scale guard {token!r}")

    print("Skill scale budget test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
