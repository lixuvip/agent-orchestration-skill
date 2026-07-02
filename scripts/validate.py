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
    SKILL_DIR / "references" / "AUTOMATION_MONITORING.md",
    SKILL_DIR / "references" / "COMMUNICATION_PROTOCOL.md",
    SKILL_DIR / "references" / "CONTROLLER_LOOP.md",
    SKILL_DIR / "references" / "ORCHESTRATION_INTAKE.md",
    SKILL_DIR / "references" / "STATE_MACHINE.md",
    SKILL_DIR / "references" / "WORKFLOWS.md",
    SKILL_DIR / "references" / "examples" / "filled_task_dispatch.md",
    SKILL_DIR / "references" / "examples" / "filled_role_reply.md",
    SKILL_DIR / "references" / "templates" / "coordinator_callback.template.md",
    SKILL_DIR / "references" / "templates" / "coordinator_callback.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "merge_readiness.template.md",
    SKILL_DIR / "references" / "templates" / "merge_readiness.zh-CN.template.md",
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
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
    ROOT / "docs" / "installation.md",
    ROOT / "docs" / "installation.zh-CN.md",
    ROOT / "docs" / "quickstart.md",
    ROOT / "docs" / "quickstart.zh-CN.md",
    ROOT / "docs" / "tutorial.md",
    ROOT / "docs" / "tutorial.zh-CN.md",
    ROOT / "docs" / "examples.md",
    ROOT / "docs" / "examples.zh-CN.md",
    ROOT / "docs" / "publishing.md",
    ROOT / "docs" / "publishing.zh-CN.md",
    ROOT / "docs" / "images" / "logo.svg",
    ROOT / "docs" / "images" / "workflow-overview.svg",
    ROOT / "docs" / "images" / "workflow-overview.zh-CN.svg",
]


TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".sh", ".py", ".svg"}

TEMPLATE_REQUIREMENTS = {
    SKILL_DIR / "references" / "templates" / "task_dispatch.template.md": [
        "Status:",
        "Verification:",
        "Risks:",
        "Callback:",
        "Branch / worktree:",
        "Merge policy:",
    ],
    SKILL_DIR / "references" / "templates" / "task_dispatch.zh-CN.template.md": [
        "Status:",
        "验证要求",
        "Risks:",
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
        "Status:",
        "Verification:",
        "Next coordinator action:",
    ],
    SKILL_DIR / "references" / "templates" / "coordinator_callback.zh-CN.template.md": [
        "任务 ID",
        "分支 / 工作区",
        "Status:",
        "验证结果",
        "协调者下一步",
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
        "Tests:",
        "Push permission:",
    ],
    SKILL_DIR / "references" / "templates" / "merge_readiness.zh-CN.template.md": [
        "合并就绪",
        "基准分支",
        "工作区",
        "测试",
        "推送权限",
    ],
    SKILL_DIR / "references" / "templates" / "role_reply.template.md": [
        "Status:",
        "Verification run:",
        "Risks / concerns:",
        "Recommended next role:",
    ],
    SKILL_DIR / "references" / "templates" / "role_reply.zh-CN.template.md": [
        "Status:",
        "Verification run:",
        "Risks / concerns:",
        "Recommended next role:",
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
}

DISCOVERABLE_REFERENCES = [
    "STATE_MACHINE.md",
    "ORCHESTRATION_INTAKE.md",
    "CONTROLLER_LOOP.md",
    "task_dispatch.zh-CN.template.md",
    "orchestration_intake.zh-CN.template.md",
    "coordinator_callback.zh-CN.template.md",
    "status_request.zh-CN.template.md",
    "merge_readiness.zh-CN.template.md",
    "role_reply.zh-CN.template.md",
    "monitoring_heartbeat.zh-CN.template.md",
    "filled_task_dispatch.md",
    "filled_role_reply.md",
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
