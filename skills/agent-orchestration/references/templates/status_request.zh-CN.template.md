# 中文状态请求模板

当角色线程静默、表达不清、状态陈旧或缺少验证结果时使用。

```text
状态请求：<TASK_ID>
协调者线程 ID：<COORDINATOR_THREAD_ID>
角色线程 ID：<ROLE_THREAD_ID_OR_UNKNOWN>

请回复一个当前状态，并附上证据。请回复一个：
- IN_PROGRESS
- DONE
- DONE_WITH_CONCERNS
- BLOCKED
- NEEDS_CONTEXT

必填信息：
- 当前摘要：
- 修改文件 / 检查文件：
- 已运行验证：
- 风险 / 阻塞：
- 预计下一步：
```

