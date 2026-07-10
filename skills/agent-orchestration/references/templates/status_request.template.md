# Status Request Template

Use this when a role thread is silent, ambiguous, stale, or missing verification.

```text
Status request for <TASK_ID>
Goal ID: <GOAL_ID>
Attempt: <ACTIVE_ATTEMPT>
Dispatch nonce: <ACTIVE_DISPATCH_NONCE>
Coordinator epoch: <ACTIVE_COORDINATOR_EPOCH>
Expected head SHA: <ACTIVE_EXPECTED_HEAD_SHA>
Coordinator thread ID: <COORDINATOR_THREAD_ID>
Role thread ID: <ROLE_THREAD_ID>

Reply only for this active dispatch identity. If your prior work belongs to another attempt, nonce, epoch, or SHA, report it as stale and do not claim current completion.

Reply with one execution status and evidence:
- IN_PROGRESS
- DONE
- DONE_WITH_CONCERNS
- BLOCKED
- NEEDS_CONTEXT
- CANCELLED

Required details:
- Current summary:
- Changed files / files inspected:
- Observed head SHA:
- Verification run:
- Gate verdict:
- Risks / blockers:
- Estimated next step:
- Complete `ORCHESTRATION_EVENT_V1` envelope from `role_reply.template.md`:
```
