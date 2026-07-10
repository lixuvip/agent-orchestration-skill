# Automation Concurrency And Lifecycle

Use this reference for any heartbeat or cron schedule that can overlap, retry after a crash, or run on more than one worker.

Prompt-level idempotency is not a concurrency primitive. Every tick that may mutate memory, post a message, or perform work must acquire a fenced lease first.

## Lease State

Keep lease files outside the target repository by default:

```text
${CODEX_HOME:-$HOME/.codex}/automations/<automation-id>/state
```

Use `scripts/automation_lease.py`. The helper uses an exclusive file lock, atomic state replacement, a random lease token, expiry, and a monotonically increasing fencing token.

```bash
python3 scripts/automation_lease.py acquire \
  --state-dir "$STATE_DIR" \
  --automation-id "$AUTOMATION_ID" \
  --owner-id "$TICK_ID" \
  --ttl-seconds 900
```

Interpret results:

- `LEASE_ACQUIRED`: this tick may proceed.
- `LEASE_ALREADY_HELD`: the same owner ID already has an active process; exit as a quiet no-op. The active token is not disclosed.
- `LEASE_BUSY`: another unexpired tick owns execution; exit as a quiet no-op.
- `LEASE_EXPIRED`: the owner waited too long and must stop; it cannot renew or write back.
- `LEASE_NOT_OWNER`: the token was replaced or does not match; stop without side effects.

## Tick Lease Protocol

1. Generate a unique tick ID and acquire the lease before reading mutable automation memory.
2. Only `LEASE_ACQUIRED` returns the new `lease_token`. Record it with the `fencing_token` and expiry in the in-memory tick context; do not persist or forward the token as a reusable capability.
3. Choose a TTL longer than the expected tick runtime plus cleanup margin, within the helper's one-day limit.
4. Renew before expiry if the tick is still legitimately running.
5. Run `verify` immediately before a user-facing message, external write, memory commit, callback, or cleanup action.
6. Write the fencing token into automation memory. Never overwrite memory whose stored fencing token is greater.
7. Release in a `finally`-equivalent cleanup path. A repeated release by the same owner/token is a successful no-op.

An expired tick can continue computing locally, but it must discard its result. Only the current lease holder may publish, write memory, or change automation lifecycle.

## Crash And Takeover

If a worker crashes, the lease becomes available only after expiry. The replacement holder receives a higher fencing token. The old holder cannot renew, release, or close the replacement lease even if it resumes later.

Use a local filesystem state directory. Do not place the lock on a filesystem whose advisory-lock or atomic-rename semantics are unknown.

## Heartbeat Lifecycle

Heartbeat state is monotonic:

```text
ACTIVE -> DRAINING -> CLOSED
```

| State | Meaning | Allowed action |
| --- | --- | --- |
| `ACTIVE` | At least one tracked role is non-terminal. | Poll, ingest current callbacks, and send deduplicated status requests. |
| `DRAINING` | All roles are terminal or shutdown has begun. | Stop new status requests, post one final summary, then request pause/delete and wait for confirmation. |
| `CLOSED` | Cleanup was confirmed. | No-op forever; do not post another summary or recreate the heartbeat. |

Terminal role states are `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`, and `CANCELLED`. They are terminal for monitoring only. The final heartbeat summary moves completed work to coordinator review; it never turns role `DONE` into coordinator `ACCEPTED`.

Use `scripts/heartbeat_lifecycle.py` to compute the next lifecycle action from current state, role states, final-summary status, and cleanup confirmation.

## Idempotency Keys

Automation memory must retain:

- processed orchestration `event_id` values;
- status-request key per task attempt and dispatch nonce;
- final-summary key per heartbeat generation;
- cleanup request ID and whether the automation tool confirmed pause/delete;
- latest lease fencing token.

If final-summary posting succeeds but the tick crashes before memory update, compare the destination's latest effective update before reposting. If cleanup fails, remain `DRAINING`, keep the summary marked posted, and retry only the cleanup action.

## Unsafe Failure Modes

- Do not run work when `LEASE_BUSY` merely because it appears read-only; duplicated reads can still trigger duplicated decisions or messages.
- Do not let a stale tick release or close a newer holder's automation.
- Do not mark `CLOSED` until the automation tool confirms cleanup.
- Do not recreate a closed heartbeat from an old callback.
- Do not use process-local locks for schedules that can run in separate processes.
