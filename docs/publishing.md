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
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/agy-second-opinion
git diff --check
git status --short
```

Review:

- `README.md`
- `docs/installation.md`
- `docs/quickstart.md`
- `docs/tutorial.md`
- `docs/examples.md`
- `docs/design-notes-v0.3.0.md`
- `skills/agent-orchestration/SKILL.md`
- `skills/agent-orchestration/references/`
- `skills/agy-second-opinion/SKILL.md`
- `skills/agy-second-opinion/references/`

## Create A GitHub Repository

Create a new public repository, then push:

```bash
git init
git add .
git commit -m "Initial release of agent orchestration skill"
git branch -M main
git remote add origin https://github.com/lixuvip/codex-agent-orchestration-skill.git
git push -u origin main
```

## Suggested Repository Metadata

Description:

```text
Lightweight native-first Codex orchestration plus an independent opt-in agy/Gemini second-opinion skill.
```

Topics:

```text
agent-orchestration, agent-skills, ai-agents, codex, codex-automations, codex-skill, codex-skills, code-review, gemini, git-worktrees, multi-agent, orchestrator, parallel-agents, qa-workflow, subagents, task-orchestration
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
- [ ] `./scripts/install.sh` and `./scripts/install.sh --skill agy-second-opinion` work from the clean release commit and report `source_dirty=false`.
- [ ] Installed parity is verified for both independent skills.
- [ ] README installation command points to the real GitHub URL.
- [ ] No private repository paths, tokens, or customer data are present.
- [ ] English and Chinese documentation links are valid.
- [ ] Any externally inspired behavior has an exact source/commit link, a local-adaptation explanation, and an explicit statement of what was not copied or adopted.
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
