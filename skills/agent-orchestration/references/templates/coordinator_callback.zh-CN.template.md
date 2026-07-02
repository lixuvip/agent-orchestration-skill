# 中文协调者回调模板

当角色线程需要直接回到协调者线程时使用。

```text
Coordinator callback:
任务 ID：<TASK_ID>
角色：<ROLE_NAME>
角色线程 ID：<ROLE_THREAD_ID_OR_UNKNOWN>
协调者线程 ID：<COORDINATOR_THREAD_ID>
分支 / 工作区：<BRANCH_OR_WORKTREE_OR_NONE>
Commit：<COMMIT_OR_NONE>
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT

摘要：
- <一到三条要点>

修改文件 / 检查文件：
- <PATH>: <为什么修改或检查>

验证结果：
- <COMMAND_OR_CHECK>: PASS | FAIL | NOT RUN
  结果 / 原因：<DETAIL>

风险：
- <无或具体风险>

协调者下一步：
- <ACCEPT | REVIEW_DIFF | SEND_TO_QA | SEND_TO_REVIEW | REQUEST_FIX | RUN_MERGE_READINESS | ESCALATE_TO_USER>
```

