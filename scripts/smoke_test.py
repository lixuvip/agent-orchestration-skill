#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "agent-orchestration"

STATUSES = ["DONE", "DONE_WITH_CONCERNS", "BLOCKED", "NEEDS_CONTEXT"]

SCENARIO_FILES = [
    ROOT / "examples" / "bugfix-with-qa.md",
    ROOT / "examples" / "multi-project-finalization.md",
    ROOT / "examples" / "release-prep.md",
    ROOT / "examples" / "simple-research-task.md",
    ROOT / "examples" / "coding-review-workflow.md",
    ROOT / "examples" / "multi-agent-product-planning.md",
    ROOT / "examples" / "branch-callback-controller-loop.md",
    ROOT / "examples" / "continuous-project-autopilot.md",
    ROOT / "examples" / "github-issue-pr-autopilot.md",
]

CORE_FILES = [
    SKILL_DIR / "SKILL.md",
    SKILL_DIR / "scripts" / "run_agy_print.py",
    SKILL_DIR / "scripts" / "build_agy_context_bundle.py",
    SKILL_DIR / "scripts" / "ensure_agy_review_agents_guidance.py",
    SKILL_DIR / "scripts" / "append_agy_review_quality_log.py",
    SKILL_DIR / "references" / "COMMUNICATION_PROTOCOL.md",
    SKILL_DIR / "references" / "CONTROLLER_LOOP.md",
    SKILL_DIR / "references" / "ORCHESTRATION_INTAKE.md",
    SKILL_DIR / "references" / "AGY_GEMINI_REVIEW.md",
    SKILL_DIR / "references" / "AGY_GEMINI_RESEARCH.md",
    SKILL_DIR / "references" / "PROJECT_AUTOPILOT.md",
    SKILL_DIR / "references" / "AUTOMATION_TOOLING.md",
    SKILL_DIR / "references" / "PROJECT_INSTRUCTIONS_DISCOVERY.md",
    SKILL_DIR / "references" / "STATE_MACHINE.md",
    SKILL_DIR / "references" / "WORKFLOWS.md",
    SKILL_DIR / "references" / "AUTOMATION_MONITORING.md",
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
    SKILL_DIR / "references" / "templates" / "role_reply.template.md",
    SKILL_DIR / "references" / "templates" / "role_reply.zh-CN.template.md",
    SKILL_DIR / "references" / "templates" / "monitoring_heartbeat.template.md",
    SKILL_DIR / "references" / "templates" / "monitoring_heartbeat.zh-CN.template.md",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"Missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_all(path: Path, tokens: list[str]) -> None:
    text = read(path)
    for token in tokens:
        if token not in text:
            fail(f"{path.relative_to(ROOT)} is missing {token!r}")


def verify_agy_print_helper_shape() -> None:
    script = SKILL_DIR / "scripts" / "run_agy_print.py"
    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            "--add-dir",
            "/tmp/example-project",
            "--prompt",
            "Reply exactly: READY",
            "--print-timeout",
            "20s",
            "--dry-run",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"run_agy_print.py dry-run failed: {completed.stderr.strip()}")

    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines or lines[0] != "AGY_PRINT_COMMAND_OK":
        fail("run_agy_print.py dry-run did not report AGY_PRINT_COMMAND_OK")
    try:
        argv = json.loads(lines[1])
    except (IndexError, json.JSONDecodeError) as exc:
        fail(f"run_agy_print.py dry-run did not emit argv JSON: {exc}")

    try:
        print_index = argv.index("--print")
    except ValueError:
        fail("run_agy_print.py dry-run argv is missing --print")
    if print_index + 1 >= len(argv) or argv[print_index + 1] != "<PROMPT>":
        fail("run_agy_print.py does not place the prompt immediately after --print")
    if "--add-dir" not in argv:
        fail("run_agy_print.py dry-run argv is missing --add-dir")
    add_dir_index = argv.index("--add-dir")
    if add_dir_index + 1 >= len(argv) or argv[add_dir_index + 1] != "/tmp/example-project":
        fail("run_agy_print.py dry-run did not preserve the --add-dir value")
    if "--expect-substring" in argv:
        fail("run_agy_print.py dry-run unexpectedly injected --expect-substring")


