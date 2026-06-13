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

- `references/COMMUNICATION_PROTOCOL.md`
- `references/WORKFLOWS.md`
- `references/templates/task_dispatch.template.md`

For a small bug, it should choose the emergency fix or engineering implementation workflow.

## 3. Dispatch Role Tasks

The coordinator sends each role a scoped prompt with:

- role name;
- repository path;
- editable and read-only scope;
- stop conditions;
- verification requirements;
- callback requirements.

## 4. Track Completion

For one or two short-running role threads, the coordinator can manually read the role replies.

For multiple or long-running role threads, the coordinator should use:

- `references/AUTOMATION_MONITORING.md`
- `references/templates/monitoring_heartbeat.template.md`

The heartbeat checks each role every 5 minutes and closes itself after all roles reach a terminal state.

## 5. Final Coordinator Delivery

The final response should include:

- what changed;
- which roles participated;
- exact verification evidence;
- unresolved risks;
- commits or branch names when relevant.
