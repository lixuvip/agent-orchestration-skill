# Orchestration Event Protocol

Use this reference for every asynchronous dispatch, callback, status request, QA or review gate, heartbeat observation, and coordinator acceptance decision.

The canonical wire format is `ORCHESTRATION_EVENT_V1`. Human-readable prose may accompany an event, but it must not replace the versioned envelope when stale or duplicate messages could affect delivery.

## Three Independent Dimensions

Do not collapse these into one `Status` field.

| Dimension | Values | Authority |
| --- | --- | --- |
| Role execution | `TODO`, `IN_PROGRESS`, `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`, `CANCELLED` | The role reports its own work state. |
| Gate verdict | `PENDING`, `PASS`, `FAIL`, `BLOCKED`, `WAIVED`, `NOT_APPLICABLE` | QA, reviewer, or the coordinator records evidence quality. |
| Coordinator state | `TODO`, `DISPATCHED`, `IN_PROGRESS`, `IN_REVIEW`, `RETURNED`, `ACCEPTED`, `ESCALATED`, `CANCELLED` | Only the coordinator owns acceptance and routing. |

`DONE` means “ready for coordinator inspection.” It never means “accepted,” “merged,” or “delivered.”

## Required Event Envelope

```json
{
  "protocol_version": "ORCHESTRATION_EVENT_V1",
  "goal_id": "GOAL-001",
  "task_id": "TASK-001",
  "attempt": 2,
  "dispatch_nonce": "dispatch-2-abc",
  "coordinator_epoch": "coordinator-epoch-7",
  "event_id": "event-task-001-2-done",
  "event_timestamp": "2026-07-10T10:00:00+08:00",
  "role": "QA Tester",
  "coordinator_thread_id": "thread-coordinator",
  "role_thread_id": "thread-qa",
  "base_sha": "0123456789abcdef0123456789abcdef01234567",
  "expected_head_sha": "1111111111111111111111111111111111111111",
  "observed_head_sha": "1111111111111111111111111111111111111111",
  "execution_status": "DONE",
  "gate_verdict": "PASS",
  "coordinator_state": "IN_REVIEW"
}
```

Use `NONE` for all three artifact fields when no Git repository applies and `UNKNOWN` only while an artifact-producing role has not created its candidate SHA. A Git-backed event cannot be accepted with `NONE`, and no event can be accepted with `UNKNOWN` or a mismatched artifact identity.

## Dispatch Identity

Every dispatch must mint and record:

- `attempt`: positive integer incremented when work is returned or redispatched;
- `dispatch_nonce`: unique value for this task attempt;
- `coordinator_epoch`: unique value for the active coordinator run or lease;
- `expected_head_sha`: exact artifact SHA the role is expected to inspect, or `UNKNOWN` only for an artifact-producing role before its candidate commit exists.

A callback is `STALE` if any active expectation differs: goal, task, attempt, nonce, epoch, expected SHA, or, when a concrete SHA was dispatched, observed SHA. An artifact-producing role dispatched with `UNKNOWN` may report its newly created concrete SHA; the coordinator must record that candidate and use the concrete SHA for every downstream gate. Do not mutate current task state from any other stale callback.

An already processed `event_id` is `DUPLICATE`. A duplicate is a successful no-op: do not re-comment, re-route, re-merge, or re-notify.

Malformed or unsupported events are `REJECTED`. Ask the role for a corrected callback; do not infer missing identity fields.

## Commit-Pinned Gates

- Engineering completion identifies the candidate `expected_head_sha`.
- QA and review must report the same SHA as `observed_head_sha`.
- Any subsequent code commit invalidates earlier QA and review verdicts for delivery.
- Documentation-only changes may be waived only when the coordinator records the scope and uses `WAIVED`; never silently reuse old evidence.
- A branch name, worktree path, or latest commit at callback time is not a stable substitute for an exact SHA.

## Accepted Delivery Predicate

Delivery is accepted only when all are true:

1. `coordinator_state` is `ACCEPTED`;
2. `execution_status` is `DONE` or `DONE_WITH_CONCERNS`;
3. `gate_verdict` is `PASS`, `WAIVED`, or `NOT_APPLICABLE`;
4. `expected_head_sha` is a concrete commit SHA, or all artifact fields are `NONE` because no Git repository applies;
5. `observed_head_sha` equals `expected_head_sha`;
6. the envelope matches the active dispatch identity.

`DONE + FAIL`, `DONE + PENDING`, or `DONE + IN_REVIEW` is not accepted delivery. `CANCELLED` is terminal for monitoring but is never delivery.

## Helper

Validate a callback and compare it with the active dispatch:

```bash
python3 scripts/orchestration_event.py \
  --event-file callback.json \
  --expectation-file active-dispatch.json
```

Add `--seen-event-id <EVENT_ID>` for deduplication and `--require-accepted-delivery` at the final delivery gate.

The helper prints one machine-readable result:

- `EVENT_ACCEPTED` — current valid event;
- `EVENT_DUPLICATE` — already processed no-op;
- `EVENT_STALE` — valid envelope for an inactive dispatch or SHA;
- `EVENT_NOT_DELIVERABLE` — current event has not passed the delivery predicate;
- `EVENT_REJECTED: ...` — malformed or unsupported event.

## Coordinator Handling Order

1. Validate the envelope.
2. Deduplicate by `event_id`.
3. Compare dispatch identity and SHA with the active expectation.
4. Record role execution status and gate verdict without rewriting them.
5. Move the coordinator state independently.
6. Run coordinator inspection and required gates.
7. Emit a new coordinator-owned event when returning, accepting, escalating, or cancelling.
