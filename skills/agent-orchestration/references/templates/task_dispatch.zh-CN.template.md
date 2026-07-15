# 中文任务分发模板

将本模板复制到角色线程，替换全部占位符后发送。同一份有效派发身份必须记录在协调者任务板中。

```text
你当前扮演的角色：<ROLE_NAME>
编排模式：<LITE | STANDARD | DURABLE>
项目：<PROJECT_NAME>
仓库：<REPO_PATH>
角色边界：<ROLE_BOUNDARY>
分支 / 工作区：<BRANCH_OR_WORKTREE_OR_NONE>
合并策略：<SUMMARIZE_ONLY | COMMIT_ALLOWED | PUSH_BRANCH_ALLOWED | MERGE_REQUIRES_CONFIRMATION | PR_ALLOWED>
期望思考级别：<INHERIT | minimal | low | medium | high | xhigh | max | ultra | 用户指定>
实际思考级别：<精确值 | INHERITED | UNSUPPORTED>
选择理由：<为什么这是最适合级别、是否使用同等适配平局规则或为何需要回退>
模型覆盖：<NONE | 用户明确指定的模型>

当前有效派发身份：
- Protocol version: ORCHESTRATION_EVENT_V1
- Goal ID: <GOAL_ID>
- Task ID: <TASK_ID>
- Attempt: <正整数>
- Dispatch nonce: <本次尝试的唯一随机值>
- Coordinator epoch: <当前协调者周期标识>
- Coordinator thread ID: <COORDINATOR_THREAD_ID>
- Role thread ID: <ROLE_THREAD_ID_OR_UNKNOWN>
- Base SHA: <精确_SHA | NONE>
- Expected head SHA: <精确_SHA | UNKNOWN | NONE>

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
- 原样带回 Goal ID、Task ID、Attempt、Dispatch nonce 和 Coordinator epoch。
- 生成唯一 Event ID，并使用含时区的 ISO-8601 Event timestamp。
- 报告实际检查的精确 SHA，不能用分支名或 `latest` 代替。
- 角色只报告执行状态和证据，只有协调者可以验收交付。
- 完成后，如有线程消息工具，请向协调者线程发送回调。
- 无法回调或回调失败时，在最终回复中包含 `CALLBACK_FAILED: <REASON>`。
- 角色完成回调使用 `coordinator_state: IN_REVIEW`，表示请求验收，不表示已经验收。

遇到以下情况请停止并报告：
- 任务需要密钥、付费账号、外部登录、生产部署、破坏性 git 操作或大文件下载；
- 请求修改的文件已有冲突性改动；
- 验收标准不清楚，继续做需要猜测；
- 必须修改可编辑范围之外的文件；
- 分支 HEAD 已偏离派发预期，且协调者尚未刷新预期 SHA。

请使用 `role_reply.zh-CN.template.md` 回复，并包含完整的 `ORCHESTRATION_EVENT_V1` 信封。
```
