# Workflows

本文件定义通用角色编排的几种运行模式。

## 1. 顺序门禁模式

适合用户可见功能、共享代码、架构变更或风险较高的需求。

```text
用户需求
-> 协调者拆解
-> 产品设计师定义验收标准
-> 协调者收窄工程范围
-> 技术工程师实现
-> 协调者检查 diff 和验证结果
-> QA 测试
-> 协调者检查测试报告
-> 代码审查
-> 协调者最终验收
-> 交付用户
```

门禁规则：

- 产品验收标准不清楚，不进入工程实现。
- 工程未交付验证结果，不进入 QA。
- QA 有阻塞缺陷，不进入最终审查。
- Reviewer 有高优先级问题，不交付用户。

## 2. 并行准备模式

适合需求还在梳理阶段，多个角色可以无冲突准备材料。

可并行的任务：

- 产品设计师输出用户流程和验收标准。
- QA 输出测试矩阵。
- 技术工程师做实现可行性调研，但不改代码。
- Reviewer 阅读相关历史设计或风险点。

协调者拿到结果后，合并成一个明确工程任务。

## 3. 工程实现模式

适合已经有清晰验收标准的开发任务。

流程：

1. 协调者给工程师发送任务。
2. 工程师实现并运行最小必要验证。
3. 工程师按模板回复。
4. 协调者检查 diff、范围和验证。
5. 通过后交给 QA。

工程任务必须包含：

- 可编辑文件。
- 禁止修改文件。
- 目标行为。
- 测试命令。
- 退出条件。

## 4. QA 回归模式

适合工程已完成后验证。

流程：

1. 协调者把工程交付摘要发给 QA。
2. QA 根据验收标准执行测试。
3. QA 报告通过项、失败项、未测项和复现步骤。
4. 协调者判断是否退回工程修复。

QA 不应只说“测试通过”，必须说明测了什么、怎么测、结果是什么。

## 5. 紧急修复模式

适合小范围、高确定性的 bug。

```text
协调者定位问题范围
-> 工程师窄范围修复
-> QA 验证受影响行为
-> 协调者交付
```

限制：

- 不做顺手重构。
- 不扩大产品范围。
- 不引入新依赖，除非用户批准。
- 修复后必须有最小验证。

## 6. 发布准备模式

适合准备版本交付。

流程：

1. Release / Docs 汇总变更。
2. QA 确认关键路径测试状态。
3. Reviewer 确认无阻塞风险。
4. 协调者生成发布说明和剩余风险。

发布前必须明确：

- 版本范围。
- 已知问题。
- 验证命令和结果。
- 是否需要迁移、配置、权限或用户手动操作。

## 7. 多线程巡检模式

适合协调者同时派发多个项目、多个仓库或多个角色对话的任务。

流程：

1. 协调者为每个角色创建或选择对话。
2. 协调者记录角色、职责、仓库路径、分支和对话 ID。
3. 协调者在任务中要求角色完成后向协调者对话回调。
4. 协调者创建 5 分钟巡检自动化，使用 `templates/monitoring_heartbeat.template.md`。
5. 巡检每次读取所有角色对话，并只接受显式终态。
6. 所有角色进入终态后，巡检发送汇总并关闭自身。
7. 协调者读取汇总，做最终验收，再交付用户。

判定规则：

- `DONE` 表示可进入协调者验收。
- `DONE_WITH_CONCERNS` 表示可汇总但必须保留风险。
- `BLOCKED` 和 `NEEDS_CONTEXT` 表示不能继续假设完成，必须解决阻塞或升级用户。
- 没有显式终态的对话，不得按完成处理。

## 8. 项目 Autopilot 模式

适合用户要求“持续推进项目直到目标完成”“定时自动继续处理”“一直做到目标效果”的任务。

流程：

1. 协调者读取 `PROJECT_AUTOPILOT.md`。
2. 协调者按 `PROJECT_INSTRUCTIONS_DISCOVERY.md` 读取目标项目的 `AGENTS.md` / `AGENTS.override.md`、项目文档、issue/PR/release 来源和验证命令。
3. 协调者用 `templates/project_goal_contract.template.md` 明确目标、完成条件、自动权限、确认门禁、频率、预算和停止条件。
4. 协调者按 `AUTOMATION_TOOLING.md` 检查现有 automation，避免重复创建。
5. 协调者用 `templates/automation_plan.template.md` 选择 heartbeat 或 cron。当前线程短期回访用 heartbeat；workspace/worktree 持续推进用 cron。
6. 自动化每次 tick 使用 `templates/automation_tick.template.md`，只做一个安全下一步。
7. 自动化每次 tick 更新 `templates/automation_memory.template.md`，避免重复评论、重复状态请求或重复工作。
8. 目标达成后发送最终摘要并暂停或删除自动化；缺权限、反复失败或超范围时用 `templates/escalation_report.template.md` 升级给用户。

判定规则：

- `AGENTS.md` 存稳定项目规则；automation memory 存临时目标状态。
- 自动化必须比较 latest effective update，不能只看更新时间。
- 不得默认 merge、push、deploy、publish、删除数据、轮换密钥、产生费用或扩大范围。

## 9. 外部模型审查辅助模式

适合用户明确要求使用 `agy`、Gemini、Antigravity 或其他外部模型做代码审查，或者协调者需要在 Codex reviewer 之外增加一个只读第二意见。

流程：

