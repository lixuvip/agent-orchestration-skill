# Controller Loop

Use this reference when the coordinator manages child threads, subagents, branches, worktrees, status requests, heartbeat automation, project autopilot, or merge readiness.

The controller loop keeps the main thread authoritative while allowing branch or role threads to work independently.

## Flow

1. Confirm or infer the execution surface from `ORCHESTRATION_INTAKE.md`.
2. Create or select the role thread, branch, or worktree.
3. Dispatch a scoped task with `templates/task_dispatch.template.md`.
4. Record task ID, role, thread ID, branch/worktree, callback policy, and merge policy.
5. Require the role to send `templates/coordinator_callback.template.md` back to the coordinator when thread messaging is available.
6. Create heartbeat monitoring for long-running work, two or more role threads, or work that may finish while the coordinator is inactive.
7. For recurring workspace progress until a goal is met, read `PROJECT_AUTOPILOT.md` and create a goal contract, automation plan, tick prompt, memory path, and escalation rule before enabling automation.
8. If a role is silent or unclear, send `templates/status_request.template.md` before inferring anything.
9. When a role reaches a terminal state, inspect changed files, verification, risks, commits, and branch state.
10. Before merge or push, run `templates/merge_readiness.template.md`.
11. Deliver only after coordinator verification, not from child-thread confidence alone.

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

Do not mark silence as completion. A status request must ask for one of `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`, or `IN_PROGRESS` with evidence.

## Merge Readiness

Run merge readiness when a role asks to merge, push, publish, or hand off completed branch work. The coordinator checks base branch, working tree state, scope, tests, conflicts, unresolved risks, and explicit push or merge permission.

## Autopilot Readiness

Run autopilot readiness before creating a recurring project automation. The coordinator checks the target `AGENTS.md` / `AGENTS.override.md`, goal contract, allowed autonomous actions, confirmation gates, verification commands, memory path, idempotency key, and stop conditions.
