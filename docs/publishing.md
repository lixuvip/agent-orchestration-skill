# Publishing Guide

Use this checklist before publishing the repository to GitHub.

## Prepare The Repository

```bash
python3 scripts/validate.py
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
git remote add origin https://github.com/<your-org>/agent-orchestration-skill.git
git push -u origin main
```

## Suggested Repository Metadata

Description:

```text
A Codex skill for coordinating multi-role agent threads, callbacks, and heartbeat monitoring.
```

Topics:

```text
codex, codex-skill, agent-orchestration, ai-agents, workflow, automation
```

## Release Checklist

- [ ] `python3 scripts/validate.py` passes.
- [ ] Installation script works on a clean checkout.
- [ ] README installation command points to the real GitHub URL.
- [ ] No private repository paths, tokens, or customer data are present.
- [ ] License is included.
- [ ] First release is tagged, for example `v0.1.0`.

## Tag A Release

```bash
git tag v0.1.0
git push origin v0.1.0
```

