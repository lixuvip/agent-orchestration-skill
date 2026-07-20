# v0.3.0 设计溯源说明

本版本一方面把原有 Skill 重构为原生优先的轻量运行时，另一方面吸收了开源 [xAI Grok Build 仓库](https://github.com/xai-org/grok-build)中部分可靠性思路。固定检查基线为仓库 commit [`ba76b0a683fa52e4e60685017b85905451be17bc`](https://github.com/xai-org/grok-build/tree/ba76b0a683fa52e4e60685017b85905451be17bc)，检查日期为 2026-07-20；该快照声明的 source revision 为 `ba69d70c2f7d70a130a323b2becdf137af784c7f`。

Grok Build 使用 [Apache License 2.0](https://github.com/xai-org/grok-build/blob/ba76b0a683fa52e4e60685017b85905451be17bc/LICENSE)。下面列出的是设计参考关系。`agent-orchestration` 没有复制 Grok Build 的运行时代码、工具实现、事件循环或验证 prompt。

## 来源到本地改造的映射

| v0.3.0 能力 | 上游参考 | 面向 Codex 的本地改造 |
| --- | --- | --- |
| 验收前完整闭环用户需求 | [`check-work/SKILL.md`](https://github.com/xai-org/grok-build/blob/ba76b0a683fa52e4e60685017b85905451be17bc/crates/codegen/xai-grok-shell/skills/check-work/SKILL.md) 会重建完整请求并检查当前状态 | 默认由协调者自己维护轻量的“请求/动作/证据/状态”清单。独立验证者是可选项；证据未失效时，不重复执行完全相同的昂贵测试。 |
| 能力预检与只读规划 | [`16-subagents.md`](https://github.com/xai-org/grok-build/blob/ba76b0a683fa52e4e60685017b85905451be17bc/crates/codegen/xai-grok-pager/docs/user-guide/16-subagents.md)、[`19-plan-mode.md`](https://github.com/xai-org/grok-build/blob/ba76b0a683fa52e4e60685017b85905451be17bc/crates/codegen/xai-grok-pager/docs/user-guide/19-plan-mode.md) 和 [`22-permissions-and-safety.md`](https://github.com/xai-org/grok-build/blob/ba76b0a683fa52e4e60685017b85905451be17bc/crates/codegen/xai-grok-pager/docs/user-guide/22-permissions-and-safety.md) 区分 Agent 能力、Plan 边界和权限层 | 派发前明确检查 read/write/execute/network/browser/connector。高歧义方案先在当前任务只读规划，并明确提醒：父任务 Plan/只读不等于子 Agent 自动只读。 |
| 中途转向与过期结果 | [`interjection.rs`](https://github.com/xai-org/grok-build/blob/ba76b0a683fa52e4e60685017b85905451be17bc/crates/codegen/xai-grok-shell/src/session/acp_session_impl/interjection.rs) 处理活跃 turn 中到达的用户输入 | 新消息分成“替换、追加、状态”；通过 Codex 原生工具更新或中断受影响 owner；旧范围迟到结果未经重验只能作参考。没有复用 Grok 的事件代码。 |
| 最终交付前活跃工作盘点 | [`stop_gate.rs`](https://github.com/xai-org/grok-build/blob/ba76b0a683fa52e4e60685017b85905451be17bc/crates/codegen/xai-grok-shell/src/session/acp_session_impl/stop_gate.rs) 与 [`20-background-tasks.md`](https://github.com/xai-org/grok-build/blob/ba76b0a683fa52e4e60685017b85905451be17bc/crates/codegen/xai-grok-pager/docs/user-guide/20-background-tasks.md) 会在停止边界暴露未完成工作 | 最终回复前盘点 Codex 原生子 Agent、用户自有任务、后台命令、monitor 和 automation，逐项等待、取消或报告；不创建自定义 stop gate 或状态文件。 |
| 可恢复的继续工作 | [`17-sessions.md`](https://github.com/xai-org/grok-build/blob/ba76b0a683fa52e4e60685017b85905451be17bc/crates/codegen/xai-grok-pager/docs/user-guide/17-sessions.md) 介绍持久 session、resume、fork 与 compaction | fork、handoff、长暂停或依赖上下文的继续工作前，在原生任务历史中保留“目标/约束/baseline/证据/决策/待办/活跃工作/阻塞/下一步”恢复胶囊，不重建 session 存储。 |
| 有界且必须产生进展的重试 | [`goal.rs`](https://github.com/xai-org/grok-build/blob/ba76b0a683fa52e4e60685017b85905451be17bc/crates/codegen/xai-grok-shell/src/session/acp_session_impl/goal.rs) 实现持续目标与重试行为 | 每次重试必须新增证据、缩小失败范围或改变方法；相同阻塞反复出现时停止并升级，不复制 Grok 的调度或 backoff 实现。 |
| 可选 Best-of-N | [`best-of-n/SKILL.md`](https://github.com/xai-org/grok-build/blob/ba76b0a683fa52e4e60685017b85905451be17bc/crates/codegen/xai-grok-shell/skills/best-of-n/SKILL.md) 会隔离多个候选并比较 | Codex 只使用 2-3 个候选，只用于明确要求或真正高歧义的工作；结果前固定标准，写入隔离，允许全部拒绝；只对集成后的胜出候选运行最终完整套件。这里明确不采用上游“始终选择最不差候选”的规则。 |
| 类型化派发/证据与扁平委派 | [`16-subagents.md`](https://github.com/xai-org/grok-build/blob/ba76b0a683fa52e4e60685017b85905451be17bc/crates/codegen/xai-grok-pager/docs/user-guide/16-subagents.md) 介绍能力模式、隔离和输入输出契约 | 不恢复 persona/角色目录，而是使用精简自然语言契约：目标、baseline、最少输入/能力、边界、证据类型、返回面、owner 和停止条件。默认保持扁平委派，保证 owner 可见。 |

## 本仓库自己的设计

6 文件运行时、当前任务优先、内部子 Agent 与用户侧边栏任务的区分、Local/Worktree handoff 语义、验证预算、独立 `agy-second-opinion` Skill、安静 automation 和安装一致性校验，均为本仓库结合 Codex 当前产品执行面和既往真实使用重新形成的设计。

## 明确没有采用的内容

- 不引入 Grok 专属 Agent 类型、persona、ACP 方法、session 文件、事件流、stop-gate 代码、scheduler、hook 或权限配置。
- 不复制验证 prompt。除非风险或用户明确要求，需求闭环由协调者负责。
- 不引入强制三轮验证循环。
- Best-of-N 不会因为“总得选一个”就选择最不差候选；全部拒绝是有效结果。
- 不把角色注册表、回调信封、任务板、heartbeat 文件、lease 或确定性路由脚本重新装回主 Skill。
