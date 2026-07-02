# Example Prompt: Branch Callback Controller Loop

```text
Use $agent-orchestration to coordinate branch work with direct callback to the main coordinator thread.

Goal:
Have a technical engineer finish the export retry branch, then have QA verify the command path before the coordinator decides whether it is merge-ready.

Execution:
- Create or continue a dedicated engineering branch/worktree.
- Keep QA read-only.
- Require every role to report back to the coordinator thread using the coordinator callback template.
- Create a heartbeat monitor if either role is long-running or if the coordinator may be inactive while they work.

Engineering role:
- Inspect current branch status before editing.
- Implement only the scoped retry behavior.
- Run the relevant unit tests.
- Commit only if the work is complete and verified.
- Callback with branch, commit, changed files, tests, risks, and next coordinator action.

QA role:
- Read the engineering callback.
- Run the documented export command path.
- Report exact commands, outputs, failures, and coverage gaps.
- Do not modify implementation files.

Coordinator:
- Send a status request if any role is silent or lacks verification.
- Run merge readiness before merging, pushing, or telling the user the branch is ready.
- Do not merge or push unless the user explicitly authorized that action.
```

