# 发布指南

发布到 GitHub 前，请使用这份清单检查仓库。

## 准备仓库

```bash
python3 scripts/validate.py
python3 scripts/smoke_test.py
git status --short
```

检查：

- `README.md`
- `README.zh-CN.md`
- `docs/installation.md`
- `docs/installation.zh-CN.md`
- `docs/quickstart.md`
- `docs/quickstart.zh-CN.md`
- `docs/tutorial.md`
- `docs/tutorial.zh-CN.md`
- `docs/examples.md`
- `docs/examples.zh-CN.md`
- `skills/agent-orchestration/SKILL.md`
- `skills/agent-orchestration/references/`

## 创建 GitHub 仓库

创建新的公开仓库后推送：

```bash
git init
git add .
git commit -m "Initial release of agent orchestration skill"
git branch -M main
git remote add origin https://github.com/lixuvip/agent-orchestration-skill.git
git push -u origin main
```

## 建议的仓库元信息

Description:

```text
Run multi-agent workflows in Codex with parallel roles, callbacks, heartbeat checks, and structured task handoffs.
```

Topics:

```text
codex, codex-skill, openai-codex, chatgpt-codex, agent-orchestration, multi-agent, multi-agent-system, multi-agent-orchestration, ai-agents, llm-agents, subagents, agent-workflow, ai-workflow, task-orchestration, task-automation, coding-agent, developer-tools, code-review, qa-workflow, release-management
```

## 发布清单

- [ ] `python3 scripts/validate.py` 通过。
- [ ] `python3 scripts/smoke_test.py` 通过。
- [ ] 安装脚本能在干净 checkout 上运行。
- [ ] README 安装命令指向真实 GitHub URL。
- [ ] 没有私有仓库路径、token、客户数据或组织专属凭据。
- [ ] 中英文文档都能正常链接。
- [ ] License 已包含。
- [ ] 首个版本已打标签，例如 `v0.1.0`。

## 标记版本

```bash
git tag v0.1.0
git push origin v0.1.0
```
