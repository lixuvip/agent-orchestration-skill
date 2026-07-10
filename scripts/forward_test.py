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
        "fenced lease",
        "ACTIVE -> DRAINING -> CLOSED",
        "one final summary",
        "confirmed delete or pause cleanup",
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
        "fenced lease and fencing token",
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
        "check-only",
        "separately authorized",
        "Uses `run_agy_print.py` for normal read-only print mode with `--sandbox`",
        "run_agy_print.py",
        "Does not use the standalone `gemini` CLI",
        "command -v gemini",
        "gemini --version",
        "gemini --help",
        "negative guardrails",
        "scope inflation",
        "WRONG_EXECUTION_SURFACE",
        "build_agy_context_bundle.py",
        "allowlisted bundle",
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
        "external-review-ledger",
        "append_agy_review_quality_log.py",
        "LOG_ALREADY_PRESENT",
        "$CODEX_HOME/external-review-ledger/",
        "later coordinator synthesis",
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
        "build_agy_context_bundle.py",
        "--expect-first-line AGY_RESEARCH_V1",
        "--expect-substring AGY_RESEARCH_V1",
        "AGY_GEMINI_RESEARCH.md",
        "check-only",
        "separate write authorization",
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
        "LOG_ALREADY_PRESENT",
        "$CODEX_HOME/external-review-ledger/",
    ],
    "Scenario 7: Stale Callback And Commit-Pinned Gates": [
        "Use $agent-orchestration",
        "Engineering attempt 1 reported DONE at commit aaaaaaa",
        "attempt 2 produced commit bbbbbbb",
        "duplicate QA callback",
        "commit ccccccc",
        "ORCHESTRATION_PROTOCOL.md",
        "role execution, gate verdict, and coordinator state separate",
        "stale by attempt and dispatch nonce",
        "duplicate no-op",
        "role `DONE` as coordinator `ACCEPTED`",
        "Invalidates QA evidence for bbbbbbb",
        "pinned to ccccccc",
        "scripts/orchestration_event.py",
        "ORCHESTRATION_EVENT_V1",
    ],
    "Scenario 8: Lite To Durable Route Escalation": [
        "Use $agent-orchestration",
        "one read-only agy second opinion",
        "one engineer and one read-only QA role asynchronously",
        "every two hours",
        "ORCHESTRATION_ROUTING.md",
        "chooses Lite",
        "external review as a modifier",
        "Upgrades to Standard",
        "dispatch identity, callbacks, task board, and heartbeat",
        "Upgrades to Durable",
        "goal contract, cron, durable memory, fenced lease, and lifecycle rules",
        "requested Lite mode remove Durable safety requirements",
        "Isolates or serializes parallel shared-file edits",
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
        "AUTOMATION_CONCURRENCY.md",
        "ACTIVE -> DRAINING -> CLOSED",
    ],
    SKILL_DIR / "references" / "AUTOMATION_CONCURRENCY.md": [
        "scripts/automation_lease.py",
        "fencing token",
        "LEASE_BUSY",
        "LEASE_NOT_OWNER",
        "ACTIVE -> DRAINING -> CLOSED",
        "scripts/heartbeat_lifecycle.py",
        "final-summary key",
        "cleanup confirmation",
    ],
    SKILL_DIR / "scripts" / "automation_lease.py": [
        "fencing_token",
        "LEASE_BUSY",
        "LEASE_EXPIRED",
        "LEASE_NOT_OWNER",
        "LEASE_ALREADY_RELEASED",
    ],
    SKILL_DIR / "scripts" / "heartbeat_lifecycle.py": [
        "ACTIVE",
        "DRAINING",
        "CLOSED",
        "POST_FINAL_SUMMARY",
        "CLOSE_HEARTBEAT",
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
        "Silence: never completion",
        "Role `DONE` moves the coordinator to `IN_REVIEW`",
        "A code-changing retry invalidates earlier QA and review evidence.",
    ],
    SKILL_DIR / "references" / "ORCHESTRATION_PROTOCOL.md": [
        "ORCHESTRATION_EVENT_V1",
        "dispatch_nonce",
        "coordinator_epoch",
        "DUPLICATE",
        "STALE",
        "Accepted Delivery Predicate",
        "Any subsequent code commit invalidates earlier QA and review verdicts",
        "scripts/orchestration_event.py",
    ],
    SKILL_DIR / "references" / "ORCHESTRATION_ROUTING.md": [
        "`LITE`",
        "`STANDARD`",
        "`DURABLE`",
        "Minimum Safe Route",
        "External-model review or research is a modifier",
        "scripts/route_orchestration.py",
        "ISOLATE_OR_SERIALIZE_SHARED_EDITS",
    ],
    SKILL_DIR / "scripts" / "route_orchestration.py": [
        "minimum_mode",
        "selected_mode",
        "requested_mode_honored",
        "HEARTBEAT",
        "CRON",
        "EXTERNAL_MODEL_SECOND_OPINION",
        "ISOLATE_OR_SERIALIZE_SHARED_EDITS",
    ],
    SKILL_DIR / "scripts" / "orchestration_event.py": [
        "ORCHESTRATION_EVENT_V1",
        "classify_event",
        "accepted_delivery",
        "EVENT_DUPLICATE",
        "EVENT_STALE",
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
        "check-only",
        "run_agy_print.py",
        "build_agy_context_bundle.py",
        "allowlisted bundle",
        "host-side timeout",
        "--expect-substring 'READY'",
        "agy --print <prompt>",
        "dual Codex + Gemini review",
        "Gemini-only",
        "Codex-only",
        "agy-review-quality.jsonl",
        "external-review-ledger",
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
        "build_agy_context_bundle.py",
        "allowlisted bundle",
        "\"task_type\": \"research\"",
        "accepted",
        "speculative",
        "append_agy_review_quality_log.py",
        "external-review-ledger",
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
        "--add-dir <allowlisted_context>",
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
        "--add-dir <allowlisted_context>",
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
    ROOT / ".github" / "workflows" / "validate.yml": [
        "python3 scripts/forward_test.py",
        "python3 scripts/protocol_test.py",
        "python3 scripts/automation_test.py",
        "python3 scripts/routing_test.py",
    ],
    ROOT / "README.md": ["python3 scripts/forward_test.py", "Project Autopilot loop"],
    ROOT / "README.zh-CN.md": ["python3 scripts/forward_test.py", "Project Autopilot 循环"],
    ROOT / "AGENTS.md": [
        "python3 scripts/forward_test.py",
        "python3 scripts/protocol_test.py",
        "python3 scripts/automation_test.py",
        "python3 scripts/routing_test.py",
    ],
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
        "guidance check-only",
        "target-repository writes",
        "quality log",
        "external-review ledger",
        "external review from external research",
        "Codex-only and Gemini-only research points",
        "role execution status, gate verdict, and coordinator state",
        "stale attempt, nonce, epoch, or SHA callbacks",
        "repeated event IDs as no-op",
        "old QA/review evidence after a new code commit",
        "coordinator `ACCEPTED`",
        "fenced lease",
        "`LEASE_BUSY` as a quiet no-op",
        "stale fencing token",
        "ACTIVE -> DRAINING -> CLOSED",
        "one final summary and confirmed cleanup",
        "Lite, Standard, and Durable from actual task shape",
        "external-model second opinion as a modifier",
        "upgrade when async roles or recurring progress appeared",
        "refuse to downgrade recurring work below Durable safety requirements",
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
