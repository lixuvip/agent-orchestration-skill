#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


DEFAULT_MODEL = "Gemini 3.5 Flash (High)"


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
    parser.add_argument(
        "--mode",
        help="Optional agy mode. Omit for normal mode; use values like plan only when explicitly needed.",
    )
    parser.add_argument("--print-timeout", default="2m0s", help="Agy --print-timeout value. Default: 2m0s")
    parser.add_argument("--agy-bin", default="agy", help="Agy executable. Default: agy")
    parser.add_argument("--no-sandbox", action="store_true", help="Do not append --sandbox.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print the argv shape without invoking agy. The prompt is redacted.",
    )
    parser.add_argument(
        "--allow-empty-output",
        action="store_true",
        help="Allow exit-0 runs that print no stdout. Default behavior treats empty stdout as a failure.",
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
    if args.mode:
        command.extend(["--mode", args.mode])
    if not args.no_sandbox:
        command.append("--sandbox")
    return command


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
    except Exception as exc:
        print(f"AGY_PRINT_COMMAND_INVALID {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print("AGY_PRINT_COMMAND_OK")
        print(json.dumps(redacted_command(command), ensure_ascii=False))
        return 0

    completed = subprocess.run(command, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    if completed.returncode != 0:
        return completed.returncode

    if not args.allow_empty_output and not completed.stdout.strip():
        print("AGY_PRINT_EMPTY_OUTPUT", file=sys.stderr)
        return 3

    if args.expect_first_line:
        first_nonempty = next((line.strip() for line in completed.stdout.splitlines() if line.strip()), "")
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
        expected for expected in args.expect_substring if expected not in completed.stdout
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
