# Agent Orchestration Kit

这是一个可复制到任意项目的多对话角色编排文档包。

它的目标是把多个 Codex 对话 ID 组织成一个小型项目团队：当前对话作为协调者，其他对话分别承担产品、工程、QA、代码审查、发布文档等角色。协调者负责下发任务、读取回复、检查交付、流转下一角色，并最终向用户交付结果。

## 适用场景

- 一个需求需要产品、工程、测试、审查多个环节。
- 你希望不同对话 ID 承担固定角色，而不是每次都重新说明身份。
- 你希望角色之间按统一格式交付，减少“已完成但无法验收”的情况。
- 你希望把项目管理规则沉淀成可复用模板。

不适合使用本套流程的情况：

- 只是一个很小的单文件改动。
- bug 需要一个连续调试上下文，不适合拆给多个角色。
- 没有分支或 worktree 隔离，但多个角色都要改同一批文件。
- 你只是想要快速诊断，而不是启动完整协作流程。

## 文件结构

```text
agent_orchestration_kit/
├── README.md
├── PROJECT_CONTEXT.template.md
├── ROLE_REGISTRY.template.md
├── COMMUNICATION_PROTOCOL.md
├── AUTOMATION_MONITORING.md
├── ORCHESTRATION_INTAKE.md
├── CONTROLLER_LOOP.md
├── PROJECT_AUTOPILOT.md
├── REQUIREMENT_WRITING_GUIDE.md
├── STATE_MACHINE.md
├── TASK_BOARD.template.md
├── WORKFLOWS.md
├── examples/
│   ├── filled_role_reply.md
│   └── filled_task_dispatch.md
├── roles/
│   ├── coordinator_pm.md
│   ├── product_designer.md
│   ├── technical_engineer.md
│   ├── qa_tester.md
│   ├── code_reviewer.md
│   └── release_docs.md
└── templates/
    ├── task_dispatch.template.md
    ├── task_dispatch.zh-CN.template.md
    ├── orchestration_intake.template.md
    ├── orchestration_intake.zh-CN.template.md
    ├── project_goal_contract.template.md
    ├── project_goal_contract.zh-CN.template.md
    ├── automation_plan.template.md
    ├── automation_plan.zh-CN.template.md
    ├── automation_tick.template.md
    ├── automation_tick.zh-CN.template.md
    ├── automation_memory.template.md
    ├── automation_memory.zh-CN.template.md
    ├── escalation_report.template.md
    ├── escalation_report.zh-CN.template.md
    ├── agents_guidance_snippet.template.md
    ├── agents_guidance_snippet.zh-CN.template.md
    ├── coordinator_callback.template.md
    ├── coordinator_callback.zh-CN.template.md
    ├── status_request.template.md
    ├── status_request.zh-CN.template.md
    ├── merge_readiness.template.md
    ├── merge_readiness.zh-CN.template.md
    ├── monitoring_heartbeat.template.md
    ├── monitoring_heartbeat.zh-CN.template.md
    ├── role_reply.template.md
    ├── role_reply.zh-CN.template.md
    ├── qa_report.template.md
    ├── review_findings.template.md
    └── handoff_note.template.md
```

## 启用步骤

1. 将整个 `agent_orchestration_kit/` 文件夹复制到目标项目的 `docs/` 或项目根目录下。
2. 复制 `PROJECT_CONTEXT.template.md` 为 `PROJECT_CONTEXT.md`，填写项目名称、路径、技术栈、分支策略、验证命令和禁止事项。
3. 复制 `ROLE_REGISTRY.template.md` 为 `ROLE_REGISTRY.md`，填写每个角色对应的真实对话 ID。
4. 复制 `TASK_BOARD.template.md` 为 `TASK_BOARD.md`，用于追踪任务状态。
5. 给每个角色对话发送对应的 `roles/*.md` 作为角色初始化说明。
6. 如果分支、线程、回调、自动化、合并或推送策略不明确，先按 `ORCHESTRATION_INTAKE.md` 和 `templates/orchestration_intake.template.md` 做短确认。
7. 后续每次分配任务时，先参考 `REQUIREMENT_WRITING_GUIDE.md` 写清楚需求，再使用 `templates/task_dispatch.template.md`。
8. 要求每个角色按 `templates/role_reply.template.md` 回复；需要回主线程时，使用 `templates/coordinator_callback.template.md`。
9. 中文团队可直接使用 `templates/*.zh-CN.template.md`。
10. 涉及多个长任务对话时，按 `AUTOMATION_MONITORING.md` 创建回调和 5 分钟巡检闭环。
11. 用户要求项目持续推进、定时自动继续或一直做到目标效果时，按 `PROJECT_AUTOPILOT.md` 建立目标契约、自动化计划、tick 提示词、memory 和升级规则。
12. 有多个任务状态时，按 `STATE_MACHINE.md` 判定状态转换。
13. 涉及主线程、子线程、分支、状态请求或合并就绪时，按 `CONTROLLER_LOOP.md` 执行。
14. 协调者按 `COMMUNICATION_PROTOCOL.md` 和 `WORKFLOWS.md` 做流转与验收。

## 最小运行方式

如果不想一次启用全部角色，建议先从三个角色开始：

- 协调者 / PM：当前对话。
- 技术工程师：独立 worktree 或功能分支。
- QA 测试：只读 checkout 或 QA worktree。

最小闭环：

```text
用户需求 -> 协调者拆解 -> 工程实现 -> 协调者检查 -> QA 验证 -> 协调者交付
```

## 核心原则

- 每个角色只做自己职责内的事。
- 每次任务都必须写清楚可改范围和禁止范围。
- 工程角色优先使用独立分支或 worktree。
- QA 和 Reviewer 默认只读，除非明确分配修复任务。
- 角色回复必须包含实际验证结果，不接受只回复“完成了”。
- 多对话异步任务必须记录对话 ID，并启用回调或巡检，不能靠记忆判断完成。
- 周期性自动化必须读取项目 `AGENTS.md` / `AGENTS.override.md` 等持久指令，并把临时状态写入 automation memory。
- 涉及密钥、付费服务、生产环境、破坏性 git 操作、大模型下载等事项时，必须停止并请求确认。
