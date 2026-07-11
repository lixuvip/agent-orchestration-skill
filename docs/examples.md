# Usage Examples

For copy-ready scenario files, see:

- [Simple research task](../examples/simple-research-task.md)
- [Coding and review workflow](../examples/coding-review-workflow.md)
- [Multi-agent product planning](../examples/multi-agent-product-planning.md)
- [Bug fix with QA](../examples/bugfix-with-qa.md)
- [Multi-project finalization](../examples/multi-project-finalization.md)
- [Release preparation](../examples/release-prep.md)
- [Branch callback controller loop](../examples/branch-callback-controller-loop.md)
- [Continuous project autopilot](../examples/continuous-project-autopilot.md)
- [GitHub issue and PR autopilot](../examples/github-issue-pr-autopilot.md)

## Example 1: Bug Fix With QA Gate

```text
Use $agent-orchestration to coordinate a bug fix.

Create:
- one engineering role that can edit the smallest needed files;
- one QA role that is read-only and runs regression tests.

Goal:
Fix the issue where an export option is requested but the final report does not include the expected fields.

Done when:
- engineering explains root cause and changed files;
- QA runs the relevant regression tests;
- coordinator confirms the fix is scoped and verified.
```

## Example 2: Parallel Research Before Implementation

```text
Use $agent-orchestration.

Split this feature into parallel preparation:
- Product Designer: define acceptance criteria and user flow.
- Technical Engineer: inspect implementation options without editing files.
- QA Tester: propose the regression matrix.

After all three reply, merge their outputs into one engineering task.
```

## Example 3: Parallel Codex + Gemini Research

```text
Use $agent-orchestration to research this repository in parallel with Codex and Gemini.

Goal:
Figure out the best approach for adding background job retries without widening the architecture unnecessarily.

Research rules:
- Codex must do its own repo reading and final synthesis.
- Gemini via agy should run as a read-only second research stream.
- Use run_agy_print.py so the prompt stays immediately after --print.
- Do not use the standalone gemini CLI; if a process opens it and returns 403, treat that as WRONG_EXECUTION_SURFACE and rerun through agy.
- Use a bounded prompt or build_agy_context_bundle.py; do not attach the full repository by default.
- Add --expect-substring AGY_RESEARCH_V1 so narration-only output is rejected automatically.
- Compare agreed points, Gemini-only points, Codex-only points, and rejected/speculative points before choosing the next engineering task.
- Append a quality log entry with task_type=research after the run.
```

## Example 4: Multi-Repository Commit Finalization

```text
Use $agent-orchestration to finalize three repositories.

Projects:
- /path/to/service
- /path/to/app-one
- /path/to/app-two

For each project thread:
- inspect git status;
- document service API contract changes;
- run tests;
- create focused commits if ready;
- report branch, commits, verification, and risks.

Create a 5-minute heartbeat monitor.
```

## Example 5: Release Preparation

```text
Use $agent-orchestration for release preparation.

Roles:
- Release Docs: summarize changes and migration notes.
- QA Tester: verify critical paths.
- Code Reviewer: inspect high-risk diffs.

Do not publish release notes until QA and review have terminal statuses.
Treat terminal role status as IN_REVIEW; publish readiness requires coordinator ACCEPTED with QA/review evidence pinned to the current commit SHA.
```

## Example 6: Callback-Required Long Task

```text
Use $agent-orchestration.

Dispatch this long-running migration to a separate engineering thread.
Require the role to callback to this coordinator thread when complete.
If callback fails, require CALLBACK_FAILED in the role's final reply.
Also create a heartbeat monitor that checks the role every 5 minutes.
Use a fenced lease for overlapping ticks and close through ACTIVE -> DRAINING -> CLOSED with one final summary and confirmed cleanup.
```

## Example 7: Branch Callback Controller Loop

```text
Use $agent-orchestration to coordinate branch work with direct callback to the main coordinator thread.

Create or continue a dedicated engineering branch/worktree.
Keep QA read-only.
Require every role to callback to the coordinator thread.
Create heartbeat monitoring if the work is long-running.
Run merge readiness before merging, pushing, or telling the user the branch is ready.
```

## Example 8: Continuous Project Autopilot

```text
Use $agent-orchestration to create a project autopilot loop for this repository.

Read AGENTS.md, AGENTS.override.md, project docs, and the release checklist first.
Create a goal contract with done criteria, allowed autonomous actions, confirmation gates, cadence, memory path, and stop conditions.
Use cron automation for workspace progress and heartbeat only for coordinator-thread callbacks.
Each tick should acquire a fenced lease, compare the latest effective update and idempotency keys, take one safe next action, verify the lease before side effects and memory writes, and escalate if merge/push/deploy or scope expansion is needed.
```

