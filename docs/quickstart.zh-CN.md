# 快速开始

这份快速开始展示一个最小但实用的编排循环。

## 1. 调用 Skill

在 Codex 中输入：

```text
Use $agent-orchestration to coordinate this bug fix with one engineering thread and one QA thread.

Goal:
Fix the failing timestamp export option in the report generation flow.

Constraints:
- Engineer may edit application and test code.
- QA is read-only and must run the regression tests.
- Both roles must report exact commands and results.
```

## 2. 协调者选择工作流

协调者会读取：

- Standard 工作读取 `references/COORDINATION_RUNBOOK.zh-CN.md`；
- 只加载实际用到的派发、回调和 QA 模板，从 `task_dispatch.zh-CN.template.md` 开始。

工程加异步 QA 通常使用 Standard。当前线程的一次性检查保持 Lite；需要周期性推进时使用 Durable。

## 3. 分发角色任务

协调者会给每个角色发送范围明确的任务提示，其中包括：

- 角色名称；
- 仓库路径；
- 可编辑范围和只读范围；
- 停止条件；
- 验证要求；
- 回调要求；
- 异步交接所需的 goal/task ID、attempt、dispatch nonce、coordinator epoch 和预期产物 SHA。

## 4. 跟踪完成状态

对于一两个短任务角色线程，协调者可以手动读取角色回复。

对于多个角色线程或长时间运行的任务，协调者应该使用：

- `references/COORDINATION_RUNBOOK.zh-CN.md`
- `references/templates/monitoring_heartbeat.template.md`

心跳每 5 分钟检查角色、校验版本化回调，并通过 fenced lease 防止重叠 tick 同时执行。所有角色终态后按 `ACTIVE -> DRAINING -> CLOSED` 收尾，最终汇总只发一次并等待清理确认。

## 5. 用 Project Autopilot 做周期性推进

当任务需要跨多次自动化运行持续推进，而不只是监控角色完成状态时，使用 Project Autopilot。

```text
Use $agent-orchestration to create a project autopilot loop.

Goal:
Keep this repository moving until the release-readiness checklist is complete.

Use:
- PROJECT_AUTOPILOT.zh-CN.md 提供统一的项目指令、automation、memory、lease、fencing 和 lifecycle 契约；
- project_goal_contract.template.md for done criteria and permissions;
- automation_tick.template.md for each recurring run;
- automation_memory.template.md so repeated runs do not duplicate work.

Escalate before merge, push, deploy, destructive changes, public API contract changes, or scope expansion.
```

当前线程回访和回调巡检用 heartbeat automation。需要独立推进 workspace 或 worktree 的长期任务，用 cron automation。

## 6. 协调者最终交付

最终回复应包含：

- 改了什么；
- 哪些角色参与；
- 精确的验证证据；
- 未解决的风险；
- 相关 commit 或分支名；
- 哪些自动化已经暂停、删除或仍保持运行；
- 最终验收的精确产物 SHA，以及 coordinator state 是否达到 `ACCEPTED`。
