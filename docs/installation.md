# Installation

This repository ships a single Codex skill:

```text
skills/agent-orchestration
```

Codex skills are folders that contain a `SKILL.md` file and optional resources such as references, scripts, assets, and UI metadata. This skill includes references and templates for multi-role thread coordination.

For the current Codex skill structure and supported skill locations, see the official [Agent Skills documentation](https://developers.openai.com/codex/skills).

## Option 1: Install From Git

```bash
git clone https://github.com/<your-org>/agent-orchestration-skill.git
cd agent-orchestration-skill
./scripts/install.sh
```

The script installs the skill to:

```text
${CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}/agent-orchestration
```

## Option 2: Manual Install

```bash
git clone https://github.com/<your-org>/agent-orchestration-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R agent-orchestration-skill/skills/agent-orchestration "${CODEX_HOME:-$HOME/.codex}/skills/"
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

## Update

Pull the latest repository changes and reinstall:

```bash
git pull
./scripts/install.sh
```

The installer replaces the previously installed `agent-orchestration` folder.
