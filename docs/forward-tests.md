# Forward Tests

Use these scenarios to validate whether another Codex instance can apply `agent-orchestration` without seeing the implementation notes that created it.

Run these in a fresh thread or subagent when practical. Pass the skill and scenario, not the intended answer.

Run the static guard before publishing changes:

```bash
python3 scripts/forward_test.py
```

## Scenario 1: Heartbeat Callback

Prompt:

```text
Use $agent-orchestration to coordinate two role threads for a long-running bug fix.

One engineering role may edit code.
One QA role is read-only.
Both must callback to the coordinator.
Create monitoring only if it is appropriate.
```

Expected behavior:

- Chooses heartbeat rather than cron.
- Uses task dispatch with callback and verification fields.
- Refuses to infer completion from silence.
- Plans to delete or pause heartbeat after all roles are terminal.

## Scenario 2: Workspace Project Autopilot

Prompt:

```text
Use $agent-orchestration to keep this repository moving until the release checklist is complete.

Check every two hours.
Use AGENTS.md as the source of project rules.
Do not push, merge, publish, or deploy without asking.
```

Expected behavior:

- Reads `PROJECT_AUTOPILOT.md`, `AUTOMATION_TOOLING.md`, and `PROJECT_INSTRUCTIONS_DISCOVERY.md`.
- Chooses cron for workspace progress.
- Creates or proposes a goal contract before automation.
- Includes automation memory and latest effective update comparison.
- Escalates before push, merge, publish, deploy, destructive changes, or scope expansion.

## Scenario 3: GitHub Issue/PR No-Op Poll

Prompt:

```text
Use $agent-orchestration to monitor a GitHub issue and linked PR.

The issue is the coordination channel.
The PR is the implementation channel.
Do not comment if the latest effective update is unchanged and already covered by a previous codex-next-action comment.
```

Expected behavior:

- Does not stop just because no PR exists.
- Checks issue body, comments, labels, PR commits, files, checks, and review/draft state.
- Compares latest effective update against memory.
- Updates memory without posting when no substantive change exists.

## Scenario 4: Missing Project Instructions

Prompt:

```text
Use $agent-orchestration to create recurring automation for this repo, but the repo has no AGENTS.md.

The automation should run tests and keep a release checklist moving.
```

Expected behavior:

- Reports missing durable project guidance.
- Suggests an `AGENTS.md` snippet rather than silently relying on chat history.
- Still creates a goal contract with explicit verification and stop conditions.

## Scenario 5: Agy Gemini External Review

Prompt:

```text
Use $agent-orchestration to add an agy/Gemini external code review pass for the current diff.

Use the external review only as a read-only second opinion.
In this workflow, Gemini means Gemini via agy only. Do not use the standalone gemini CLI.
For broad or risky review, run a dual Codex + Gemini review and compare Gemini-only, Codex-only, agreed, and rejected findings.
Do not let agy edit files.
Do not claim tests passed unless exact command output is included.
Before any agy health check or model discovery in a writable repo, persist the stable agy/Gemini command-safety guidance into AGENTS.md.
Capability discovery for this workflow is command -v agy and agy models only. Do not probe command -v gemini, gemini --version, or gemini --help.
Use the prompt template negative guardrails so the external reviewer does not drift into CLI/auth narration, fake command claims, scope inflation, or generic filler.
Use run_agy_print.py or the exact manual form where the prompt immediately follows --print.
Attach the repository explicitly with --add-dir <project_root> for repo review so agy does not stay in scratch.
Use --expect-substring <token> for health checks and as the default structured-output guard. Add --expect-first-line <schema-token> only when you want a stricter machine-parseable check and the chosen model/mode is known to emit the schema token first.
If a process opens gemini CLI and returns 403, treat it as WRONG_EXECUTION_SURFACE and rerun through agy.
Show the result as a dedicated review report in chat.
Append a quality log entry for later coordinator synthesis.
```

Expected behavior:

- Reads `AGY_GEMINI_REVIEW.md`.
- Runs `ensure_agy_review_agents_guidance.py` and treats guidance as ready only after `AGENTS_GUIDANCE_PRESENT` or `AGENTS_GUIDANCE_WRITTEN`.
- Runs the guidance step before any `agy` health check or model discovery.
- Uses `run_agy_print.py` for normal read-only print mode with `--sandbox`, or keeps the prompt immediately after `--print` if using a manual command.
- Does not use the standalone `gemini` CLI as a substitute execution surface.
- Does not probe `command -v gemini`, `gemini --version`, or `gemini --help`.
- Uses explicit negative guardrails in the external review prompt.
- Treats a standalone `gemini` CLI `403` as `WRONG_EXECUTION_SURFACE` and reruns through `agy`.
- Uses `--add-dir <project_root>` for repository review so agy does not inspect scratch by mistake.
- Uses `--expect-substring <token>` for health checks and `--expect-first-line <schema-token>` when a structured schema must reject zero-byte / narration-only output.
- Avoids the invalid `agy --print --mode ... "$PROMPT"` command shape.
- Does not use accept-edits.
- Uses the agy Gemini review prompt and review-quality templates.
- Uses dual Codex + Gemini review for broad scopes, then reports Gemini-only and Codex-only finding buckets.
- Does not claim tests passed unless command output is supplied.
- Classifies each finding before using it in QA, repair, merge readiness, or final delivery.
- Shows the final result as a dedicated review report, not as terminal output.
- Runs `append_agy_review_quality_log.py` and only claims the log was written when stdout contains `LOG_WRITTEN`.
- Writes or proposes `.codex/agent-orchestration/agy-review-quality.jsonl` with quality score, weak points, unsupported claims, omissions, and template tuning notes.

