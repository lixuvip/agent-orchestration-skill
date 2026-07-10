#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import tempfile


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
    SKILL_DIR / "scripts" / "run_agy_print.py",
    SKILL_DIR / "scripts" / "ensure_agy_review_agents_guidance.py",
    SKILL_DIR / "scripts" / "append_agy_review_quality_log.py",
    SKILL_DIR / "references" / "COMMUNICATION_PROTOCOL.md",
    SKILL_DIR / "references" / "CONTROLLER_LOOP.md",
    SKILL_DIR / "references" / "ORCHESTRATION_INTAKE.md",
    SKILL_DIR / "references" / "AGY_GEMINI_REVIEW.md",
    SKILL_DIR / "references" / "AGY_GEMINI_RESEARCH.md",
    SKILL_DIR / "references" / "PROJECT_AUTOPILOT.md",
    SKILL_DIR / "references" / "AUTOMATION_TOOLING.md",
    SKILL_DIR / "references" / "PROJECT_INSTRUCTIONS_DISCOVERY.md",
    SKILL_DIR / "references" / "STATE_MACHINE.md",
    SKILL_DIR / "references" / "WORKFLOWS.md",
    SKILL_DIR / "references" / "AUTOMATION_MONITORING.md",
    SKILL_DIR / "references" / "templates" / "agents_guidance_snippet.template.md",
    SKILL_DIR / "references" / "templates" / "agents_guidance_snippet.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_prompt.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_prompt.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality_log.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality_log.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_report.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_report.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_prompt.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_prompt.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_quality.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_quality.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_quality_log.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_quality_log.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_report.template.md",
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_report.zh-CN.template.md",
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


def verify_agy_print_helper_shape() -> None:
    script = SKILL_DIR / "scripts" / "run_agy_print.py"
    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            "--add-dir",
            "/tmp/example-project",
            "--prompt",
            "Reply exactly: READY",
            "--print-timeout",
            "20s",
            "--dry-run",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"run_agy_print.py dry-run failed: {completed.stderr.strip()}")

    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines or lines[0] != "AGY_PRINT_COMMAND_OK":
        fail("run_agy_print.py dry-run did not report AGY_PRINT_COMMAND_OK")
    try:
        argv = json.loads(lines[1])
    except (IndexError, json.JSONDecodeError) as exc:
        fail(f"run_agy_print.py dry-run did not emit argv JSON: {exc}")

    try:
        print_index = argv.index("--print")
    except ValueError:
        fail("run_agy_print.py dry-run argv is missing --print")
    if print_index + 1 >= len(argv) or argv[print_index + 1] != "<PROMPT>":
        fail("run_agy_print.py does not place the prompt immediately after --print")
    if "--add-dir" not in argv:
        fail("run_agy_print.py dry-run argv is missing --add-dir")
    add_dir_index = argv.index("--add-dir")
    if add_dir_index + 1 >= len(argv) or argv[add_dir_index + 1] != "/tmp/example-project":
        fail("run_agy_print.py dry-run did not preserve the --add-dir value")
    if "--expect-substring" in argv:
        fail("run_agy_print.py dry-run unexpectedly injected --expect-substring")


