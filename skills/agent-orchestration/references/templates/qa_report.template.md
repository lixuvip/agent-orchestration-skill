# QA Report Template

QA evidence is valid only for the exact observed head SHA.

```text
Goal ID: <GOAL_ID>
Task ID: <TASK_ID>
Attempt: <ACTIVE_ATTEMPT>
Dispatch nonce: <ACTIVE_DISPATCH_NONCE>
Expected head SHA: <EXPECTED_HEAD_SHA>
Observed head SHA: <OBSERVED_HEAD_SHA>
Execution status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT | CANCELLED
Gate verdict: PASS | FAIL | BLOCKED | NOT_APPLICABLE

Summary:
- <OVERALL_TEST_RESULT>

Test matrix:
| Area | Scenario | Expected | Actual | Result |
| --- | --- | --- | --- | --- |
| <AREA> | <SCENARIO> | <EXPECTED> | <ACTUAL> | PASS / FAIL / BLOCKED / NOT TESTED |

Verification run:
- <COMMAND_OR_MANUAL_CHECK>: PASS | FAIL | NOT RUN
  Evidence: <LOG_PATH_SCREENSHOT_DESCRIPTION_OR_OUTPUT_SUMMARY>

Failures:
- Issue: <TITLE>
  Severity: P0 | P1 | P2 | P3
  Steps to reproduce:
  Expected:
  Actual:

Not tested:
- <SCENARIO_AND_REASON>

Risks / concerns:
- <NONE_OR_SPECIFIC_RISK>

Recommended coordinator action:
- <ACCEPT_GATE | RETURN_TO_ENGINEERING | REQUEST_MORE_EVIDENCE | ESCALATE>

ORCHESTRATION_EVENT_V1:
<COMPLETE_EVENT_WITH_COORDINATOR_STATE_IN_REVIEW>
```

If `observed_head_sha` differs from `expected_head_sha`, stop and report stale evidence. Any later code commit invalidates this verdict.
