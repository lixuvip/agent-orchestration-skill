# Tutorial: Coordinate A Multi-Project Release

This tutorial models a realistic task where one coordinator asks three project threads to finalize work and report back.

## Scenario

You have three projects:

- `Service API`: shared backend service.
- `Web Client`: browser client using the shared service.
- `Mobile Client`: mobile client using the shared service.

You want each project to finish its changes, commit them, document the remote contract, and return a clean final status.

## Step 1: Start With A Coordinator Prompt

```text
Use $agent-orchestration.

Coordinate final delivery across Service API, Web Client, and Mobile Client.

For each project:
- inspect current git status;
- ensure shared service API documentation is clear;
- run relevant verification;
- create focused commits if the work is ready;
- return branch, commits, verification, and remaining risks.

Create a 5-minute heartbeat monitor and close it when every project reaches a terminal status.
```

## Step 2: Register Roles

The coordinator records a role table:

| Role | Project | Thread ID | Scope |
| --- | --- | --- | --- |
| API Engineer | Service API | `<thread-id>` | backend service and docs |
| Web Client Engineer | Web Client | `<thread-id>` | browser client and integration docs |
| Mobile Client Engineer | Mobile Client | `<thread-id>` | mobile client, API bridge, and docs |

Use `references/ROLE_REGISTRY.template.md` if this is a recurring setup.

## Step 3: Dispatch Work

Each role gets a prompt based on `references/templates/task_dispatch.template.md`.

Critical fields:

- `Task ID`
- `Coordinator thread ID`
- `This role thread ID`
- `Editable scope`
- `Read-only scope`
- `Verification`
- `Callback`
- `Stop and report if`

## Step 4: Create Heartbeat Monitoring

The coordinator creates a recurring automation using `references/templates/monitoring_heartbeat.template.md`.

Recommended interval:

```text
Every 5 minutes
```

The monitor reads every tracked thread and only accepts explicit terminal states:

- `DONE`
- `DONE_WITH_CONCERNS`
- `BLOCKED`
- `NEEDS_CONTEXT`

## Step 5: Summarize Results

When all roles finish, the coordinator produces a concise final summary:

```text
All three project threads reached terminal status.

Service API:
- Status: DONE_WITH_CONCERNS
- Commits: ...
- Verification: ...
- Risk: untracked dist/ left untouched

Web Client:
- Status: DONE_WITH_CONCERNS
- Commits: ...
- Verification: ...
- Risk: end-to-end browser tests were skipped because no test account was available

Mobile Client:
- Status: DONE
- Commits: ...
- Verification: ...
- Risk: none reported
```

## Step 6: Close The Loop

The coordinator disables or deletes the heartbeat automation after the all-complete summary is posted.

Do not leave stale monitors running after the task has reached terminal state.
