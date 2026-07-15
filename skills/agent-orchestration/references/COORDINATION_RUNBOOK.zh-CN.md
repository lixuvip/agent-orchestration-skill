# 协调运行手册

这是 Standard/Durable 的权威协调契约。Lite 不读取本文件。中英文只加载一个版本。

## 不可省略的原则

- 每个任务只有一个 owner，并明确可编辑、只读和禁止范围。
- 重叠编辑必须隔离或串行；路由不能让共享文件并行写入自动变安全。
- 不能从静默或角色信心推断完成；只记录真实运行的命令和结果。
- 角色 `DONE` 只是申请验收；只有协调者 `ACCEPTED` 才是交付。
- QA/Review 证据只对实际检查的精确产物 SHA 有效。
- 重复或过期回调都是 no-op。
- merge、push、deploy、publish、破坏性改动、密钥、费用和范围扩大必须符合用户/项目明确授权。

## 确认与路由

只有答案会实质改变执行位置、写权限、用户可见线程、回调/自动化或 merge/push 权限时才询问；否则推断最低安全模式。

| 模式 | 最低适用形态 | 运行成本 |
| --- | --- | --- |
| Lite | 当前上下文一次性工作；无异步边界、无 recurring。 | 不用 task board、事件信封、heartbeat、cron 或 memory。 |
| Standard | 多角色、异步/用户可见线程、跨仓库交接、正式 QA/Review/Release 门禁或有限期长任务。 | 任务 owner + 事件协议；只有异步/长任务才启用 heartbeat。 |
| Durable | recurring 或必须跨 tick 恢复。 | Standard + `PROJECT_AUTOPILOT.zh-CN.md`。 |

路由不明显时使用 `scripts/route_orchestration.py`。用户要求的轻模式不能绕过安全下限，可以明确升级重模式。外部模型审查/调研只是 modifier，本身不升级路由。

## 子对话思考级别

每次创建新的用户可见子对话前，协调者都要单独评估认知难度；编排模式与思考级别相互独立。综合歧义程度、推理深度、影响范围、验证难度和延迟/成本，选择最低足够且工具支持的级别。

| 级别 | 典型任务 |
| --- | --- |
| `minimal` | 机械提取、格式整理或已知命令检查。 |
| `low` | 有边界的盘点、文档修改或确定性 QA。 |
| `medium` | 常规实现、调研、调试或审查。 |
| `high` | 模糊根因、多模块改动、非平凡设计或探索性审查。 |
| `xhigh` | 安全分析、跨仓库契约、困难综合或高风险发布判断。 |
| `max` / `ultra` | 仅限宿主支持且预期质量收益足以覆盖额外延迟/成本的例外任务。 |

- 用户明确指定且工具支持时优先遵从；否则由协调者选择。只有会实质违反用户延迟/成本约束时才询问。
- 不能按角色名称固定级别：机械 QA 可以是 `low`，探索性 QA 可以是 `high`。
- 只有创建工具暴露 `thinking` 时才传值。不需要覆盖时省略并记录 `INHERITED`；工具无法设置时记录 `UNSUPPORTED` 和继承回退，不能谎称已应用。
- 精确级别不可用时，选择仍足够完成任务的最低可用级别，并记录期望值、实际值和回退原因。
- 未经用户明确指定，不传 `model`，也不能为了获得某个思考级别自行换模型。
- 在派发和任务板记录期望思考级别、实际思考级别与选择理由。没有 effort 控制的 fork 或内部 subagent 继承运行时默认值。

## Standard 执行事务

1. 记录用户目标、验收标准、权限、相关项目指令和执行位置。
2. 只拆独立工作；每个任务指定一个 owner 和隔离边界。
3. 创建每个用户可见子对话前，在工具支持时选择并应用思考级别；记录继承或不支持回退。
4. 每次异步派发生成 goal/task ID、attempt、dispatch nonce、coordinator epoch、base artifact 和 expected artifact。
5. 使用 `templates/task_dispatch.zh-CN.template.md`；存在多个任务时，把线程、思考级别、分支/worktree、回调和 merge policy 记到 `TASK_BOARD.template.md`。
6. 只有异步/长任务可能在协调者不活跃时完成，才创建 heartbeat。
7. 更新状态前校验回调；缺明确状态或验证时只请求一次状态。
8. 角色终态进入协调者 `IN_REVIEW`；检查范围、diff、验证、风险、分支和精确产物。
9. 针对同一个精确产物派发 QA/Review。代码修复使用新 attempt/nonce，并使旧门禁失效。
10. 退回、升级、取消或验收。声明 merge/push ready 前使用 `templates/merge_readiness.zh-CN.template.md`。
11. 只交付协调者已验收结果、真实验证和遗留风险。

## 状态和门禁

三个维度必须独立：

