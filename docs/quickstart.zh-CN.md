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

- `references/COMMUNICATION_PROTOCOL.md`
- `references/WORKFLOWS.md`
- `references/templates/task_dispatch.template.md`

对于小型 bug，通常选择 emergency fix 或 engineering implementation 工作流。

## 3. 分发角色任务

协调者会给每个角色发送范围明确的任务提示，其中包括：

- 角色名称；
- 仓库路径；
- 可编辑范围和只读范围；
- 停止条件；
- 验证要求；
- 回调要求。

## 4. 跟踪完成状态

对于一两个短任务角色线程，协调者可以手动读取角色回复。

对于多个角色线程或长时间运行的任务，协调者应该使用：

- `references/AUTOMATION_MONITORING.md`
- `references/templates/monitoring_heartbeat.template.md`

心跳监控每 5 分钟检查一次各角色状态，并在所有角色到达终态后关闭自身。

## 5. 协调者最终交付

最终回复应包含：

- 改了什么；
- 哪些角色参与；
- 精确的验证证据；
- 未解决的风险；
- 相关 commit 或分支名。
