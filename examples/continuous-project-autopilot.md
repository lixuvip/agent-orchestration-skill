# Continuous Project Autopilot

```text
Use $agent-orchestration to create a project autopilot loop for this repository.

Goal:
Keep this project moving until the release-readiness checklist is complete.

Use Codex project guidance:
- Read AGENTS.md and any nested AGENTS.override.md before acting.
- Use .codex/config.toml only as Codex configuration, not as task memory.
- If repeated rules are missing, suggest an AGENTS.md patch instead of silently relying on chat history.

Automation:
- Use a recurring cron automation for workspace checks.
- Use a heartbeat only for coordinator-thread follow-up or short callback polling.
- Keep an automation memory file and compare the latest effective update before posting comments or repeating work.

Allowed autonomously:
- inspect git status, issues, PRs, tests, and docs;
- run non-destructive validation commands;
- make scoped docs/test updates if already allowed by the user;
- request status from child threads;
- summarize progress.

Requires confirmation:
- merge, push, deploy, publish, delete data, rotate secrets, spend money, change public API contracts, or expand scope.

Done when:
- all release-readiness checklist items are verified;
- tests or documented checks have passed;
- unresolved risks are either fixed or explicitly reported.

Stop and escalate if:
- verification fails twice for the same reason;
- required permissions are missing;
- the next action would exceed the allowed autonomous scope.
```
