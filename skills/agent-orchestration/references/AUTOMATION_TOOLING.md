# Automation Tooling

Use this reference before creating, updating, viewing, or deleting Codex automations for orchestration work.

## Choose The Automation Surface

| Need | Preferred automation | Why |
| --- | --- | --- |
| Continue this coordinator thread later | Heartbeat | It wakes the current thread and is best for short follow-up or callback polling. |
| Poll role threads until all terminal | Heartbeat | It stays attached to the coordinator loop. |
| Repeatedly inspect and advance a workspace | Cron | It runs against local/worktree workspaces and can continue project autopilot. |
| Worktree setup needs review | Suggested cron create/update | The user should review the environment before saving. |
| Existing automation already covers the goal | Update existing automation | Avoid duplicate runs, duplicate comments, and conflicting memory. |

Do not create a cron automation as a workaround for a thread heartbeat unless the user explicitly asks for workspace-level recurrence.

## Existing Automation Check

Before creating an automation:

1. Inspect existing automations by name, prompt, cwd, and target thread when the environment exposes them.
2. Match on goal, repository, issue/PR, branch, or coordinator thread.
3. Prefer update over duplicate creation.
4. Preserve existing fields unless the user asked to change them.
5. If the user asks for a temporary window, create a separate temporary overlay or schedule change without overwriting the durable automation contract.

## Prompt Contract

Automation prompts must include:

- goal ID and automation ID if known;
- target repository, cwd, branch, issue, PR, release, or thread IDs;
- project instruction sources such as `AGENTS.md` and `AGENTS.override.md`;
- automation memory path;
- lease state directory, tick owner ID, TTL, and fencing-token policy;
- latest effective update / idempotency key;
- allowed autonomous actions;
- confirmation gates;
- verification commands;
- stop, pause, or escalation conditions.

Do not rely on raw updated timestamps alone. Compare the latest effective update against memory before posting comments or repeating work.

## Schedule Handling

Let the automation tool own schedule serialization. Do not show raw RRULE strings to the user. Describe cadence in natural language in user-facing text.

Use short heartbeat intervals only when the user expects active follow-up. For durable project autopilot, prefer a cadence that matches the project's update rate, such as hourly, twice daily, daily, or weekday work windows.

## Memory Handling

Use an automation-specific memory file. Prefer:

```text
${CODEX_HOME:-$HOME/.codex}/automations/<automation-id>/memory.md
```

If `CODEX_HOME` is unset, resolve through `$HOME/.codex`; never allow the path to collapse to `/automations`.

Each run must update memory when it observes state, even when no user-facing action is needed.

Recurring runs must follow `AUTOMATION_CONCURRENCY.md`: acquire before reading mutable memory, verify before external side effects or memory writes, record the fencing token, and release after cleanup. A run that receives `LEASE_ALREADY_HELD`, `LEASE_BUSY`, `LEASE_EXPIRED`, or `LEASE_NOT_OWNER` must not post or write.

## Lifecycle

- Keep active when work is still `IN_PROGRESS` and within scope.
- Pause when blocked, missing authority, or waiting for user confirmation.
- Heartbeat monitors use `ACTIVE -> DRAINING -> CLOSED`: stop new requests in `DRAINING`, post the final summary once, request pause/delete, and wait for tool confirmation.
- Delete or pause after final done summary, depending on whether the user expects future reuse. Record `CLOSED` only after confirmation.
- A cleanup retry must not repost the final summary, and a late callback must not recreate a `CLOSED` monitor.
- Archive a completed thread only through the thread archive tool when the user asks for that behavior.

## Safety Gates

Stop and escalate before:

- merge, push, deploy, publish, or release;
- destructive file/data changes;
- secret, credential, or billing operations;
- public API contract changes;
- product scope expansion;
- repeated verification failure;
- environment setup that would materially change the workspace.
