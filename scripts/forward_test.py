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
    "Scenario 5: Agy Gemini External Review": [
        "Use $agent-orchestration",
        "agy/Gemini external code review",
        "Gemini means Gemini via agy only",
        "AGY_GEMINI_REVIEW.md",
        "ensure_agy_review_agents_guidance.py",
        "AGENTS_GUIDANCE_PRESENT",
        "AGENTS_GUIDANCE_WRITTEN",
        "agy health check or model discovery",
        "Uses `run_agy_print.py` for normal read-only print mode with `--sandbox`",
        "run_agy_print.py",
        "Does not use the standalone `gemini` CLI",
        "command -v gemini",
        "gemini --version",
        "gemini --help",
        "negative guardrails",
        "scope inflation",
        "WRONG_EXECUTION_SURFACE",
        "--add-dir <project_root>",
        "--expect-substring <token>",
        "--expect-first-line <schema-token>",
        "prompt immediately follows --print",
        "agy --print --mode",
        "dual Codex + Gemini review",
        "Gemini-only",
        "Codex-only",
        "Does not use accept-edits.",
        "Does not claim tests passed unless command output is supplied",
        "Classifies each finding",
        "dedicated review report",
        "agy-review-quality.jsonl",
        "append_agy_review_quality_log.py",
        "LOG_WRITTEN",
        "template tuning",
    ],
    "Scenario 6: Parallel Codex + Gemini Research": [
        "Use $agent-orchestration",
        "parallel with Codex and Gemini",
        "Gemini via agy",
        "read-only second research stream",
        "Codex must still do its own repository reading",
        "run_agy_print.py",
        "Does not use the standalone `gemini` CLI",
        "WRONG_EXECUTION_SURFACE",
        "--add-dir <project_root>",
        "--expect-first-line AGY_RESEARCH_V1",
        "--expect-substring AGY_RESEARCH_V1",
        "AGY_GEMINI_RESEARCH.md",
        "AGENTS_GUIDANCE_PRESENT",
        "AGENTS_GUIDANCE_WRITTEN",
        "agy health check or model discovery",
        "command -v gemini",
        "gemini --version",
        "gemini --help",
        "negative guardrails",
        "scope inflation",
        "agreed points",
        "Gemini-only points",
        "Codex-only points",
        "rejected/speculative points",
        "task_type=research",
        "LOG_WRITTEN",
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
    SKILL_DIR / "references" / "AGY_GEMINI_REVIEW.md": [
        "Gemini 3.5 Flash (High)",
        "AGY_UNAVAILABLE",
        "NO_STRUCTURED_OUTPUT",
        "WRONG_EXECUTION_SURFACE",
        "command -v gemini",
        "gemini --version",
        "gemini --help",
        "Negative Guardrails",
        "standalone `gemini` CLI",
        "AGY_PRINT_EMPTY_OUTPUT",
        "AGY_PRINT_FIRST_LINE_FAILED",
        "Coordinator Acceptance",
        "dedicated report",
        "ensure_agy_review_agents_guidance.py",
        "AGENTS_GUIDANCE_WRITTEN",
        "run_agy_print.py",
        "--add-dir \"$PROJECT_ROOT\"",
        "--expect-substring 'READY'",
        "agy --print <prompt>",
        "dual Codex + Gemini review",
        "Gemini-only",
        "Codex-only",
        "agy-review-quality.jsonl",
        "append_agy_review_quality_log.py",
        "LOG_WRITTEN",
        "template_tuning_suggestions",
    ],
    SKILL_DIR / "references" / "AGY_GEMINI_RESEARCH.md": [
        "Gemini 3.5 Flash (High)",
        "parallel Codex + Gemini research",
        "AGY_RESEARCH_V1",
        "NO_STRUCTURED_OUTPUT",
        "WRONG_EXECUTION_SURFACE",
        "command -v gemini",
        "gemini --version",
        "gemini --help",
        "Negative Guardrails",
        "standalone `gemini` CLI",
        "--add-dir \"$PROJECT_ROOT\"",
        "\"task_type\": \"research\"",
        "accepted",
        "speculative",
        "append_agy_review_quality_log.py",
    ],
    SKILL_DIR / "agents" / "openai.yaml": [
        "Use $agent-orchestration immediately",
        "do not inspect or launch the standalone gemini CLI",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_prompt.template.md": [
        "AGY_REVIEW_V2",
        "Gemini via agy",
        "Negative guardrails:",
        "standalone `gemini` CLI",
        "--expect-first-line",
        "commands_run: NONE",
        "verification_claims:",
        "coordinator_check:",
        "no_cli_drift",
        "no_scope_inflation",
        "no_generic_padding",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality.template.md": [
        "AGY_REVIEW_QUALITY_V1",
        "unsupported_claims:",
        "scope_drift:",
        "coordinator_follow_up:",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality_log.template.md": [
        "agy-review-quality.jsonl",
        "append_agy_review_quality_log.py",
        "LOG_WRITTEN",
        "Do not store secrets",
        "quality_score",
        "template_tuning_suggestions",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_report.template.md": [
        "Agy External Review Report",
        "Preflight:",
        "--add-dir <project_root>",
        "--print <prompt> --sandbox",
        "Quality log:",
        "Agy Findings",
        "Dual Review Comparison",
        "Gemini-only findings",
        "Codex-only findings",
        "Codex Verification",
        "Recommended Next Steps",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_prompt.template.md": [
        "AGY_RESEARCH_V1",
        "Gemini via agy",
        "Negative guardrails:",
        "standalone `gemini` CLI",
        "--expect-first-line",
        "external_fact_mode:",
        "coordinator_check:",
        "no_fake_validation",
        "no_cli_drift",
        "no_scope_inflation",
        "no_generic_padding",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_quality.template.md": [
        "AGY_RESEARCH_QUALITY_V1",
        "unsupported_claims:",
        "scope_drift:",
        "missed_angles:",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_quality_log.template.md": [
        "agy-review-quality.jsonl",
        "append_agy_review_quality_log.py",
        "\"task_type\": \"research\"",
        "valuable_takeaways",
        "follow_up_questions",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_report.template.md": [
        "Agy External Research Report",
        "Parallel Research Comparison",
        "Gemini-only points",
        "Codex-only points",
        "Codex Synthesis",
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
        "external model review",
        "test/build hallucinations",
        "command -v gemini",
        "negative guardrails",
        "invalid `agy --print --mode ... \"$PROMPT\"` command shape",
        "--expect-first-line <schema-token>",
        "stable agy/Gemini command-safety guidance in `AGENTS.md`",
        "agy health check or model discovery",
        "quality log",
        "external review from external research",
        "Codex-only and Gemini-only research points",
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
