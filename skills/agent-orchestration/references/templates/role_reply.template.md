# Role Reply Template

Every role uses this format. The prose is for humans; the event envelope is authoritative for routing and deduplication.

```text
Execution status: IN_PROGRESS | DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT | CANCELLED
Gate verdict: PENDING | PASS | FAIL | BLOCKED | WAIVED | NOT_APPLICABLE

Summary:
- <WHAT_WAS_DONE_OR_INSPECTED>

Changed files / Files inspected:
- <PATH>: <WHY_IT_WAS_CHANGED_OR_INSPECTED>

Verification run:
- <COMMAND_OR_CHECK>: PASS | FAIL | NOT RUN
  Result / reason: <DETAIL>

Risks / concerns:
- <NONE_OR_SPECIFIC_RISK>

Branch / worktree:
- <BRANCH_OR_WORKTREE_OR_NONE>

Commit / observed head SHA:
- <EXACT_SHA | NONE>

Coordinator callback:
- Sent: <YES | NO | NOT_AVAILABLE>
- Destination / reason: <COORDINATOR_THREAD_ID_OR_REASON>

Recommended next role:
- <Coordinator | Product Designer | Technical Engineer | QA Tester | Code Reviewer | Release / Docs>

ORCHESTRATION_EVENT_V1:
{
  "protocol_version": "ORCHESTRATION_EVENT_V1",
  "goal_id": "<GOAL_ID>",
  "task_id": "<TASK_ID>",
  "attempt": <POSITIVE_INTEGER>,
  "dispatch_nonce": "<DISPATCH_NONCE>",
  "coordinator_epoch": "<COORDINATOR_EPOCH>",
  "event_id": "<UNIQUE_EVENT_ID>",
  "event_timestamp": "<ISO_8601_WITH_TIMEZONE>",
  "role": "<ROLE_NAME>",
  "coordinator_thread_id": "<COORDINATOR_THREAD_ID>",
  "role_thread_id": "<ROLE_THREAD_ID>",
  "base_sha": "<EXACT_SHA | NONE>",
  "expected_head_sha": "<EXACT_SHA | NONE>",
  "observed_head_sha": "<EXACT_SHA | NONE>",
  "execution_status": "<EXECUTION_STATUS>",
  "gate_verdict": "<GATE_VERDICT>",
  "coordinator_state": "<IN_PROGRESS | IN_REVIEW | ESCALATED | CANCELLED>"
}
```

- `NOT RUN` requires a reason.
- A failed required check uses `FAIL` or `BLOCKED`, not `PASS`.
- Risk or coverage gaps use `DONE_WITH_CONCERNS`.
- Completed role work normally requests `IN_REVIEW`; it cannot claim `ACCEPTED`.
- Preserve the dispatch identity exactly. Never increment `attempt` or mint a coordinator epoch yourself.
