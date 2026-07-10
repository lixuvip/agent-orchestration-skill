#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "agent-orchestration"
SKILL_MD = SKILL_DIR / "SKILL.md"


REQUIRED_FILES = [
    SKILL_MD,
    SKILL_DIR / "agents" / "openai.yaml",
    SKILL_DIR / "scripts" / "run_agy_print.py",
    SKILL_DIR / "scripts" / "build_agy_context_bundle.py",
    SKILL_DIR / "scripts" / "ensure_agy_review_agents_guidance.py",
    SKILL_DIR / "scripts" / "append_agy_review_quality_log.py",
    SKILL_DIR / "scripts" / "orchestration_event.py",
    SKILL_DIR / "references" / "AUTOMATION_MONITORING.md",
    SKILL_DIR / "references" / "AUTOMATION_TOOLING.md",
    SKILL_DIR / "references" / "AGY_GEMINI_REVIEW.md",
    SKILL_DIR / "references" / "AGY_GEMINI_RESEARCH.md",
    SKILL_DIR / "references" / "COMMUNICATION_PROTOCOL.md",
    SKILL_DIR / "references" / "CONTROLLER_LOOP.md",
    SKILL_DIR / "references" / "ORCHESTRATION_INTAKE.md",
    SKILL_DIR / "references" / "ORCHESTRATION_PROTOCOL.md",
    SKILL_DIR / "references" / "ORCHESTRATION_PROTOCOL.zh-CN.md",
    SKILL_DIR / "references" / "PROJECT_AUTOPILOT.md",
    SKILL_DIR / "references" / "PROJECT_INSTRUCTIONS_DISCOVERY.md",
    SKILL_DIR / "references" / "STATE_MACHINE.md",
    SKILL_DIR / "references" / "WORKFLOWS.md",
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
    SKILL_DIR / "references" / "examples" / "filled_task_dispatch.md",
    SKILL_DIR / "references" / "examples" / "filled_role_reply.md",
    SKILL_DIR / "references" / "examples" / "filled_project_goal_contract.md",
    SKILL_DIR / "references" / "examples" / "filled_automation_memory.md",
    SKILL_DIR / "references" / "examples" / "filled_noop_tick.md",
    SKILL_DIR / "references" / "examples" / "filled_escalation_report.md",
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
    SKILL_DIR / "references" / "templates" / "monitoring_heartbeat.template.md",
    SKILL_DIR / "references" / "templates" / "monitoring_heartbeat.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "role_reply.template.md",
    SKILL_DIR / "references" / "templates" / "role_reply.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "qa_report.template.md",
    SKILL_DIR / "references" / "templates" / "qa_report.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "review_findings.template.md",
    SKILL_DIR / "references" / "templates" / "review_findings.zh-CN.template.md",
    ROOT / "scripts" / "install_skill.py",
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
    ROOT / "AGENTS.md",
    ROOT / "docs" / "installation.md",
    ROOT / "docs" / "installation.zh-CN.md",
    ROOT / "docs" / "quickstart.md",
    ROOT / "docs" / "quickstart.zh-CN.md",
    ROOT / "docs" / "tutorial.md",
    ROOT / "docs" / "tutorial.zh-CN.md",
    ROOT / "docs" / "examples.md",
    ROOT / "docs" / "examples.zh-CN.md",
    ROOT / "docs" / "forward-tests.md",
    ROOT / "docs" / "publishing.md",
    ROOT / "docs" / "publishing.zh-CN.md",
    ROOT / "docs" / "images" / "logo.svg",
    ROOT / "docs" / "images" / "workflow-overview.svg",
    ROOT / "docs" / "images" / "workflow-overview.zh-CN.svg",
    ROOT / "docs" / "images" / "project-autopilot-loop.svg",
    ROOT / "docs" / "images" / "project-autopilot-loop.zh-CN.svg",
    ROOT / "docs" / "releases" / "v0.1.4.md",
    ROOT / "scripts" / "forward_test.py",
    ROOT / "scripts" / "protocol_test.py",
]


TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".sh", ".py", ".svg"}

