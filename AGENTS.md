# AGENTS.md

## Repository Expectations

- Keep the installable skill under `skills/agent-orchestration`; keep human-facing docs, examples, release notes, CI, and installer scripts at the repository root.
- After changing the skill, run `python3 scripts/validate.py`, `python3 scripts/smoke_test.py`, `python3 scripts/forward_test.py`, `python3 scripts/protocol_test.py`, `python3 scripts/automation_test.py`, `python3 scripts/routing_test.py`, `python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/agent-orchestration`, and `git diff --check`.
- Run `./scripts/install.sh --allow-dirty` after validated behavior changes so the local Codex skill copy stays in sync during development. The installer records provenance, retains the previous copy, and verifies parity; use `./scripts/install.sh --restore` to roll back.
- Update `README.md`, `README.zh-CN.md`, `docs/examples.md`, `docs/examples.zh-CN.md`, and `CHANGELOG.md` when a user-visible workflow changes.
- Do not publish a release, push, merge, or edit GitHub repository metadata unless the user asks for that explicitly.

## Skill Authoring Rules

- Keep `SKILL.md` concise and route detailed workflow logic to direct reference files.
- Make every new reference discoverable from `SKILL.md` or `skills/agent-orchestration/references/README.md`.
- Add validator and smoke-test coverage for new required templates or workflow states.
- Prefer templates for repeatable prompts and reports instead of duplicating long instructions in prose.
- Preserve bilingual coverage when a workflow is likely to be used by Chinese-only teams.
