#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEASE_SCRIPT = ROOT / "skills" / "agent-orchestration" / "scripts" / "automation_lease.py"
LIFECYCLE_SCRIPT = ROOT / "skills" / "agent-orchestration" / "scripts" / "heartbeat_lifecycle.py"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def run(
    state_dir: Path,
    command: str,
    *,
    owner: str | None = None,
    token: str | None = None,
    now: int = 1000,
    ttl: int = 30,
) -> subprocess.CompletedProcess[str]:
    argv = [
        sys.executable,
        str(LEASE_SCRIPT),
        command,
        "--state-dir",
        str(state_dir),
        "--automation-id",
        "automation-smoke",
        "--now-epoch",
        str(now),
    ]
    if owner is not None:
        argv.extend(["--owner-id", owner])
    if token is not None:
        argv.extend(["--lease-token", token])
    if command in {"acquire", "renew"}:
        argv.extend(["--ttl-seconds", str(ttl)])
    env = os.environ.copy()
    env["AGENT_ORCHESTRATION_TESTING"] = "1"
    return subprocess.run(argv, text=True, capture_output=True, check=False, env=env)


def payload(result: subprocess.CompletedProcess[str], prefix: str) -> dict[str, object]:
    if not result.stdout.startswith(prefix + " "):
        fail(f"expected {prefix}, got stdout={result.stdout!r} stderr={result.stderr!r}")
    try:
        return json.loads(result.stdout.split(" ", 1)[1])
    except json.JSONDecodeError as exc:
        fail(f"invalid lease JSON: {exc}")


def lifecycle(state: dict[str, object]) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, str(LIFECYCLE_SCRIPT)],
        input=json.dumps(state),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        fail(f"heartbeat lifecycle rejected valid state: {result.stderr}")
    return payload(result, "HEARTBEAT_TRANSITION")


