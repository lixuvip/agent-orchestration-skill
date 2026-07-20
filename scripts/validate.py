#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH = ROOT / "skills" / "agent-orchestration"
AGY = ROOT / "skills" / "agy-second-opinion"

ORCH_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/COORDINATION.md",
    "references/COORDINATION.zh-CN.md",
    "references/AUTOMATION.md",
    "references/AUTOMATION.zh-CN.md",
}
AGY_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/REVIEW.md",
    "references/RESEARCH.md",
    "scripts/run_agy_print.py",
    "scripts/build_agy_context_bundle.py",
    "scripts/append_agy_review_quality_log.py",
    "scripts/ensure_agy_review_agents_guidance.py",
}
for task in ("review", "research"):
    for kind in ("prompt", "quality", "quality_log", "report"):
        for suffix in (".template.md", ".zh-CN.template.md"):
            AGY_FILES.add(f"references/templates/agy_gemini_{task}_{kind}{suffix}")

ROOT_FILES = {
    "README.md",
    "README.zh-CN.md",
    "CHANGELOG.md",
    "docs/examples.md",
    "docs/examples.zh-CN.md",
    "docs/forward-tests.md",
    "docs/quickstart.md",
    "docs/quickstart.zh-CN.md",
    "docs/design-notes-v0.3.0.md",
    "docs/design-notes-v0.3.0.zh-CN.md",
}


def fail(message: str) -> None:
    print(f"VALIDATION_FAILED {message}", file=sys.stderr)
    raise SystemExit(1)


def tree_files(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require(path: Path, *tokens: str) -> None:
    text = read(path)
    for token in tokens:
        if token not in text:
            fail(f"{path.relative_to(ROOT)} missing {token!r}")


def validate_frontmatter(path: Path, name: str) -> None:
    text = read(path)
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(f"{path.relative_to(ROOT)} has invalid frontmatter")
    header = match.group(1)
    if f"name: {name}" not in header or "description:" not in header:
        fail(f"{path.relative_to(ROOT)} has incomplete frontmatter")


def validate_links(skill_dir: Path) -> None:
    text = read(skill_dir / "SKILL.md")
    for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
        if "://" in target or target.startswith("#"):
            continue
        if not (skill_dir / target).is_file():
            fail(f"{skill_dir.name}/SKILL.md links to missing {target}")


def main() -> None:
    for relative in ROOT_FILES:
        if not (ROOT / relative).is_file():
            fail(f"missing {relative}")

    actual_orch = tree_files(ORCH)
    if actual_orch != ORCH_FILES:
        fail(
            "agent-orchestration runtime drift: "
            f"missing={sorted(ORCH_FILES - actual_orch)} extra={sorted(actual_orch - ORCH_FILES)}"
        )
    actual_agy = tree_files(AGY)
    if actual_agy != AGY_FILES:
        fail(
            "agy-second-opinion runtime drift: "
            f"missing={sorted(AGY_FILES - actual_agy)} extra={sorted(actual_agy - AGY_FILES)}"
        )

    validate_frontmatter(ORCH / "SKILL.md", "agent-orchestration")
    validate_frontmatter(AGY / "SKILL.md", "agy-second-opinion")
    validate_links(ORCH)
    validate_links(AGY)

    require(
        ORCH / "SKILL.md",
        "Use the least coordination",
        "one internal subagent",
        "user-owned thread",
        "Do not create task boards",
        "Trust native agent/thread status",
        "one final relevant suite",
        "required read, write, execute, network, browser, and connector capabilities",
        "replace, add, or status",
        "map every user request and follow-up",
        "no work is silently orphaned",
    )
    require(
        ORCH / "references" / "COORDINATION.md",
        "Choose The Surface",
        "Do not create callback envelopes",
        "Verification Budget",
        "Formal Gates",
        "Dispatch And Evidence Contract",
        "Steering And Stale Results",
        "closure checklist",
        "Retries are bounded",
        "Optional Best Of N",
        "recovery capsule",
        "Before final delivery",
    )
    require(
        ORCH / "references" / "AUTOMATION.md",
        "product's automation tools",
        "quiet no-op",
        "stop conditions",
    )
    require(
        ROOT / "docs" / "design-notes-v0.3.0.md",
        "ba76b0a683fa52e4e60685017b85905451be17bc",
        "Source-to-adaptation map",
        "does not copy Grok Build runtime code",
        "Explicit non-adoptions",
    )

    orch_text = "\n".join(read(ORCH / path) for path in sorted(ORCH_FILES))
    for forbidden in (
        "ORCHESTRATION_EVENT_V1",
        "TASK_BOARD",
        "automation_lease.py",
        "heartbeat_lifecycle.py",
        "route_orchestration.py",
        "agy",
        "Gemini",
        "Antigravity",
    ):
        if forbidden in orch_text:
            fail(f"agent-orchestration still contains {forbidden!r}")

    require(
        AGY / "SKILL.md",
        "independent from agent orchestration",
        "explicit request",
        "Load exactly one reference",
        "untrusted advice",
        "continue Codex-only",
    )
    require(
        AGY / "references" / "REVIEW.md",
        "one read-only second opinion",
        "exact review baseline",
        "run_agy_print.py",
        "build_agy_context_bundle.py",
        "AGY_UNAVAILABLE",
    )
    require(
        AGY / "references" / "RESEARCH.md",
        "one independent idea stream",
        "run_agy_print.py",
        "Codex",
    )
    agy_text = "\n".join(read(AGY / path) for path in sorted(AGY_FILES))
    for forbidden in ("$agent-orchestration", "skills/agent-orchestration", "TASK_BOARD.md", " for Lite", " for Standard", " for Durable"):
        if forbidden in agy_text:
            fail(f"agy-second-opinion still depends on orchestration: {forbidden!r}")

    for skill_dir in (ORCH, AGY):
        for path in skill_dir.rglob("*"):
            if path.is_symlink():
                fail(f"symlink not allowed: {path.relative_to(ROOT)}")
            if "__pycache__" in path.parts or path.suffix == ".pyc":
                fail(f"generated cache in runtime: {path.relative_to(ROOT)}")

    print(f"VALIDATION_OK agent_files={len(actual_orch)} agy_files={len(actual_agy)}")


if __name__ == "__main__":
    main()
