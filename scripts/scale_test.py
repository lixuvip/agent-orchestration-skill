#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH = ROOT / "skills" / "agent-orchestration"
AGY = ROOT / "skills" / "agy-second-opinion"


def files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*") if path.is_file()]


def size(paths: list[Path]) -> int:
    return sum(path.stat().st_size for path in paths)


orch_files = files(ORCH)
agy_files = files(AGY)
orch_bytes = size(orch_files)
agy_bytes = size(agy_files)
skill_lines = len((ORCH / "SKILL.md").read_text(encoding="utf-8").splitlines())

limits = [
    (len(orch_files) <= 6, f"agent-orchestration file count {len(orch_files)} > 6"),
    (orch_bytes <= 24_000, f"agent-orchestration size {orch_bytes} > 24000"),
    (skill_lines <= 45, f"agent-orchestration SKILL lines {skill_lines} > 45"),
    (len(agy_files) <= 24, f"agy-second-opinion file count {len(agy_files)} > 24"),
    (agy_bytes <= 180_000, f"agy-second-opinion size {agy_bytes} > 180000"),
]
for passed, message in limits:
    if not passed:
        print(f"SCALE_TEST_FAILED {message}", file=sys.stderr)
        raise SystemExit(1)

if any("__pycache__" in path.parts or path.suffix == ".pyc" for path in orch_files + agy_files):
    print("SCALE_TEST_FAILED generated cache is packaged", file=sys.stderr)
    raise SystemExit(1)

print(
    "SCALE_TEST_OK "
    f"agent_files={len(orch_files)} agent_bytes={orch_bytes} "
    f"agy_files={len(agy_files)} agy_bytes={agy_bytes}"
)
