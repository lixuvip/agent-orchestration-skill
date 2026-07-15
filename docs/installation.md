# Installation

This repository ships a single Codex skill:

```text
skills/agent-orchestration
```

Codex skills are folders that contain a `SKILL.md` file and optional resources such as references, scripts, assets, and UI metadata. This skill includes references and templates for multi-role thread coordination.

For the current Codex skill structure and supported skill locations, see the official [Agent Skills documentation](https://developers.openai.com/codex/skills).

## Option 1: Install From Git

```bash
git clone https://github.com/lixuvip/codex-agent-orchestration-skill.git
cd codex-agent-orchestration-skill
./scripts/install.sh
```

The script installs the skill to:

```text
${CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}/agent-orchestration
```

Before replacement, the installer runs repository, smoke, forward, protocol, concurrency/lifecycle, routing, skill-creator, and diff checks; refuses a dirty skill source by default; stages and verifies the new copy; records a provenance manifest beside the installed skill; and retains the previous installation for rollback.

For an intentional local development install:

```bash
./scripts/install.sh --allow-dirty
```

Preview without changing the installed copy:

```bash
./scripts/install.sh --allow-dirty --dry-run
```

Restore the retained previous installation:

```bash
./scripts/install.sh --restore
```

## Option 2: Manual Install

Manual copying skips validation, provenance, and rollback. Prefer the installer unless those guarantees are intentionally unnecessary.

```bash
git clone https://github.com/lixuvip/codex-agent-orchestration-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R codex-agent-orchestration-skill/skills/agent-orchestration "${CODEX_HOME:-$HOME/.codex}/skills/"
```

If your Codex installation scans `$HOME/.agents/skills`, run:

```bash
CODEX_SKILLS_DIR="$HOME/.agents/skills" ./scripts/install.sh
```

## Option 3: Repo-Scoped Install

If you want the skill to apply only to one repository, copy it into that repository's `.agents/skills` folder:

```bash
mkdir -p /path/to/your/repo/.agents/skills
cp -R skills/agent-orchestration /path/to/your/repo/.agents/skills/
```

This is useful when a team wants to version the skill with a project.

## Verify Installation

Start a new Codex session and invoke:

```text
Use $agent-orchestration to create a two-role plan for a small bug fix.
```

If the skill is not detected, restart Codex and verify that this file exists:

```text
${CODEX_HOME:-$HOME/.codex}/skills/agent-orchestration/SKILL.md
```

For `$HOME/.agents/skills` installs, check:

```text
$HOME/.agents/skills/agent-orchestration/SKILL.md
```

## Optional: Add Project Guidance

Project Autopilot works best when the target repository has durable Codex guidance.

Use `AGENTS.md` for stable project rules:

```markdown
# AGENTS.md

## Repository Expectations

- Run the documented test command before claiming release readiness.
- Ask before merge, push, deploy, destructive changes, or public API contract changes.
- Keep temporary automation state in automation memory, not in this file.
```

Use nested `AGENTS.override.md` files only when a subdirectory needs stronger local rules. Use `.codex/config.toml` for Codex configuration such as fallback instruction filenames; do not store secrets or live task state there.

## Update

Pull the latest repository changes and reinstall:

```bash
git pull
./scripts/install.sh
```

The installer stages the new copy, keeps the prior version under the skills root, and verifies source/install parity before reporting success.
