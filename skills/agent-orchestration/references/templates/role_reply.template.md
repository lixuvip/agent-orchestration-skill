# Role Reply Template

Human-readable role result. For async Standard/Durable work, send the machine event separately with `coordinator_callback.template.md`; do not duplicate its JSON here.

```text
Execution status: IN_PROGRESS | DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT | CANCELLED
Gate verdict: PENDING | PASS | FAIL | BLOCKED | WAIVED | NOT_APPLICABLE

Summary:
- <WHAT_WAS_DONE_OR_INSPECTED>

Changed files / Files inspected:
- <PATH>: <WHY>

Verification:
- <COMMAND_OR_CHECK>: PASS | FAIL | NOT RUN — <RESULT_OR_REASON>

Artifact / branch / worktree:
- <OBSERVED_SHA_OR_NONE>; <BRANCH_OR_WORKTREE_OR_NONE>

Risks / concerns:
- <NONE_OR_SPECIFIC_RISK>

Callback:
- <SENT_TO_COORDINATOR | NOT_AVAILABLE: REASON | NOT_APPLICABLE>

Recommended next action:
- <COORDINATOR_REVIEW | QA | REVIEW | FIX | ESCALATE | NONE>
```

`NOT RUN` requires a reason. Failed required checks use `FAIL`/`BLOCKED`; coverage gaps use `DONE_WITH_CONCERNS`. A role cannot claim coordinator `ACCEPTED`.
