# Coordinator Callback Template

Use this when a role thread reports directly back to the coordinator thread.

```text
Coordinator callback:
Task ID: <TASK_ID>
Role: <ROLE_NAME>
Role thread ID: <ROLE_THREAD_ID_OR_UNKNOWN>
Coordinator thread ID: <COORDINATOR_THREAD_ID>
Branch / worktree: <BRANCH_OR_WORKTREE_OR_NONE>
Commit: <COMMIT_OR_NONE>
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT

Summary:
- <ONE_TO_THREE_BULLETS>

Changed files / Files inspected:
- <PATH>: <WHY_IT_CHANGED_OR_WAS_INSPECTED>

Verification:
- <COMMAND_OR_CHECK>: PASS | FAIL | NOT RUN
  Result / reason: <DETAIL>

Risks:
- <NONE_OR_RISK>

Next coordinator action:
- <ACCEPT | REVIEW_DIFF | SEND_TO_QA | SEND_TO_REVIEW | REQUEST_FIX | RUN_MERGE_READINESS | ESCALATE_TO_USER>
```

