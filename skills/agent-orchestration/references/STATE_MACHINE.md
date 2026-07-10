# State Machine

Use this reference when coordinating more than one role, thread, repository, gate, or heartbeat monitor. Read `ORCHESTRATION_PROTOCOL.md` first; this file describes transitions while the protocol defines the canonical event envelope.

## Role Execution State

| State | Meaning | Terminal for the role attempt |
| --- | --- | --- |
| `TODO` | Work is known but not started. | No |
| `IN_PROGRESS` | Work has started or a status request confirms activity. | No |
| `DONE` | Work and claimed verification are ready for coordinator inspection. | Yes |
| `DONE_WITH_CONCERNS` | Work is ready for inspection with explicit risk or coverage gaps. | Yes |
| `NEEDS_CONTEXT` | Missing facts prevent safe continuation. | Yes |
| `BLOCKED` | Environment, permission, conflict, dependency, or safety boundary prevents continuation. | Yes |
| `CANCELLED` | User or coordinator intentionally stopped the attempt. | Yes |

```text
TODO -> IN_PROGRESS
TODO -> CANCELLED
IN_PROGRESS -> DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED | CANCELLED
NEEDS_CONTEXT | BLOCKED | DONE_WITH_CONCERNS -> new attempt at TODO
```

Do not transition directly from `TODO` to `DONE`. Retrying a terminal attempt increments `attempt` and mints a new `dispatch_nonce`.

## Coordinator State

| State | Meaning | Typical next state |
| --- | --- | --- |
| `TODO` | Task is being scoped. | `DISPATCHED`, `CANCELLED` |
| `DISPATCHED` | Current attempt and nonce were sent. | `IN_PROGRESS`, `IN_REVIEW`, `ESCALATED`, `CANCELLED` |
| `IN_PROGRESS` | Current callback confirms active work. | `IN_REVIEW`, `ESCALATED`, `CANCELLED` |
| `IN_REVIEW` | Role reported a terminal result; coordinator or gate is inspecting it. | `ACCEPTED`, `RETURNED`, `ESCALATED`, `CANCELLED` |
| `RETURNED` | Current attempt was rejected and a new attempt must be dispatched. | `DISPATCHED`, `CANCELLED` |
| `ACCEPTED` | Coordinator accepted commit-pinned, gate-satisfying evidence. | Terminal |
| `ESCALATED` | User input or external authority is required. | `DISPATCHED`, `CANCELLED` |
| `CANCELLED` | User or coordinator intentionally stopped the task. | Terminal |

Role `DONE` moves the coordinator to `IN_REVIEW`, never directly to `ACCEPTED`.

## Gate Verdict

| Verdict | Meaning |
| --- | --- |
| `PENDING` | Required evidence has not been evaluated. |
| `PASS` | Required check passed against the exact expected SHA. |
| `FAIL` | Check found a defect or unmet criterion. |
| `BLOCKED` | Check could not execute due to an external blocker. |
| `WAIVED` | Coordinator explicitly waived a check and recorded why. |
| `NOT_APPLICABLE` | This task has no such gate. |

`FAIL` returns the task for another attempt. A code-changing retry invalidates earlier QA and review evidence.

## Stale, Duplicate, Or Silent Roles

Process callbacks in the order defined by `ORCHESTRATION_PROTOCOL.md`.

- Old attempt, nonce, coordinator epoch, or SHA: record as `STALE`; do not mutate current state.
- Repeated event ID: record as `DUPLICATE`; perform no external side effect.
- No explicit status: keep the current coordinator state and ask for status.
- Silence: never completion, failure, or cancellation.
- `BLOCKED`: use only when evidence names the blocker.
- `CANCELLED`: use only when the user or coordinator intentionally stops work.

## Acceptance Rules

- Inspect output, diff scope, verification, risks, and exact commit SHA before acceptance.
- Require current gate evidence; do not reuse a verdict from an older SHA.
- `DONE_WITH_CONCERNS` may be accepted only with the concerns preserved and an allowed gate verdict.
- Do not deliver while a required role is `TODO` or `IN_PROGRESS`, a gate is `PENDING`, `FAIL`, or `BLOCKED`, or coordinator state is not `ACCEPTED`.
- Do not hide `BLOCKED`, `NEEDS_CONTEXT`, `CANCELLED`, stale evidence, or waived checks in final delivery.
