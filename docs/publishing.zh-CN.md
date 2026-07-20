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
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/agent-orchestration
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/agy-second-opinion
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
- `docs/design-notes-v0.3.0.zh-CN.md`
- `skills/agent-orchestration/SKILL.md`
- `skills/agent-orchestration/references/`
- `skills/agy-second-opinion/SKILL.md`
- `skills/agy-second-opinion/references/`

## 创建 GitHub 仓库

创建新的公开仓库后推送：

```bash
git init
git add .
git commit -m "Initial release of agent orchestration skill"
git branch -M main
git remote add origin https://github.com/lixuvip/codex-agent-orchestration-skill.git
git push -u origin main
```

## 建议的仓库元信息

Description:

```text
Lightweight native-first Codex orchestration plus an independent opt-in agy/Gemini second-opinion skill.
```

Topics:

```text
agent-orchestration, agent-skills, ai-agents, codex, codex-automations, codex-skill, codex-skills, code-review, gemini, git-worktrees, multi-agent, orchestrator, parallel-agents, qa-workflow, subagents, task-orchestration
```

## 发布清单

- [ ] `python3 scripts/validate.py` 通过。
- [ ] `python3 scripts/smoke_test.py` 通过。
- [ ] `python3 scripts/forward_test.py` 通过。
- [ ] `python3 scripts/protocol_test.py` 通过。
- [ ] `python3 scripts/automation_test.py` 通过。
- [ ] `python3 scripts/routing_test.py` 通过。
- [ ] `python3 scripts/scale_test.py` 通过。
- [ ] 内置 skill 校验通过。
- [ ] `git diff --check` 通过。
- [ ] `./scripts/install.sh` 和 `./scripts/install.sh --skill agy-second-opinion` 都能从干净发布 commit 运行，并报告 `source_dirty=false`。
- [ ] 已验证两个独立 skill 的本机安装副本都与仓库一致。
- [ ] README 安装命令指向真实 GitHub URL。
- [ ] 没有私有仓库路径、token、客户数据或组织专属凭据。
- [ ] 中英文文档都能正常链接。
- [ ] 每项外部启发都记录准确来源/commit、本地改造方式，以及明确没有复制或采用的内容。
- [ ] License 已包含。
- [ ] 发布分支和 `main` 指向预期发布 commit。
- [ ] 分支与 `main` 的 CI 在打 tag 前均通过。
- [ ] Release tag 和 GitHub Release 指向同一个 commit。

## 发布版本

使用语义化版本号和同名发布说明文件。例如：

```bash
VERSION=v0.2.1
RELEASE_BRANCH=codex/orchestration-reliability

git push origin "$RELEASE_BRANCH"
git switch main
git merge --ff-only "$RELEASE_BRANCH"
git push origin main
```

等待发布分支和 `main` 的验证工作流通过，再给 `main` 的精确 commit 打 tag 并发布对应说明：

```bash
git tag -a "$VERSION" -m "$VERSION"
git push origin "$VERSION"
gh release create "$VERSION" --title "$VERSION — Adaptive Role Threads" --notes-file "docs/releases/$VERSION.md" --verify-tag
```

最后显式核验远端和本机状态：

```bash
gh release view "$VERSION"
gh run list --limit 10
git ls-remote --heads --tags origin
./scripts/install.sh
git status --short
```

发布 commit 不干净、安装一致性未通过，或者分支/main CI 未通过时，不要创建 tag。
