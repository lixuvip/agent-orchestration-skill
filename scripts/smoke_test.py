#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "agent-orchestration"

STATUSES = ["DONE", "DONE_WITH_CONCERNS", "BLOCKED", "NEEDS_CONTEXT"]

SCENARIO_FILES = [
    ROOT / "examples" / "bugfix-with-qa.md",
    ROOT / "examples" / "multi-project-finalization.md",
    ROOT / "examples" / "release-prep.md",
    ROOT / "examples" / "simple-research-task.md",
    ROOT / "examples" / "coding-review-workflow.md",
    ROOT / "examples" / "multi-agent-product-planning.md",
]

CORE_FILES = [
    SKILL_DIR / "SKILL.md",
    SKILL_DIR / "references" / "COMMUNICATION_PROTOCOL.md",
    SKILL_DIR / "references" / "STATE_MACHINE.md",
    SKILL_DIR / "references" / "WORKFLOWS.md",
    SKILL_DIR / "references" / "AUTOMATION_MONITORING.md",
    SKILL_DIR / "references" / "templates" / "task_dispatch.template.md",
    SKILL_DIR / "references" / "templates" / "task_dispatch.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "role_reply.template.md",
    SKILL_DIR / "references" / "templates" / "role_reply.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "monitoring_heartbeat.template.md",
    SKILL_DIR / "references" / "templates" / "monitoring_heartbeat.zh-CN.template.md",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"Missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_all(path: Path, tokens: list[str]) -> None:
    text = read(path)
    for token in tokens:
        if token not in text:
            fail(f"{path.relative_to(ROOT)} is missing {token!r}")


def main() -> int:
    combined_core = "\n".join(read(path) for path in CORE_FILES)
    for status in STATUSES:
        if status not in combined_core:
            fail(f"Core skill files do not mention status {status}")

    require_all(
        SKILL_DIR / "references" / "STATE_MACHINE.md",
        [
            "TODO -> IN_PROGRESS",
            "IN_PROGRESS -> DONE",
            "Silence is never completion.",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "AUTOMATION_MONITORING.md",
        [
            "CALLBACK_FAILED",
            "每 5 分钟",
            "DONE_WITH_CONCERNS",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "task_dispatch.template.md",
        [
            "Coordinator thread ID",
            "Callback format",
            "Stop and report if",
            "Verification",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "task_dispatch.zh-CN.template.md",
        [
            "协调者线程 ID",
            "回调格式",
            "遇到以下情况请停止并报告",
            "验证要求",
        ],
    )

    for path in SCENARIO_FILES:
        text = read(path)
        if "Use $agent-orchestration" not in text:
            fail(f"Scenario {path.relative_to(ROOT)} does not invoke the skill")

    print("Smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
