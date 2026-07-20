#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH = ROOT / "skills" / "agent-orchestration"
EN = (ORCH / "references" / "AUTOMATION.md").read_text(encoding="utf-8")
ZH = (ORCH / "references" / "AUTOMATION.zh-CN.md").read_text(encoding="utf-8")

for token in ("product's automation tools", "quiet no-op", "stop conditions", "cleanup", "authority"):
    if token not in EN:
        print(f"AUTOMATION_TEST_FAILED English reference missing {token}", file=sys.stderr)
        raise SystemExit(1)
for token in ("原生 automation", "安静 no-op", "停止条件", "清理", "权限"):
    if token not in ZH:
        print(f"AUTOMATION_TEST_FAILED Chinese reference missing {token}", file=sys.stderr)
        raise SystemExit(1)

tree = "\n".join(path.name for path in ORCH.rglob("*"))
for obsolete in ("automation_lease.py", "heartbeat_lifecycle.py", "automation_memory.template.md"):
    if obsolete in tree:
        print(f"AUTOMATION_TEST_FAILED obsolete runtime {obsolete}", file=sys.stderr)
        raise SystemExit(1)

print("AUTOMATION_TEST_OK native_tools_no_custom_scheduler")
