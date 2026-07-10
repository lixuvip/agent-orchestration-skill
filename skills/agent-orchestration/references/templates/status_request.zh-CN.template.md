# 中文状态请求模板

当角色线程静默、表达不清、状态陈旧或缺少验证结果时使用。

```text
状态请求：<TASK_ID>
Goal ID: <GOAL_ID>
Attempt: <当前有效_ATTEMPT>
Dispatch nonce: <当前有效_DISPATCH_NONCE>
Coordinator epoch: <当前有效_COORDINATOR_EPOCH>
Expected head SHA: <当前有效_EXPECTED_HEAD_SHA>
协调者线程 ID：<COORDINATOR_THREAD_ID>
角色线程 ID：<ROLE_THREAD_ID>

只回复这份当前有效派发。如果先前工作属于其他 attempt、nonce、epoch 或 SHA，请说明它已过期，不要声称当前任务已完成。

请回复一个执行状态并附上证据：
- IN_PROGRESS
- DONE
- DONE_WITH_CONCERNS
- BLOCKED
- NEEDS_CONTEXT
- CANCELLED

必填信息：
- 当前摘要：
- 修改文件 / 检查文件：
- 实际检查的 HEAD SHA：
- 已运行验证：
- Gate verdict：
- 风险 / 阻塞：
- 预计下一步：
- 按 `role_reply.zh-CN.template.md` 填写的完整 `ORCHESTRATION_EVENT_V1` 信封：
```
