# Role Registry

复制本文件为 `ROLE_REGISTRY.md`，填写真实对话 ID。每次启用一个角色前，协调者必须确认该对话的项目、分支、工作区和运行状态。

## 角色登记表

| 角色 | 对话 ID | 工作模式 | 职责 | 边界 | 当前状态 |
| --- | --- | --- | --- | --- | --- |
| Coordinator / PM | 当前对话 | 主控对话 | 拆解任务、分配角色、检查交付、最终验收。 | 不发布未验证结果；不合并不明来源改动。 | Active |
| Product Designer | `<PRODUCT_THREAD_ID>` | 只读或设计分支 | 需求澄清、用户流程、交互状态、验收标准。 | 不直接实现生产代码；不擅自改 API 合约。 | `<ACTIVE_OR_INACTIVE>` |
| Technical Engineer | `<ENGINEER_THREAD_ID>` | 独立 worktree / 功能分支 | 实现代码、补测试、跑验证、提交工程交付。 | 只改任务指定范围；不擅自扩大需求。 | `<ACTIVE_OR_INACTIVE>` |
| QA Tester | `<QA_THREAD_ID>` | 只读 checkout 或 QA worktree | 执行测试、复现缺陷、报告阻塞。 | 默认不修代码；不改变实现。 | `<ACTIVE_OR_INACTIVE>` |
| Code Reviewer | `<REVIEW_THREAD_ID>` | 只读 checkout | 审查 diff、找风险、评估测试缺口。 | 默认只评论不改代码。 | `<ACTIVE_OR_INACTIVE>` |
| Release / Docs | `<RELEASE_THREAD_ID>` | 发布分支或文档分支 | 更新 changelog、用户文档、发布检查清单。 | 不修改功能实现。 | `<ACTIVE_OR_INACTIVE>` |

## 角色启用检查

启用角色前，协调者应确认：

- 对话 ID 是否正确。
- 对话是否在目标项目中。
- 对话是否正在运行任务。
- 对话所在分支或 worktree 是否符合角色职责。
- 对话是否有未提交改动。
- 该角色是否需要只读、可编辑、或独立分支权限。

## 角色状态

| 状态 | 含义 |
| --- | --- |
| `ACTIVE` | 可接收任务。 |
| `BUSY` | 正在执行任务，暂不派发新任务。 |
| `BLOCKED` | 等待上下文、权限或环境修复。 |
| `PAUSED` | 暂停使用。 |
| `RETIRED` | 不再用于当前项目。 |

