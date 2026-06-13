# Task Dispatch Template

将本模板复制到目标角色对话中，替换占位符后发送。

```text
You are acting as: <ROLE_NAME>
Project: <PROJECT_NAME>
Repository: <REPO_PATH>
Thread role boundary: <ROLE_BOUNDARY>
Task ID: <TASK_ID>
Coordinator thread ID: <COORDINATOR_THREAD_ID>
This role thread ID: <ROLE_THREAD_ID_OR_UNKNOWN>

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
- On completion, send a callback to the coordinator thread if thread messaging tools are available.
- If callback is unavailable or fails, include `CALLBACK_FAILED: <REASON>` in your final reply.
- Callback format:
  Coordinator callback:
  Task ID: <TASK_ID>
  Role: <ROLE_NAME>
  Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
  Summary:
  - <ONE_TO_THREE_BULLETS>
  Verification:
  - <COMMAND_OR_CHECK>: <RESULT>
  Risks:
  - <NONE_OR_RISK>

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