| 维度 | 值 | 权威方 |
| --- | --- | --- |
| 角色执行 | `TODO`, `IN_PROGRESS`, `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`, `CANCELLED` | 角色 |
| 门禁结论 | `PENDING`, `PASS`, `FAIL`, `BLOCKED`, `WAIVED`, `NOT_APPLICABLE` | QA/Reviewer/协调者 |
| 协调者 | `TODO`, `DISPATCHED`, `IN_PROGRESS`, `IN_REVIEW`, `RETURNED`, `ACCEPTED`, `ESCALATED`, `CANCELLED` | 协调者 |

```text
TODO -> DISPATCHED -> IN_PROGRESS -> IN_REVIEW -> ACCEPTED
                                      |-> RETURNED -> 新 attempt
                                      |-> ESCALATED | CANCELLED
```

`DONE_WITH_CONCERNS`、`BLOCKED`、`NEEDS_CONTEXT`、`CANCELLED` 是角色巡检终态，不是自动成功。

## 版本化回调

异步消息使用 `ORCHESTRATION_EVENT_V1`。完整 schema 在 `templates/coordinator_callback.zh-CN.template.md`，文字摘要不能覆盖机器字段。

身份字段包括：

- goal/task ID、正整数 attempt、dispatch nonce、coordinator epoch；
- 唯一 event ID 和含时区时间；
- 角色与协调者/角色 thread ID；
- base、expected、observed artifact；
- 角色执行状态、门禁结论、协调者状态。

不涉及 Git 时三个 artifact 都用 `NONE`。产物生产角色尚未生成候选时才用 `UNKNOWN`。

处理顺序：

1. 用 `scripts/orchestration_event.py` 校验。
2. 按 `event_id` 去重；`DUPLICATE` 成功 no-op。
3. 比较当前 goal/task、attempt、nonce、epoch 和 expected/observed artifact；不一致为 `STALE`，不能改变当前状态。
4. 原样记录角色状态和门禁结论。
5. 独立推进协调者状态。

交付必须同时满足：协调者 `ACCEPTED`、角色已完成、门禁为 `PASS/WAIVED/NOT_APPLICABLE`、当前产物一致、派发身份有效。`DONE + FAIL`、`DONE + PENDING`、`DONE + IN_REVIEW` 都不是交付。

## Commit 固定门禁

- 工程完成后确定候选 SHA。
- QA/Review 报告同一个 observed SHA。
- 后续任何代码 commit 都使旧结论失效。
- 纯文档变更只有协调者明确记录原因时才可 `WAIVED`，不能静默复用证据。
- 分支名、worktree 路径或“latest”不是产物身份。

使用 `templates/qa_report.zh-CN.template.md`、`templates/review_findings.zh-CN.template.md`、`templates/merge_readiness.zh-CN.template.md`。

## 常见工作流

| 形态 | 顺序 |
| --- | --- |
| 顺序门禁 | 验收标准 -> 工程 -> QA -> Review -> 协调者验收 |
| 并行准备 | 产品/QA/调研只读准备 -> 协调者综合 -> 一个工程任务 |
| 紧急修复 | 窄范围工程修复 -> 受影响回归 -> 协调者验收；不顺手重构 |
| 跨仓库 | 每仓库隔离 owner -> 明确契约摘要 -> 分仓验证 -> 协调者综合 |
| 发布准备 | Release/Docs + QA + Review -> 精确产物门禁 -> 权限检查 -> readiness 报告 |

## Heartbeat 巡检

Heartbeat 是有限期 Standard monitor，不是项目 Autopilot。

- 跟踪当前派发身份和已处理 event ID。
- 每次 recurring tick 用 `scripts/automation_lease.py` 取得 fenced lease；`LEASE_ALREADY_HELD`、`LEASE_BUSY`、过期或被替换 owner 都不能产生副作用。
- 每个 task-attempt-nonce 最多发送一次状态请求。
- 生命周期为 `ACTIVE -> DRAINING -> CLOSED`：所有角色终态后停止请求，只发一次汇总，请求暂停/删除并等待工具确认。
- 使用 `scripts/heartbeat_lifecycle.py`；最终 heartbeat 只把完成工作送入 `IN_REVIEW`，不能写 `ACCEPTED`。

使用 `templates/monitoring_heartbeat.zh-CN.template.md`。没有 automation 工具时按 task board 手动巡检。

## 工具和交付

- 只有用户明确想要可见角色对话时才创建用户线程；工具可用时用 thread 工具。
- 只有用户明确要求 subagent/并行委派且文件 owner 不重叠时，才用内部 subagent。
- 无法回调时要求 `CALLBACK_FAILED: <reason>`，并手动检查角色结果。
- 最终交付包含完成内容、参与者、真实验证、分支/commit/文件、豁免和遗留风险。
- 项目专属服务/API 契约写在目标仓库，不写进通用 skill。

需要跨 tick 持续推进时加载 `PROJECT_AUTOPILOT.zh-CN.md`。使用 `agy` 时只加载对应审查或调研包。