1. 协调者读取 `AGY_GEMINI_REVIEW.md`。
2. 协调者按目标项目 `AGENTS.md` 和隐私规则确认哪些 diff 可以发给外部模型。
3. 外部审查默认不改目标仓库。`scripts/ensure_agy_review_agents_guidance.py --project-root <项目根目录>` 默认只检查；缺少持久规则不阻断一次性审查。只有用户另行授权写入稳定项目指令时，才加 `--write` 更新根目录 `AGENTS.md`。
4. 协调者使用 `templates/agy_gemini_review_prompt.template.md` 或中文版本构造只读审查 prompt。
5. `agy` 只通过 `scripts/run_agy_print.py` 的固定 `--sandbox` 路径运行；helper 不提供 `accept-edits` 或关闭 sandbox 的入口，并额外执行宿主超时和输出上限。工具探测只允许 `command -v agy` 和 `agy models`。diff-only 审查直接把有界 diff 放进 prompt；需要源码时先用 `scripts/build_agy_context_bundle.py` 建立 allowlist bundle，再把 bundle 传给 `--add-dir`。只有用户明确批准整仓披露时才能挂载项目根目录。
6. 如果用户要求对比、审查范围是全项目、或变更足够宽，协调者同时启动 Codex reviewer 角色，形成 dual Codex + Gemini review；两个审查互相独立，直到都返回或进入终态。
7. 审查返回后，协调者使用 `templates/agy_gemini_review_quality.template.md` 或同等检查评估质量。
8. 协调者逐条复核外部 findings，标记为 `valid`、`partially_valid`、`not_supported` 或 `needs_human_check`；高严重度 finding 必须有源码行号和反证检查。
9. 协调者使用 `templates/agy_gemini_review_report.template.md` 或中文版本展示专属审查报告，并包含共同命中、Gemini-only、Codex-only、被驳回 finding 和验证对比。
10. 协调者使用质量日志模板准备 JSON，再运行 `scripts/append_agy_review_quality_log.py --project-root <项目根目录>`；默认写入 `$CODEX_HOME/external-review-ledger/`，不改变目标仓库。项目内日志必须显式指定路径并加 `--allow-project-write`。只有看到 `LOG_WRITTEN <path>` 或 `LOG_ALREADY_PRESENT <path>` 才能声明日志已持久化。
11. 只有经协调者验证的 findings 才能进入 QA、修复或合并就绪判断。

判定规则：

- 外部模型输出不是验证结果；测试是否通过只能来自实际命令输出。
- `TIMED_OUT`、`SCOPE_DRIFT`、`NO_STRUCTURED_OUTPUT` 等失败状态不能当作已审查；`exit 0` 但 0 输出也属于失败。
- 更重模型不是自动更可靠。模型选择必须记录，findings 必须复核。
- 审查内容默认以专属报告展示，不依赖底部终端可见性。
- 模板优化默认阶段性处理：累计约 5 条质量日志、完成一次全项目基线审查，或发现重复误报/遗漏后，再统一调整 prompt、模型选择或审查范围。

## 10. 外部模型并行调研模式

适合用户明确要求使用 `agy`、Gemini、Antigravity 或其他外部模型做调研、方案扩展、仓库盘点，或者协调者希望在 Codex 自己调研的同时再跑一个外部只读研究流。

流程：

1. 协调者读取 `AGY_GEMINI_RESEARCH.md`。
2. 协调者按目标项目 `AGENTS.md` 和隐私规则确认哪些 repo 上下文、文档和外部事实可以发给外部模型。
3. 外部调研默认不改目标仓库。持久规则 helper 默认只检查；只有用户另行授权稳定项目指令写入时才使用 `--write`。
4. 协调者自己做一轮 Codex 调研，必要时补充源码阅读、项目文档和外部一手资料。
5. 协调者构造有界外部调研 prompt 并通过 `scripts/run_agy_print.py` 执行；工具探测只允许 `command -v agy` 和 `agy models`。需要源码时先用 allowlist bundle，再传给 `--add-dir`；结构化输出优先加 `--expect-substring AGY_RESEARCH_V1`。
6. Codex 调研流和 Gemini 调研流保持独立，直到两边都返回或一边进入终态失败。
7. 协调者使用 `templates/agy_gemini_research_quality.template.md` 或同等检查评估外部调研质量。
8. 协调者逐条复核外部观点，标记为 `accepted`、`partially_accepted`、`speculative` 或 `rejected`；涉及当前外部事实的观点必须由 Codex 用一手来源额外核验。
9. 协调者使用 `templates/agy_gemini_research_report.template.md` 或中文版本展示专属调研报告，并包含共同观点、Gemini-only、Codex-only、被驳回观点和下一步建议。
10. 协调者准备质量日志 JSON，并通过 helper 写入默认 Codex 外部任务台账；调研场景把 `task_type` 设为 `research`。项目内日志仍需单独授权。只有看到 `LOG_WRITTEN` 或 `LOG_ALREADY_PRESENT` 才能声明日志已持久化。
11. 外部调研结果只能作为协调者综合判断的输入，不能代替 Codex 的源码阅读、Web 核验和最终结论。

判定规则：

- 时间敏感或高风险外部事实仍由 Codex 负责浏览和核验，外部模型只能作为补充视角。
- `TIMED_OUT`、`SCOPE_DRIFT`、`NO_STRUCTURED_OUTPUT` 等失败状态不能当作已完成调研。
- 调研内容默认以专属报告展示，不依赖底部终端可见性。
- 模板优化默认阶段性处理：累计约 5 条质量日志、完成一次全项目基线调研，或发现重复低价值输出后，再统一调整 prompt、模型选择或范围。
