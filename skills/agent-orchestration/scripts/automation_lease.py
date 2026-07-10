#!/usr/bin/env python3
"""File-locked leases with fencing tokens for recurring automation ticks."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import secrets
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Iterator
from contextlib import contextmanager


STATE_VERSION = 1
MIN_TTL_SECONDS = 1
MAX_TTL_SECONDS = 86_400
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")


class LeaseError(ValueError):
    """Raised for invalid lease state or input."""


def _require_id(value: str | None, field: str) -> str:
    if not value or not _ID_RE.fullmatch(value):
        raise LeaseError(f"{field} must match {_ID_RE.pattern}")
    return value


def _state_paths(state_dir: Path, automation_id: str) -> tuple[Path, Path]:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", automation_id).strip("-")[:48] or "automation"
    digest = hashlib.sha256(automation_id.encode("utf-8")).hexdigest()[:12]
    stem = f"{slug}-{digest}"
    return state_dir / f"{stem}.lease.json", state_dir / f"{stem}.lease.lock"


def _empty_state(automation_id: str) -> dict[str, Any]:
    return {
        "version": STATE_VERSION,
        "automation_id": automation_id,
        "fencing_counter": 0,
        "active": None,
        "last_released": None,
    }


def _load_state(path: Path, automation_id: str) -> dict[str, Any]:
    if not path.exists():
        return _empty_state(automation_id)
    if path.is_symlink():
        raise LeaseError("lease state file must not be a symlink")
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LeaseError(f"could not read lease state: {exc}") from exc
    if not isinstance(state, dict):
        raise LeaseError("lease state must be a JSON object")
    if state.get("version") != STATE_VERSION or state.get("automation_id") != automation_id:
        raise LeaseError("lease state identity or version mismatch")
    counter = state.get("fencing_counter")
    if isinstance(counter, bool) or not isinstance(counter, int) or counter < 0:
        raise LeaseError("invalid fencing_counter")
    if state.get("active") is not None and not isinstance(state.get("active"), dict):
        raise LeaseError("invalid active lease record")
    return state


def _write_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(state, handle, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        os.chmod(path, 0o600)
        dir_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    finally:
        if temp_path.exists():
            temp_path.unlink()


@contextmanager
def _locked_state(
    state_dir: Path, automation_id: str
) -> Iterator[tuple[Path, dict[str, Any]]]:
    state_dir.mkdir(parents=True, exist_ok=True)
    state_dir = state_dir.resolve()
    state_path, lock_path = _state_paths(state_dir, automation_id)
    if lock_path.is_symlink():
        raise LeaseError("lease lock file must not be a symlink")
    lock_fd = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        os.fchmod(lock_fd, 0o600)
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        state = _load_state(state_path, automation_id)
        yield state_path, state
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        os.close(lock_fd)


def _public(
    active: dict[str, Any] | None, automation_id: str, *, include_token: bool = False
) -> dict[str, Any]:
    if active is None:
        return {"automation_id": automation_id, "active": False}
    result = {
        "automation_id": automation_id,
        "active": True,
        "owner_id": active["owner_id"],
        "fencing_token": active["fencing_token"],
        "acquired_at_epoch": active["acquired_at_epoch"],
        "heartbeat_at_epoch": active["heartbeat_at_epoch"],
        "expires_at_epoch": active["expires_at_epoch"],
    }
    if include_token:
        result["lease_token"] = active["lease_token"]
    return result


def acquire(
    state_dir: Path, automation_id: str, owner_id: str, ttl_seconds: int, now: int
) -> tuple[str, dict[str, Any], int]:
    with _locked_state(state_dir, automation_id) as (state_path, state):
        active = state.get("active")
        if isinstance(active, dict) and active.get("expires_at_epoch", 0) > now:
            if active.get("owner_id") == owner_id:
                return "LEASE_ALREADY_HELD", _public(active, automation_id), 3
            return "LEASE_BUSY", _public(active, automation_id), 3

        fencing_token = int(state["fencing_counter"]) + 1
        active = {
            "owner_id": owner_id,
            "lease_token": secrets.token_hex(16),
            "fencing_token": fencing_token,
            "acquired_at_epoch": now,
            "heartbeat_at_epoch": now,
            "expires_at_epoch": now + ttl_seconds,
        }
        state["fencing_counter"] = fencing_token
        state["active"] = active
        _write_state(state_path, state)
        return "LEASE_ACQUIRED", _public(active, automation_id, include_token=True), 0


def _current_owner(
    state: dict[str, Any], owner_id: str, lease_token: str, now: int
) -> tuple[dict[str, Any] | None, str, int]:
    active = state.get("active")
    if not isinstance(active, dict):
        return None, "LEASE_NOT_OWNER", 4
    if active.get("owner_id") != owner_id or active.get("lease_token") != lease_token:
        return active, "LEASE_NOT_OWNER", 4
    if active.get("expires_at_epoch", 0) <= now:
        return active, "LEASE_EXPIRED", 5
    return active, "LEASE_VALID", 0


def renew(
    state_dir: Path,
    automation_id: str,
    owner_id: str,
    lease_token: str,
    ttl_seconds: int,
    now: int,
) -> tuple[str, dict[str, Any], int]:
    with _locked_state(state_dir, automation_id) as (state_path, state):
        active, status, code = _current_owner(state, owner_id, lease_token, now)
        if code:
            return status, _public(active, automation_id), code
        assert active is not None
        active["heartbeat_at_epoch"] = now
        active["expires_at_epoch"] = now + ttl_seconds
        _write_state(state_path, state)
        return "LEASE_RENEWED", _public(active, automation_id, include_token=True), 0


def verify(
    state_dir: Path, automation_id: str, owner_id: str, lease_token: str, now: int
) -> tuple[str, dict[str, Any], int]:
    with _locked_state(state_dir, automation_id) as (_state_path, state):
        active, status, code = _current_owner(state, owner_id, lease_token, now)
        if code:
            return status, _public(active, automation_id), code
        return "LEASE_VALID", _public(active, automation_id, include_token=True), 0


def release(
    state_dir: Path, automation_id: str, owner_id: str, lease_token: str, now: int
) -> tuple[str, dict[str, Any], int]:
    with _locked_state(state_dir, automation_id) as (state_path, state):
        active = state.get("active")
        if not isinstance(active, dict):
            previous = state.get("last_released")
            if (
                isinstance(previous, dict)
                and previous.get("owner_id") == owner_id
                and previous.get("lease_token") == lease_token
            ):
                return "LEASE_ALREADY_RELEASED", _public(None, automation_id), 0
            return "LEASE_NOT_OWNER", _public(None, automation_id), 4
        if active.get("owner_id") != owner_id or active.get("lease_token") != lease_token:
            return "LEASE_NOT_OWNER", _public(active, automation_id), 4
        state["last_released"] = {
            "owner_id": owner_id,
            "lease_token": lease_token,
            "fencing_token": active["fencing_token"],
            "released_at_epoch": now,
        }
        state["active"] = None
        _write_state(state_path, state)
        return "LEASE_RELEASED", _public(None, automation_id), 0


def inspect(state_dir: Path, automation_id: str, now: int) -> tuple[str, dict[str, Any], int]:
    with _locked_state(state_dir, automation_id) as (_state_path, state):
        active = state.get("active")
        payload = _public(active if isinstance(active, dict) else None, automation_id)
        if isinstance(active, dict):
            payload["expired"] = active.get("expires_at_epoch", 0) <= now
        payload["fencing_counter"] = state["fencing_counter"]
        return "LEASE_STATE", payload, 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Acquire a fenced, file-locked lease for an automation tick."
    )
    parser.add_argument("command", choices=("acquire", "renew", "verify", "release", "inspect"))
    parser.add_argument("--state-dir", required=True)
    parser.add_argument("--automation-id", required=True)
    parser.add_argument("--owner-id")
    parser.add_argument("--lease-token")
    parser.add_argument("--ttl-seconds", type=int, default=900)
    parser.add_argument("--now-epoch", type=int, help=argparse.SUPPRESS)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        automation_id = _require_id(args.automation_id, "automation_id")
        if not MIN_TTL_SECONDS <= args.ttl_seconds <= MAX_TTL_SECONDS:
            raise LeaseError(
                f"ttl_seconds must be between {MIN_TTL_SECONDS} and {MAX_TTL_SECONDS}"
            )
        if args.now_epoch is not None:
            if os.environ.get("AGENT_ORCHESTRATION_TESTING") != "1":
                raise LeaseError("--now-epoch is available only for test fixtures")
            now = args.now_epoch
        else:
            now = int(time.time())
        if now < 0:
            raise LeaseError("current epoch must be non-negative")

        state_dir = Path(args.state_dir).expanduser()
        if args.command == "inspect":
            result = inspect(state_dir, automation_id, now)
        else:
            owner_id = _require_id(args.owner_id, "owner_id")
            if args.command == "acquire":
                result = acquire(state_dir, automation_id, owner_id, args.ttl_seconds, now)
            else:
                lease_token = _require_id(args.lease_token, "lease_token")
                if args.command == "renew":
                    result = renew(
                        state_dir,
                        automation_id,
                        owner_id,
                        lease_token,
                        args.ttl_seconds,
                        now,
                    )
                elif args.command == "verify":
                    result = verify(state_dir, automation_id, owner_id, lease_token, now)
                else:
                    result = release(state_dir, automation_id, owner_id, lease_token, now)
        status, payload, code = result
        print(f"{status} {json.dumps(payload, sort_keys=True, separators=(',', ':'))}")
        return code
    except (OSError, LeaseError) as exc:
        print(f"LEASE_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
