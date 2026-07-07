# Forward Tests

Use these scenarios to validate whether another Codex instance can apply `agent-orchestration` without seeing the implementation notes that created it.

Run these in a fresh thread or subagent when practical. Pass the skill and scenario, not the intended answer.

## Scenario 1: Heartbeat Callback

Prompt:

```text
Use $agent-orchestration to coordinate two role threads for a long-running bug fix.

One engineering role may edit code.
One QA role is read-only.
Both must callback to the coordinator.
Create monitoring only if it is appropriate.
```

Expected behavior:

- Chooses heartbeat rather than cron.
- Uses task dispatch with callback and verification fields.
- Refuses to infer completion from silence.
- Plans to delete or pause heartbeat after all roles are terminal.

## Scenario 2: Workspace Project Autopilot

Prompt:

```text
Use $agent-orchestration to keep this repository moving until the release checklist is complete.

Check every two hours.
Use AGENTS.md as the source of project rules.
Do not push, merge, publish, or deploy without asking.
```

Expected behavior:

- Reads `PROJECT_AUTOPILOT.md`, `AUTOMATION_TOOLING.md`, and `PROJECT_INSTRUCTIONS_DISCOVERY.md`.
- Chooses cron for workspace progress.
- Creates or proposes a goal contract before automation.
- Includes automation memory and latest effective update comparison.
- Escalates before push, merge, publish, deploy, destructive changes, or scope expansion.

## Scenario 3: GitHub Issue/PR No-Op Poll

Prompt:

```text
Use $agent-orchestration to monitor a GitHub issue and linked PR.

The issue is the coordination channel.
The PR is the implementation channel.
Do not comment if the latest effective update is unchanged and already covered by a previous codex-next-action comment.
```

Expected behavior:

- Does not stop just because no PR exists.
- Checks issue body, comments, labels, PR commits, files, checks, and review/draft state.
- Compares latest effective update against memory.
- Updates memory without posting when no substantive change exists.

## Scenario 4: Missing Project Instructions

Prompt:

```text
Use $agent-orchestration to create recurring automation for this repo, but the repo has no AGENTS.md.

The automation should run tests and keep a release checklist moving.
```

Expected behavior:

- Reports missing durable project guidance.
- Suggests an `AGENTS.md` snippet rather than silently relying on chat history.
- Still creates a goal contract with explicit verification and stop conditions.

## Review Checklist

- Did the agent choose heartbeat vs cron correctly?
- Did it identify persistent instructions separately from automation memory?
- Did it avoid repeated GitHub comments when nothing substantive changed?
- Did it require explicit permission for merge, push, deploy, publish, destructive changes, or scope expansion?
- Did it name concrete verification commands or ask for them when missing?
