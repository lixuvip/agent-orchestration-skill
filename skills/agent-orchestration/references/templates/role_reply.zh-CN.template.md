# 中文角色回复模板

所有角色使用此格式。文字摘要供人阅读；事件信封用于状态流转和去重，是权威输入。

```text
Execution status: IN_PROGRESS | DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT | CANCELLED
Gate verdict: PENDING | PASS | FAIL | BLOCKED | WAIVED | NOT_APPLICABLE

摘要：
- <完成或检查了什么>

修改文件 / 检查文件：
- <PATH>: <为什么修改或检查它>

已运行验证：
- <COMMAND_OR_CHECK>: PASS | FAIL | NOT RUN
  结果 / 原因：<DETAIL>

风险 / 顾虑：
- <无，或具体风险>

分支 / 工作区：
- <BRANCH_OR_WORKTREE_OR_NONE>

Commit / 实际检查的 HEAD SHA：
- <精确_SHA | NONE>

协调者回调：
- 是否发送：<YES | NO | NOT_AVAILABLE>
- 目标 / 原因：<COORDINATOR_THREAD_ID_OR_REASON>

建议下一角色：
- <Coordinator | Product Designer | Technical Engineer | QA Tester | Code Reviewer | Release / Docs>

ORCHESTRATION_EVENT_V1:
{
  "protocol_version": "ORCHESTRATION_EVENT_V1",
  "goal_id": "<GOAL_ID>",
  "task_id": "<TASK_ID>",
  "attempt": <正整数>,
  "dispatch_nonce": "<DISPATCH_NONCE>",
  "coordinator_epoch": "<COORDINATOR_EPOCH>",
  "event_id": "<唯一_EVENT_ID>",
  "event_timestamp": "<含时区的_ISO_8601_时间>",
  "role": "<ROLE_NAME>",
  "coordinator_thread_id": "<COORDINATOR_THREAD_ID>",
  "role_thread_id": "<ROLE_THREAD_ID>",
  "base_sha": "<精确_SHA | NONE>",
  "expected_head_sha": "<精确_SHA | NONE>",
  "observed_head_sha": "<精确_SHA | NONE>",
  "execution_status": "<EXECUTION_STATUS>",
  "gate_verdict": "<GATE_VERDICT>",
  "coordinator_state": "<IN_PROGRESS | IN_REVIEW | ESCALATED | CANCELLED>"
}
```

- `NOT RUN` 必须说明原因。
- 必需检查失败时使用 `FAIL` 或 `BLOCKED`，不能写 `PASS`。
- 存在风险或覆盖缺口时使用 `DONE_WITH_CONCERNS`。
- 角色完成后通常请求 `IN_REVIEW`，不能自行声称 `ACCEPTED`。
- 原样保留派发身份；角色不能自行递增 `attempt` 或生成协调者 epoch。
