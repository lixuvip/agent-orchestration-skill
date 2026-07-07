# Publishing Guide

Use this checklist before publishing the repository to GitHub.

## Prepare The Repository

```bash
python3 scripts/validate.py
python3 scripts/smoke_test.py
python3 scripts/forward_test.py
git status --short
```

Review:

- `README.md`
- `docs/installation.md`
- `docs/quickstart.md`
- `docs/tutorial.md`
- `docs/examples.md`
- `skills/agent-orchestration/SKILL.md`
- `skills/agent-orchestration/references/`

## Create A GitHub Repository

Create a new public repository, then push:

```bash
git init
git add .
git commit -m "Initial release of agent orchestration skill"
git branch -M main
git remote add origin https://github.com/lixuvip/agent-orchestration-skill.git
git push -u origin main
```

## Suggested Repository Metadata

Description:

```text
Codex skill for role-thread coordination, project autopilot, callbacks, heartbeat/cron automation, QA/review gates, and branch readiness.
```

Topics:

```text
agent-orchestration, agent-skills, agents-md, ai-agents, codex, codex-automations, codex-skill, codex-skills, code-review, git-worktrees, multi-agent, multi-agent-orchestration, project-autopilot, orchestrator, parallel-agents, parallel-coding, qa-workflow, release-management, subagents, task-orchestration
```

## Release Checklist

- [ ] `python3 scripts/validate.py` passes.
- [ ] `python3 scripts/smoke_test.py` passes.
- [ ] `python3 scripts/forward_test.py` passes.
- [ ] Installation script works on a clean checkout.
- [ ] README installation command points to the real GitHub URL.
- [ ] No private repository paths, tokens, or customer data are present.
- [ ] English and Chinese documentation links are valid.
- [ ] License is included.
- [ ] First release is tagged, for example `v0.1.0`.

## Tag A Release

```bash
git tag v0.1.0
git push origin v0.1.0
```
