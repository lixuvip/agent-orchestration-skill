# Publishing Guide

Use this checklist before publishing the repository to GitHub.

## Prepare The Repository

```bash
python3 scripts/validate.py
python3 scripts/smoke_test.py
python3 scripts/forward_test.py
python3 scripts/protocol_test.py
python3 scripts/automation_test.py
python3 scripts/routing_test.py
python3 scripts/scale_test.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/agent-orchestration
git diff --check
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
Progressive Codex orchestration with adaptive per-thread thinking, callbacks, QA/review gates, fenced automations, project autopilot, and optional agy/Gemini review.
```

Topics:

```text
agent-orchestration, agent-skills, agents-md, ai-agents, codex, codex-automations, codex-skill, codex-skills, code-review, git-worktrees, multi-agent, multi-agent-orchestration, project-autopilot, orchestrator, parallel-agents, parallel-coding, qa-workflow, release-management, subagents, task-orchestration
```

## Release Checklist

- [ ] `python3 scripts/validate.py` passes.
- [ ] `python3 scripts/smoke_test.py` passes.
- [ ] `python3 scripts/forward_test.py` passes.
- [ ] `python3 scripts/protocol_test.py` passes.
- [ ] `python3 scripts/automation_test.py` passes.
- [ ] `python3 scripts/routing_test.py` passes.
- [ ] `python3 scripts/scale_test.py` passes.
- [ ] Built-in skill validation passes.
- [ ] `git diff --check` passes.
- [ ] `./scripts/install.sh` works from the clean release commit and reports `source_dirty=false`.
- [ ] Installed skill parity is verified.
- [ ] README installation command points to the real GitHub URL.
- [ ] No private repository paths, tokens, or customer data are present.
- [ ] English and Chinese documentation links are valid.
- [ ] License is included.
- [ ] Release branch and `main` point to the intended release commit.
- [ ] Branch and `main` CI runs pass before tagging.
- [ ] The release tag and GitHub Release point to the same commit.

## Publish A Release

Use a semantic version and a matching release-note file. Example:

```bash
VERSION=v0.2.1
RELEASE_BRANCH=codex/orchestration-reliability

git push origin "$RELEASE_BRANCH"
git switch main
git merge --ff-only "$RELEASE_BRANCH"
git push origin main
```

Wait for the branch and `main` validation runs to pass. Then tag the exact `main` commit and publish the matching notes:

```bash
git tag -a "$VERSION" -m "$VERSION"
git push origin "$VERSION"
gh release create "$VERSION" --title "$VERSION — Adaptive Role Threads" --notes-file "docs/releases/$VERSION.md" --verify-tag
```

Finish with explicit remote and local verification:

```bash
gh release view "$VERSION"
gh run list --limit 10
git ls-remote --heads --tags origin
./scripts/install.sh
git status --short
```

Do not publish the tag until the release commit is clean, installed parity passes, and branch/main CI is green.
