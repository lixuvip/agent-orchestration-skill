# 发布指南

发布到 GitHub 前，请使用这份清单检查仓库。

## 准备仓库

```bash
python3 scripts/validate.py
python3 scripts/smoke_test.py
python3 scripts/forward_test.py
python3 scripts/protocol_test.py
python3 scripts/automation_test.py
python3 scripts/routing_test.py
python3 scripts/scale_test.py
git diff --check
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
Codex skill for role-thread coordination, project autopilot, callbacks, heartbeat/cron automation, QA/review gates, and branch readiness.
```

Topics:

```text
agent-orchestration, agent-skills, agents-md, ai-agents, codex, codex-automations, codex-skill, codex-skills, code-review, git-worktrees, multi-agent, multi-agent-orchestration, project-autopilot, orchestrator, parallel-agents, parallel-coding, qa-workflow, release-management, subagents, task-orchestration
```

## 发布清单

- [ ] `python3 scripts/validate.py` 通过。
- [ ] `python3 scripts/smoke_test.py` 通过。
- [ ] `python3 scripts/forward_test.py` 通过。
- [ ] `python3 scripts/protocol_test.py` 通过。
- [ ] `python3 scripts/automation_test.py` 通过。
- [ ] `python3 scripts/routing_test.py` 通过。
- [ ] `python3 scripts/scale_test.py` 通过。
- [ ] `git diff --check` 通过。
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
