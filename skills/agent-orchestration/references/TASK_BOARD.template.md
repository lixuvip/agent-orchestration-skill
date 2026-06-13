# Task Board

复制本文件为 `TASK_BOARD.md`，用于协调者追踪多角色任务状态。

## 状态说明

| 状态 | 含义 |
| --- | --- |
| `TODO` | 尚未派发。 |
| `DISPATCHED` | 已发送给角色，等待回复。 |
| `IN_REVIEW` | 协调者正在检查角色交付。 |
| `RETURNED` | 已退回角色补充或修复。 |
| `BLOCKED` | 被权限、环境、需求或冲突阻塞。 |
| `DONE` | 已验收完成。 |

## 任务表

| Task ID | 标题 | 负责人角色 | 对话 ID | 状态 | 分支 / 工作区 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- |
| `<TASK-001>` | `<TITLE>` | `<ROLE>` | `<THREAD_ID>` | `TODO` | `<BRANCH_OR_WORKTREE>` | `<NEXT_ACTION>` |

## 当前任务详情

### `<TASK-001>` - `<TITLE>`

| 字段 | 内容 |
| --- | --- |
| 目标 | `<GOAL>` |
| 背景 | `<CONTEXT>` |
| 可编辑范围 | `<EDITABLE_SCOPE>` |
| 只读范围 | `<READ_ONLY_SCOPE>` |
| 禁止范围 | `<OUT_OF_SCOPE>` |
| 验收标准 | `<ACCEPTANCE_CRITERIA>` |
| 验证方式 | `<VERIFICATION>` |
| 当前阻塞 | `<BLOCKER_OR_NONE>` |

## 流转记录

| 时间 | 角色 | 状态 | 摘要 | 下一步 |
| --- | --- | --- | --- | --- |
| `<YYYY-MM-DD HH:MM>` | `<ROLE>` | `<STATUS>` | `<SUMMARY>` | `<NEXT_ACTION>` |

