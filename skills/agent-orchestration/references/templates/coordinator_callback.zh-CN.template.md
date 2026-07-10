# 中文协调者回调模板

角色线程直接回调协调者时使用。派发身份必须原样带回，并附上 `role_reply.zh-CN.template.md` 中的角色事件。

```text
Coordinator callback:
Goal ID: <GOAL_ID>
Task ID: <TASK_ID>
Attempt: <正整数>
Dispatch nonce: <DISPATCH_NONCE>
Coordinator epoch: <COORDINATOR_EPOCH>
Event ID: <唯一_EVENT_ID>
Event timestamp: <含时区的_ISO_8601_时间>
角色：<ROLE_NAME>
角色线程 ID：<ROLE_THREAD_ID>
协调者线程 ID：<COORDINATOR_THREAD_ID>
分支 / 工作区：<BRANCH_OR_WORKTREE_OR_NONE>
Base SHA: <精确_SHA | NONE>
Expected head SHA: <精确_SHA | NONE>
Observed head SHA: <精确_SHA | NONE>
Execution status: IN_PROGRESS | DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT | CANCELLED
Gate verdict: PENDING | PASS | FAIL | BLOCKED | WAIVED | NOT_APPLICABLE
请求的 coordinator state: IN_PROGRESS | IN_REVIEW | ESCALATED | CANCELLED

摘要：
- <一到三条要点>

修改文件 / 检查文件：
- <PATH>: <为什么修改或检查>

验证结果：
- <COMMAND_OR_CHECK>: PASS | FAIL | NOT RUN
  结果 / 原因：<DETAIL>

风险：
- <无或具体风险>

建议协调者下一步：
- <REVIEW_DIFF | SEND_TO_QA | SEND_TO_REVIEW | REQUEST_FIX | RUN_MERGE_READINESS | ESCALATE_TO_USER>

ORCHESTRATION_EVENT_V1:
<复制角色回复里的完整_JSON_事件>
```

回调只能请求 `IN_REVIEW`，不能授予 `ACCEPTED`。协调者负责校验、去重、拒绝过期身份，并另行产生权威状态变更。
