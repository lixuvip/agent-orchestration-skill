# Coordinator Callback Template

Use this when a role thread reports directly to the coordinator. Copy the dispatch identity exactly and include the role event from `role_reply.template.md`.

```text
Coordinator callback:
Goal ID: <GOAL_ID>
Task ID: <TASK_ID>
Attempt: <POSITIVE_INTEGER>
Dispatch nonce: <DISPATCH_NONCE>
Coordinator epoch: <COORDINATOR_EPOCH>
Event ID: <UNIQUE_EVENT_ID>
Event timestamp: <ISO_8601_WITH_TIMEZONE>
Role: <ROLE_NAME>
Role thread ID: <ROLE_THREAD_ID>
Coordinator thread ID: <COORDINATOR_THREAD_ID>
Branch / worktree: <BRANCH_OR_WORKTREE_OR_NONE>
Base SHA: <EXACT_SHA | NONE>
Expected head SHA: <EXACT_SHA | NONE>
Observed head SHA: <EXACT_SHA | NONE>
Execution status: IN_PROGRESS | DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT | CANCELLED
Gate verdict: PENDING | PASS | FAIL | BLOCKED | WAIVED | NOT_APPLICABLE
Requested coordinator state: IN_PROGRESS | IN_REVIEW | ESCALATED | CANCELLED

Summary:
- <ONE_TO_THREE_BULLETS>

Changed files / Files inspected:
- <PATH>: <WHY_IT_CHANGED_OR_WAS_INSPECTED>

Verification:
- <COMMAND_OR_CHECK>: PASS | FAIL | NOT RUN
  Result / reason: <DETAIL>

Risks:
- <NONE_OR_RISK>

Suggested coordinator action:
- <REVIEW_DIFF | SEND_TO_QA | SEND_TO_REVIEW | REQUEST_FIX | RUN_MERGE_READINESS | ESCALATE_TO_USER>

ORCHESTRATION_EVENT_V1:
<COPY_THE_COMPLETE_JSON_EVENT_FROM_ROLE_REPLY>
```

The callback can request `IN_REVIEW`; it cannot grant `ACCEPTED`. The coordinator validates, deduplicates, rejects stale identities, and then emits its own authoritative state change.
