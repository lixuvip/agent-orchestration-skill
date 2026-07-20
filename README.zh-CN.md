# Codex Agent Orchestration Skills

本仓库现在提供两个互相独立的 Codex skill：

- `agent-orchestration`：面向 Codex 任务、内部子 Agent、用户可见任务、worktree、正式门禁和周期自动化的轻量原生编排。
- `agy-second-opinion`：只有用户明确要求时，才通过本机 `agy` 运行只读外部审查或调研。

两者不会互相加载或依赖。普通委派不会探测 `agy`，外部第二意见也不会自动启动编排流程。

[English](README.md)

## 主 skill 为什么更轻

可安装的 `agent-orchestration` 运行包只剩 6 个文件：一个入口、一份 UI metadata，以及精简的中英文协调与自动化参考。

默认路径是：

1. 单 owner 工作留在当前任务。
2. 需要一个有边界的独立结果时，使用内部子 Agent，结果回到当前协调者。
3. 只有需要侧边栏独立可见或用户直接后续交流时，才创建用户自有任务。
4. 只有多 owner、跨仓库/worktree 或正式 QA/Review/Release 门禁，才读取协调参考。
5. 只有必须跨越当前 turn 的周期或延迟工作，才读取自动化参考。

生命周期和状态完全依赖 Codex 原生能力，不再安装回调 JSON、task board、自定义 heartbeat、lease、角色目录或路由脚本。

## v0.3.0 可靠性增强

- 派发前预检每个 owner 真正需要的能力和权限。
- 默认保持扁平委派；用户中途转向后，旧范围结果自动视为过期。
- 使用按任务类型定义的证据契约、需求到证据闭环、有界重试和最终活跃工作盘点。
- 修正交回原 owner 继续，独立 Reviewer 则只接收新上下文和原始产物。
- 在 fork、handoff、长暂停或依赖上下文的继续工作前保留精简恢复胶囊。
- Best-of-N 只用于明确要求或真正高歧义的工作，候选隔离，并允许全部拒绝。

[v0.3.0 设计溯源说明](docs/design-notes-v0.3.0.zh-CN.md)逐项列出了参考的 Grok Build 文件，以及这些思路如何基于 Codex 原生任务、子 Agent、worktree 和 automation 重新设计。本版本没有把 Grok Build 的代码或 prompt 打包进来。

## 执行面选择

| 需求 | 执行面 |
| --- | --- |
| 一个 owner、一个交付 | 当前任务 |
| 独立分析，结果回到这里 | 内部子 Agent |
| 侧边栏独立可见或用户直接跟进 | 用户自有任务 |
| 带着已完成历史进入新任务 | Fork |
| 隔离仓库写入 | Worktree 任务 |
| 同一个任务在 Local/Worktree 间移动 | Handoff |
| 周期或延迟继续 | 原生 automation |
| 明确要求外部模型第二意见 | `agy-second-opinion` |

委派前，协调者会说明是否出现侧边栏新任务、结果回到哪里、后续由谁负责。

## 安装

```bash
git clone https://github.com/lixuvip/codex-agent-orchestration-skill.git
cd codex-agent-orchestration-skill
./scripts/install.sh
```

默认安装器只验证并安装轻量编排 skill。本地 dirty 开发版本使用：

```bash
./scripts/install.sh --allow-dirty
```

独立 AGY skill 需要显式安装：

```bash
./scripts/install.sh --skill agy-second-opinion --allow-dirty
```

手动安装时，也可以只复制 `skills/` 下需要的那个 skill。

## 示例

轻量内部委派：

```text
使用 $agent-orchestration。让一个内部子 Agent 只读检查认证链路，把证据返回当前任务。
```

创建用户可见的独立任务：

```text
使用 $agent-orchestration。为发布审计创建一个用户自有任务，并说明后续在哪个任务继续。
```

明确要求外部第二意见：

```text
使用 $agy-second-opinion，通过 agy 对当前 diff 做一次有边界的只读审查，再由 Codex 验证每条采纳结论。
```

## 开发验证

```bash
python3 scripts/validate.py
python3 scripts/smoke_test.py
python3 scripts/forward_test.py
python3 scripts/protocol_test.py
python3 scripts/automation_test.py
python3 scripts/routing_test.py
python3 scripts/scale_test.py
git diff --check
```

更多内容见[快速开始](docs/quickstart.zh-CN.md)、[示例](docs/examples.zh-CN.md)、[安装说明](docs/installation.zh-CN.md)、[前向测试](docs/forward-tests.md)和 [v0.3.0 设计溯源](docs/design-notes-v0.3.0.zh-CN.md)。
