# 中文协调者回调模板

机器权威的异步回调。原样保留派发身份并附简短摘要；JSON 外不重复身份字段。

```text
ORCHESTRATION_EVENT_V1:
{
  "protocol_version": "ORCHESTRATION_EVENT_V1",
  "goal_id": "<GOAL_ID>",
  "task_id": "<TASK_ID>",
  "attempt": <正整数>,
  "dispatch_nonce": "<DISPATCH_NONCE>",
  "coordinator_epoch": "<COORDINATOR_EPOCH>",
  "event_id": "<唯一_EVENT_ID>",
  "event_timestamp": "<含时区_ISO_8601>",
  "role": "<ROLE_NAME>",
  "coordinator_thread_id": "<COORDINATOR_THREAD_ID>",
  "role_thread_id": "<ROLE_THREAD_ID>",
  "base_sha": "<精确_SHA | NONE>",
  "expected_head_sha": "<精确_SHA | UNKNOWN | NONE>",
  "observed_head_sha": "<精确_SHA | NONE>",
  "execution_status": "<EXECUTION_STATUS>",
  "gate_verdict": "<GATE_VERDICT>",
  "coordinator_state": "<IN_PROGRESS | IN_REVIEW | ESCALATED | CANCELLED>"
}

摘要：<一到三条>
验证：<COMMAND_OR_CHECK_AND_RESULT>
风险：<无或具体风险>
建议协调者动作：<REVIEW | QA | FIX | MERGE_READINESS | ESCALATE>
```

角色通常请求 `IN_REVIEW`，不能授予 `ACCEPTED`。使用文字前先校验并去重 JSON。