def main() -> int:
    if not LEASE_SCRIPT.exists():
        fail(f"Missing automation lease helper: {LEASE_SCRIPT.relative_to(ROOT)}")
    if not LIFECYCLE_SCRIPT.exists():
        fail(f"Missing heartbeat lifecycle helper: {LIFECYCLE_SCRIPT.relative_to(ROOT)}")

    with tempfile.TemporaryDirectory() as tmp:
        state_dir = Path(tmp) / "state"

        first = run(state_dir, "acquire", owner="tick-a")
        if first.returncode != 0:
            fail(f"first lease acquire failed: {first.stderr}")
        first_payload = payload(first, "LEASE_ACQUIRED")
        first_token = str(first_payload["lease_token"])
        if first_payload.get("fencing_token") != 1:
            fail("first lease did not receive fencing token 1")

        same_owner = run(state_dir, "acquire", owner="tick-a", now=1001)
        if same_owner.returncode != 3:
            fail("same-owner overlap was not stopped as a no-op")
        same_payload = payload(same_owner, "LEASE_ALREADY_HELD")
        if "lease_token" in same_payload:
            fail("same-owner overlap disclosed the active lease token")

        busy = run(state_dir, "acquire", owner="tick-b", now=1001)
        if busy.returncode != 3 or "LEASE_BUSY" not in busy.stdout:
            fail("a second owner acquired an unexpired lease")
        if "lease_token" in payload(busy, "LEASE_BUSY"):
            fail("busy lease response disclosed another owner's lease token")

        wrong_renew = run(state_dir, "renew", owner="tick-a", token="wrong-token", now=1002)
        if wrong_renew.returncode != 4 or "LEASE_NOT_OWNER" not in wrong_renew.stdout:
            fail("renew accepted the wrong lease token")

        takeover = run(state_dir, "acquire", owner="tick-b", now=1031)
        if takeover.returncode != 0:
            fail(f"expired lease takeover failed: {takeover.stderr}")
        takeover_payload = payload(takeover, "LEASE_ACQUIRED")
        takeover_token = str(takeover_payload["lease_token"])
        if takeover_payload.get("fencing_token") != 2:
            fail("lease takeover did not increment the fencing token")

        stale_verify = run(state_dir, "verify", owner="tick-a", token=first_token, now=1032)
        if stale_verify.returncode != 4 or "LEASE_NOT_OWNER" not in stale_verify.stdout:
            fail("stale owner remained valid after takeover")

        stale_release = run(state_dir, "release", owner="tick-a", token=first_token, now=1032)
        if stale_release.returncode != 4 or "LEASE_NOT_OWNER" not in stale_release.stdout:
            fail("stale owner released the replacement lease")

        renewed = run(state_dir, "renew", owner="tick-b", token=takeover_token, now=1032, ttl=60)
        if renewed.returncode != 0:
            fail(f"current owner could not renew: {renewed.stderr}")
        renewed_payload = payload(renewed, "LEASE_RENEWED")
        if renewed_payload.get("expires_at_epoch") != 1092:
            fail("renew did not extend expiry from the supplied time")

        released = run(state_dir, "release", owner="tick-b", token=takeover_token, now=1033)
        if released.returncode != 0 or "LEASE_RELEASED" not in released.stdout:
            fail("current owner could not release")
        duplicate_release = run(state_dir, "release", owner="tick-b", token=takeover_token, now=1034)
        if duplicate_release.returncode != 0 or "LEASE_ALREADY_RELEASED" not in duplicate_release.stdout:
            fail("duplicate release was not an idempotent no-op")

        # Verify the file lock under contention: exactly one distinct owner wins.
        contenders: list[subprocess.Popen[str]] = []
        for index in range(8):
            argv = [
                sys.executable,
                str(LEASE_SCRIPT),
                "acquire",
                "--state-dir",
                str(state_dir),
                "--automation-id",
                "automation-race",
                "--owner-id",
                f"race-{index}",
                "--ttl-seconds",
                "30",
                "--now-epoch",
                "2000",
            ]
            env = os.environ.copy()
            env["AGENT_ORCHESTRATION_TESTING"] = "1"
            contenders.append(
                subprocess.Popen(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            )
        results = [process.communicate() + (process.returncode,) for process in contenders]
        acquired = [stdout for stdout, _stderr, code in results if code == 0 and stdout.startswith("LEASE_ACQUIRED ")]
        busy_count = sum(code == 3 and stdout.startswith("LEASE_BUSY ") for stdout, _stderr, code in results)
        if len(acquired) != 1 or busy_count != 7:
            fail(f"concurrent acquire did not elect exactly one owner: acquired={len(acquired)} busy={busy_count}")

        active = lifecycle(
            {
                "lifecycle_state": "ACTIVE",
                "role_states": ["DONE", "IN_PROGRESS"],
                "final_summary_posted": False,
                "cleanup_confirmed": False,
            }
        )
        if active.get("next_state") != "ACTIVE" or active.get("action") != "KEEP_ACTIVE":
            fail("heartbeat drained before all roles were terminal")

        draining = lifecycle(
            {
                "lifecycle_state": "ACTIVE",
                "role_states": ["DONE", "CANCELLED", "BLOCKED"],
                "final_summary_posted": False,
                "cleanup_confirmed": False,
            }
        )
        if draining.get("next_state") != "DRAINING" or draining.get("action") != "POST_FINAL_SUMMARY":
            fail("heartbeat did not enter DRAINING when all roles became terminal")
        if draining.get("coordinator_action") != "REVIEW_TERMINAL_RESULTS":
            fail("heartbeat treated terminal role states as coordinator acceptance")

        close = lifecycle(
            {
                "lifecycle_state": "DRAINING",
                "role_states": ["DONE", "CANCELLED", "BLOCKED"],
                "final_summary_posted": True,
                "cleanup_confirmed": False,
            }
        )
        if close.get("next_state") != "DRAINING" or close.get("action") != "CLOSE_HEARTBEAT":
            fail("heartbeat did not wait for cleanup confirmation")

        closed = lifecycle(
            {
                "lifecycle_state": "DRAINING",
                "role_states": ["DONE", "CANCELLED", "BLOCKED"],
                "final_summary_posted": True,
                "cleanup_confirmed": True,
            }
        )
        if closed.get("next_state") != "CLOSED" or closed.get("action") != "NOOP":
            fail("heartbeat did not close after confirmed cleanup")

        closed_noop = lifecycle(
            {
                "lifecycle_state": "CLOSED",
                "role_states": ["IN_PROGRESS"],
                "final_summary_posted": True,
                "cleanup_confirmed": True,
            }
        )
        if closed_noop.get("next_state") != "CLOSED" or closed_noop.get("action") != "NOOP":
            fail("closed heartbeat was not an idempotent no-op")

        invalid_closed = subprocess.run(
            [sys.executable, str(LIFECYCLE_SCRIPT)],
            input=json.dumps(
                {
                    "lifecycle_state": "CLOSED",
                    "role_states": ["DONE"],
                    "final_summary_posted": False,
                    "cleanup_confirmed": False,
                }
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        if invalid_closed.returncode != 2 or "HEARTBEAT_REJECTED" not in invalid_closed.stderr:
            fail("heartbeat accepted CLOSED without summary and cleanup confirmation")

    print("Automation concurrency and lifecycle test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
