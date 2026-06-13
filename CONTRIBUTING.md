# Contributing

Contributions should keep the skill focused on one job: coordinating Codex role threads and handoffs.

## Development

Run validation before opening a pull request:

```bash
python3 scripts/validate.py
```

If available, also run Codex's skill validator:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/agent-orchestration
```

## Guidelines

- Keep `skills/agent-orchestration/SKILL.md` concise.
- Put detailed templates and long workflow docs in `references/`.
- Do not add private project paths, tokens, customer data, or organization-specific credentials.
- Prefer explicit status, verification, and risk reporting over vague completion language.
- Add examples when changing behavior that users need to learn.

