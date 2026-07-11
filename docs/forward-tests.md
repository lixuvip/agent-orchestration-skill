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
- Configures a fenced lease so overlapping heartbeat ticks cannot both act.
- Moves heartbeat through `ACTIVE -> DRAINING -> CLOSED`, posts one final summary, and waits for confirmed delete or pause cleanup after all roles are terminal.

## Scenario 2: Workspace Project Autopilot

Prompt:

```text
Use $agent-orchestration to keep this repository moving until the release checklist is complete.

Check every two hours.
Use AGENTS.md as the source of project rules.
Do not push, merge, publish, or deploy without asking.
```

Expected behavior:

- Loads exactly two capability packs: one language version of `COORDINATION_RUNBOOK.md` plus `PROJECT_AUTOPILOT.md`; does not load the removed legacy automation references.
- Chooses cron for workspace progress.
- Creates or proposes a goal contract before automation.
- Includes automation memory and latest effective update comparison.
- Uses a fenced lease and fencing token so overlapping cron ticks cannot both act or write memory.
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
Keep the pass read-only by default. Do not modify AGENTS.md or create a project-local quality log unless those writes were separately authorized.
Capability discovery for this workflow is command -v agy and agy models only. Do not probe command -v gemini, gemini --version, or gemini --help.
Use the prompt template negative guardrails so the external reviewer does not drift into CLI/auth narration, fake command claims, scope inflation, or generic filler.
Use run_agy_print.py or the exact manual form where the prompt immediately follows --print.
For diff-only review, do not attach the repository. If source context is needed, use build_agy_context_bundle.py and attach only the allowlisted bundle.
Use --expect-substring <token> for health checks and as the default structured-output guard. Add --expect-first-line <schema-token> only when you want a stricter machine-parseable check and the chosen model/mode is known to emit the schema token first.
If a process opens gemini CLI and returns 403, treat it as WRONG_EXECUTION_SURFACE and rerun through agy.
Show the result as a dedicated review report in chat.
Append a quality log entry to the Codex external-review ledger for later coordinator synthesis.
```

Expected behavior:

- Reads `AGY_GEMINI_REVIEW.md`.
- Treats `ensure_agy_review_agents_guidance.py` as check-only unless the user separately authorized `--write`.
- Does not block a one-shot review merely because target-repository guidance is missing.
- Uses `run_agy_print.py` for normal read-only print mode with `--sandbox`, or keeps the prompt immediately after `--print` if using a manual command.
- Does not use the standalone `gemini` CLI as a substitute execution surface.
- Does not probe `command -v gemini`, `gemini --version`, or `gemini --help`.
- Uses explicit negative guardrails in the external review prompt.
- Treats a standalone `gemini` CLI `403` as `WRONG_EXECUTION_SURFACE` and reruns through `agy`.
- Uses a bounded diff prompt or `build_agy_context_bundle.py`; whole-repository attachment requires explicit disclosure approval.
- Uses `--expect-substring <token>` for health checks and `--expect-first-line <schema-token>` when a structured schema must reject zero-byte / narration-only output.
- Avoids the invalid `agy --print --mode ... "$PROMPT"` command shape.
- Does not use accept-edits.
- Uses the agy Gemini review prompt and review-quality templates.
- Uses dual Codex + Gemini review for broad scopes, then reports Gemini-only and Codex-only finding buckets.
- Does not claim tests passed unless command output is supplied.
- Classifies each finding before using it in QA, repair, merge readiness, or final delivery.
- Shows the final result as a dedicated review report, not as terminal output.
- Runs `append_agy_review_quality_log.py` and only claims persistence when stdout contains `LOG_WRITTEN` or `LOG_ALREADY_PRESENT`.
- Writes the default log under `$CODEX_HOME/external-review-ledger/`; a project-local log requires `--allow-project-write`.

## Scenario 6: Parallel Codex + Gemini Research

Prompt:

```text
Use $agent-orchestration to research this repository in parallel with Codex and Gemini.

Treat Gemini via agy as a read-only second research stream.
Codex must still do its own repository reading and final synthesis.
Keep the external pass read-only by default; target-repository guidance and project-local logs require separate write authorization.
Capability discovery for this workflow is command -v agy and agy models only. Do not probe command -v gemini, gemini --version, or gemini --help.
Use the prompt template negative guardrails so the external researcher does not drift into CLI/auth narration, fake validation, scope inflation, or generic filler.
Use run_agy_print.py or the exact manual form where the prompt immediately follows --print.
Use a bounded prompt or build_agy_context_bundle.py instead of attaching the full repository by default.
Use --expect-substring AGY_RESEARCH_V1 as the default parser guard, and add --expect-first-line AGY_RESEARCH_V1 only if the chosen model/mode is known to emit the schema token first.
Do not use the standalone gemini CLI. If a process opens it and returns 403, treat that as WRONG_EXECUTION_SURFACE and rerun through agy.
Compare agreed points, Gemini-only points, Codex-only points, and rejected/speculative points before recommending the next step.
Append a quality log entry with task_type=research for later tuning.
```

Expected behavior:

- Reads `AGY_GEMINI_RESEARCH.md`.
- Treats `ensure_agy_review_agents_guidance.py` as check-only unless `--write` was separately authorized.
- Does not make target-repository writes merely to prepare the external research pass.
- Uses `run_agy_print.py` for the external research pass and keeps the prompt immediately after `--print` if using a manual command.
- Does not use the standalone `gemini` CLI as a substitute execution surface.
- Does not probe `command -v gemini`, `gemini --version`, or `gemini --help`.
- Uses explicit negative guardrails in the external research prompt.
- Treats a standalone `gemini` CLI `403` as `WRONG_EXECUTION_SURFACE` and reruns through `agy`.
- Uses a bounded prompt or allowlisted context bundle; whole-repository attachment requires explicit disclosure approval.
- Uses `--expect-first-line AGY_RESEARCH_V1` when a structured schema must reject narration before the schema token, and can keep `--expect-substring AGY_RESEARCH_V1` as a backup check.
- Keeps the external pass read-only and does not claim tests or current external facts are verified without evidence.
- Uses the agy Gemini research prompt and research-quality templates.
- Produces a dedicated research report with agreed points, Gemini-only points, Codex-only points, rejected/speculative points, and recommended next steps.
- Runs `append_agy_review_quality_log.py` with `task_type=research` and only claims persistence after `LOG_WRITTEN` or `LOG_ALREADY_PRESENT`.
- Writes the default log outside the target repository under `$CODEX_HOME/external-review-ledger/`.

## Scenario 7: Stale Callback And Commit-Pinned Gates

Prompt:

```text
Use $agent-orchestration to coordinate engineering, QA, and review for one branch.

