# Coordinator Callback Template

Machine-authoritative async callback. Preserve the dispatch identity exactly and add a short human summary; do not repeat identity fields outside the JSON.

```text
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
  "expected_head_sha": "<EXACT_SHA | UNKNOWN | NONE>",
  "observed_head_sha": "<EXACT_SHA | NONE>",
  "execution_status": "<EXECUTION_STATUS>",
  "gate_verdict": "<GATE_VERDICT>",
  "coordinator_state": "<IN_PROGRESS | IN_REVIEW | ESCALATED | CANCELLED>"
}

Summary: <ONE_TO_THREE_BULLETS_OR_LINES>
Verification: <COMMAND_OR_CHECK_AND_RESULT>
Risks: <NONE_OR_RISK>
Suggested coordinator action: <REVIEW | QA | FIX | MERGE_READINESS | ESCALATE>
```

The role normally requests `IN_REVIEW`; it cannot grant `ACCEPTED`. Validate and deduplicate the JSON before using the prose.
