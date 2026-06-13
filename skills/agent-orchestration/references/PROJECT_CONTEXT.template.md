# Project Context

复制本文件为 `PROJECT_CONTEXT.md`，并在每个项目中填写一次。协调者给角色下发任务时，应把相关内容摘入任务上下文。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 项目名称 | `<PROJECT_NAME>` |
| 仓库路径 | `<REPO_PATH>` |
| 默认主分支 | `<MAIN_BRANCH>` |
| 当前工作分支 | `<CURRENT_BRANCH>` |
| 项目负责人 | `<OWNER_OR_COORDINATOR>` |
| 主要用户 | `<TARGET_USERS>` |
| 产品目标 | `<PRODUCT_GOAL>` |

## 技术栈

| 层级 | 技术 |
| --- | --- |
| 前端 | `<FRONTEND_STACK>` |
| 后端 | `<BACKEND_STACK>` |
| 数据库 | `<DATABASE_STACK>` |
| 测试 | `<TEST_STACK>` |
| 构建 / 打包 | `<BUILD_STACK>` |
| 部署 | `<DEPLOY_STACK>` |

## 目录边界

| 路径 | 用途 | 默认角色权限 |
| --- | --- | --- |
| `<PATH_1>` | `<PURPOSE>` | `<READ_ONLY_OR_EDITABLE_BY_ROLE>` |
| `<PATH_2>` | `<PURPOSE>` | `<READ_ONLY_OR_EDITABLE_BY_ROLE>` |
| `<PATH_3>` | `<PURPOSE>` | `<READ_ONLY_OR_EDITABLE_BY_ROLE>` |

## 分支与工作区策略

| 场景 | 策略 |
| --- | --- |
| 产品设计 | `<READ_ONLY_OR_DESIGN_BRANCH>` |
| 技术开发 | `<FEATURE_BRANCH_OR_WORKTREE_RULE>` |
| QA 测试 | `<READ_ONLY_OR_QA_WORKTREE_RULE>` |
| 代码审查 | `<READ_ONLY_RULE>` |
| 发布准备 | `<RELEASE_BRANCH_RULE>` |

## 常用验证命令

按任务范围选择最小必要验证。

```bash
<VERIFY_COMMAND_UNIT_TEST>
```

```bash
<VERIFY_COMMAND_BUILD>
```

```bash
<VERIFY_COMMAND_LINT_OR_FORMAT>
```

## 禁止事项

未经用户明确批准，任何角色都不能执行：

- 粘贴、读取、外传密钥、Token、私有证书、生产凭据。
- 删除数据库、重置仓库、强推、清空缓存等破坏性操作。
- 部署到生产环境。
- 下载超大模型、付费资源或门控资源。
- 修改项目范围之外的文件。
- 修改用户未授权的业务规则、API 合约或数据结构。

## 项目特有注意事项

- `<PROJECT_SPECIFIC_RULE_1>`
- `<PROJECT_SPECIFIC_RULE_2>`
- `<PROJECT_SPECIFIC_RULE_3>`

