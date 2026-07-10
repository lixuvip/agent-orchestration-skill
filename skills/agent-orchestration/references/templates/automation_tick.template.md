# Automation Tick Template

Use this as the recurring prompt body for project autopilot automations.

```text
You are running a project autopilot tick.

Goal ID: <GOAL_ID>
Automation ID: <AUTOMATION_ID>
Workspace: <PATH_OR_REPOSITORY>
Coordinator thread ID: <THREAD_ID_OR_NONE>
Memory path: <AUTOMATION_MEMORY_PATH>
Lease state directory: <AUTOMATION_STATE_DIRECTORY>
Tick ID: <UNIQUE_TICK_ID>
Lease TTL seconds: <TTL_SECONDS>
Lifecycle state: <ACTIVE | DRAINING | CLOSED>

Goal contract:
<PASTE_OR_REFERENCE_GOAL_CONTRACT>

On each tick:
1. Generate Tick ID and acquire a fenced lease with `scripts/automation_lease.py`. On `LEASE_ALREADY_HELD` or `LEASE_BUSY`, exit as a quiet no-op.
2. Read project instructions from AGENTS.md, AGENTS.override.md, configured fallback instruction files, and relevant project docs.
3. Read automation memory. Stop if its fencing token is newer than this lease. If memory is missing, initialize it after this tick.
4. Inspect live state for the goal: git status, branch, issue/PR activity, role callbacks, tests, builds, logs, and blockers.
5. Identify the latest effective update, not just the newest timestamp; validate and deduplicate callback event IDs.
6. Compare state and idempotency keys with memory to avoid duplicate comments, status requests, summaries, or work.
7. Choose exactly one Next safe action inside Allowed autonomously.
8. Verify the lease immediately before the action, then run it and the smallest relevant verification.
9. Verify the lease again and atomically update memory with fencing token, observed state, action, evidence, risks, and next step.
10. If Done when is satisfied, post the final summary once and request pause/delete. Record cleanup only after tool confirmation.
11. If blocked, missing authority, or outside scope, post one deduplicated escalation and stop or wait according to the goal contract.
12. Release the lease in a finally-equivalent cleanup path. If the lease is expired or replaced, discard results and do not write or post.

Required tick summary:
Latest effective update: <SUMMARY_OR_UNCHANGED>
Lease result: <ACQUIRED | ALREADY_HELD | BUSY | EXPIRED | NOT_OWNER>
Fencing token: <INTEGER_OR_NONE>
Action taken: <ONE_ACTION_OR_NONE>
Verification: <COMMAND_OR_CHECK_AND_RESULT>
Memory updated: <YES_OR_NO>
Next safe action: <ACTION_OR_NONE>
Done: <YES_OR_NO>
Lifecycle state: <ACTIVE | DRAINING | CLOSED>
Cleanup confirmed: <YES_OR_NO_OR_NOT_APPLICABLE>
Escalation needed: <YES_OR_NO_AND_REASON>

Do not merge, push, deploy, delete data, rotate secrets, spend money, change public API contracts, or broaden scope unless explicitly allowed in the goal contract.
```