def verify_agy_print_helper_empty_output_failure() -> None:
    script = SKILL_DIR / "scripts" / "run_agy_print.py"
    with tempfile.TemporaryDirectory() as tmp:
        stub = Path(tmp) / "agy-empty"
        stub.write_text("#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n", encoding="utf-8")
        stub.chmod(0o755)

        completed = subprocess.run(
            [
                sys.executable,
                str(script),
                "--agy-bin",
                str(stub),
                "--prompt",
                "Reply exactly: READY",
                "--print-timeout",
                "20s",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 3:
            fail(
                "run_agy_print.py did not treat zero-byte stdout as failure: "
                f"code={completed.returncode} stderr={completed.stderr.strip()!r}"
            )
        if "AGY_PRINT_EMPTY_OUTPUT" not in completed.stderr:
            fail("run_agy_print.py did not emit AGY_PRINT_EMPTY_OUTPUT for zero-byte stdout")


def verify_agy_print_helper_first_line_failure() -> None:
    script = SKILL_DIR / "scripts" / "run_agy_print.py"
    with tempfile.TemporaryDirectory() as tmp:
        stub = Path(tmp) / "agy-narration"
        stub.write_text(
            "#!/usr/bin/env python3\nprint('I will inspect the repo first.')\nprint('AGY_RESEARCH_V1')\n",
            encoding="utf-8",
        )
        stub.chmod(0o755)

        completed = subprocess.run(
            [
                sys.executable,
                str(script),
                "--agy-bin",
                str(stub),
                "--prompt",
                "Reply exactly: READY",
                "--print-timeout",
                "20s",
                "--expect-first-line",
                "AGY_RESEARCH_V1",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 5:
            fail(
                "run_agy_print.py did not reject narration before the schema token: "
                f"code={completed.returncode} stderr={completed.stderr.strip()!r}"
            )
        if "AGY_PRINT_FIRST_LINE_FAILED" not in completed.stderr:
            fail("run_agy_print.py did not emit AGY_PRINT_FIRST_LINE_FAILED for narration-first output")


def verify_agy_print_helper_rejects_gemini_cli() -> None:
    script = SKILL_DIR / "scripts" / "run_agy_print.py"
    with tempfile.TemporaryDirectory() as tmp:
        stub = Path(tmp) / "gemini"
        stub.write_text("#!/usr/bin/env python3\nprint('wrong surface')\n", encoding="utf-8")
        stub.chmod(0o755)

        completed = subprocess.run(
            [
                sys.executable,
                str(script),
                "--agy-bin",
                str(stub),
                "--prompt",
                "Reply exactly: READY",
                "--print-timeout",
                "20s",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 2:
            fail(
                "run_agy_print.py did not reject the standalone gemini CLI surface: "
                f"code={completed.returncode} stderr={completed.stderr.strip()!r}"
            )
        if "standalone gemini CLI" not in completed.stderr:
            fail("run_agy_print.py did not explain the gemini CLI surface rejection")


def verify_agents_guidance_helper() -> None:
    script = SKILL_DIR / "scripts" / "ensure_agy_review_agents_guidance.py"
    with tempfile.TemporaryDirectory() as tmp:
        project_root = Path(tmp)
        first = subprocess.run(
            [sys.executable, str(script), "--project-root", str(project_root)],
            text=True,
            capture_output=True,
            check=False,
        )
        if first.returncode != 0 or "AGENTS_GUIDANCE_WRITTEN" not in first.stdout:
            fail(
                "ensure_agy_review_agents_guidance.py first write failed: "
                f"{first.stderr.strip()} {first.stdout.strip()}"
        )
        agents_text = (project_root / "AGENTS.md").read_text(encoding="utf-8")
        if "agent-orchestration:agy-gemini-review:start" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not write the guidance marker")
        if "$agent-orchestration" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not require the installed skill at first use")
        if "AGENTS_GUIDANCE_PRESENT" not in agents_text or "AGENTS_GUIDANCE_WRITTEN" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not explain the readiness gate")
        if "--add-dir" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not mention explicit workspace attachment")
        if "command -v agy" not in agents_text or "agy models" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not constrain discovery to agy")
        if "command -v gemini" not in agents_text or "gemini --help" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not forbid gemini CLI probing")
        if "Wrong first moves to avoid" not in agents_text or "gemini` auth/login flows" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not add negative guardrails for the first move")
        if "--expect-substring" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not mention structured-output expectation checks")
        if "Zero-byte stdout" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not mention zero-byte stdout failure")
        if "standalone `gemini` CLI" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not forbid the standalone gemini CLI")
        if "WRONG_EXECUTION_SURFACE" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not mention WRONG_EXECUTION_SURFACE")
        if "AGY_RESEARCH_V1" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not mention research schema checks")
        if "task_type" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not mention research log task_type")

        second = subprocess.run(
            [sys.executable, str(script), "--project-root", str(project_root)],
            text=True,
            capture_output=True,
            check=False,
        )
        if second.returncode != 0 or "AGENTS_GUIDANCE_PRESENT" not in second.stdout:
            fail("ensure_agy_review_agents_guidance.py is not idempotent")

        stale_text = agents_text.replace("Zero-byte stdout is not a successful review or research pass.", "Old text.")
        (project_root / "AGENTS.md").write_text(stale_text, encoding="utf-8")
        stale_check = subprocess.run(
            [sys.executable, str(script), "--project-root", str(project_root), "--check"],
            text=True,
            capture_output=True,
            check=False,
        )
        if stale_check.returncode == 0 or "AGENTS_GUIDANCE_STALE" not in stale_check.stdout:
            fail("ensure_agy_review_agents_guidance.py did not report stale guidance")

        refresh = subprocess.run(
            [sys.executable, str(script), "--project-root", str(project_root)],
            text=True,
            capture_output=True,
            check=False,
        )
        if refresh.returncode != 0 or "AGENTS_GUIDANCE_WRITTEN" not in refresh.stdout:
            fail("ensure_agy_review_agents_guidance.py did not refresh stale guidance")


def main() -> int:
    combined_core = "\n".join(read(path) for path in CORE_FILES)
    for status in STATUSES:
        if status not in combined_core:
            fail(f"Core skill files do not mention status {status}")

    verify_agy_print_helper_shape()
    verify_agy_print_helper_empty_output_failure()
    verify_agy_print_helper_first_line_failure()
    verify_agy_print_helper_rejects_gemini_cli()
    verify_agents_guidance_helper()

    require_all(
        SKILL_DIR / "agents" / "openai.yaml",
        [
            "Use $agent-orchestration immediately",
            "agy/Gemini external review or research",
            "do not inspect or launch the standalone gemini CLI",
        ],
    )
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
        SKILL_DIR / "references" / "AGY_GEMINI_REVIEW.md",
        [
            "Gemini 3.5 Flash (High)",
            "AGY_UNAVAILABLE",
            "TIMED_OUT",
            "SCOPE_DRIFT",
            "WRONG_EXECUTION_SURFACE",
            "standalone `gemini` CLI",
            "AGY_PRINT_EMPTY_OUTPUT",
            "AGY_PRINT_FIRST_LINE_FAILED",
            "--expect-substring",
            "coordinator must classify",
            "dedicated report",
            "agy-review-quality.jsonl",
            "ensure_agy_review_agents_guidance.py",
            "AGENTS_GUIDANCE_WRITTEN",
            "run_agy_print.py",
            "--add-dir \"$PROJECT_ROOT\"",
            "agy --print <prompt>",
            "agy --print --model",
            "dual Codex + Gemini review",
            "Gemini-only",
            "Codex-only",
            "falsification check",
            "append_agy_review_quality_log.py",
            "LOG_WRITTEN",
            "template_tuning_suggestions",
            "Negative Guardrails",
            "stop and return to the documented preflight",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "AGY_GEMINI_RESEARCH.md",
        [
            "parallel Codex + Gemini research",
            "Gemini 3.5 Flash (High)",
            "AGY_RESEARCH_V1",
            "WRONG_EXECUTION_SURFACE",
            "standalone `gemini` CLI",
            "--expect-substring",
            "\"task_type\": \"research\"",
            "append_agy_review_quality_log.py",
            "follow-up questions",
            "accepted",
            "rejected",
            "Negative Guardrails",
            "stop and return to the documented preflight",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_review_prompt.template.md",
        [
            "AGY_REVIEW_V2",
            "Gemini via agy",
            "run_agy_print.py",
            "Negative guardrails:",
            "standalone `gemini` CLI",
            "--expect-first-line",
            "--expect-substring",
            "commands_run: NONE",
            "verification_claims:",
            "coordinator_check:",
            "no_test_claims",
            "no_cli_drift",
            "no_scope_inflation",
            "no_generic_padding",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_review_prompt.zh-CN.template.md",
        [
            "Negative guardrails:",
            "standalone `gemini` CLI",
            "no_cli_drift",
            "no_scope_inflation",
            "no_generic_padding",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality.template.md",
        [
            "AGY_REVIEW_QUALITY_V1",
            "unsupported_claims:",
            "scope_drift:",
            "coordinator_follow_up:",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality_log.template.md",
        [
            "agy-review-quality.jsonl",
            "append_agy_review_quality_log.py",
            "LOG_WRITTEN",
            "Do not store secrets",
            "quality_score",
            "template_tuning_suggestions",
            "unsupported_claims",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality_log.zh-CN.template.md",
        [
            "agy-review-quality.jsonl",
            "append_agy_review_quality_log.py",
            "LOG_WRITTEN",
            "不要记录密钥",
            "quality_score",
            "template_tuning_suggestions",
            "unsupported_claims",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_review_report.template.md",
        [
            "Agy External Review Report",
            "Preflight:",
            "--add-dir <project_root>",
            "--print <prompt> --sandbox",
            "Quality log:",
            "Agy Findings",
            "Dual Review Comparison",
            "Gemini-only findings",
            "Codex-only findings",
            "Quality Evaluation",
            "Codex Verification",
            "Recommended Next Steps",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_review_report.zh-CN.template.md",
        [
            "Agy 外部审查报告",
            "前置检查",
            "--add-dir <project_root>",
            "--print <prompt> --sandbox",
            "质量日志",
            "Agy Findings",
            "双轨审查对比",
            "Gemini-only",
            "Codex-only",
            "质量评估",
            "Codex 复核结论",
            "建议下一步",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_research_prompt.template.md",
        [
            "AGY_RESEARCH_V1",
            "Gemini via agy",
            "run_agy_print.py",
            "Negative guardrails:",
            "standalone `gemini` CLI",
            "--expect-first-line",
            "--expect-substring",
            "external_fact_mode:",
            "coordinator_check:",
            "no_fake_validation",
            "no_cli_drift",
            "no_scope_inflation",
            "no_generic_padding",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_research_prompt.zh-CN.template.md",
        [
            "Negative guardrails:",
            "standalone `gemini` CLI",
            "no_cli_drift",
            "no_scope_inflation",
            "no_generic_padding",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_research_quality.template.md",
        [
            "AGY_RESEARCH_QUALITY_V1",
            "unsupported_claims:",
            "scope_drift:",
            "missed_angles:",
            "coordinator_follow_up:",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_research_quality_log.template.md",
        [
            "agy-review-quality.jsonl",
            "append_agy_review_quality_log.py",
            "\"task_type\": \"research\"",
            "valuable_takeaways",
            "follow_up_questions",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_research_report.template.md",
        [
            "Agy External Research Report",
            "Parallel Research Comparison",
            "Gemini-only points",
            "Codex-only points",
            "Codex Synthesis",
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
