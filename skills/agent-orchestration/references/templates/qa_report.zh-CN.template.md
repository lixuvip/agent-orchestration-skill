# 中文 QA 报告模板

QA 证据只对实际检查的精确 HEAD SHA 有效。

```text
Goal ID: <GOAL_ID>
Task ID: <TASK_ID>
Attempt: <当前有效_ATTEMPT>
Dispatch nonce: <当前有效_DISPATCH_NONCE>
Expected head SHA: <EXPECTED_HEAD_SHA>
Observed head SHA: <OBSERVED_HEAD_SHA>
Execution status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT | CANCELLED
Gate verdict: PASS | FAIL | BLOCKED | NOT_APPLICABLE

摘要：
- <整体测试结果>

测试矩阵：
| 范围 | 场景 | 预期 | 实际 | 结果 |
| --- | --- | --- | --- | --- |
| <AREA> | <SCENARIO> | <EXPECTED> | <ACTUAL> | PASS / FAIL / BLOCKED / NOT TESTED |

已运行验证：
- <COMMAND_OR_MANUAL_CHECK>: PASS | FAIL | NOT RUN
  证据：<日志路径_截图描述_或输出摘要>

失败项：
- 问题：<TITLE>
  严重度：P0 | P1 | P2 | P3
  复现步骤：
  预期：
  实际：

未测试：
- <场景和原因>

风险 / 顾虑：
- <无或具体风险>

建议协调者动作：
- <ACCEPT_GATE | RETURN_TO_ENGINEERING | REQUEST_MORE_EVIDENCE | ESCALATE>

ORCHESTRATION_EVENT_V1:
<完整事件，coordinator_state 使用 IN_REVIEW>
```

如果 `observed_head_sha` 与 `expected_head_sha` 不一致，请停止并报告证据已过期。后续任何代码 commit 都会使本次结论失效。