## Example 9: GitHub Issue And PR Autopilot

```text
Use $agent-orchestration to run a GitHub issue/PR project autopilot.

Issue is the coordination channel.
PR is the implementation channel.
Do not stop just because there is no open PR.
Do not comment if the latest effective update is unchanged and already covered by a previous codex-next-action comment.
Read issue body, labels, comments, linked PR commits, files, checks, and review state before deciding the next safe action.
```

## Example 10: Forward-Test Audit Before Release

```text
Use $agent-orchestration to audit this skill release before publishing.

Check that the forward-test scenarios still cover heartbeat callbacks, cron project autopilot, GitHub issue/PR no-op polling, missing AGENTS.md guidance, automation memory, latest effective update comparison, and escalation gates.
Run python3 scripts/forward_test.py, scripts/protocol_test.py, scripts/automation_test.py, and scripts/routing_test.py with the normal validation suite.
Report any missing trigger coverage before preparing release notes.
```

## Example 11: Optional Agy / Gemini Review

```text
Use $agent-orchestration to add an agy/Gemini external review pass for the current branch diff.

Treat agy as a read-only second opinion.
In this workflow, Gemini means Gemini via agy only. Do not use the standalone gemini CLI.
For broad or full-project review, run a dual Codex + Gemini review: keep a Codex reviewer role independent from the agy pass, then compare agreed findings, Gemini-only findings, Codex-only findings, rejected findings, and verification evidence.
Keep the pass read-only by default. Only write stable AGENTS.md guidance when that repository change was separately authorized.
Capability discovery for this workflow is command -v agy and agy models only. Do not probe command -v gemini, gemini --version, or gemini --help.
Use the negative guardrails from the review prompt template: do not drift into CLI/auth narration, do not claim commands ran, do not inflate scope beyond the diff, and do not pad with generic advice.
Use run_agy_print.py in fixed sandboxed mode. For source-backed review, attach an allowlisted context bundle rather than the project root. Add --expect-substring READY or Status: when the wrapper should reject narration-only output automatically.
If a process opens gemini CLI and returns 403, treat that as WRONG_EXECUTION_SURFACE and rerun through agy.
Do not let agy edit files or claim tests passed unless exact command output is supplied.
After the review returns, evaluate review quality and classify each finding as valid, partially_valid, not_supported, or needs_human_check before deciding the next role.
Show the result as a dedicated review report with Agy findings, dual-review comparison, quality evaluation, Codex verification, and recommended next steps.
Append a quality log entry to the default Codex external-review ledger, and only claim persistence after LOG_WRITTEN or LOG_ALREADY_PRESENT.
```

## Example 12: Route From Lite To Durable

```text
Use $agent-orchestration and choose the minimum safe mode at each stage.

Stage 1: get one read-only agy second opinion on the current diff and synthesize it in this thread. Keep this Lite; do not create extra threads or recurring automation.
Stage 2: if a fix is required, coordinate one isolated engineering role and one read-only QA role asynchronously. Upgrade to Standard with versioned callbacks, a task board, commit-pinned gates, and a leased heartbeat.
Stage 3: only if I ask to keep checking the issue/PR every two hours, upgrade to Durable with a goal contract, cron, automation memory, fenced lease, and lifecycle rules.

State the selected mode and why. Keep the context budget explicit: Lite loads no core pack, Standard loads one language version of COORDINATION_RUNBOOK.md, and Durable adds only the matching PROJECT_AUTOPILOT.md. Never load both languages or carry heavier machinery into an earlier stage.
```

## Example 13: Reject A Stale Callback

```text
Use $agent-orchestration to evaluate these callbacks.

The active task is attempt 2 with dispatch nonce dispatch-2, coordinator epoch epoch-7, and expected commit bbbbbbb.
A delayed DONE callback arrives from attempt 1 at commit aaaaaaa.
Then the QA event for bbbbbbb arrives twice with the same event ID.
Finally engineering creates ccccccc after review feedback.

Classify stale and duplicate events without changing current state. Do not accept role DONE as delivery. Invalidate QA/review evidence for bbbbbbb after ccccccc and redispatch gates against the new exact SHA.
```

## Example 14: Overlapping Autopilot Ticks

```text
Use $agent-orchestration in Durable mode for a two-hour issue/PR autopilot.

Assume two cron ticks may overlap or one tick may resume after its lease expires.
Acquire a file-locked lease before reading mutable memory.
Treat LEASE_ALREADY_HELD and LEASE_BUSY as quiet no-ops.
Verify the current owner token before posting, writing memory, or cleanup.
Persist the latest fencing token and reject lower-token writes.
If a heartbeat reaches all terminal role states, move ACTIVE -> DRAINING -> CLOSED, post one final summary, and wait for automation-tool cleanup confirmation.
```