TEMPLATE_REQUIREMENTS = {
    SKILL_DIR / "references" / "templates" / "task_dispatch.template.md": [
        "ORCHESTRATION_EVENT_V1",
        "Dispatch nonce:",
        "Coordinator epoch:",
        "Expected head SHA:",
        "Verification:",
        "Callback:",
        "Branch / worktree:",
        "Merge policy:",
    ],
    SKILL_DIR / "references" / "templates" / "task_dispatch.zh-CN.template.md": [
        "ORCHESTRATION_EVENT_V1",
        "Dispatch nonce:",
        "Coordinator epoch:",
        "Expected head SHA:",
        "验证要求",
        "回调",
        "分支 / 工作区",
        "合并策略",
    ],
    SKILL_DIR / "references" / "templates" / "orchestration_intake.template.md": [
        "Execution surface:",
        "Callback behavior:",
        "Merge/push permission:",
        "Ask only if",
    ],
    SKILL_DIR / "references" / "templates" / "orchestration_intake.zh-CN.template.md": [
        "执行位置",
        "回调方式",
        "合并/推送权限",
        "仅在",
    ],
    SKILL_DIR / "references" / "templates" / "coordinator_callback.template.md": [
        "Task ID:",
        "Branch / worktree:",
        "Execution status:",
        "Gate verdict:",
        "ORCHESTRATION_EVENT_V1",
        "Verification:",
        "Suggested coordinator action:",
    ],
    SKILL_DIR / "references" / "templates" / "coordinator_callback.zh-CN.template.md": [
        "Task ID:",
        "分支 / 工作区",
        "Execution status:",
        "Gate verdict:",
        "ORCHESTRATION_EVENT_V1",
        "验证结果",
        "建议协调者下一步",
    ],
    SKILL_DIR / "references" / "templates" / "status_request.template.md": [
        "Status request",
        "Coordinator thread ID",
        "Reply with one",
    ],
    SKILL_DIR / "references" / "templates" / "status_request.zh-CN.template.md": [
        "状态请求",
        "协调者线程 ID",
        "请回复一个",
    ],
    SKILL_DIR / "references" / "templates" / "merge_readiness.template.md": [
        "Merge readiness",
        "Base branch:",
        "Working tree:",
        "Expected head SHA:",
        "Gates pinned to observed head SHA:",
        "Coordinator state:",
        "Push permission:",
    ],
    SKILL_DIR / "references" / "templates" / "merge_readiness.zh-CN.template.md": [
        "合并就绪",
        "基准分支",
        "工作区",
        "Expected head SHA:",
        "绑定到 observed head SHA 的门禁",
        "Coordinator state:",
        "推送权限",
    ],
    SKILL_DIR / "references" / "templates" / "role_reply.template.md": [
        "Execution status:",
        "Gate verdict:",
        "ORCHESTRATION_EVENT_V1",
        '"dispatch_nonce"',
        '"observed_head_sha"',
        "Verification run:",
        "Risks / concerns:",
        "Recommended next role:",
    ],
    SKILL_DIR / "references" / "templates" / "role_reply.zh-CN.template.md": [
        "Execution status:",
        "Gate verdict:",
        "ORCHESTRATION_EVENT_V1",
        '"dispatch_nonce"',
        '"observed_head_sha"',
        "已运行验证",
        "风险 / 顾虑",
        "建议下一角色",
    ],
    SKILL_DIR / "references" / "templates" / "qa_report.template.md": [
        "Expected head SHA:",
        "Observed head SHA:",
        "Gate verdict:",
        "ORCHESTRATION_EVENT_V1",
    ],
    SKILL_DIR / "references" / "templates" / "qa_report.zh-CN.template.md": [
        "Expected head SHA:",
        "Observed head SHA:",
        "Gate verdict:",
        "ORCHESTRATION_EVENT_V1",
    ],
    SKILL_DIR / "references" / "templates" / "review_findings.template.md": [
        "Expected head SHA:",
        "Observed head SHA:",
        "Gate verdict:",
        "ORCHESTRATION_EVENT_V1",
    ],
    SKILL_DIR / "references" / "templates" / "review_findings.zh-CN.template.md": [
        "Expected head SHA:",
        "Observed head SHA:",
        "Gate verdict:",
        "ORCHESTRATION_EVENT_V1",
    ],
    SKILL_DIR / "references" / "templates" / "monitoring_heartbeat.template.md": [
        "Status",
        "Verification",
        "Risks",
        "All roles terminal",
        "status request",
    ],
    SKILL_DIR / "references" / "templates" / "monitoring_heartbeat.zh-CN.template.md": [
        "Status",
        "Verification",
        "Risks",
        "All roles terminal",
        "状态请求",
    ],
    SKILL_DIR / "references" / "templates" / "project_goal_contract.template.md": [
        "Done when:",
        "Instruction sources:",
        "Allowed autonomously:",
        "Requires confirmation:",
        "Verification commands:",
        "Memory path:",
    ],
    SKILL_DIR / "references" / "templates" / "project_goal_contract.zh-CN.template.md": [
        "完成条件",
        "指令来源",
        "可自动执行",
        "必须确认",
        "验证命令",
        "记忆路径",
    ],
    SKILL_DIR / "references" / "templates" / "automation_plan.template.md": [
        "Automation kind:",
        "Existing automation check:",
        "Memory path:",
        "Prompt responsibilities:",
        "Requires user review before saving:",
    ],
    SKILL_DIR / "references" / "templates" / "automation_plan.zh-CN.template.md": [
        "自动化类型",
        "已有自动化检查",
        "记忆路径",
        "提示词职责",
        "保存前需要用户确认",
    ],
    SKILL_DIR / "references" / "templates" / "automation_tick.template.md": [
        "Latest effective update:",
        "Action taken:",
        "Verification:",
        "Memory updated:",
        "Next safe action:",
        "Escalation needed:",
    ],
    SKILL_DIR / "references" / "templates" / "automation_tick.zh-CN.template.md": [
        "Latest effective update:",
        "Action taken:",
        "Verification:",
        "Memory updated:",
        "Next safe action:",
        "Escalation needed:",
    ],
    SKILL_DIR / "references" / "templates" / "automation_memory.template.md": [
        "Latest Effective Update",
        "Last Tick",
        "Next Safe Action",
        "Blocker History",
        "Posted Messages",
    ],
    SKILL_DIR / "references" / "templates" / "automation_memory.zh-CN.template.md": [
        "最新有效更新",
        "上一次 Tick",
        "下一步安全动作",
        "阻塞历史",
        "已发送消息",
    ],
    SKILL_DIR / "references" / "templates" / "escalation_report.template.md": [
        "Project autopilot escalation",
        "Why I stopped:",
        "Evidence:",
        "Decision needed:",
        "Recommended next action:",
    ],
    SKILL_DIR / "references" / "templates" / "escalation_report.zh-CN.template.md": [
        "项目 Autopilot 升级",
        "我为什么停止",
        "证据",
        "需要你决策",
        "建议下一步",
    ],
    SKILL_DIR / "references" / "templates" / "agents_guidance_snippet.template.md": [
        "Codex Project Autopilot",
        "Required verification",
        "Safe autonomous actions",
        "Actions requiring confirmation",
        "Idempotency rule",
    ],
    SKILL_DIR / "references" / "templates" / "agents_guidance_snippet.zh-CN.template.md": [
        "Codex 项目 Autopilot",
        "声明进展前必须验证",
        "可自动执行的安全动作",
        "必须确认的动作",
        "幂等规则",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_prompt.template.md": [
        "AGY_REVIEW_V2",
        "Gemini via agy",
        "run_agy_print.py",
        "Negative guardrails:",
        "standalone `gemini` CLI",
        "--expect-first-line",
        "build_agy_context_bundle.py",
        "allowlisted bundle",
        "--expect-substring",
        "commands_run: NONE",
        "verification_claims:",
        "coordinator_check:",
        "self_check:",
        "no_cli_drift:",
        "no_scope_inflation:",
        "no_generic_padding:",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_prompt.zh-CN.template.md": [
        "AGY_REVIEW_V2",
        "Gemini via agy",
        "run_agy_print.py",
        "Negative guardrails:",
        "standalone `gemini` CLI",
        "--expect-first-line",
        "build_agy_context_bundle.py",
        "allowlist bundle",
        "--expect-substring",
        "commands_run: NONE",
        "verification_claims:",
        "coordinator_check:",
        "self_check:",
        "no_cli_drift:",
        "no_scope_inflation:",
        "no_generic_padding:",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality.template.md": [
        "AGY_REVIEW_QUALITY_V1",
        "unsupported_claims:",
        "scope_drift:",
        "coordinator_follow_up:",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality.zh-CN.template.md": [
        "AGY_REVIEW_QUALITY_V1",
        "unsupported_claims:",
        "scope_drift:",
        "coordinator_follow_up:",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality_log.template.md": [
        "agy-review-quality.jsonl",
        "append_agy_review_quality_log.py",
        "run_agy_print.py",
        "--add-dir <allowlisted_context>",
        "--print <prompt> --sandbox",
        "LOG_WRITTEN",
        "LOG_ALREADY_PRESENT",
        "external-review-ledger",
        "Do not store secrets",
        "quality_score",
        "template_tuning_suggestions",
        "unsupported_claims",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality_log.zh-CN.template.md": [
        "agy-review-quality.jsonl",
        "append_agy_review_quality_log.py",
        "run_agy_print.py",
        "--add-dir <allowlisted_context>",
        "--print <prompt> --sandbox",
        "LOG_WRITTEN",
        "LOG_ALREADY_PRESENT",
        "external-review-ledger",
        "不要记录密钥",
        "quality_score",
        "template_tuning_suggestions",
        "unsupported_claims",
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
        "Quality Evaluation",
        "Codex Verification",
        "Recommended Next Steps",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_review_report.zh-CN.template.md": [
        "Agy 外部审查报告",
        "前置检查",
        "--add-dir <allowlisted_context>",
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
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_prompt.template.md": [
        "AGY_RESEARCH_V1",
        "Gemini via agy",
        "run_agy_print.py",
        "Negative guardrails:",
        "standalone `gemini` CLI",
        "--expect-first-line",
        "build_agy_context_bundle.py",
        "allowlisted bundle",
        "--expect-substring",
        "commands_run: NONE",
        "external_fact_mode:",
        "coordinator_check:",
        "self_check:",
        "no_cli_drift:",
        "no_scope_inflation:",
        "no_generic_padding:",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_prompt.zh-CN.template.md": [
        "AGY_RESEARCH_V1",
        "Gemini via agy",
        "run_agy_print.py",
        "Negative guardrails:",
        "standalone `gemini` CLI",
        "--expect-first-line",
        "build_agy_context_bundle.py",
        "allowlist bundle",
        "--expect-substring",
        "commands_run: NONE",
        "external_fact_mode:",
        "coordinator_check:",
        "self_check:",
        "no_cli_drift:",
        "no_scope_inflation:",
        "no_generic_padding:",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_quality.template.md": [
        "AGY_RESEARCH_QUALITY_V1",
        "unsupported_claims:",
        "scope_drift:",
        "missed_angles:",
        "coordinator_follow_up:",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_quality.zh-CN.template.md": [
        "AGY_RESEARCH_QUALITY_V1",
        "unsupported_claims:",
        "scope_drift:",
        "missed_angles:",
        "coordinator_follow_up:",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_quality_log.template.md": [
        "agy-review-quality.jsonl",
        "append_agy_review_quality_log.py",
        "run_agy_print.py",
        "--add-dir <allowlisted_context>",
        "--print <prompt> --sandbox",
        "LOG_WRITTEN",
        "LOG_ALREADY_PRESENT",
        "external-review-ledger",
        "Do not store secrets",
        "\"task_type\": \"research\"",
        "valuable_takeaways",
        "follow_up_questions",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_quality_log.zh-CN.template.md": [
        "agy-review-quality.jsonl",
        "append_agy_review_quality_log.py",
        "run_agy_print.py",
        "--add-dir <allowlisted_context>",
        "--print <prompt> --sandbox",
        "LOG_WRITTEN",
        "LOG_ALREADY_PRESENT",
        "external-review-ledger",
        "不要记录密钥",
        "\"task_type\": \"research\"",
        "valuable_takeaways",
        "follow_up_questions",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_report.template.md": [
        "Agy External Research Report",
        "Preflight:",
        "--add-dir <allowlisted_context>",
        "--print <prompt> --sandbox",
        "Quality log:",
        "Agy Research Points",
        "Parallel Research Comparison",
        "Gemini-only points",
        "Codex-only points",
        "Quality Evaluation",
        "Codex Synthesis",
        "Recommended Next Steps",
    ],
    SKILL_DIR / "references" / "templates" / "agy_gemini_research_report.zh-CN.template.md": [
        "Agy 外部调研报告",
        "前置检查",
        "--add-dir <allowlisted_context>",
        "--print <prompt> --sandbox",
        "质量日志",
        "Agy Research Points",
        "并行调研对比",
        "Gemini-only",
        "Codex-only",
        "质量评估",
        "Codex 综合判断",
        "建议下一步",
    ],
}

