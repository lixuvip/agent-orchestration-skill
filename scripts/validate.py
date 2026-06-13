#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "agent-orchestration"
SKILL_MD = SKILL_DIR / "SKILL.md"


REQUIRED_FILES = [
    SKILL_MD,
    SKILL_DIR / "agents" / "openai.yaml",
    SKILL_DIR / "references" / "AUTOMATION_MONITORING.md",
    SKILL_DIR / "references" / "COMMUNICATION_PROTOCOL.md",
    SKILL_DIR / "references" / "WORKFLOWS.md",
    SKILL_DIR / "references" / "templates" / "task_dispatch.template.md",
    SKILL_DIR / "references" / "templates" / "monitoring_heartbeat.template.md",
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
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".sh", ".py"}:
            content = path.read_text(encoding="utf-8")
            for token in forbidden:
                if token in content and path != Path(__file__).resolve():
                    fail(f"Placeholder token {token!r} found in {path.relative_to(ROOT)}")
            for lineno, line in enumerate(content.splitlines(), start=1):
                if line.rstrip() != line:
                    fail(f"Trailing whitespace in {path.relative_to(ROOT)}:{lineno}")

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
