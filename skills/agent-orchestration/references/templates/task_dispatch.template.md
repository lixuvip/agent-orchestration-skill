# Task Dispatch Template

Copy this template into the role thread and replace every placeholder. The active dispatch identity must also be recorded on the coordinator task board.

```text
You are acting as: <ROLE_NAME>
Orchestration mode: <LITE | STANDARD | DURABLE>
Project: <PROJECT_NAME>
Repository: <REPO_PATH>
Thread role boundary: <ROLE_BOUNDARY>
Branch / worktree: <BRANCH_OR_WORKTREE_OR_NONE>
Merge policy: <SUMMARIZE_ONLY | COMMIT_ALLOWED | PUSH_BRANCH_ALLOWED | MERGE_REQUIRES_CONFIRMATION | PR_ALLOWED>

Active dispatch identity:
- Protocol version: ORCHESTRATION_EVENT_V1
- Goal ID: <GOAL_ID>
- Task ID: <TASK_ID>
- Attempt: <POSITIVE_INTEGER>
- Dispatch nonce: <UNIQUE_NONCE_FOR_THIS_ATTEMPT>
- Coordinator epoch: <ACTIVE_COORDINATOR_EPOCH>
- Coordinator thread ID: <COORDINATOR_THREAD_ID>
- Role thread ID: <ROLE_THREAD_ID_OR_UNKNOWN>
- Base SHA: <EXACT_SHA | NONE>
- Expected head SHA: <EXACT_SHA | UNKNOWN | NONE>

Goal:
<ONE_SENTENCE_GOAL>

Context:
<RELEVANT_BACKGROUND>

Acceptance criteria:
- <CRITERION_1>
- <CRITERION_2>
- <CRITERION_3>

Editable scope:
- <EDITABLE_FILE_OR_MODULE_1>
- <EDITABLE_FILE_OR_MODULE_2>

Read-only scope:
- <READ_ONLY_FILE_OR_MODULE_1>
- <READ_ONLY_FILE_OR_MODULE_2>

Out of scope:
- <FORBIDDEN_ITEM_1>
- <FORBIDDEN_ITEM_2>

Verification:
- <VERIFY_COMMAND_OR_MANUAL_CHECK_1>
- <VERIFY_COMMAND_OR_MANUAL_CHECK_2>

Callback:
- Reply with the same goal ID, task ID, attempt, dispatch nonce, and coordinator epoch.
- Generate a unique event ID and a timezone-qualified ISO-8601 event timestamp.
- Report the exact observed head SHA. Do not substitute a branch name or `latest`.
- A role reports execution state and evidence; only the coordinator can accept delivery.
- On completion, send the callback to the coordinator thread when thread messaging tools are available.
- If callback is unavailable or fails, include `CALLBACK_FAILED: <REASON>` in the final reply.
- Use `coordinator_state: IN_REVIEW` for a completed role callback; this requests inspection and does not claim acceptance.

Stop and report if:
- the task requires secrets, paid access, external login, production deployment, destructive git operations, or large downloads;
- requested files already have conflicting changes;
- acceptance criteria are unclear enough that continuing would require guessing;
- files outside editable scope must be modified;
- the branch head no longer matches the dispatch expectation and the coordinator has not refreshed it.

Reply using `role_reply.template.md` and include one complete `ORCHESTRATION_EVENT_V1` envelope.
```