DISCOVERABLE_REFERENCES = [
    "ORCHESTRATION_PROTOCOL.md",
    "ORCHESTRATION_PROTOCOL.zh-CN.md",
    "STATE_MACHINE.md",
    "ORCHESTRATION_INTAKE.md",
    "CONTROLLER_LOOP.md",
    "AGY_GEMINI_REVIEW.md",
    "AGY_GEMINI_RESEARCH.md",
    "PROJECT_AUTOPILOT.md",
    "AUTOMATION_TOOLING.md",
    "PROJECT_INSTRUCTIONS_DISCOVERY.md",
    "task_dispatch.zh-CN.template.md",
    "orchestration_intake.zh-CN.template.md",
    "coordinator_callback.zh-CN.template.md",
    "status_request.zh-CN.template.md",
    "merge_readiness.zh-CN.template.md",
    "project_goal_contract.zh-CN.template.md",
    "automation_plan.zh-CN.template.md",
    "automation_tick.zh-CN.template.md",
    "automation_memory.zh-CN.template.md",
    "escalation_report.zh-CN.template.md",
    "agents_guidance_snippet.zh-CN.template.md",
    "agy_gemini_review_prompt.template.md",
    "agy_gemini_review_prompt.zh-CN.template.md",
    "agy_gemini_review_quality.template.md",
    "agy_gemini_review_quality.zh-CN.template.md",
    "agy_gemini_review_quality_log.template.md",
    "agy_gemini_review_quality_log.zh-CN.template.md",
    "agy_gemini_research_prompt.template.md",
    "agy_gemini_research_prompt.zh-CN.template.md",
    "agy_gemini_research_quality.template.md",
    "agy_gemini_research_quality.zh-CN.template.md",
    "agy_gemini_research_quality_log.template.md",
    "agy_gemini_research_quality_log.zh-CN.template.md",
    "agy_gemini_research_report.template.md",
    "agy_gemini_research_report.zh-CN.template.md",
    "run_agy_print.py",
    "build_agy_context_bundle.py",
    "ensure_agy_review_agents_guidance.py",
    "append_agy_review_quality_log.py",
    "orchestration_event.py",
    "agy_gemini_review_report.template.md",
    "agy_gemini_review_report.zh-CN.template.md",
    "role_reply.zh-CN.template.md",
    "qa_report.zh-CN.template.md",
    "review_findings.zh-CN.template.md",
    "monitoring_heartbeat.zh-CN.template.md",
    "filled_task_dispatch.md",
    "filled_role_reply.md",
    "filled_project_goal_contract.md",
    "filled_automation_memory.md",
    "filled_noop_tick.md",
    "filled_escalation_report.md",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(?P<body>.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail("SKILL.md must start with YAML frontmatter")

    fields: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            fail(f"Invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def iter_text_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix in TEXT_SUFFIXES
    ]


def validate_markdown_links(path: Path, content: str) -> None:
    if path.suffix != ".md":
        return

    for match in re.finditer(r"!?\[[^\]]+\]\(([^)]+)\)", content):
        target = match.group(1).strip()
        if not target or "://" in target or target.startswith("#") or target.startswith("mailto:"):
            continue

        target = target.split("#", 1)[0].strip()
        if not target:
            continue

        target = target.strip("<>")
        target = unquote(target)
        if not (path.parent / target).exists():
            fail(f"Broken local markdown link in {path.relative_to(ROOT)}: {match.group(1)}")


def validate_svg(path: Path) -> None:
    if path.suffix != ".svg":
        return
    try:
        ET.parse(path)
    except ET.ParseError as exc:
        fail(f"Invalid SVG XML in {path.relative_to(ROOT)}: {exc}")


def validate_template_requirements() -> None:
    for path, required_tokens in TEMPLATE_REQUIREMENTS.items():
        content = path.read_text(encoding="utf-8")
        for token in required_tokens:
            if token not in content:
                fail(f"Template {path.relative_to(ROOT)} is missing required token {token!r}")


def validate_reference_discovery() -> None:
    skill_text = SKILL_MD.read_text(encoding="utf-8")
    reference_readme = (SKILL_DIR / "references" / "README.md").read_text(encoding="utf-8")
    combined = f"{skill_text}\n{reference_readme}"
    for token in DISCOVERABLE_REFERENCES:
        if token not in combined:
            fail(f"Reference resource {token!r} is not discoverable from SKILL.md or references/README.md")


def main() -> int:
    for path in REQUIRED_FILES:
        if not path.exists():
            fail(f"Required file is missing: {path.relative_to(ROOT)}")

    text = SKILL_MD.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)

    if fields.get("name") != "agent-orchestration":
        fail("SKILL.md frontmatter name must be agent-orchestration")

    description = fields.get("description", "")
    if len(description) < 80:
        fail("SKILL.md description is too short for reliable triggering")

    forbidden = ["[TODO", "TODO:", "<your-org>"]
    for path in iter_text_files():
        content = path.read_text(encoding="utf-8")
        for token in forbidden:
            if token in content and path != Path(__file__).resolve():
                fail(f"Placeholder token {token!r} found in {path.relative_to(ROOT)}")
        for lineno, line in enumerate(content.splitlines(), start=1):
            if line.rstrip() != line:
                fail(f"Trailing whitespace in {path.relative_to(ROOT)}:{lineno}")
        validate_markdown_links(path, content)
        validate_svg(path)

    validate_template_requirements()
    validate_reference_discovery()

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
