# Automation Plan Template

Use this to prepare a heartbeat or cron automation before calling the automation tool.

```text
Automation plan

Name: <AUTOMATION_NAME>
Goal ID: <GOAL_ID>
Automation kind: <heartbeat | cron>
Destination: <thread | local | worktree>
Workspace(s): <CWD_LIST_OR_NONE>
Target thread ID: <THREAD_ID_OR_NONE>
Schedule: <NATURAL_LANGUAGE_INTERVAL; translate to tool schedule internally>
Reasoning effort: <minimal | low | medium | high>

Existing automation check:
- Matching automation ID: <ID_OR_NONE>
- Update instead of duplicate: <YES_OR_NO>

Goal contract:
- <PATH_OR_INLINE_SUMMARY>

Memory:
- Memory path: <AUTOMATION_MEMORY_PATH>
- Latest effective update key: <KEY>

Prompt responsibilities:
- Read AGENTS.md, AGENTS.override.md, configured fallback instruction files, and relevant project docs.
- Read automation memory before acting.
- Inspect live git, issue, PR, test, thread, or release state.
- Perform one safe next action per tick.
- Update memory every tick.
- Pause, delete, or escalate when done, blocked, or missing authority.

Requires user review before saving:
- <YES_IF_WORKTREE_SETUP_OR_RISKY_AUTHORITY_ELSE_NO>
```
