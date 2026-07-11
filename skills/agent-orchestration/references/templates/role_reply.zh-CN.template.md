# 中文角色回复模板

供人阅读的角色结果。异步 Standard/Durable 使用 `coordinator_callback.zh-CN.template.md` 单独发送机器事件，不在这里重复 JSON。

```text
Execution status: IN_PROGRESS | DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT | CANCELLED
Gate verdict: PENDING | PASS | FAIL | BLOCKED | WAIVED | NOT_APPLICABLE

摘要：
- <完成或检查了什么>

修改文件 / 检查文件：
- <PATH>: <原因>

验证：
- <COMMAND_OR_CHECK>: PASS | FAIL | NOT RUN — <结果或原因>

产物 / 分支 / 工作区：
- <OBSERVED_SHA_OR_NONE>; <BRANCH_OR_WORKTREE_OR_NONE>

风险 / 顾虑：
- <无或具体风险>

回调：
- <SENT_TO_COORDINATOR | NOT_AVAILABLE: REASON | NOT_APPLICABLE>

建议下一步：
- <COORDINATOR_REVIEW | QA | REVIEW | FIX | ESCALATE | NONE>
```

`NOT RUN` 必须说明原因。必需检查失败使用 `FAIL/BLOCKED`；覆盖缺口使用 `DONE_WITH_CONCERNS`。角色不能声称协调者 `ACCEPTED`。
