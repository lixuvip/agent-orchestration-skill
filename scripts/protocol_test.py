#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH = ROOT / "skills" / "agent-orchestration"
TEXT = "\n".join(path.read_text(encoding="utf-8") for path in ORCH.rglob("*") if path.is_file())

FORBIDDEN = [
    "ORCHESTRATION_EVENT_V1",
    "protocol_version",
    "dispatch_nonce",
    "coordinator_epoch",
    "fencing token",
    "TASK_BOARD",
]
REQUIRED = [
    "native agent/thread status",
    "Do not create callback envelopes",
    "meaningful state",
    "superseded scope is stale",
    "Before final delivery",
    "no work is silently orphaned",
]

for token in FORBIDDEN:
    if token in TEXT:
        print(f"PROTOCOL_TEST_FAILED obsolete token {token}", file=sys.stderr)
        raise SystemExit(1)
for token in REQUIRED:
    if token not in TEXT:
        print(f"PROTOCOL_TEST_FAILED missing {token}", file=sys.stderr)
        raise SystemExit(1)

if any((ORCH / "scripts").glob("*")) if (ORCH / "scripts").exists() else False:
    print("PROTOCOL_TEST_FAILED custom protocol scripts remain", file=sys.stderr)
    raise SystemExit(1)

print("PROTOCOL_TEST_OK native_lifecycle_only")
