# Merge Readiness Template

Use this before merging, pushing, publishing, or telling the user a branch is ready.

```text
Merge readiness for <TASK_ID>

Repository: <REPO_PATH>
Branch / worktree: <BRANCH_OR_WORKTREE>
Base branch: <BASE_BRANCH>
Target branch: <TARGET_BRANCH>

Working tree:
- Clean: <YES_OR_NO>
- Untracked files: <NONE_OR_LIST>
- Uncommitted changes: <NONE_OR_LIST>

Scope:
- Expected files changed:
- Unexpected files changed:
- Forbidden areas touched: <YES_OR_NO>

Tests:
- <COMMAND_OR_CHECK>: PASS | FAIL | NOT RUN
  Result / reason: <DETAIL>

Conflicts:
- Up to date with base: <YES_OR_NO>
- Merge conflicts expected: <YES_OR_NO_OR_UNKNOWN>

Risks:
- <NONE_OR_RISK>

Push permission:
- <NOT_REQUESTED | COMMIT_ONLY | PUSH_BRANCH | MERGE_TO_TARGET | CREATE_PR>

Decision:
- <READY | NEEDS_FIX | NEEDS_USER_CONFIRMATION | BLOCKED>
```