def verify_agy_print_helper_empty_output_failure() -> None:
    script = SKILL_DIR / "scripts" / "run_agy_print.py"
    with tempfile.TemporaryDirectory() as tmp:
        stub = Path(tmp) / "agy-empty"
        stub.write_text("#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n", encoding="utf-8")
        stub.chmod(0o755)

        env = os.environ.copy()
        env["AGENT_ORCHESTRATION_TESTING"] = "1"
        completed = subprocess.run(
            [
                sys.executable,
                str(script),
                "--agy-bin",
                str(stub),
                "--prompt",
                "Reply exactly: READY",
                "--print-timeout",
                "20s",
            ],
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        if completed.returncode != 3:
            fail(
                "run_agy_print.py did not treat zero-byte stdout as failure: "
                f"code={completed.returncode} stderr={completed.stderr.strip()!r}"
            )
        if "AGY_PRINT_EMPTY_OUTPUT" not in completed.stderr:
            fail("run_agy_print.py did not emit AGY_PRINT_EMPTY_OUTPUT for zero-byte stdout")


def verify_agy_print_helper_first_line_failure() -> None:
    script = SKILL_DIR / "scripts" / "run_agy_print.py"
    with tempfile.TemporaryDirectory() as tmp:
        stub = Path(tmp) / "agy-narration"
        stub.write_text(
            "#!/usr/bin/env python3\nprint('I will inspect the repo first.')\nprint('AGY_RESEARCH_V1')\n",
            encoding="utf-8",
        )
        stub.chmod(0o755)

        env = os.environ.copy()
        env["AGENT_ORCHESTRATION_TESTING"] = "1"
        completed = subprocess.run(
            [
                sys.executable,
                str(script),
                "--agy-bin",
                str(stub),
                "--prompt",
                "Reply exactly: READY",
                "--print-timeout",
                "20s",
                "--expect-first-line",
                "AGY_RESEARCH_V1",
            ],
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        if completed.returncode != 5:
            fail(
                "run_agy_print.py did not reject narration before the schema token: "
                f"code={completed.returncode} stderr={completed.stderr.strip()!r}"
            )
        if "AGY_PRINT_FIRST_LINE_FAILED" not in completed.stderr:
            fail("run_agy_print.py did not emit AGY_PRINT_FIRST_LINE_FAILED for narration-first output")


def verify_agy_print_helper_rejects_gemini_cli() -> None:
    script = SKILL_DIR / "scripts" / "run_agy_print.py"
    with tempfile.TemporaryDirectory() as tmp:
        stub = Path(tmp) / "gemini"
        stub.write_text("#!/usr/bin/env python3\nprint('wrong surface')\n", encoding="utf-8")
        stub.chmod(0o755)

        env = os.environ.copy()
        env["AGENT_ORCHESTRATION_TESTING"] = "1"
        completed = subprocess.run(
            [
                sys.executable,
                str(script),
                "--agy-bin",
                str(stub),
                "--prompt",
                "Reply exactly: READY",
                "--print-timeout",
                "20s",
            ],
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        if completed.returncode != 2:
            fail(
                "run_agy_print.py did not reject the standalone gemini CLI surface: "
                f"code={completed.returncode} stderr={completed.stderr.strip()!r}"
            )
        if "standalone gemini CLI" not in completed.stderr:
            fail("run_agy_print.py did not explain the gemini CLI surface rejection")


def verify_agy_print_helper_rejects_unsafe_flags() -> None:
    script = SKILL_DIR / "scripts" / "run_agy_print.py"
    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            "--prompt",
            "noop",
            "--mode",
            "accept-edits",
            "--no-sandbox",
            "--dry-run",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode == 0 or "AGY_PRINT_COMMAND_OK" in completed.stdout:
        fail("run_agy_print.py still permits accept-edits or no-sandbox")


def verify_agy_print_helper_host_timeout() -> None:
    script = SKILL_DIR / "scripts" / "run_agy_print.py"
    with tempfile.TemporaryDirectory() as tmp:
        stub = Path(tmp) / "agy-slow"
        stub.write_text(
            "#!/usr/bin/env python3\nimport time\ntime.sleep(2)\nprint('READY')\n",
            encoding="utf-8",
        )
        stub.chmod(0o755)
        env = os.environ.copy()
        env["AGENT_ORCHESTRATION_TESTING"] = "1"
        started = time.monotonic()
        completed = subprocess.run(
            [
                sys.executable,
                str(script),
                "--agy-bin",
                str(stub),
                "--prompt",
                "Reply exactly: READY",
                "--print-timeout",
                "20s",
                "--host-timeout",
                "0.1s",
            ],
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        elapsed = time.monotonic() - started
        if completed.returncode != 6 or "AGY_PRINT_HOST_TIMEOUT" not in completed.stderr:
            fail(
                "run_agy_print.py did not enforce its host timeout: "
                f"code={completed.returncode} stderr={completed.stderr.strip()!r}"
            )
        if elapsed > 1.5:
            fail(f"run_agy_print.py host timeout was too slow: {elapsed:.2f}s")


def verify_agents_guidance_helper() -> None:
    script = SKILL_DIR / "scripts" / "ensure_agy_review_agents_guidance.py"
    with tempfile.TemporaryDirectory() as tmp:
        project_root = Path(tmp)
        check_only = subprocess.run(
            [sys.executable, str(script), "--project-root", str(project_root)],
            text=True,
            capture_output=True,
            check=False,
        )
        if check_only.returncode == 0 or "AGENTS_GUIDANCE_MISSING" not in check_only.stdout:
            fail("ensure_agy_review_agents_guidance.py did not default to check-only")
        if (project_root / "AGENTS.md").exists():
            fail("ensure_agy_review_agents_guidance.py wrote AGENTS.md without --write")

        first = subprocess.run(
            [sys.executable, str(script), "--project-root", str(project_root), "--write"],
            text=True,
            capture_output=True,
            check=False,
        )
        if first.returncode != 0 or "AGENTS_GUIDANCE_WRITTEN" not in first.stdout:
            fail(
                "ensure_agy_review_agents_guidance.py first write failed: "
                f"{first.stderr.strip()} {first.stdout.strip()}"
        )
        agents_text = (project_root / "AGENTS.md").read_text(encoding="utf-8")
        if "agent-orchestration:agy-gemini-review:start" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not write the guidance marker")
        if "$agent-orchestration" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not require the installed skill at first use")
        if "--add-dir" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not mention explicit workspace attachment")
        if "command -v agy" not in agents_text or "agy models" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not constrain discovery to agy")
        if "command -v gemini" not in agents_text or "gemini --help" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not forbid gemini CLI probing")
        if "Wrong first moves to avoid" not in agents_text or "gemini` auth/login flows" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not add negative guardrails for the first move")
        if "--expect-substring" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not mention structured-output expectation checks")
        if "Zero-byte stdout" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not mention zero-byte stdout failure")
        if "standalone `gemini` CLI" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not forbid the standalone gemini CLI")
        if "WRONG_EXECUTION_SURFACE" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not mention WRONG_EXECUTION_SURFACE")
        if "AGY_RESEARCH_V1" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not mention research schema checks")
        if "external-review ledger" not in agents_text:
            fail("ensure_agy_review_agents_guidance.py did not explain external review logging")

        second = subprocess.run(
            [sys.executable, str(script), "--project-root", str(project_root)],
            text=True,
            capture_output=True,
            check=False,
        )
        if second.returncode != 0 or "AGENTS_GUIDANCE_PRESENT" not in second.stdout:
            fail("ensure_agy_review_agents_guidance.py is not idempotent")

        stale_text = agents_text.replace("Zero-byte stdout is not a successful review or research pass.", "Old text.")
        (project_root / "AGENTS.md").write_text(stale_text, encoding="utf-8")
        stale_check = subprocess.run(
            [sys.executable, str(script), "--project-root", str(project_root), "--check"],
            text=True,
            capture_output=True,
            check=False,
        )
        if stale_check.returncode == 0 or "AGENTS_GUIDANCE_STALE" not in stale_check.stdout:
            fail("ensure_agy_review_agents_guidance.py did not report stale guidance")

        refresh = subprocess.run(
            [sys.executable, str(script), "--project-root", str(project_root), "--write"],
            text=True,
            capture_output=True,
            check=False,
        )
        if refresh.returncode != 0 or "AGENTS_GUIDANCE_WRITTEN" not in refresh.stdout:
            fail("ensure_agy_review_agents_guidance.py did not refresh stale guidance")

        outside = project_root.parent / "outside-agents.md"
        escaped = subprocess.run(
            [
                sys.executable,
                str(script),
                "--project-root",
                str(project_root),
                "--agents-file",
                "../outside-agents.md",
                "--write",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if escaped.returncode == 0 or outside.exists():
            fail("ensure_agy_review_agents_guidance.py allowed AGENTS.md path escape")

        linked = project_root / "linked-agents.md"
        linked.symlink_to(project_root / "AGENTS.md")
        symlinked = subprocess.run(
            [
                sys.executable,
                str(script),
                "--project-root",
                str(project_root),
                "--agents-file",
                "linked-agents.md",
                "--write",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if symlinked.returncode == 0:
            fail("ensure_agy_review_agents_guidance.py allowed a symlinked AGENTS.md")

        malformed = project_root / "malformed-agents.md"
        malformed.write_text(
            "<!-- agent-orchestration:agy-gemini-review:start -->\n",
            encoding="utf-8",
        )
        malformed_result = subprocess.run(
            [
                sys.executable,
                str(script),
                "--project-root",
                str(project_root),
                "--agents-file",
                "malformed-agents.md",
                "--write",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if malformed_result.returncode == 0:
            fail("ensure_agy_review_agents_guidance.py accepted malformed guidance markers")


def verify_quality_log_helper() -> None:
    script = SKILL_DIR / "scripts" / "append_agy_review_quality_log.py"
    entry = {
        "review_id": "agy-task-smoke-001",
        "task_type": "review",
        "project": "smoke",
        "model": "Gemini test",
        "mode": "read-only sandbox",
        "timeout": "20s",
        "scope": "bounded fixture",
        "status": "DONE",
        "quality_score": 5,
    }
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        project_root = root / "project"
        project_root.mkdir()
        codex_home = root / "codex-home"
        env = os.environ.copy()
        env["CODEX_HOME"] = str(codex_home)

        first = subprocess.run(
            [sys.executable, str(script), "--project-root", str(project_root)],
            input=json.dumps(entry),
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        if first.returncode != 0 or "LOG_WRITTEN" not in first.stdout:
            fail(f"quality log helper did not write the default ledger: {first.stderr.strip()}")
        if (project_root / ".codex").exists():
            fail("quality log helper wrote into the project by default")
        ledger_paths = list((codex_home / "external-review-ledger").glob("*/agy-review-quality.jsonl"))
        if len(ledger_paths) != 1:
            fail("quality log helper did not create exactly one CODEX_HOME ledger")

        duplicate = subprocess.run(
            [sys.executable, str(script), "--project-root", str(project_root)],
            input=json.dumps(entry),
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        if duplicate.returncode != 0 or "LOG_ALREADY_PRESENT" not in duplicate.stdout:
            fail("quality log helper did not deduplicate review_id")

        project_write = subprocess.run(
            [
                sys.executable,
                str(script),
                "--project-root",
                str(project_root),
                "--log-path",
                ".codex/agent-orchestration/custom.jsonl",
            ],
            input=json.dumps({**entry, "review_id": "agy-task-smoke-002"}),
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        if project_write.returncode == 0:
            fail("quality log helper allowed a project write without --allow-project-write")

        authorized_project_write = subprocess.run(
            [
                sys.executable,
                str(script),
                "--project-root",
                str(project_root),
                "--log-path",
                ".codex/agent-orchestration/custom.jsonl",
                "--allow-project-write",
            ],
            input=json.dumps({**entry, "review_id": "agy-task-smoke-002"}),
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        if authorized_project_write.returncode != 0 or "LOG_WRITTEN" not in authorized_project_write.stdout:
            fail("quality log helper rejected an explicitly authorized project-local log")

        nested_secret = subprocess.run(
            [sys.executable, str(script), "--project-root", str(project_root), "--dry-run"],
            input=json.dumps(
                {**entry, "coordinator_notes": [{"api_token": "not-for-logs"}]}
            ),
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        if nested_secret.returncode == 0 or "LOG_NOT_WRITTEN" not in nested_secret.stderr:
            fail("quality log helper did not reject a nested sensitive key")

        processes: list[subprocess.Popen[str]] = []
        for index in range(8):
            entry_file = root / f"entry-{index:02d}.json"
            entry_file.write_text(
                json.dumps({**entry, "review_id": f"agy-task-concurrent-{index:02d}"}),
                encoding="utf-8",
            )
            process = subprocess.Popen(
                [
                    sys.executable,
                    str(script),
                    "--project-root",
                    str(project_root),
                    "--entry-file",
                    str(entry_file),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )
            processes.append(process)
        for process in processes:
            stdout, stderr = process.communicate()
            if process.returncode != 0 or "LOG_WRITTEN" not in stdout:
                fail(f"concurrent quality-log append failed: {stderr.strip()}")
        lines = ledger_paths[0].read_text(encoding="utf-8").splitlines()
        if len(lines) != 9:
            fail(f"concurrent quality-log append lost or duplicated entries: {len(lines)}")
        for line in lines:
            json.loads(line)


def verify_context_bundle_helper() -> None:
    script = SKILL_DIR / "scripts" / "build_agy_context_bundle.py"
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        project_root = root / "project"
        source_dir = project_root / "src"
        source_dir.mkdir(parents=True)
        (source_dir / "app.py").write_text("print('safe')\n", encoding="utf-8")
        (project_root / ".env").write_text("SECRET=value\n", encoding="utf-8")
        output_dir = root / "bundle"

        bundled = subprocess.run(
            [
                sys.executable,
                str(script),
                "--project-root",
                str(project_root),
                "--output-dir",
                str(output_dir),
                "--include",
                "src/app.py",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if bundled.returncode != 0 or "AGY_CONTEXT_WRITTEN" not in bundled.stdout:
            fail(f"context bundle helper failed: {bundled.stderr.strip()}")
        if not (output_dir / "src" / "app.py").is_file():
            fail("context bundle helper omitted the allowlisted file")
        if (output_dir / ".env").exists():
            fail("context bundle helper copied an unlisted secret file")

        blocked = subprocess.run(
            [
                sys.executable,
                str(script),
                "--project-root",
                str(project_root),
                "--output-dir",
                str(root / "blocked-bundle"),
                "--include",
                ".env",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if blocked.returncode == 0 or "AGY_CONTEXT_NOT_WRITTEN" not in blocked.stderr:
            fail("context bundle helper allowed a sensitive path")

        escaped = subprocess.run(
            [
                sys.executable,
                str(script),
                "--project-root",
                str(project_root),
                "--output-dir",
                str(root / "escaped-bundle"),
                "--include",
                "../outside.txt",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if escaped.returncode == 0:
            fail("context bundle helper allowed a path escape")


def verify_install_helper() -> None:
    script = ROOT / "scripts" / "install_skill.py"
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "source"
        source.mkdir()
        (source / "SKILL.md").write_text("---\nname: demo\ndescription: demo\n---\n", encoding="utf-8")
        (source / "reference.md").write_text("v1\n", encoding="utf-8")
        target_root = root / "skills"

        dirty = subprocess.run(
            [
                sys.executable,
                str(script),
                "--source-dir",
                str(source),
                "--target-root",
                str(target_root),
                "--skill-name",
                "demo",
                "--source-commit",
                "abc123",
                "--source-dirty",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if dirty.returncode == 0:
            fail("install helper accepted a dirty source without --allow-dirty")

        installed = subprocess.run(
            [
                sys.executable,
                str(script),
                "--source-dir",
                str(source),
                "--target-root",
                str(target_root),
                "--skill-name",
                "demo",
                "--source-commit",
                "abc123",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if installed.returncode != 0 or "INSTALL_COMPLETE" not in installed.stdout:
            fail(f"install helper failed: {installed.stderr.strip()}")
        manifest_path = target_root / ".demo.install-manifest.json"
        if not manifest_path.exists():
            fail("install helper did not write a provenance manifest")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("source_commit") != "abc123" or manifest.get("source_dirty") is not False:
            fail("install helper provenance manifest is incomplete")

        (source / "reference.md").write_text("v2\n", encoding="utf-8")
        upgraded = subprocess.run(
            [
                sys.executable,
                str(script),
                "--source-dir",
                str(source),
                "--target-root",
                str(target_root),
                "--skill-name",
                "demo",
                "--source-commit",
                "def456",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if upgraded.returncode != 0 or not (target_root / ".demo.previous").exists():
            fail("install helper did not keep the previous installation")

        restored = subprocess.run(
            [
                sys.executable,
                str(script),
                "--target-root",
                str(target_root),
                "--skill-name",
                "demo",
                "--restore",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if restored.returncode != 0 or "INSTALL_RESTORED" not in restored.stdout:
            fail("install helper could not restore the previous installation")
        if (target_root / "demo" / "reference.md").read_text(encoding="utf-8") != "v1\n":
            fail("install helper restored the wrong content")


def main() -> int:
    combined_core = "\n".join(read(path) for path in CORE_FILES)
    for status in STATUSES:
        if status not in combined_core:
            fail(f"Core skill files do not mention status {status}")

    verify_agy_print_helper_shape()
    verify_agy_print_helper_empty_output_failure()
    verify_agy_print_helper_first_line_failure()
    verify_agy_print_helper_rejects_gemini_cli()
    verify_agy_print_helper_rejects_unsafe_flags()
    verify_agy_print_helper_host_timeout()
    verify_agents_guidance_helper()
    verify_quality_log_helper()
    verify_context_bundle_helper()
    verify_install_helper()

    require_all(
        SKILL_DIR / "agents" / "openai.yaml",
        [
            "Use $agent-orchestration immediately",
            "agy/Gemini external review or research",
            "do not inspect or launch the standalone gemini CLI",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "STATE_MACHINE.md",
        [
            "TODO -> IN_PROGRESS",
            "IN_PROGRESS -> DONE",
            "Silence is never completion.",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "AUTOMATION_MONITORING.md",
        [
            "CALLBACK_FAILED",
            "每 5 分钟",
            "DONE_WITH_CONCERNS",
            "status request",
            "PROJECT_AUTOPILOT.md",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "PROJECT_AUTOPILOT.md",
        [
            "AGENTS.md",
            "PROJECT_INSTRUCTIONS_DISCOVERY.md",
            "AUTOMATION_TOOLING.md",
            "cron",
            "Goal Contract",
            "Tick Loop",
            "latest effective update",
            "automation memory",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "AUTOMATION_TOOLING.md",
        [
            "Heartbeat",
            "Cron",
            "Existing Automation Check",
            "Do not show raw RRULE",
            "Safety Gates",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "PROJECT_INSTRUCTIONS_DISCOVERY.md",
        [
            "AGENTS.md",
            "AGENTS.override.md",
            ".codex/config.toml",
            "automation memory",
            "Discovery Report",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "ORCHESTRATION_INTAKE.md",
        [
            "request_user_input",
            "Ask only when",
            "Do not ask when",
            "Execution surface",
            "project autopilot",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "CONTROLLER_LOOP.md",
        [
            "controller loop",
            "send_message_to_thread",
            "status request",
            "merge readiness",
            "Autopilot Readiness",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "AGY_GEMINI_REVIEW.md",
        [
            "Gemini 3.5 Flash (High)",
            "AGY_UNAVAILABLE",
            "TIMED_OUT",
            "SCOPE_DRIFT",
            "WRONG_EXECUTION_SURFACE",
            "standalone `gemini` CLI",
            "AGY_PRINT_EMPTY_OUTPUT",
            "AGY_PRINT_FIRST_LINE_FAILED",
            "--expect-substring",
            "coordinator must classify",
            "dedicated report",
            "agy-review-quality.jsonl",
            "ensure_agy_review_agents_guidance.py",
            "check-only",
            "run_agy_print.py",
            "build_agy_context_bundle.py",
            "--add-dir \"$CONTEXT_PARENT/context\"",
            "host-side timeout",
            "external-review-ledger",
            "agy --print <prompt>",
            "agy --print --model",
            "dual Codex + Gemini review",
            "Gemini-only",
            "Codex-only",
            "falsification check",
            "append_agy_review_quality_log.py",
            "external-review-ledger",
            "LOG_WRITTEN",
            "template_tuning_suggestions",
            "Negative Guardrails",
            "stop and return to the documented preflight",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "AGY_GEMINI_RESEARCH.md",
        [
            "parallel Codex + Gemini research",
            "Gemini 3.5 Flash (High)",
            "AGY_RESEARCH_V1",
            "WRONG_EXECUTION_SURFACE",
            "standalone `gemini` CLI",
            "--expect-substring",
            "\"task_type\": \"research\"",
            "append_agy_review_quality_log.py",
            "follow-up questions",
            "accepted",
            "rejected",
            "Negative Guardrails",
            "stop and return to the documented preflight",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_review_prompt.template.md",
        [
            "AGY_REVIEW_V2",
            "Gemini via agy",
            "run_agy_print.py",
            "Negative guardrails:",
            "standalone `gemini` CLI",
            "--expect-first-line",
            "--expect-substring",
            "commands_run: NONE",
            "verification_claims:",
            "coordinator_check:",
            "no_test_claims",
            "no_cli_drift",
            "no_scope_inflation",
            "no_generic_padding",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_review_prompt.zh-CN.template.md",
        [
            "Negative guardrails:",
            "standalone `gemini` CLI",
            "no_cli_drift",
            "no_scope_inflation",
            "no_generic_padding",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality.template.md",
        [
            "AGY_REVIEW_QUALITY_V1",
            "unsupported_claims:",
            "scope_drift:",
            "coordinator_follow_up:",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality_log.template.md",
        [
            "agy-review-quality.jsonl",
            "append_agy_review_quality_log.py",
            "LOG_WRITTEN",
            "LOG_ALREADY_PRESENT",
            "external-review-ledger",
            "Do not store secrets",
            "quality_score",
            "template_tuning_suggestions",
            "unsupported_claims",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_review_quality_log.zh-CN.template.md",
        [
            "agy-review-quality.jsonl",
            "append_agy_review_quality_log.py",
            "LOG_WRITTEN",
            "LOG_ALREADY_PRESENT",
            "external-review-ledger",
            "不要记录密钥",
            "quality_score",
            "template_tuning_suggestions",
            "unsupported_claims",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_review_report.template.md",
        [
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
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_review_report.zh-CN.template.md",
        [
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
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_research_prompt.template.md",
        [
            "AGY_RESEARCH_V1",
            "Gemini via agy",
            "run_agy_print.py",
            "Negative guardrails:",
            "standalone `gemini` CLI",
            "--expect-first-line",
            "--expect-substring",
            "external_fact_mode:",
            "coordinator_check:",
            "no_fake_validation",
            "no_cli_drift",
            "no_scope_inflation",
            "no_generic_padding",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_research_prompt.zh-CN.template.md",
        [
            "Negative guardrails:",
            "standalone `gemini` CLI",
            "no_cli_drift",
            "no_scope_inflation",
            "no_generic_padding",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_research_quality.template.md",
        [
            "AGY_RESEARCH_QUALITY_V1",
            "unsupported_claims:",
            "scope_drift:",
            "missed_angles:",
            "coordinator_follow_up:",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_research_quality_log.template.md",
        [
            "agy-review-quality.jsonl",
            "append_agy_review_quality_log.py",
            "\"task_type\": \"research\"",
            "external-review-ledger",
            "valuable_takeaways",
            "follow_up_questions",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agy_gemini_research_report.template.md",
        [
            "Agy External Research Report",
            "--add-dir <allowlisted_context>",
            "Parallel Research Comparison",
            "Gemini-only points",
            "Codex-only points",
            "Codex Synthesis",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "project_goal_contract.template.md",
        [
            "Done when:",
            "Allowed autonomously:",
            "Requires confirmation:",
            "Verification commands:",
            "Memory path:",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "automation_tick.template.md",
        [
            "Latest effective update:",
            "Action taken:",
            "Verification:",
            "Next safe action:",
            "Escalation needed:",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "agents_guidance_snippet.template.md",
        [
            "Codex Project Autopilot",
            "Safe autonomous actions",
            "Actions requiring confirmation",
            "Idempotency rule",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "task_dispatch.template.md",
        [
            "Coordinator thread ID",
            "Callback format",
            "Stop and report if",
            "Verification",
            "Branch / worktree",
            "Merge policy",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "task_dispatch.zh-CN.template.md",
        [
            "协调者线程 ID",
            "回调格式",
            "遇到以下情况请停止并报告",
            "验证要求",
            "分支 / 工作区",
            "合并策略",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "orchestration_intake.template.md",
        [
            "Execution surface:",
            "Callback behavior:",
            "Merge/push permission:",
            "Ask only if",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "coordinator_callback.template.md",
        [
            "Task ID:",
            "Branch / worktree:",
            "Status:",
            "Verification:",
            "Next coordinator action:",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "status_request.template.md",
        [
            "Status request",
            "Coordinator thread ID",
            "Reply with one",
        ],
    )
    require_all(
        SKILL_DIR / "references" / "templates" / "merge_readiness.template.md",
        [
            "Merge readiness",
            "Base branch:",
            "Working tree:",
            "Tests:",
            "Push permission:",
        ],
    )

    for path in SCENARIO_FILES:
        text = read(path)
        if "Use $agent-orchestration" not in text:
            fail(f"Scenario {path.relative_to(ROOT)} does not invoke the skill")

    print("Smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
