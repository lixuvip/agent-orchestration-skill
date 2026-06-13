# Filled Role Reply Example

```text
Status: DONE_WITH_CONCERNS

Summary:
- Added `--retry-once` handling to the CSV export command.
- Covered normal success, retry success, and retry failure paths.

Changed files / Files inspected:
- src/exporter/cli.py: added the flag and passed retry intent to the exporter.
- src/exporter/client.py: wrapped transient export errors in one bounded retry.
- tests/exporter/test_retry.py: added regression coverage for the retry paths.

Verification run:
- pytest tests/exporter: PASS
  Result / reason: 18 tests passed.
- python -m example_export --help: PASS
  Result / reason: help output includes `--retry-once`.

Risks / concerns:
- Manual verification against the production export service was NOT RUN because it requires external credentials.

Recommended next role:
- QA Tester
```
