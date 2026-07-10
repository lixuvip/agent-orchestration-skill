#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
from pathlib import Path


DEFAULT_MODEL = "Gemini 3.5 Flash (High)"
DEFAULT_MAX_OUTPUT_BYTES = 1_000_000
MAX_OUTPUT_BYTES = 5_000_000
DURATION_RE = re.compile(
    r"^(?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+(?:\.\d+)?)s)?$"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run agy in print mode with the prompt immediately after --print."
    )
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Prompt text to pass immediately after --print.")
    prompt_group.add_argument(
        "--prompt-file",
        help="Prompt file path. Use '-' to read prompt text from stdin.",
    )
    parser.add_argument(
        "--add-dir",
        action="append",
        default=[],
        help="Directory to attach to the agy workspace. Repeat for multiple directories.",
    )
    parser.add_argument(
        "--project",
        help="Optional agy project ID to target instead of the default scratch workspace.",
    )
    parser.add_argument(
        "--expect-substring",
        action="append",
        default=[],
        help="Require stdout to contain this substring. Repeat for multiple required substrings.",
    )
    parser.add_argument(
        "--expect-first-line",
        help="Require the first non-empty stdout line to match this string exactly.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Agy model name. Default: {DEFAULT_MODEL}")
    parser.add_argument("--print-timeout", default="2m0s", help="Agy --print-timeout value. Default: 2m0s")
    parser.add_argument(
        "--host-timeout",
        help="Host-side timeout. Defaults to the print timeout plus 10 seconds.",
    )
    parser.add_argument(
        "--max-output-bytes",
        type=int,
        default=DEFAULT_MAX_OUTPUT_BYTES,
        help=f"Reject output larger than this many bytes. Default: {DEFAULT_MAX_OUTPUT_BYTES}.",
    )
    parser.add_argument("--agy-bin", default="agy", help=argparse.SUPPRESS)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print the argv shape without invoking agy. The prompt is redacted.",
    )
    return parser.parse_args()


def load_prompt(args: argparse.Namespace) -> str:
    if args.prompt is not None:
        prompt = args.prompt
    elif args.prompt_file == "-":
        prompt = sys.stdin.read()
    else:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8")

    if not prompt.strip():
        raise ValueError("prompt is empty")
    return prompt


def build_command(args: argparse.Namespace, prompt: str) -> list[str]:
    agy_name = Path(args.agy_bin).name
    if agy_name == "gemini":
        raise ValueError("agy_bin must target agy, not the standalone gemini CLI")
    if args.agy_bin != "agy" and os.environ.get("AGENT_ORCHESTRATION_TESTING") != "1":
        raise ValueError("agy_bin override is available only to the test harness")
    command = [args.agy_bin]
    for add_dir in args.add_dir:
        command.extend(["--add-dir", add_dir])
    if args.project:
        command.extend(["--project", args.project])
    command.extend(
        [
            "--print-timeout",
            args.print_timeout,
            "--print",
            prompt,
            "--model",
            args.model,
        ]
    )
    command.append("--sandbox")
    return command


def parse_duration(value: str) -> float:
    match = DURATION_RE.fullmatch(value.strip())
    if not match or not any(match.groupdict().values()):
        raise ValueError(f"invalid duration: {value}")
    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes") or 0)
    seconds = float(match.group("seconds") or 0)
    total = hours * 3600 + minutes * 60 + seconds
    if total <= 0:
        raise ValueError("duration must be greater than zero")
    return total


def run_command(command: list[str], host_timeout: float) -> tuple[int, str, str, bool]:
    process = subprocess.Popen(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=host_timeout)
        return process.returncode, stdout, stderr, False
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr, True


def validate_print_position(command: list[str], prompt: str) -> None:
    try:
        print_index = command.index("--print")
    except ValueError as exc:
        raise ValueError("command is missing --print") from exc

    if print_index + 1 >= len(command):
        raise ValueError("--print must be followed by the prompt argument")
    if command[print_index + 1] != prompt:
        raise ValueError("--print must be followed immediately by the prompt argument")


def redacted_command(command: list[str]) -> list[str]:
    result = list(command)
    if "--print" in result:
        prompt_index = result.index("--print") + 1
        if prompt_index < len(result):
            result[prompt_index] = "<PROMPT>"
    return result


def main() -> int:
    args = parse_args()
    try:
        prompt = load_prompt(args)
        command = build_command(args, prompt)
        validate_print_position(command, prompt)
        print_timeout_seconds = parse_duration(args.print_timeout)
        host_timeout_seconds = (
            parse_duration(args.host_timeout) if args.host_timeout else print_timeout_seconds + 10
        )
        if args.max_output_bytes <= 0 or args.max_output_bytes > MAX_OUTPUT_BYTES:
            raise ValueError(f"max-output-bytes must be between 1 and {MAX_OUTPUT_BYTES}")
    except Exception as exc:
        print(f"AGY_PRINT_COMMAND_INVALID {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print("AGY_PRINT_COMMAND_OK")
        print(json.dumps(redacted_command(command), ensure_ascii=False))
        return 0

    returncode, stdout, stderr, timed_out = run_command(command, host_timeout_seconds)
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    if timed_out:
        print(f"AGY_PRINT_HOST_TIMEOUT {host_timeout_seconds:g}s", file=sys.stderr)
        return 6
    if len(stdout.encode("utf-8")) + len(stderr.encode("utf-8")) > args.max_output_bytes:
        print(f"AGY_PRINT_OUTPUT_LIMIT_EXCEEDED {args.max_output_bytes}", file=sys.stderr)
        return 7
    if returncode != 0:
        return returncode

    if not stdout.strip():
        print("AGY_PRINT_EMPTY_OUTPUT", file=sys.stderr)
        return 3

    if args.expect_first_line:
        first_nonempty = next((line.strip() for line in stdout.splitlines() if line.strip()), "")
        if first_nonempty != args.expect_first_line:
            print(
                "AGY_PRINT_FIRST_LINE_FAILED "
                + json.dumps(args.expect_first_line, ensure_ascii=False)
                + " "
                + json.dumps(first_nonempty, ensure_ascii=False),
                file=sys.stderr,
            )
            return 5

    missing_substrings = [
        expected for expected in args.expect_substring if expected not in stdout
    ]
    if missing_substrings:
        print(
            "AGY_PRINT_EXPECTATION_FAILED "
            + ", ".join(json.dumps(item, ensure_ascii=False) for item in missing_substrings),
            file=sys.stderr,
        )
        return 4

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
