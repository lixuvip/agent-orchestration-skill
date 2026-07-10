# 自动化记忆模板

项目 Autopilot 自动化写入持久状态文件时使用本模板。

```markdown
# 自动化记忆

目标 ID: <GOAL_ID>
自动化 ID: <AUTOMATION_ID>
工作区: <PATH_OR_REPOSITORY>
最后更新: <ISO_TIMESTAMP>

## 并发租约

- 状态目录: <AUTOMATION_STATE_DIRECTORY>
- 上一个 owner ID: <TICK_ID_OR_NONE>
- 最新 fencing token: <非负整数>
- 租约过期时间: <ISO_TIMESTAMP_OR_NONE>
- 上一次租约结果: <ACQUIRED | ALREADY_HELD | BUSY | EXPIRED | NOT_OWNER | RELEASED | NONE>

低 fencing token 的 tick 禁止覆盖本文件。

## 生命周期

- 状态: <ACTIVE | DRAINING | CLOSED>
- Heartbeat generation: <GENERATION_ID_OR_NOT_APPLICABLE>
- 最终汇总键: <KEY_OR_NONE>
- 最终汇总已发送: <YES_OR_NO>
- 清理请求 ID: <ID_OR_NONE>
- 清理已确认: <YES_OR_NO>

## 目标

<一句话目标>

## 完成条件

- <验收条件 1>
- <验收条件 2>

## 最新有效更新

- 来源: <issue | pr | branch | tests | thread | release | none>
- 值: <UPDATE_SUMMARY_OR_HASH>
- 是否已被 Codex 动作覆盖: <YES_OR_NO>

## 上一次 Tick

- 观察状态: <SUMMARY>
- 执行动作: <ONE_ACTION_OR_NONE>
- 验证: <COMMAND_OR_CHECK_AND_RESULT>
- 结果: <DONE | IN_PROGRESS | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>
- 风险: <NONE_OR_RISK>
- Fencing token: <INTEGER>

## 下一步安全动作

<ONE_ACTION_OR_NONE>

## 阻塞历史

- <TIMESTAMP>: <BLOCKER_OR_NONE>

## 已发送消息

- <TIMESTAMP_OR_ID>: <WHERE_AND_SUMMARY>

## 已处理事件和动作

- Event IDs: <EVENT_ID_LIST_OR_NONE>
- 状态请求键: <TASK_ATTEMPT_NONCE_KEY_LIST_OR_NONE>
- 动作幂等键: <ACTION_KEY_LIST_OR_NONE>
- 升级报告键: <ESCALATION_KEY_LIST_OR_NONE>
```
