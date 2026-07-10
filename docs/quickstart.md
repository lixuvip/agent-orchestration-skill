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

- `references/ORCHESTRATION_ROUTING.md`
- `references/ORCHESTRATION_PROTOCOL.md`
- `references/COMMUNICATION_PROTOCOL.md`
- `references/WORKFLOWS.md`
- `references/templates/task_dispatch.template.md`

With engineering plus asynchronous QA, this is normally Standard mode. A one-shot current-thread inspection would stay Lite; recurring progress would use Durable.

## 3. Dispatch Role Tasks

The coordinator sends each role a scoped prompt with:

- role name;
- repository path;
- editable and read-only scope;
- stop conditions;
- verification requirements;
- callback requirements.
- goal/task ID, attempt, dispatch nonce, coordinator epoch, and expected artifact SHA for asynchronous handoffs.

## 4. Track Completion

For one or two short-running role threads, the coordinator can manually read the role replies.

For multiple or long-running role threads, the coordinator should use:

- `references/AUTOMATION_MONITORING.md`
- `references/templates/monitoring_heartbeat.template.md`

The heartbeat checks each role every 5 minutes, validates versioned callbacks, and uses a fenced lease so overlapping ticks cannot both act. After all roles reach terminal state it moves `ACTIVE -> DRAINING -> CLOSED`, posts one final summary, and waits for cleanup confirmation.

## 5. Use Project Autopilot For Recurring Progress

Use Project Autopilot when the task should continue across repeated automation runs, not just monitor role completion.

```text
Use $agent-orchestration to create a project autopilot loop.

Goal:
Keep this repository moving until the release-readiness checklist is complete.

Use:
- AGENTS.md and AGENTS.override.md for durable project rules;
- PROJECT_AUTOPILOT.md for the recurring control loop;
- project_goal_contract.template.md for done criteria and permissions;
- automation_tick.template.md for each recurring run;
- automation_memory.template.md so repeated runs do not duplicate work.
- AUTOMATION_CONCURRENCY.md so every tick acquires a lease, records a fencing token, and discards stale-owner results.

Escalate before merge, push, deploy, destructive changes, public API contract changes, or scope expansion.
```

Use heartbeat automation for current-thread callback checks. Use cron automation for workspace or worktree progress that should run independently.

## 6. Final Coordinator Delivery

The final response should include:

- what changed;
- which roles participated;
- exact verification evidence;
- unresolved risks;
- commits or branch names when relevant.
- whether any automation was paused, deleted, or left active.
- the exact accepted artifact SHA and whether coordinator state reached `ACCEPTED`.
