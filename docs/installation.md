# Installation

This repository ships two independent Codex skills:

```text
skills/agent-orchestration
skills/agy-second-opinion
```

## Installer

```bash
git clone https://github.com/lixuvip/codex-agent-orchestration-skill.git
cd codex-agent-orchestration-skill
./scripts/install.sh
```

The default command validates the repository and installs only `agent-orchestration` with provenance and parity checks. Install the external skill separately:

```bash
./scripts/install.sh --skill agy-second-opinion
```

For intentional local development:

```bash
./scripts/install.sh --allow-dirty
./scripts/install.sh --allow-dirty --dry-run
./scripts/install.sh --skill agy-second-opinion --allow-dirty
```

Restore the retained previous copy for one selected skill:

```bash
./scripts/install.sh --restore
./scripts/install.sh --skill agy-second-opinion --restore
```

The default target is `${CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}`.

## Install only one skill manually

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/agent-orchestration "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Or copy `skills/agy-second-opinion` instead. A repo-scoped install can place either folder under `.agents/skills/`.

## Verify

Start a new Codex task and invoke one skill explicitly:

```text
Use $agent-orchestration for one bounded internal subagent.
Use $agy-second-opinion for one explicit agy review.
```

If discovery is stale, restart Codex and confirm each installed `SKILL.md` exists.
