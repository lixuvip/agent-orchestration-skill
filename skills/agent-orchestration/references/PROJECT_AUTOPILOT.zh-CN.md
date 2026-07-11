# 项目 Autopilot 运行手册

这是 Durable 的权威能力包。只有工作必须 recurring 或跨 tick 恢复时，才在 `COORDINATION_RUNBOOK.zh-CN.md` 之后加载。中英文只加载一个版本。

## 启用边界

Durable Autopilot 用于围绕明确完成条件反复推进 workspace/worktree：issue/PR 协调、QA/发布就绪、backlog/checklist 推进，或稍后唤醒后可能执行安全动作。

一次性编辑、纯提醒、有限期角色 heartbeat，或每一步都必须由用户判断的任务，不使用 Autopilot。

## Durable 契约

创建/更新 automation 前填写 `templates/project_goal_contract.zh-CN.template.md` 和 `templates/automation_plan.zh-CN.template.md`：

- goal ID、结果、可衡量完成条件、workspace/branch/issue/PR/release；
- 稳定指令来源和验证命令；
- 可自动动作和明确确认门禁；
- 频率、tick 最长时间/次数、预算和停止条件；
- automation/memory/state 路径、幂等键、lease TTL、lifecycle、清理策略。

“完全自动”也不等于默认授权 merge、push、deploy、publish、破坏性数据/文件动作、密钥/计费操作、公开 API 变化、费用或产品范围扩大。

## 项目指令

读取最窄相关来源：

1. 根目录和适用嵌套 `AGENTS.md`；
2. 更强局部规则 `AGENTS.override.md`；
3. 已配置 fallback 指令；
4. `.codex/config.toml`，只读配置；
5. 相关 README、贡献、测试、发布、issue/PR 文档。

稳定构建/测试、分支、审查、安全、沟通和升级规则放 `AGENTS.md`。实时目标状态、阻塞、计数、消息和下一步放 automation memory。两者都不能存密钥。未经授权不修改项目指令。

只有同一命令、错误或反馈被反复重新发现时，才建议稳定规则更新；使用 `templates/agents_guidance_snippet.zh-CN.template.md`。

## Automation 位置

| 需求 | 位置 |
| --- | --- |
| 有限期当前线程角色巡检 | Standard heartbeat；回到 `COORDINATION_RUNBOOK.zh-CN.md` |
| recurring workspace/worktree 推进 | Cron |
| worktree/环境设置需要用户检查 | Suggested cron create/update |
| 已有相同 goal/cwd/target automation | 更新，不重复创建 |

有 app automation 工具时使用工具，让工具序列化 schedule，对用户用自然语言描述频率。创建前检查现有名称、prompt、cwd、target、仓库、issue/PR、分支和 goal；保留用户未要求改变的字段。

## Tick 事务

每次 tick 使用 `templates/automation_tick.zh-CN.template.md`，最多执行一个安全下一步：

1. 生成唯一 tick ID，在读取可变 memory 前用 `scripts/automation_lease.py` 获取 fenced lease。
2. `LEASE_ALREADY_HELD` 或 `LEASE_BUSY` 安静退出；租约过期/被替换时丢弃结果，不能产生副作用。
3. 读取项目指令、目标契约和 memory。memory fencing token 更大时停止。
4. 检查与 goal 相关的 git/issue/PR/thread/test/build/log/release 实时状态。
5. 计算 latest effective update；只改时间戳或 metadata 不等于进展。
6. 对比已处理 event ID、已发送消息键、动作键和上次状态，防止重复。
7. 只选择一个属于自动权限的最小动作。
8. 发消息、外部写入、回调、cleanup 或提交 memory 前立即验证租约。
9. 执行动作和最小相关验证。
10. 原子写 memory：fencing token、观察状态、动作/证据、风险、阻塞历史、下一步和幂等键。
11. 完成时只发一次最终汇总并请求暂停/删除；工具确认前不能写 `CLOSED`。
12. 缺权限/范围/预算或失败达到契约限制时，只发一次去重的 `templates/escalation_report.zh-CN.template.md`，按契约暂停/等待。
13. 在 finally 等价路径释放租约。

没有有效变化时更新内部观察 memory，但除非契约要求，不发用户进度消息。

## 租约和 Fencing

默认 state 目录：

```text
${CODEX_HOME:-$HOME/.codex}/automations/<automation-id>/state
```

helper 使用独占文件锁、原子替换、过期时间、随机 lease token 和单调递增 fencing token。

```bash
python3 scripts/automation_lease.py acquire \
  --state-dir "$STATE_DIR" \
  --automation-id "$AUTOMATION_ID" \
  --owner-id "$TICK_ID" \
  --ttl-seconds 900
```

- 只有 `LEASE_ACQUIRED` 返回 token；只放在当前 tick 上下文，不持久化复用。
- 合法长任务在过期前续租；TTL 大于预计运行时间加收尾余量。
- 副作用和 memory 写入前验证。
- 低 fencing token 不能覆盖 memory。
- 相同 owner/token 重复 release 是 no-op；旧 owner 不能释放或关闭替代者。
- 使用锁和原子 rename 语义明确的本地文件系统。

## Durable Memory

默认 memory：

```text
${CODEX_HOME:-$HOME/.codex}/automations/<automation-id>/memory.md
```

未设置 `CODEX_HOME` 时从 `$HOME/.codex` 解析，不能退化为 `/automations`。使用 `templates/automation_memory.zh-CN.template.md`，保留：

- goal/automation ID、workspace、完成条件；
- latest effective update 及是否已覆盖；
- 上次 tick/动作/验证/风险和下一安全动作；
- 阻塞历史和运行/尝试计数；
- 已发送消息、已处理事件、状态请求/动作/升级键；
- lifecycle、最终汇总/清理状态和最新 fencing token。

## 生命周期和完成

Automation lifecycle 单向变化：

```text
ACTIVE -> DRAINING -> CLOSED
```

- `ACTIVE`：检查并执行一个已授权安全动作。
- `DRAINING`：停止新工作，最终汇总只发一次，暂停/删除只请求一次；失败时只重试 cleanup。
- `CLOSED`：清理已确认；晚到 tick/update 永久 no-op。

automation 监控角色终态时使用 `scripts/heartbeat_lifecycle.py`。持久化 final-summary key、cleanup request ID 和确认，避免崩溃后重复汇总。

只有全部完成条件和当前必需验证通过，才能声明 goal 达成。部分结果保持 `DONE_WITH_CONCERNS`。丢失 lease 不是用户 blocker，说明另一个 tick 正在推进。

## 安全和升级

未经授权的 merge/push/deploy/publish/release、破坏性动作、密钥/凭据/计费、公开 API 变化、产品范围扩大、重大环境设置或反复验证失败前，停止/暂停并升级。

最终汇总包含已达成条件、真实验证、遗留风险/豁免、automation 清理结果和仍需用户决定的事项。
