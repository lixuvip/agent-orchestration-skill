# Controller Loop

Use this reference when the coordinator manages child threads, subagents, branches, worktrees, status requests, heartbeat automation, project autopilot, or merge readiness.

The controller loop keeps the main thread authoritative while allowing branch or role threads to work independently.

## Flow

1. Confirm or infer the execution surface from `ORCHESTRATION_INTAKE.md`.
2. Create or select the role thread, branch, or worktree.
3. Mint a `ORCHESTRATION_EVENT_V1` dispatch identity: goal ID, task ID, attempt, nonce, coordinator epoch, base SHA, and expected head SHA.
4. Dispatch a scoped task with `templates/task_dispatch.template.md`.
5. Record the full dispatch identity, role, thread ID, branch/worktree, callback policy, and merge policy.
6. Require the role to send `templates/coordinator_callback.template.md` back to the coordinator when thread messaging is available.
7. Create heartbeat monitoring for long-running work, two or more role threads, or work that may finish while the coordinator is inactive. Configure a fenced lease, automation memory, generation ID, and `ACTIVE -> DRAINING -> CLOSED` lifecycle from `AUTOMATION_CONCURRENCY.md`.
8. For recurring workspace progress until a goal is met, read `PROJECT_AUTOPILOT.md` and create a goal contract, automation plan, tick prompt, memory path, and escalation rule before enabling automation.
9. If a role is silent or unclear, send `templates/status_request.template.md` before inferring anything.
10. Validate and deduplicate every callback before updating state. Ignore old attempt, nonce, epoch, and SHA events as stale.
11. When a role reaches a terminal execution state, move the coordinator state to `IN_REVIEW` and inspect changed files, verification, risks, exact SHA, and branch state.
12. Before merge or push, run `templates/merge_readiness.template.md` against the same exact SHA used by required QA and review gates.
13. Deliver only after the coordinator emits `ACCEPTED`; role confidence alone cannot accept work.

## Tool Preference

- Use `send_message_to_thread` for direct coordinator callbacks when available.
- Use `read_thread` to inspect role state before accepting completion.
- Use heartbeat automation for long-running or multi-thread work.
- Use cron automation for durable project autopilot tied to a workspace or worktree.
- Use internal subagents only when the user explicitly asked for subagents, delegation, or parallel agent work and the work scopes do not overlap.
- Use manual task-board polling when thread, subagent, or automation tools are unavailable.

## Status Request Policy

Send a status request when:

- the latest role message lacks an explicit terminal status;
- the role reports progress but no verification;
- the heartbeat sees no state change after a reasonable polling interval;
- the branch/worktree state is unclear before merge readiness.

Do not mark silence as completion. A status request must include the current dispatch identity and ask for one of `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`, `CANCELLED`, or `IN_PROGRESS` with evidence and observed SHA.

## Merge Readiness

Run merge readiness when a role asks to merge, push, publish, or hand off completed branch work. The coordinator checks base branch, working tree state, scope, tests, conflicts, unresolved risks, explicit push or merge permission, and whether every required gate examined the exact candidate SHA. A new code commit invalidates prior gate evidence.

## Autopilot Readiness

Run autopilot readiness before creating a recurring project automation. The coordinator checks the target `AGENTS.md` / `AGENTS.override.md`, goal contract, allowed autonomous actions, confirmation gates, verification commands, memory path, lease state directory, TTL, fencing-token policy, lifecycle state, idempotency keys, and stop conditions.
