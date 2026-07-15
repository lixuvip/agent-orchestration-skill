# Quickstart

This quickstart shows the smallest useful orchestration loop.

## 1. Invoke The Skill

In Codex, write:

```text
Use $agent-orchestration to coordinate this bug fix with one engineering thread and one QA thread.

Goal:
Fix the failing timestamp export option in the report generation flow.

Constraints:
- Engineer may edit application and test code.
- QA is read-only and must run the regression tests.
- Both roles must report exact commands and results.
```

## 2. Coordinator Chooses A Workflow

The coordinator reads:

- `references/COORDINATION_RUNBOOK.md` for Standard work;
- only the specific dispatch/callback/QA templates used, starting with `task_dispatch.template.md`.

With engineering plus asynchronous QA, this is normally Standard mode. A one-shot current-thread inspection would stay Lite; recurring progress would use Durable.

Before creating each new user-visible role thread, the coordinator separately selects the lowest adequate supported thinking effort. Thinking is not inferred from Lite/Standard/Durable or from the role name, and the coordinator does not set a model unless the user explicitly requested one.

## 3. Dispatch Role Tasks

The coordinator sends each role a scoped prompt with:

- role name;
- repository path;
- editable and read-only scope;
- stop conditions;
- verification requirements;
- callback requirements;
- thinking requested, thinking applied, and the coordinator's selection rationale;
- goal/task ID, attempt, dispatch nonce, coordinator epoch, and expected artifact SHA for asynchronous handoffs.

## 4. Track Completion

For one or two short-running role threads, the coordinator can manually read the role replies.

For multiple or long-running role threads, the coordinator should use:

- `references/COORDINATION_RUNBOOK.md`
- `references/templates/monitoring_heartbeat.template.md`

The heartbeat checks each role every 5 minutes, validates versioned callbacks, and uses a fenced lease so overlapping ticks cannot both act. After all roles reach terminal state it moves `ACTIVE -> DRAINING -> CLOSED`, posts one final summary, and waits for cleanup confirmation.

## 5. Use Project Autopilot For Recurring Progress

Use Project Autopilot when the task should continue across repeated automation runs, not just monitor role completion.

```text
Use $agent-orchestration to create a project autopilot loop.

Goal:
Keep this repository moving until the release-readiness checklist is complete.

Use:
- PROJECT_AUTOPILOT.md for the unified instruction, automation, memory, lease, fencing, and lifecycle contract;
- project_goal_contract.template.md for done criteria and permissions;
- automation_tick.template.md for each recurring run;
- automation_memory.template.md so repeated runs do not duplicate work.

Escalate before merge, push, deploy, destructive changes, public API contract changes, or scope expansion.
```

Use heartbeat automation for current-thread callback checks. Use cron automation for workspace or worktree progress that should run independently.

## 6. Add An Optional External Audit

For a normal code audit, the coordinator can ask once whether the user wants `agy` as an auxiliary reviewer. Without confirmation it continues Codex-only and does not probe the tool. After opt-in, it checks `command -v agy` once per goal and host; an unavailable or unhealthy result is cached, shown once, and not retried until the goal or environment changes or the user requests a recheck.

## 7. Final Coordinator Delivery

The final response should include:

- what changed;
- which roles participated;
- exact verification evidence;
- unresolved risks;
- commits or branch names when relevant;
- whether any automation was paused, deleted, or left active;
- the exact accepted artifact SHA and whether coordinator state reached `ACCEPTED`.
