# 中文任务分发模板

将本模板复制到目标角色对话中，替换占位符后发送。

```text
你当前扮演的角色：<ROLE_NAME>
项目：<PROJECT_NAME>
仓库：<REPO_PATH>
角色边界：<ROLE_BOUNDARY>
任务 ID：<TASK_ID>
协调者线程 ID：<COORDINATOR_THREAD_ID>
当前角色线程 ID：<ROLE_THREAD_ID_OR_UNKNOWN>

目标：
<ONE_SENTENCE_GOAL>

上下文：
<RELEVANT_BACKGROUND>

验收标准：
- <CRITERION_1>
- <CRITERION_2>
- <CRITERION_3>

可编辑范围：
- <EDITABLE_FILE_OR_MODULE_1>
- <EDITABLE_FILE_OR_MODULE_2>

只读范围：
- <READ_ONLY_FILE_OR_MODULE_1>
- <READ_ONLY_FILE_OR_MODULE_2>

禁止事项：
- <FORBIDDEN_ITEM_1>
- <FORBIDDEN_ITEM_2>

验证要求：
- <VERIFY_COMMAND_OR_MANUAL_CHECK_1>
- <VERIFY_COMMAND_OR_MANUAL_CHECK_2>

回调：
- 完成后，如果有线程消息工具，请向协调者线程发送回调。
- 如果无法回调或回调失败，请在最终回复中包含 `CALLBACK_FAILED: <REASON>`。
- 回调格式：
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

遇到以下情况请停止并报告：
- 任务需要密钥、付费账号、外部登录、生产部署、破坏性 git 操作或大文件下载；
- 请求修改的文件已有冲突性改动；
- 验收标准不清楚，继续做需要猜测；
- 你需要修改可编辑范围之外的文件。

请使用以下格式回复：
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Summary:
Changed files / Files inspected:
Verification run:
Risks / concerns:
Recommended next role:
```
