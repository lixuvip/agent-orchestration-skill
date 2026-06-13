# State Machine

Use this reference when coordinating more than one role, thread, repository, or heartbeat monitor.

## States

| State | Meaning | Terminal | Coordinator action |
| --- | --- | --- | --- |
| `TODO` | Task is known but not dispatched. | No | Fill scope, owner, verification, and stop conditions. |
| `IN_PROGRESS` | Role has accepted or started the task. | No | Wait, poll, or heartbeat. Do not infer completion. |
| `DONE` | Role completed and verified the task. | Yes | Inspect output, diff scope, and verification before accepting. |
| `DONE_WITH_CONCERNS` | Role completed but risk or coverage gaps remain. | Yes | Preserve concerns and decide whether to remediate or escalate. |
| `NEEDS_CONTEXT` | Role cannot continue without missing facts. | Yes | Provide context, narrow scope, or ask the user. |
| `BLOCKED` | Role hit an environment, permissions, conflict, or safety blocker. | Yes | Resolve blocker or escalate to the user. |
| `CANCELLED` | Coordinator or user intentionally stopped the task. | Yes | Record reason and do not treat it as delivered. |

## Allowed Transitions

```text
TODO -> IN_PROGRESS
TODO -> CANCELLED
IN_PROGRESS -> DONE
IN_PROGRESS -> DONE_WITH_CONCERNS
IN_PROGRESS -> NEEDS_CONTEXT
IN_PROGRESS -> BLOCKED
IN_PROGRESS -> CANCELLED
NEEDS_CONTEXT -> TODO
BLOCKED -> TODO
DONE_WITH_CONCERNS -> TODO
```

Do not transition directly from `TODO` to `DONE`. A role must explicitly report terminal status with evidence.

## Stale Or Silent Roles

If a role has no explicit terminal status:

1. Keep it `IN_PROGRESS`.
2. Read the latest role thread message when tools allow.
3. Send a focused status request if needed.
4. Mark `BLOCKED` only when the latest evidence shows a blocker.
5. Mark `CANCELLED` only when the user or coordinator intentionally stops the task.

Silence is never completion.

## Acceptance Rules

- Accept `DONE` only after checking scope, changed files, verification, and risks.
- Accept `DONE_WITH_CONCERNS` only as a terminal status for monitoring; it is not a risk-free delivery.
- Do not deliver if any required role is `TODO` or `IN_PROGRESS`.
- Do not hide `BLOCKED`, `NEEDS_CONTEXT`, `CANCELLED`, or unverified work in the final summary.
