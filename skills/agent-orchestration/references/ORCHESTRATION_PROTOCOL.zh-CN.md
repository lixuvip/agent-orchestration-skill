# 编排事件协议

异步任务派发、回调、状态请求、QA/审查门禁、heartbeat 巡检和协调者验收统一使用 `ORCHESTRATION_EVENT_V1`。文字摘要可以附加，但不能替代版本化事件信封。

## 三个独立维度

| 维度 | 取值 | 权威方 |
| --- | --- | --- |
| 角色执行状态 | `TODO`, `IN_PROGRESS`, `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`, `CANCELLED` | 角色报告自己的工作状态。 |
| 门禁结论 | `PENDING`, `PASS`, `FAIL`, `BLOCKED`, `WAIVED`, `NOT_APPLICABLE` | QA、Reviewer 或协调者记录证据质量。 |
| 协调者状态 | `TODO`, `DISPATCHED`, `IN_PROGRESS`, `IN_REVIEW`, `RETURNED`, `ACCEPTED`, `ESCALATED`, `CANCELLED` | 只有协调者负责验收和流转。 |

角色 `DONE` 只表示“可以开始协调者验收”，不表示已验收、已合并或已交付。

## 必填事件信封

```json
{
  "protocol_version": "ORCHESTRATION_EVENT_V1",
  "goal_id": "GOAL-001",
  "task_id": "TASK-001",
  "attempt": 2,
  "dispatch_nonce": "dispatch-2-abc",
  "coordinator_epoch": "coordinator-epoch-7",
  "event_id": "event-task-001-2-done",
  "event_timestamp": "2026-07-10T10:00:00+08:00",
  "role": "QA Tester",
  "coordinator_thread_id": "thread-coordinator",
  "role_thread_id": "thread-qa",
  "base_sha": "0123456789abcdef0123456789abcdef01234567",
  "expected_head_sha": "1111111111111111111111111111111111111111",
  "observed_head_sha": "1111111111111111111111111111111111111111",
  "execution_status": "DONE",
  "gate_verdict": "PASS",
  "coordinator_state": "IN_REVIEW"
}
```

无 Git 仓库时三个产物字段都使用 `NONE`；只有产物生产角色尚未生成候选 commit 时临时使用 `UNKNOWN`。Git 任务不能用 `NONE` 验收，任何任务都不能用 `UNKNOWN` 或不一致的产物身份验收。

## 派发身份、过期与去重

每次派发记录：

- `attempt`：退回或重新派发时递增；
- `dispatch_nonce`：本次任务尝试的唯一值；
- `coordinator_epoch`：当前协调者运行或租约的唯一值；
- `expected_head_sha`：角色应检查的精确产物 SHA；只有产物尚未生成的工程角色可以在派发时使用 `UNKNOWN`。

目标、任务、attempt、nonce、epoch、expected SHA，或在已派发具体 SHA 时 observed SHA 不符合当前预期，回调就是 `STALE`。派发时为 `UNKNOWN` 的产物生产角色可以报告新生成的具体 SHA；协调者记录该候选 commit，后续所有门禁必须使用这个具体 SHA。其他过期回调不能修改当前状态。

已经处理过的 `event_id` 是 `DUPLICATE`，应成功 no-op：不能重复评论、流转、合并或通知。

缺字段、格式错误或未知协议版本是 `REJECTED`。请角色修正回调，不能猜测缺失身份。

## Commit 固定门禁

- 工程完成后记录候选 `expected_head_sha`。
- QA 和审查必须把同一个 SHA 写为 `observed_head_sha`。
- 后续任何代码 commit 都会使旧 QA/审查结论对交付失效。
- 只有协调者明确记录范围和原因时，纯文档变更才可以用 `WAIVED`；不能静默复用旧证据。
- 分支名、worktree 路径或回调时的 `latest` 都不能替代精确 SHA。

## 已验收交付条件

以下条件必须同时成立：

1. `coordinator_state` 为 `ACCEPTED`；
2. `execution_status` 为 `DONE` 或 `DONE_WITH_CONCERNS`；
3. `gate_verdict` 为 `PASS`、`WAIVED` 或 `NOT_APPLICABLE`；
4. `expected_head_sha` 是具体 commit，或者任务不涉及 Git 且三个产物字段全部为 `NONE`；
5. `observed_head_sha` 等于 `expected_head_sha`；
6. 事件符合当前有效派发身份。

`DONE + FAIL`、`DONE + PENDING`、`DONE + IN_REVIEW` 都不是已验收交付。`CANCELLED` 是巡检终态，但永远不是交付。

## 校验 helper

```bash
python3 scripts/orchestration_event.py \
  --event-file callback.json \
  --expectation-file active-dispatch.json
```

用 `--seen-event-id <EVENT_ID>` 去重，在最终交付门禁增加 `--require-accepted-delivery`。

helper 输出：`EVENT_ACCEPTED`、`EVENT_DUPLICATE`、`EVENT_STALE`、`EVENT_NOT_DELIVERABLE` 或 `EVENT_REJECTED: ...`。

协调者处理顺序固定为：校验 → 去重 → 对比当前派发身份和 SHA → 分别记录角色状态与门禁 → 独立推进协调者状态 → 验收 → 产生协调者自己的新状态事件。
