# Orchestration Routing

Use the smallest mode that safely preserves ownership, verification, recovery, and user authority. Do not turn every skill invocation into a multi-thread project.

## Modes

| Mode | Use when | Required artifacts | Avoid |
| --- | --- | --- | --- |
| `LITE` | One-shot work in the current context, normally one active role, no asynchronous callback, no recurring execution. | Scope, stop conditions, verification, concise delivery. | Task board, heartbeat, cron, automation memory, or a full event envelope when no async boundary exists. |
| `STANDARD` | Two or more roles, asynchronous or user-visible threads, cross-repository handoff, merge/release gate, or long-running finite work. | Explicit dispatch ownership, task board, `ORCHESTRATION_EVENT_V1` for async handoffs, coordinator acceptance, branch/worktree isolation where edits overlap. | Durable cron and project memory when the work has a finite coordinator session. |
| `DURABLE` | Recurring project progress, work that must survive multiple ticks, or a user-requested durable operating loop. | Everything needed from Standard plus goal contract, automation plan, durable memory, cron, fenced lease, idempotency keys, lifecycle and escalation rules. | Treating a timestamp change as progress or running without concurrency fencing. |

Standard work uses a heartbeat only when it is asynchronous, long-running, or tied to user-visible role threads. A finite synchronous Standard flow can use manual task-board polling. Every recurring heartbeat or cron tick still requires the concurrency lease.

## Minimum Safe Route

Choose at least `STANDARD` when any applies:

- two or more active roles;
- any role callback can arrive asynchronously;
- user-visible role threads are created;
- work crosses repositories or independent worktrees;
- merge, release, QA, or review gates must be coordinated;
- work is long-running enough to need recoverable monitoring.

Choose `DURABLE` when any applies:

- the schedule repeats after the current coordinator turn;
- automation memory is required to resume safely;
- the user explicitly asks for project autopilot or an equivalent durable mode.

Do not downgrade below this minimum even if a requested mode is lighter. Explain the safety reason briefly. A user may explicitly upgrade to a heavier mode.

## Independent Modifiers

External-model review or research is a modifier, not automatically a heavier orchestration mode. A one-shot read-only `agy` second opinion can remain `LITE` while following `AGY_GEMINI_REVIEW.md` or `AGY_GEMINI_RESEARCH.md`. It becomes Standard or Durable only if its actual coordination shape requires that.

## Shared Edit Safety

If two roles would edit the same files or shared working tree in parallel, routing alone does not make it safe. The router emits `ISOLATE_OR_SERIALIZE_SHARED_EDITS`: isolate with branches/worktrees and non-overlapping ownership, or serialize the edits. If neither is possible, keep the work in one execution context.

## Router Helper

For repeatable intake decisions, send task characteristics as JSON:

```bash
printf '%s\n' '{
  "role_count": 2,
  "asynchronous": true,
  "recurring": false,
  "user_visible_threads": true,
  "requested_mode": "AUTO"
}' | python3 scripts/route_orchestration.py
```

The helper returns `ORCHESTRATION_ROUTE` with:

- minimum and selected mode;
- whether the requested mode was honored;
- `NONE`, `HEARTBEAT`, or `CRON` monitoring;
- required protocol, task board, goal contract, memory, lease, and lifecycle controls;
- external-model modifiers and shared-edit warnings.

Treat the helper as a deterministic default. Project instructions and explicit user constraints may require a heavier route, but never a route that violates a hard safety or authorization boundary.

## Route Changes During Work

- `LITE -> STANDARD`: a second independent role, asynchronous callback, cross-repository handoff, or formal gate appears.
- `STANDARD -> DURABLE`: work must continue across recurring ticks or needs durable recovery memory.
- Do not discard protocol, event ledger, or gate evidence when upgrading.
- Do not downshift an active automation merely to remove lease or memory requirements. Close it cleanly first.
- After a Durable automation is `CLOSED`, a later one-shot follow-up may start as a new Lite task with a new goal identity.

## Practical Examples

| Scenario | Route |
| --- | --- |
| Review one local diff with Codex in the current thread | Lite |
| One read-only `agy` review and coordinator synthesis | Lite + external-model modifier |
| Engineer branch, QA thread, reviewer gate | Standard; heartbeat if asynchronous |
| Collect two finite research threads and synthesize once | Standard |
| Poll an issue/PR every two hours and take safe next actions | Durable cron |
| Continue release readiness until its goal contract passes | Durable cron |
