# Review Findings Template

Review evidence is pinned to one exact commit SHA.

```text
Goal ID: <GOAL_ID>
Task ID: <TASK_ID>
Attempt: <ACTIVE_ATTEMPT>
Dispatch nonce: <ACTIVE_DISPATCH_NONCE>
Expected head SHA: <EXPECTED_HEAD_SHA>
Observed head SHA: <OBSERVED_HEAD_SHA>
Execution status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT | CANCELLED
Gate verdict: PASS | FAIL | BLOCKED | NOT_APPLICABLE

Findings:
- [P0 | P1 | P2 | P3] <TITLE>
  File: <PATH:LINE>
  Problem: <WHAT_IS_WRONG>
  Impact: <WHY_IT_MATTERS>
  Suggested fix: <HOW_TO_FIX_OR_DIRECTION>

Open questions:
- <QUESTION_OR_NONE>

Test gaps:
- <GAP_OR_NONE>

Merge recommendation:
- APPROVE | APPROVE_WITH_CONCERNS | REQUEST_CHANGES | BLOCKED

Recommended coordinator action:
- <ACCEPT_GATE | RETURN_TO_ENGINEERING | SEND_TO_QA | ESCALATE>

ORCHESTRATION_EVENT_V1:
<COMPLETE_EVENT_WITH_COORDINATOR_STATE_IN_REVIEW>
```

- Use `FAIL` when a blocking finding remains; an `APPROVE` label cannot override a failed gate.
- If `observed_head_sha` differs from `expected_head_sha`, report stale evidence instead of reviewing a moving branch.
- Any later code commit invalidates this verdict.
