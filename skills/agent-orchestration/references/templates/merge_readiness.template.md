# Merge Readiness Template

Use this before merging, pushing, publishing, or telling the user a branch is ready.

```text
Merge readiness for <TASK_ID>

Goal ID: <GOAL_ID>
Attempt: <ACTIVE_ATTEMPT>
Dispatch nonce: <ACTIVE_DISPATCH_NONCE>
Coordinator epoch: <ACTIVE_COORDINATOR_EPOCH>
Repository: <REPO_PATH>
Branch / worktree: <BRANCH_OR_WORKTREE>
Base branch: <BASE_BRANCH>
Target branch: <TARGET_BRANCH>
Expected head SHA: <EXPECTED_HEAD_SHA>
Observed head SHA: <OBSERVED_HEAD_SHA>

Working tree:
- Clean: <YES_OR_NO>
- Untracked files: <NONE_OR_LIST>
- Uncommitted changes: <NONE_OR_LIST>

Scope:
- Expected files changed:
- Unexpected files changed:
- Forbidden areas touched: <YES_OR_NO>

Gates pinned to observed head SHA:
- Engineering verification: PASS | FAIL | BLOCKED | WAIVED | NOT_APPLICABLE
- QA: PASS | FAIL | BLOCKED | WAIVED | NOT_APPLICABLE
- Code review: PASS | FAIL | BLOCKED | WAIVED | NOT_APPLICABLE
- Evidence SHA matches: <YES_OR_NO>

Conflicts:
- Up to date with base: <YES_OR_NO>
- Merge conflicts expected: <YES_OR_NO_OR_UNKNOWN>

Risks and waivers:
- <NONE_OR_RISK_OR_EXPLICIT_WAIVER_REASON>

Push permission:
- <NOT_REQUESTED | COMMIT_ONLY | PUSH_BRANCH | MERGE_TO_TARGET | CREATE_PR>

Coordinator state:
- <IN_REVIEW | RETURNED | ACCEPTED | ESCALATED | CANCELLED>

Decision:
- <READY | NEEDS_FIX | NEEDS_USER_CONFIRMATION | BLOCKED>
```

`READY` requires matching exact SHAs, required passing or explicitly waived gates, and coordinator state `ACCEPTED`. A branch name alone is insufficient evidence.