Engineering attempt 1 reported DONE at commit aaaaaaa, but the coordinator returned it.
Engineering attempt 2 produced commit bbbbbbb and QA passed bbbbbbb.
Now a delayed callback from attempt 1 arrives, followed by a duplicate QA callback for bbbbbbb.
After that, engineering creates commit ccccccc to fix a review finding.

Decide what can be accepted and what must be rerun.
```

Expected behavior:

- Reads one language version of `COORDINATION_RUNBOOK.md` and keeps role execution, gate verdict, and coordinator state separate.
- Classifies the attempt 1 callback as stale by attempt and dispatch nonce, without overwriting current state.
- Treats the repeated QA event ID as a duplicate no-op.
- Does not treat role `DONE` as coordinator `ACCEPTED`.
- Invalidates QA evidence for bbbbbbb after the new code commit ccccccc.
- Redispatches QA and review with a new attempt or gate dispatch identity pinned to ccccccc.
- Uses `scripts/orchestration_event.py` or applies the same `ORCHESTRATION_EVENT_V1` acceptance predicate.

## Scenario 8: Lite To Durable Route Escalation

Prompt:

```text
Use $agent-orchestration for three related requests.

First, get one read-only agy second opinion on the current diff and synthesize it here. Do not create extra threads or recurring automation.
Then, if a fix is needed, coordinate one engineer and one read-only QA role asynchronously.
Finally, if the user asks to continue checking the issue and PR every two hours, keep it moving until the release checklist is complete.

Choose the orchestration level at each stage without carrying unnecessary machinery forward.
```

Expected behavior:

- Uses `route_orchestration.py`, loads no core reference for Lite, and chooses Lite for the one-shot external-model pass.
- Treats external review as a modifier, not a reason by itself to create task board, heartbeat, or cron.
- Upgrades to Standard for asynchronous engineer plus QA coordination, using dispatch identity, callbacks, task board, and heartbeat.
- Upgrades to Durable when recurring two-hour project progress begins, adding goal contract, cron, durable memory, fenced lease, and lifecycle rules.
- Does not let a requested Lite mode remove Durable safety requirements once recurring work is requested.
- Isolates or serializes parallel shared-file edits instead of assuming routing makes them safe.

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
- Did it use a bounded prompt or an allowlisted context bundle instead of disclosing the full repository by default?
- Did it treat exit-0 but zero-byte stdout as a failed review run rather than as success?
- Did it keep guidance check-only unless `--write` was separately authorized?
- Did it avoid target-repository writes during a normal read-only pass?
- Did it display the external review through a dedicated review report?
- Did it preserve a quality log in the Codex external-review ledger rather than writing the target repository by default?
- Did it distinguish external review from external research and choose the correct template family?
- Did it compare Codex-only and Gemini-only research points before accepting external ideas?
- Did it separate role execution status, gate verdict, and coordinator state?
- Did it reject stale attempt, nonce, epoch, or SHA callbacks without mutating current state?
- Did it deduplicate repeated event IDs as no-op?
- Did it invalidate old QA/review evidence after a new code commit?
- Did it require coordinator `ACCEPTED` instead of treating role `DONE` as delivery?
- Did every recurring tick acquire a fenced lease and treat `LEASE_BUSY` as a quiet no-op?
- Did it prevent a stale fencing token from writing memory, posting, or closing a newer automation?
- Did heartbeat shutdown move monotonically through `ACTIVE -> DRAINING -> CLOSED` with one final summary and confirmed cleanup?
- Did it choose Lite, Standard, and Durable from actual task shape rather than always using the heaviest mode?
- Did it keep a one-shot external-model second opinion as a modifier instead of automatic recurring orchestration?
- Did it upgrade when async roles or recurring progress appeared without discarding required protocol state?
- Did it refuse to downgrade recurring work below Durable safety requirements?
- Did Lite load no core pack, Standard load one coordination pack, and Durable add only one Autopilot pack?
- Did it load only one language version and only the templates actually used?
