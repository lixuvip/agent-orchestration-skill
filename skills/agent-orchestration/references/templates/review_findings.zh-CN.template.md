# 中文代码审查报告模板

审查证据只绑定一个精确 commit SHA。

```text
Goal ID: <GOAL_ID>
Task ID: <TASK_ID>
Attempt: <当前有效_ATTEMPT>
Dispatch nonce: <当前有效_DISPATCH_NONCE>
Expected head SHA: <EXPECTED_HEAD_SHA>
Observed head SHA: <OBSERVED_HEAD_SHA>
Execution status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT | CANCELLED
Gate verdict: PASS | FAIL | BLOCKED | NOT_APPLICABLE

发现项：
- [P0 | P1 | P2 | P3] <TITLE>
  文件：<PATH:LINE>
  问题：<WHAT_IS_WRONG>
  影响：<WHY_IT_MATTERS>
  建议修复：<HOW_TO_FIX_OR_DIRECTION>

待确认问题：
- <QUESTION_OR_NONE>

测试缺口：
- <GAP_OR_NONE>

合并建议：
- APPROVE | APPROVE_WITH_CONCERNS | REQUEST_CHANGES | BLOCKED

建议协调者动作：
- <ACCEPT_GATE | RETURN_TO_ENGINEERING | SEND_TO_QA | ESCALATE>

ORCHESTRATION_EVENT_V1:
<完整事件，coordinator_state 使用 IN_REVIEW>
```

- 仍有阻断 finding 时使用 `FAIL`；`APPROVE` 文案不能覆盖失败门禁。
- `observed_head_sha` 与 `expected_head_sha` 不一致时，报告证据已过期，不要审查正在移动的分支。
- 后续任何代码 commit 都会使本次结论失效。
