# Automation Monitoring

本文件定义多对话异步任务的完成回传和自动巡检规则。

## 目标

当协调者把任务下发给多个 Codex 对话后，不能只依赖角色主动回复。协调者必须建立一个可恢复的监控闭环：

```text
下发任务 -> 记录对话 ID -> 要求角色回调 -> 创建 5 分钟巡检 -> 读取角色状态 -> 全部结束后汇总 -> 关闭巡检
```

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

推荐回调格式：

```text
Coordinator callback:
Task ID: <TASK_ID>
Role: <ROLE_NAME>
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Summary:
- <ONE_TO_THREE_BULLETS>
Verification:
- <COMMAND_OR_CHECK>: <RESULT>
Risks:
- <NONE_OR_RISK>
```

## 巡检自动化

如果当前 Codex 环境支持 automation 工具，协调者在下发异步任务后创建一个巡检自动化：

- 频率：每 5 分钟。
- 目标：当前协调者对话。
- 输入：任务 ID、角色清单、对话 ID、完成判定规则。
- 动作：读取每个角色对话的最新消息并更新状态。
- 结束条件：全部角色进入终态后汇总结果并关闭或暂停该自动化。

终态包括：

- `DONE`
- `DONE_WITH_CONCERNS`
- `BLOCKED`
- `NEEDS_CONTEXT`

`DONE_WITH_CONCERNS` 是可汇总状态，但不是无风险通过；协调者必须在最终交付中列出风险。

## 无自动化工具时

如果没有 automation 工具，协调者仍然要维护手动巡检表：

- 在 `TASK_BOARD.md` 记录每个角色对话 ID。
- 每次恢复上下文时先读取所有未完成对话。
- 不把“未读取到最终回复”的任务当作完成。

## 巡检提示词模板

可使用 `templates/monitoring_heartbeat.template.md` 创建自动化巡检提示词。

