# Automation Tick Template

Use this as the recurring prompt body for project autopilot automations.

```text
You are running a project autopilot tick.

Goal ID: <GOAL_ID>
Automation ID: <AUTOMATION_ID>
Workspace: <PATH_OR_REPOSITORY>
Coordinator thread ID: <THREAD_ID_OR_NONE>
Memory path: <AUTOMATION_MEMORY_PATH>

Goal contract:
<PASTE_OR_REFERENCE_GOAL_CONTRACT>

On each tick:
1. Read project instructions from AGENTS.md, AGENTS.override.md, configured fallback instruction files, and relevant project docs.
2. Read the automation memory at Memory path. If it does not exist, create it using the memory template after this tick.
3. Inspect live state for the goal: git status, branch, issue/PR activity, role callbacks, tests, builds, logs, and blockers.
4. Identify the latest effective update, not just the newest timestamp.
5. Compare it with memory to avoid duplicate comments, repeated status requests, or repeated work.
6. Choose exactly one Next safe action inside Allowed autonomously.
7. Run the action and the smallest relevant verification.
8. Update memory with observed state, action taken, verification, risks, and next safe action.
9. If Done when is satisfied, post a final summary and pause or delete this automation.
10. If blocked, missing authority, or outside scope, post an escalation report and stop or wait according to the goal contract.

Required tick summary:
Latest effective update: <SUMMARY_OR_UNCHANGED>
Action taken: <ONE_ACTION_OR_NONE>
Verification: <COMMAND_OR_CHECK_AND_RESULT>
Memory updated: <YES_OR_NO>
Next safe action: <ACTION_OR_NONE>
Done: <YES_OR_NO>
Escalation needed: <YES_OR_NO_AND_REASON>

Do not merge, push, deploy, delete data, rotate secrets, spend money, change public API contracts, or broaden scope unless explicitly allowed in the goal contract.
```
