# Filled Task Dispatch Example

```text
You are acting as: Technical Engineer
Project: Example Analytics App
Repository: /path/to/example-analytics
Thread role boundary: Implement only the scoped export retry fix.
Task ID: TASK-2026-001
Coordinator thread ID: thread-coordinator-123
This role thread ID: thread-engineer-456

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
- On completion, send a callback to the coordinator thread if thread messaging tools are available.
- If callback is unavailable or fails, include `CALLBACK_FAILED: <REASON>` in your final reply.

Stop and report if:
- the task requires secrets, paid access, external login, production deployment, destructive git operations, or large downloads;
- the requested files already have conflicting changes;
- the acceptance criteria are unclear enough that continuing would require guessing;
- you need to modify files outside the editable scope.

Reply using this format:
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Summary:
Changed files / Files inspected:
Verification run:
Risks / concerns:
Recommended next role:
```
