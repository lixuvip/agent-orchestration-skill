# Automation Plan Template

Use this to prepare a heartbeat or cron automation before calling the automation tool.

```text
Automation plan

Name: <AUTOMATION_NAME>
Orchestration mode: DURABLE
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

Concurrency lease:
- State directory: <AUTOMATION_STATE_DIRECTORY>
- Lease helper: scripts/automation_lease.py
- Unique owner per tick: <TICK_ID_STRATEGY>
- TTL / maximum tick runtime: <SECONDS> / <SECONDS>
- Overlap policy: LEASE_ALREADY_HELD and LEASE_BUSY are quiet no-ops

Lifecycle:
- Initial state: <ACTIVE>
- Heartbeat generation: <GENERATION_ID_OR_NOT_APPLICABLE>
- Final summary idempotency key: <KEY_OR_NOT_APPLICABLE>
- Cleanup confirmation source: <AUTOMATION_TOOL_RESULT_OR_NOT_APPLICABLE>

Prompt responsibilities:
- Read AGENTS.md, AGENTS.override.md, configured fallback instruction files, and relevant project docs.
- Read automation memory before acting.
- Acquire a fenced lease before reading mutable memory; verify before messages and writes.
- Inspect live git, issue, PR, test, thread, or release state.
- Perform one safe next action per tick.
- Update memory every tick.
- Record fencing token and idempotency keys, then release the lease in cleanup.
- Pause, delete, or escalate when done, blocked, or missing authority.

Requires user review before saving:
- <YES_IF_WORKTREE_SETUP_OR_RISKY_AUTHORITY_ELSE_NO>
```
