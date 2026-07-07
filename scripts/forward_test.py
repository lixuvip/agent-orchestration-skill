#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "agent-orchestration"
FORWARD_TESTS = ROOT / "docs" / "forward-tests.md"


SCENARIO_REQUIREMENTS = {
    "Scenario 1: Heartbeat Callback": [
        "Use $agent-orchestration",
        "long-running bug fix",
        "callback to the coordinator",
        "Chooses heartbeat rather than cron.",
        "Uses task dispatch with callback and verification fields.",
        "Refuses to infer completion from silence.",
        "delete or pause heartbeat",
    ],
    "Scenario 2: Workspace Project Autopilot": [
        "Use $agent-orchestration",
        "Check every two hours.",
        "Use AGENTS.md as the source of project rules.",
        "Do not push, merge, publish, or deploy without asking.",
        "PROJECT_AUTOPILOT.md",
        "AUTOMATION_TOOLING.md",
        "PROJECT_INSTRUCTIONS_DISCOVERY.md",
        "Chooses cron for workspace progress.",
        "goal contract",
        "automation memory",
        "latest effective update",
        "push, merge, publish, deploy",
    ],
    "Scenario 3: GitHub Issue/PR No-Op Poll": [
        "GitHub issue and linked PR",
        "The issue is the coordination channel.",
        "The PR is the implementation channel.",
        "Do not comment if the latest effective update is unchanged",
        "Does not stop just because no PR exists.",
        "review/draft state",
        "Updates memory without posting",
    ],
    "Scenario 4: Missing Project Instructions": [
        "the repo has no AGENTS.md",
        "Reports missing durable project guidance.",
        "Suggests an `AGENTS.md` snippet",
        "Still creates a goal contract",
        "verification and stop conditions",
    ],
}

CORE_COVERAGE = {
    SKILL_DIR / "references" / "PROJECT_AUTOPILOT.md": [
        "Goal Contract",
        "Tick Loop",
        "latest effective update",
        "automation memory",
        "escalation",
    ],
    SKILL_DIR / "references" / "AUTOMATION_TOOLING.md": [
        "Heartbeat",
        "Cron",
        "Existing Automation Check",
        "Safety Gates",
    ],
    SKILL_DIR / "references" / "PROJECT_INSTRUCTIONS_DISCOVERY.md": [
        "AGENTS.md",
        "AGENTS.override.md",
        ".codex/config.toml",
        "automation memory",
    ],
    SKILL_DIR / "references" / "AUTOMATION_MONITORING.md": [
        "heartbeat",
        "CALLBACK_FAILED",
        "不把“未读取到最终回复”的任务当作完成。",
    ],
    SKILL_DIR / "references" / "STATE_MACHINE.md": [
        "Silence is never completion.",
        "Do not infer completion.",
    ],
    SKILL_DIR / "references" / "CONTROLLER_LOOP.md": [
        "status request",
        "merge readiness",
        "Autopilot Readiness",
    ],
    SKILL_DIR / "references" / "templates" / "automation_tick.template.md": [
        "Latest effective update:",
        "Action taken:",
        "Memory updated:",
        "Escalation needed:",
    ],
    SKILL_DIR / "references" / "templates" / "automation_memory.template.md": [
        "Latest Effective Update",
        "Posted Messages",
        "Blocker History",
    ],
}

RELEASE_SURFACES = {
    ROOT / ".github" / "workflows" / "validate.yml": ["python3 scripts/forward_test.py"],
    ROOT / "README.md": ["python3 scripts/forward_test.py", "Project Autopilot loop"],
    ROOT / "README.zh-CN.md": ["python3 scripts/forward_test.py", "Project Autopilot 循环"],
    ROOT / "AGENTS.md": ["python3 scripts/forward_test.py"],
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"Missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_tokens(path: Path, tokens: list[str]) -> None:
    text = read(path)
    for token in tokens:
        if token not in text:
            fail(f"{path.relative_to(ROOT)} is missing {token!r}")


def extract_section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start == -1:
        fail(f"{FORWARD_TESTS.relative_to(ROOT)} is missing heading {marker!r}")
    next_heading = text.find("\n## ", start + len(marker))
    if next_heading == -1:
        return text[start:]
    return text[start:next_heading]


def main() -> int:
    forward_text = read(FORWARD_TESTS)

    for scenario, tokens in SCENARIO_REQUIREMENTS.items():
        section = extract_section(forward_text, scenario)
        for token in tokens:
            if token not in section:
                fail(f"{scenario} is missing {token!r}")

    checklist_tokens = [
        "heartbeat vs cron",
        "persistent instructions",
        "repeated GitHub comments",
        "merge, push, deploy, publish",
        "verification commands",
    ]
    review_section = extract_section(forward_text, "Review Checklist")
    for token in checklist_tokens:
        if token not in review_section:
            fail(f"Review checklist is missing {token!r}")

    for path, tokens in CORE_COVERAGE.items():
        require_tokens(path, tokens)

    for path, tokens in RELEASE_SURFACES.items():
        require_tokens(path, tokens)

    print("Forward-test validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
