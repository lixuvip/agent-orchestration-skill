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
    ROOT / "examples" / "branch-callback-controller-loop.md",
    ROOT / "examples" / "continuous-project-autopilot.md",
    ROOT / "examples" / "github-issue-pr-autopilot.md",
]

CORE_FILES = [
    SKILL_DIR / "SKILL.md",
    SKILL_DIR / "references" / "COMMUNICATION_PROTOCOL.md",
    SKILL_DIR / "references" / "CONTROLLER_LOOP.md",
    SKILL_DIR / "references" / "ORCHESTRATION_INTAKE.md",
    SKILL_DIR / "references" / "PROJECT_AUTOPILOT.md",
    SKILL_DIR / "references" / "AUTOMATION_TOOLING.md",
    SKILL_DIR / "references" / "PROJECT_INSTRUCTIONS_DISCOVERY.md",
    SKILL_DIR / "references" / "STATE_MACHINE.md",
    SKILL_DIR / "references" / "WORKFLOWS.md",
    SKILL_DIR / "references" / "AUTOMATION_MONITORING.md",
    SKILL_DIR / "references" / "templates" / "agents_guidance_snippet.template.md",
    SKILL_DIR / "references" / "templates" / "agents_guidance_snippet.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "automation_memory.template.md",
    SKILL_DIR / "references" / "templates" / "automation_memory.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "automation_plan.template.md",
    SKILL_DIR / "references" / "templates" / "automation_plan.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "automation_tick.template.md",
    SKILL_DIR / "references" / "templates" / "automation_tick.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "coordinator_callback.template.md",
    SKILL_DIR / "references" / "templates" / "coordinator_callback.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "escalation_report.template.md",
    SKILL_DIR / "references" / "templates" / "escalation_report.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "merge_readiness.template.md",
    SKILL_DIR / "references" / "templates" / "merge_readiness.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "project_goal_contract.template.md",
    SKILL_DIR / "references" / "templates" / "project_goal_contract.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "task_dispatch.template.md",
    SKILL_DIR / "references" / "templates" / "task_dispatch.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "orchestration_intake.template.md",
    SKILL_DIR / "references" / "templates" / "orchestration_intake.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "status_request.template.md",
    SKILL_DIR / "references" / "templates" / "status_request.zh-CN.template.md",
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
            "status request",
            "PROJECT_AUTOPILOT.md",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "PROJECT_AUTOPILOT.md",
        [
            "AGENTS.md",
            "PROJECT_INSTRUCTIONS_DISCOVERY.md",
            "AUTOMATION_TOOLING.md",
            "cron",
            "Goal Contract",
            "Tick Loop",
            "latest effective update",
            "automation memory",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "AUTOMATION_TOOLING.md",
        [
            "Heartbeat",
            "Cron",
            "Existing Automation Check",
            "Do not show raw RRULE",
            "Safety Gates",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "PROJECT_INSTRUCTIONS_DISCOVERY.md",
        [
            "AGENTS.md",
            "AGENTS.override.md",
            ".codex/config.toml",
            "automation memory",
            "Discovery Report",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "ORCHESTRATION_INTAKE.md",
        [
            "request_user_input",
            "Ask only when",
            "Do not ask when",
            "Execution surface",
            "project autopilot",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "CONTROLLER_LOOP.md",
        [
            "controller loop",
            "send_message_to_thread",
            "status request",
            "merge readiness",
            "Autopilot Readiness",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "project_goal_contract.template.md",
        [
            "Done when:",
            "Allowed autonomously:",
            "Requires confirmation:",
            "Verification commands:",
            "Memory path:",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "automation_tick.template.md",
        [
            "Latest effective update:",
            "Action taken:",
            "Verification:",
            "Next safe action:",
            "Escalation needed:",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agents_guidance_snippet.template.md",
        [
            "Codex Project Autopilot",
            "Safe autonomous actions",
            "Actions requiring confirmation",
            "Idempotency rule",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "task_dispatch.template.md",
        [
            "Coordinator thread ID",
            "Callback format",
            "Stop and report if",
            "Verification",
            "Branch / worktree",
            "Merge policy",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "task_dispatch.zh-CN.template.md",
        [
            "协调者线程 ID",
            "回调格式",
            "遇到以下情况请停止并报告",
            "验证要求",
            "分支 / 工作区",
            "合并策略",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "orchestration_intake.template.md",
        [
            "Execution surface:",
            "Callback behavior:",
            "Merge/push permission:",
            "Ask only if",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "coordinator_callback.template.md",
        [
            "Task ID:",
            "Branch / worktree:",
            "Status:",
            "Verification:",
            "Next coordinator action:",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "status_request.template.md",
        [
            "Status request",
            "Coordinator thread ID",
            "Reply with one",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "merge_readiness.template.md",
        [
            "Merge readiness",
            "Base branch:",
            "Working tree:",
            "Tests:",
            "Push permission:",
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
