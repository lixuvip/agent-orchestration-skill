# Task Board

Copy this file to `TASK_BOARD.md` when a coordinator needs durable multi-role state. Record role state, gate verdict, and coordinator state separately.

## State Dimensions

| Dimension | Values |
| --- | --- |
| Role execution | `TODO`, `IN_PROGRESS`, `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`, `CANCELLED` |
| Gate verdict | `PENDING`, `PASS`, `FAIL`, `BLOCKED`, `WAIVED`, `NOT_APPLICABLE` |
| Coordinator | `TODO`, `DISPATCHED`, `IN_PROGRESS`, `IN_REVIEW`, `RETURNED`, `ACCEPTED`, `ESCALATED`, `CANCELLED` |

## Active Dispatches

| Mode | Goal ID | Task ID | Role | Thread ID | Attempt | Dispatch nonce | Coordinator epoch | Expected SHA | Role state | Gate | Coordinator state | Next action |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `<STANDARD_OR_DURABLE>` | `<GOAL-001>` | `<TASK-001>` | `<ROLE>` | `<THREAD_ID>` | `<1>` | `<NONCE>` | `<EPOCH>` | `<SHA_OR_NONE>` | `TODO` | `PENDING` | `TODO` | `<NEXT_ACTION>` |

## Current Task Detail

### `<TASK-001>` — `<TITLE>`

| Field | Value |
| --- | --- |
| Goal | `<GOAL>` |
| Context | `<CONTEXT>` |
| Editable scope | `<EDITABLE_SCOPE>` |
| Read-only scope | `<READ_ONLY_SCOPE>` |
| Out of scope | `<OUT_OF_SCOPE>` |
| Acceptance criteria | `<ACCEPTANCE_CRITERIA>` |
| Verification | `<VERIFICATION>` |
| Base SHA | `<SHA_OR_NONE>` |
| Expected head SHA | `<SHA_OR_NONE>` |
| Last observed head SHA | `<SHA_OR_NONE>` |
| Current blocker | `<BLOCKER_OR_NONE>` |
| Explicit waivers | `<WAIVER_AND_REASON_OR_NONE>` |

## Processed Events

Keep this ledger append-only for the active goal. Duplicate event IDs are no-op acknowledgements.

| Event timestamp | Event ID | Task ID | Attempt | Observed SHA | Classification | Summary |
| --- | --- | --- | ---: | --- | --- | --- |
| `<ISO_8601>` | `<EVENT_ID>` | `<TASK_ID>` | `<1>` | `<SHA_OR_NONE>` | `ACCEPT | DUPLICATE | STALE | REJECTED` | `<SUMMARY>` |

## Transition Log

| Time | Task ID | Role execution | Gate verdict | Coordinator state | Evidence SHA | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| `<ISO_8601>` | `<TASK_ID>` | `<STATUS>` | `<VERDICT>` | `<STATE>` | `<SHA_OR_NONE>` | `<NEXT_ACTION>` |

Never overwrite current state from a stale callback. Never write `ACCEPTED` merely because a role reported `DONE`.
