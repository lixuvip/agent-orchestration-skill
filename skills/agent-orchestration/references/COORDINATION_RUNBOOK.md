# Coordination Runbook

Canonical Standard/Durable coordination contract. Lite work does not load this file. Load only one language version.

## Non-Negotiable Invariants

- One owner and explicit editable/read-only/out-of-scope boundaries per task.
- Isolate or serialize overlapping edits; routing never makes shared-file parallel writes safe.
- Never infer completion from silence or confidence. Record commands actually run and their results.
- Role `DONE` requests inspection; only coordinator `ACCEPTED` is delivery.
- QA/review evidence is valid only for the exact inspected artifact SHA.
- Duplicate or stale callbacks are no-ops.
- Merge, push, deploy, publish, destructive changes, secrets, spending, or scope expansion require the authority stated by the user/project.

## Intake And Route

Ask only when the answer materially changes execution surface, write authority, user-visible thread creation, callback/automation behavior, or merge/push permission. Otherwise infer the narrowest safe route.

| Mode | Minimum shape | Runtime |
| --- | --- | --- |
| Lite | One-shot current-context work; no async boundary or recurrence. | No task board, event envelope, heartbeat, cron, or memory. |
| Standard | Multiple roles, async/user-visible threads, cross-repo handoff, formal QA/review/release gate, or finite long work. | Task ownership + event protocol; heartbeat only when async/long. |
| Durable | Recurring work or recovery across ticks. | Standard + `PROJECT_AUTOPILOT.md`. |

Use `scripts/route_orchestration.py` when the route is not obvious. A requested lighter mode cannot bypass the minimum; an explicit heavier mode is allowed. External-model review/research is a modifier, not a route upgrade by itself.

## Standard Transaction

1. Record user goal, acceptance criteria, authority, relevant project instructions, and execution surface.
2. Split only independent work. Assign one owner and isolation boundary per task.
3. For every async dispatch, mint goal/task ID, attempt, dispatch nonce, coordinator epoch, base artifact, and expected artifact.
4. Send `templates/task_dispatch.template.md`; record thread, branch/worktree, callback, and merge policy on `TASK_BOARD.template.md` when more than one task is active.
5. Use a heartbeat only for async/long work that may finish while the coordinator is inactive.
6. Validate incoming callbacks before changing state. Request status once when explicit state or verification is missing.
7. Move terminal role work to coordinator `IN_REVIEW`; inspect scope, diff, verification, risks, branch, and exact artifact.
8. Dispatch QA/review against that exact artifact. A code-changing retry creates a new attempt/nonce and invalidates old gate evidence.
9. Return, escalate, cancel, or accept. Run `templates/merge_readiness.template.md` before any claimed merge/push readiness.
10. Deliver only the coordinator-accepted result with real verification and unresolved risks.

## State And Gate Model

Keep three dimensions independent:

| Dimension | Values | Owner |
| --- | --- | --- |
| Role execution | `TODO`, `IN_PROGRESS`, `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`, `CANCELLED` | Role |
| Gate verdict | `PENDING`, `PASS`, `FAIL`, `BLOCKED`, `WAIVED`, `NOT_APPLICABLE` | QA/reviewer/coordinator |
| Coordinator | `TODO`, `DISPATCHED`, `IN_PROGRESS`, `IN_REVIEW`, `RETURNED`, `ACCEPTED`, `ESCALATED`, `CANCELLED` | Coordinator |

Normal flow:

```text
TODO -> DISPATCHED -> IN_PROGRESS -> IN_REVIEW -> ACCEPTED
                                      |-> RETURNED -> new attempt
                                      |-> ESCALATED | CANCELLED
```

`DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`, and `CANCELLED` are terminal for role monitoring, not automatic success.

## Versioned Callback Contract

Async messages use `ORCHESTRATION_EVENT_V1`. The complete schema lives in `templates/coordinator_callback.template.md`; human summaries cannot override it.

Identity fields:

- goal/task ID, positive attempt, dispatch nonce, coordinator epoch;
- unique event ID and timezone-qualified timestamp;
- role and coordinator/role thread IDs;
- base, expected, and observed artifact identity;
- role execution status, gate verdict, and coordinator state.

Use `NONE` for all artifact fields when Git does not apply. Use `UNKNOWN` only before an artifact-producing role creates its candidate.

Process in this order:

1. Validate the envelope with `scripts/orchestration_event.py`.
2. Deduplicate `event_id`; `DUPLICATE` is a successful no-op.
3. Compare active goal/task, attempt, nonce, epoch, and expected/observed artifact; mismatch is `STALE` and cannot mutate current state.
4. Record role state and gate verdict without rewriting them.
5. Move coordinator state independently.

Accepted delivery requires coordinator `ACCEPTED`, completed role status, a `PASS`/`WAIVED`/`NOT_APPLICABLE` gate, matching current artifact identity, and the active dispatch identity. `DONE + FAIL`, `DONE + PENDING`, or `DONE + IN_REVIEW` is not delivery.

## Commit-Pinned Gates

- Engineering completion establishes the candidate SHA.
- QA/review report the same SHA as observed.
- Any later code commit invalidates those verdicts.
- Documentation-only changes may be explicitly waived with a recorded reason; never reuse evidence silently.
- Branch name, worktree path, or “latest” is not an artifact identity.

Use `templates/qa_report.template.md`, `templates/review_findings.template.md`, and `templates/merge_readiness.template.md`.

## Workflow Shapes

| Shape | Order |
| --- | --- |
| Sequential gate | acceptance criteria -> engineering -> QA -> review -> coordinator acceptance |
| Parallel preparation | product/QA/research read-only preparation -> coordinator synthesis -> one engineering task |
| Emergency fix | narrow engineering fix -> affected regression -> coordinator acceptance; no opportunistic refactor |
| Cross-repository | isolated owner per repository -> explicit contract summary -> per-repo verification -> coordinator synthesis |
| Release readiness | release/docs + QA + review -> exact artifact gates -> permission check -> readiness report |

## Heartbeat Monitoring

Heartbeat is a finite Standard monitor, not project Autopilot.

- Track current dispatch identities and processed event IDs.
- Acquire a fenced lease for every recurring tick with `scripts/automation_lease.py`; `LEASE_ALREADY_HELD`, `LEASE_BUSY`, expired, or replaced owners perform no side effect.
- Send at most one status request per task-attempt-nonce.
- Lifecycle is `ACTIVE -> DRAINING -> CLOSED`: after all roles are terminal, stop requests, post one final summary, request pause/delete, and wait for tool confirmation.
- Use `scripts/heartbeat_lifecycle.py`; final heartbeat output moves completed work to `IN_REVIEW`, never `ACCEPTED`.

Use `templates/monitoring_heartbeat.template.md`. If automation tools are absent, poll manually from the task board.

## Tool And Delivery Rules

- User-visible role conversations require explicit user intent; use thread tools when available.
- Internal parallel work uses subagents only when explicitly requested and file ownership does not overlap.
- If callbacks are unavailable, require `CALLBACK_FAILED: <reason>` and inspect the role result manually.
- Final delivery states work done, participants, actual verification, branch/commit/files, waivers, and remaining risk.
- Keep project-specific service/API contracts in the target repository, not in this generic skill.

For recurring progress beyond a finite heartbeat, load `PROJECT_AUTOPILOT.md`. For `agy` work, load only the matching review or research pack.
