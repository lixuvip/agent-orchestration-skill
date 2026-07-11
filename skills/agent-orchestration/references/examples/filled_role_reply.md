# Filled Role Reply Example

```text
Execution status: DONE_WITH_CONCERNS
Gate verdict: PENDING

Summary:
- Added `--retry-once` handling and regression coverage for normal success, retry success, and retry failure.

Changed files / Files inspected:
- src/exporter/cli.py: added the flag and passed retry intent.
- src/exporter/client.py: added one bounded retry for transient failures.
- tests/exporter/test_retry.py: covered the three retry paths.

Verification:
- pytest tests/exporter: PASS — 18 tests passed.
- python -m example_export --help: PASS — help includes `--retry-once`.

Artifact / branch / worktree:
- 1111111111111111111111111111111111111111; codex/export-retry / /worktrees/export-retry

Risks / concerns:
- Production-service verification was not run because it requires external credentials.

Callback:
- SENT_TO_COORDINATOR

Recommended next action:
- QA
```

For async work, send a separate `coordinator_callback.template.md` event with the same dispatch identity and observed SHA. The human reply does not duplicate that JSON.
