# Automation Monitoring

本文件定义多对话异步任务的完成回传和自动巡检规则。

## 目标

当协调者把任务下发给多个 Codex 对话后，不能只依赖角色主动回复。协调者必须建立一个可恢复的监控闭环：

```text
下发任务 -> 记录对话 ID -> 要求角色回调 -> 创建 5 分钟巡检 -> 读取角色状态 -> 全部结束后汇总 -> 关闭巡检
```

如果用户要求“持续推进项目直到目标完成”，不要只创建 heartbeat。改用 `PROJECT_AUTOPILOT.md` 建立目标契约、cron/heartbeat 选择、automation memory 和升级规则。

## 适用条件

满足任一条件时启用本规则：

- 同时创建或继续两个以上角色对话。
- 角色任务会运行较长时间，协调者不适合一直等待。
- 任务需要最终合并多个项目、分支、提交或验证结果。
- 角色回复不一定能主动返回到协调者上下文。

## 下发任务时的要求

协调者必须在任务中写明：

- 协调者对话 ID。
- 本角色对话 ID，如已知。
- 是否要求完成后回调。
- 回调格式。
- 如无法回调，应在本角色最终回复中写 `CALLBACK_FAILED` 和原因。

回调必须使用 `templates/coordinator_callback.template.md` 的完整 `ORCHESTRATION_EVENT_V1` 信封。巡检先做协议校验、event ID 去重和 attempt/nonce/epoch/SHA 过期检查，再更新任务状态。

## 巡检自动化

如果当前 Codex 环境支持 automation 工具，协调者在下发异步任务后创建一个巡检自动化：

- 频率：每 5 分钟。
- 目标：当前协调者对话。
- 输入：任务 ID、角色清单、对话 ID、完成判定规则。
- 动作：读取每个角色对话的最新消息并更新状态。
- 结束条件：全部角色进入终态后汇总结果并关闭或暂停该自动化。
- 状态不清时：优先发送一次 status request，要求角色补充显式状态、验证和风险。
- 并发：按 `AUTOMATION_CONCURRENCY.md` 获取 fenced lease；`LEASE_ALREADY_HELD` 或 `LEASE_BUSY` 时安静退出。
- 生命周期：`ACTIVE -> DRAINING -> CLOSED`。全员终态后停止新状态请求，只发送一次汇总，收到暂停/删除确认后才写 `CLOSED`。

Heartbeat 适合当前线程回访、角色回调收集和短周期巡检。Cron 适合绑定 workspace/worktree 的持续项目推进，例如 issue/PR 巡检、测试、发布就绪和下一步安全动作。创建或更新自动化时，优先使用 Codex automation 工具；有现成自动化时优先更新，避免重复。

终态包括：

- `DONE`
- `DONE_WITH_CONCERNS`
- `BLOCKED`
- `NEEDS_CONTEXT`
- `CANCELLED`

`DONE_WITH_CONCERNS` 是可汇总状态，但不是无风险通过；协调者必须在最终交付中列出风险。

所有角色进入终态只表示 heartbeat 可以进入 `DRAINING`。其中 `DONE` 和 `DONE_WITH_CONCERNS` 进入协调者 `IN_REVIEW`，不能由 heartbeat 直接写成 `ACCEPTED`。

## 无自动化工具时

如果没有 automation 工具，协调者仍然要维护手动巡检表：

- 在 `TASK_BOARD.md` 记录每个角色对话 ID。
- 每次恢复上下文时先读取所有未完成对话。
- 不把“未读取到最终回复”的任务当作完成。

## 巡检提示词模板

可使用 `templates/monitoring_heartbeat.template.md` 创建自动化巡检提示词。
可使用 `scripts/heartbeat_lifecycle.py` 计算单向收尾动作，使用 `scripts/automation_lease.py` 防止重叠 tick。
状态不清或缺少验证时，可使用 `templates/status_request.template.md` 向角色线程请求更新。
项目 Autopilot 可使用 `templates/project_goal_contract.template.md`、`templates/automation_plan.template.md`、`templates/automation_tick.template.md`、`templates/automation_memory.template.md` 和 `templates/escalation_report.template.md`。