## Scenario 6: Parallel Codex + Gemini Research

Prompt:

```text
Use $agent-orchestration to research this repository in parallel with Codex and Gemini.

Treat Gemini via agy as a read-only second research stream.
Codex must still do its own repository reading and final synthesis.
Before any agy health check or model discovery in a writable repo, persist the stable agy/Gemini command-safety guidance into AGENTS.md.
Capability discovery for this workflow is command -v agy and agy models only. Do not probe command -v gemini, gemini --version, or gemini --help.
Use the prompt template negative guardrails so the external researcher does not drift into CLI/auth narration, fake validation, scope inflation, or generic filler.
Use run_agy_print.py or the exact manual form where the prompt immediately follows --print.
Attach the repository explicitly with --add-dir <project_root>.
Use --expect-substring AGY_RESEARCH_V1 as the default parser guard, and add --expect-first-line AGY_RESEARCH_V1 only if the chosen model/mode is known to emit the schema token first.
Do not use the standalone gemini CLI. If a process opens it and returns 403, treat that as WRONG_EXECUTION_SURFACE and rerun through agy.
Compare agreed points, Gemini-only points, Codex-only points, and rejected/speculative points before recommending the next step.
Append a quality log entry with task_type=research for later tuning.
```

Expected behavior:

- Reads `AGY_GEMINI_RESEARCH.md`.
- Runs `ensure_agy_review_agents_guidance.py` and treats guidance as ready only after `AGENTS_GUIDANCE_PRESENT` or `AGENTS_GUIDANCE_WRITTEN`.
- Runs the guidance step before any `agy` health check or model discovery.
- Uses `run_agy_print.py` for the external research pass and keeps the prompt immediately after `--print` if using a manual command.
- Does not use the standalone `gemini` CLI as a substitute execution surface.
- Does not probe `command -v gemini`, `gemini --version`, or `gemini --help`.
- Uses explicit negative guardrails in the external research prompt.
- Treats a standalone `gemini` CLI `403` as `WRONG_EXECUTION_SURFACE` and reruns through `agy`.
- Uses `--add-dir <project_root>` for repository research so agy does not inspect scratch by mistake.
- Uses `--expect-first-line AGY_RESEARCH_V1` when a structured schema must reject narration before the schema token, and can keep `--expect-substring AGY_RESEARCH_V1` as a backup check.
- Keeps the external pass read-only and does not claim tests or current external facts are verified without evidence.
- Uses the agy Gemini research prompt and research-quality templates.
- Produces a dedicated research report with agreed points, Gemini-only points, Codex-only points, rejected/speculative points, and recommended next steps.
- Runs `append_agy_review_quality_log.py` with `task_type=research` and only claims the log was written when stdout contains `LOG_WRITTEN`.
- Writes or proposes `.codex/agent-orchestration/agy-review-quality.jsonl` with quality score, weak points, unsupported claims, missed angles, and template tuning notes.

## Review Checklist

- Did the agent choose heartbeat vs cron correctly?
- Did it identify persistent instructions separately from automation memory?
- Did it avoid repeated GitHub comments when nothing substantive changed?
- Did it require explicit permission for merge, push, deploy, publish, destructive changes, or scope expansion?
- Did it name concrete verification commands or ask for them when missing?
- Did it treat external model review as a second opinion and guard against test/build hallucinations?
- Did it keep Gemini on the agy execution surface rather than silently switching to standalone `gemini` CLI?
- Did it avoid probing `command -v gemini`, `gemini --version`, or `gemini --help` instead of going straight to the agy path?
- Did it include explicit negative guardrails against CLI/auth drift, fake validation, scope inflation, and generic filler?
- Did it avoid the invalid `agy --print --mode ... "$PROMPT"` command shape?
- Did it use `--expect-first-line <schema-token>` when structured output needed a strict first-line check?
- Did it attach the repository explicitly with `--add-dir <project_root>` for repo review?
- Did it treat exit-0 but zero-byte stdout as a failed review run rather than as success?
- Did it persist stable agy/Gemini command-safety guidance in `AGENTS.md` when writes were allowed?
- Did it persist that guidance before any agy health check or model discovery?
- Did it display the external review through a dedicated review report?
- Did it preserve a quality log entry for later template tuning through the helper script rather than only describing the log?
- Did it distinguish external review from external research and choose the correct template family?
- Did it compare Codex-only and Gemini-only research points before accepting external ideas?
