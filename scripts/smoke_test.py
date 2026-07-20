#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH = ROOT / "skills" / "agent-orchestration"
AGY = ROOT / "skills" / "agy-second-opinion"


def fail(message: str) -> None:
    print(f"SMOKE_FAILED {message}", file=sys.stderr)
    raise SystemExit(1)


def run(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, text=True, capture_output=True, check=False, **kwargs)


def test_python_sources() -> None:
    for path in AGY.rglob("*.py"):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            fail(f"syntax error in {path.relative_to(ROOT)}: {exc}")


def test_print_helper() -> None:
    result = run([
        sys.executable,
        str(AGY / "scripts" / "run_agy_print.py"),
        "--add-dir",
        "/tmp/bounded-context",
        "--prompt",
        "Reply exactly: READY",
        "--print-timeout",
        "20s",
        "--dry-run",
    ])
    if result.returncode != 0:
        fail(result.stderr.strip())
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if not lines or lines[0] != "AGY_PRINT_COMMAND_OK":
        fail("agy print helper did not validate command")
    argv = json.loads(lines[1])
    index = argv.index("--print")
    if argv[index + 1] != "<PROMPT>" or "--sandbox" not in argv:
        fail("agy print command is not bounded read-only shape")


def test_context_bundle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        (root / "safe.txt").write_text("safe\n", encoding="utf-8")
        result = run([
            sys.executable,
            str(AGY / "scripts" / "build_agy_context_bundle.py"),
            "--project-root",
            str(root),
            "--output-dir",
            str(Path(tmp) / "bundle"),
            "--include",
            "safe.txt",
            "--dry-run",
        ])
        if result.returncode != 0:
            fail(result.stderr.strip())
        manifest = json.loads(result.stdout)
        if manifest["files"][0]["path"] != "safe.txt":
            fail("context bundle did not preserve allowlist")


def test_quality_log() -> None:
    entry = {
        "project": "smoke",
        "model": "test",
        "mode": "sandbox",
        "timeout": "20s",
        "scope": "bounded",
        "status": "DONE",
    }
    with tempfile.TemporaryDirectory() as tmp:
        result = run([
            sys.executable,
            str(AGY / "scripts" / "append_agy_review_quality_log.py"),
            "--project-root",
            tmp,
            "--dry-run",
        ], input=json.dumps(entry), env={**os.environ, "CODEX_HOME": str(Path(tmp) / "codex")})
        if result.returncode != 0:
            fail(f"quality log dry-run failed: {result.stderr.strip() or result.stdout.strip()}")
        normalized = json.loads(result.stdout)
        if normalized.get("task_type") != "review" or normalized.get("scope") != "bounded":
            fail("quality log dry-run did not normalize the entry")


def test_runtime_prompts() -> None:
    orch = (ORCH / "agents" / "openai.yaml").read_text(encoding="utf-8")
    agy = (AGY / "agents" / "openai.yaml").read_text(encoding="utf-8")
    if "$agent-orchestration" not in orch or "$agy-second-opinion" not in agy:
        fail("skill prompts do not point at their own skill")
    if "agy" in orch.lower() or "agent-orchestration" in agy:
        fail("skill prompts are still coupled")


def main() -> None:
    test_python_sources()
    test_print_helper()
    test_context_bundle()
    test_quality_log()
    test_runtime_prompts()
    print("SMOKE_OK native_orchestration_and_independent_agy")


if __name__ == "__main__":
    main()
