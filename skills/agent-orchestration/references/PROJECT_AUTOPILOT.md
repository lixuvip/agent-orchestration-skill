# Project Autopilot Runbook

Canonical Durable capability pack. Load after `COORDINATION_RUNBOOK.md` only when work must recur or recover across ticks. Load only one language version.

## Activation Boundary

Use Durable Autopilot for repeated workspace/worktree progress toward explicit done criteria: issue/PR coordination, QA/release readiness, backlog/checklist progress, or later wakeups that may safely take action.

Do not use it for a one-shot edit, reminder-only request, finite role heartbeat, or a task whose next step always needs user judgment.

## Durable Contract

Before creating/updating automation, fill `templates/project_goal_contract.template.md` and `templates/automation_plan.template.md`:

- goal ID, outcome, measurable done criteria, workspace/branch/issue/PR/release;
- stable instruction sources and verification commands;
- allowed autonomous actions and explicit confirmation gates;
- cadence, maximum tick runtime/attempts, budget, and stop conditions;
- automation/memory/state paths, idempotency key, lease TTL, lifecycle, and cleanup policy.

“Fully autonomous” does not authorize merge, push, deploy, publish, destructive data/file actions, secret/billing operations, public API changes, spending, or product-scope expansion unless separately explicit.

## Project Instructions

Read the narrowest relevant sources:

1. root and applicable nested `AGENTS.md`;
2. `AGENTS.override.md` as the stronger local rule;
3. configured fallback instruction files;
4. `.codex/config.toml` for configuration only;
5. relevant README/contributing/test/release/issue/PR docs.

Keep stable build/test, branch, review, safety, communication, and escalation rules in `AGENTS.md`. Keep live goal state, blockers, counters, messages, and next action in automation memory. Never store secrets in either. Do not edit project instructions without authorization.

Suggest a stable rule update only when the same command, mistake, or feedback is repeatedly rediscovered; use `templates/agents_guidance_snippet.template.md`.

## Automation Surface

| Need | Surface |
| --- | --- |
| Finite current-thread role polling | Standard heartbeat; return to `COORDINATION_RUNBOOK.md` |
| Recurring workspace/worktree progress | Cron |
| Worktree/environment setup needing review | Suggested cron create/update |
| Existing automation with the same goal/cwd/target | Update it; do not duplicate |

Use the app automation tool when available; let it serialize schedules and describe cadence to users in natural language. Before creation, inspect existing name, prompt, cwd, target, repository, issue/PR, branch, and goal. Preserve fields the user did not ask to change.

## Tick Transaction

Each tick uses `templates/automation_tick.template.md` and performs at most one safe next action:

1. Generate a unique tick ID and acquire a fenced lease with `scripts/automation_lease.py` before reading mutable memory.
2. On `LEASE_ALREADY_HELD` or `LEASE_BUSY`, exit quietly. On expired/replaced ownership, discard results and produce no side effect.
3. Read project instructions, goal contract, and memory. Stop if memory has a greater fencing token.
4. Inspect live git/issue/PR/thread/test/build/log/release state relevant to the goal.
5. Compute the latest effective update; timestamp-only or metadata-only change is not progress.
6. Compare processed event IDs, posted-message keys, action keys, and last state to prevent duplicates.
7. Choose exactly one smallest action inside autonomous authority.
8. Verify the lease immediately before any message, external write, callback, cleanup, or memory commit.
9. Execute the action and smallest relevant verification.
10. Atomically write memory with fencing token, observed state, action/evidence, risks, blocker history, next step, and idempotency keys.
11. If done, post one final summary and request pause/delete; record `CLOSED` only after tool confirmation.
12. If authority/scope/budget is missing or failure repeats to the contract limit, post one deduplicated `templates/escalation_report.template.md` and pause/wait as contracted.
13. Release the lease in a finally-equivalent path.

An unchanged tick should update internal observation memory but remain user-facing quiet unless the contract requires a progress message.

## Lease And Fencing

Default state directory:

```text
${CODEX_HOME:-$HOME/.codex}/automations/<automation-id>/state
```

The helper uses an exclusive file lock, atomic replacement, expiry, random lease token, and monotonically increasing fencing token.

```bash
python3 scripts/automation_lease.py acquire \
  --state-dir "$STATE_DIR" \
  --automation-id "$AUTOMATION_ID" \
  --owner-id "$TICK_ID" \
  --ttl-seconds 900
```

- Only `LEASE_ACQUIRED` returns the token; keep it in the tick context, not reusable memory.
- Renew before expiry for legitimate long work; TTL must exceed expected runtime plus cleanup margin.
- Verify before side effects and memory writes.
- Never overwrite memory with a lower fencing token.
- Repeated release by the same owner/token is a no-op; stale owners cannot release or close replacements.
- Use a local filesystem with known advisory-lock and atomic-rename semantics.

## Durable Memory

Default memory path:

```text
${CODEX_HOME:-$HOME/.codex}/automations/<automation-id>/memory.md
```

Resolve through `$HOME/.codex` when `CODEX_HOME` is unset; never allow `/automations`. Use `templates/automation_memory.template.md` and retain:

- goal/automation ID, workspace, done criteria;
- latest effective update and whether already covered;
- last tick/action/verification/risk and next safe action;
- blocker history and run/attempt counters;
- posted messages, processed events, status-request/action/escalation keys;
- lifecycle, final-summary/cleanup state, and latest fencing token.

## Lifecycle And Completion

Automation lifecycle is monotonic:

```text
ACTIVE -> DRAINING -> CLOSED
```

- `ACTIVE`: inspect and take one authorized safe action.
- `DRAINING`: stop new work, post final summary once, request pause/delete once, retry only cleanup if needed.
- `CLOSED`: confirmed cleanup; every late tick/update is a permanent no-op.

Use `scripts/heartbeat_lifecycle.py` when the automation is monitoring role terminal states. Persist final-summary key, cleanup request ID, and confirmation so a crash cannot cause duplicate summaries.

Declare the goal reached only when all done criteria and required current verification pass. Partial results remain `DONE_WITH_CONCERNS`. Losing a lease is not a user blocker; another tick owns progress.

## Safety And Escalation

Stop/pause and escalate before unauthorized merge/push/deploy/publish/release, destructive change, secret/credential/billing action, public API change, product-scope expansion, material environment setup, or repeated verification failure.

Final summary includes achieved criteria, actual verification, remaining risk/waivers, automation cleanup result, and any user decision still required.
