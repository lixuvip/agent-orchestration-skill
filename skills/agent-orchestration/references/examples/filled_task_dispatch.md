# Filled Task Dispatch Example

```text
You are acting as: Technical Engineer
Project: Example Analytics App
Repository: /path/to/example-analytics
Thread role boundary: Implement only the scoped export retry fix.
Branch / worktree: codex/export-retry / /worktrees/export-retry
Merge policy: COMMIT_ALLOWED

Active dispatch identity:
- Protocol version: ORCHESTRATION_EVENT_V1
- Goal ID: GOAL-2026-001
- Task ID: TASK-2026-001
- Attempt: 1
- Dispatch nonce: dispatch-task-2026-001-a1-7f42
- Coordinator epoch: coordinator-2026-07-10-01
- Coordinator thread ID: thread-coordinator-123
- Role thread ID: thread-engineer-456
- Base SHA: 0123456789abcdef0123456789abcdef01234567
- Expected head SHA: UNKNOWN

Goal:
Add a bounded retry option to the CSV export command.

Context:
The export command occasionally fails on transient network errors. Product has approved one retry with no new dependency.

Acceptance criteria:
- CLI accepts `--retry-once`.
- Existing export behavior is unchanged when the flag is absent.
- Unit tests cover success, retry success, and retry failure.

Editable scope:
- src/exporter/
- tests/exporter/

Read-only scope:
- README.md
- docs/

Out of scope:
- New third-party dependencies.
- Changes to authentication, billing, or deployment.

Verification:
- pytest tests/exporter
- python -m example_export --help

Callback:
- Copy the active identity exactly and generate a unique event ID.
- Report the concrete candidate commit as observed head SHA.
- Use coordinator state `IN_REVIEW`; the coordinator will separately accept or return it.
- Send the callback to thread-coordinator-123 when thread messaging is available.
- If callback is unavailable or fails, include `CALLBACK_FAILED: <REASON>`.

Stop and report if:
- the task requires secrets, paid access, external login, production deployment, destructive git operations, or large downloads;
- requested files already have conflicting changes;
- acceptance criteria are unclear enough that continuing would require guessing;
- files outside editable scope must be modified;
- the checkout no longer descends from the dispatched base SHA.

Reply using role_reply.template.md with a complete ORCHESTRATION_EVENT_V1 envelope.
```
