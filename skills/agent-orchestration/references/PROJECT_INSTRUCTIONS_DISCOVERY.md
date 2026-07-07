# Project Instructions Discovery

Use this reference when orchestration or Project Autopilot needs durable project rules.

## Sources To Inspect

Read the narrowest relevant instruction sources before creating goals, dispatching roles, or enabling recurring automation:

1. `AGENTS.md` at the target repository root.
2. Nested `AGENTS.md` files that apply to the target subdirectory.
3. `AGENTS.override.md` files when present; treat them as stronger local rules.
4. Fallback instruction filenames configured in Codex config, when known.
5. `.codex/config.toml` for Codex configuration only.
6. Project docs such as `README.md`, `CONTRIBUTING.md`, issue templates, PR templates, release docs, and test docs.

Do not store live task state, secrets, or automation memory in `AGENTS.md` or `.codex/config.toml`.

## What Belongs In AGENTS.md

Use `AGENTS.md` for stable instructions:

- build and test commands;
- branch, worktree, commit, merge, push, and deploy rules;
- read-only areas and forbidden files;
- review and QA expectations;
- project-specific stop conditions;
- automation escalation rules;
- preferred issue/PR communication channels.

## What Belongs In Automation Memory

Use automation memory for temporary state:

- latest effective update;
- last action and verification;
- blocker history;
- posted messages and comment markers;
- current next safe action;
- run counters, attempt limits, and unresolved questions.

## When To Suggest An Update

Suggest an `AGENTS.md` change when:

- automation repeatedly rediscovers the same command or rule;
- the same review feedback appears across runs;
- a coordinator has to restate branch or push policy repeatedly;
- a project lacks clear verification or escalation rules;
- a user asks to make behavior persistent.

Do not edit `AGENTS.md` silently when the instruction is temporary, contested, or tied to one task.

## Discovery Report

When instructions are material, include this summary in the coordinator plan:

```text
Project instruction discovery
- AGENTS.md: <FOUND_PATH_OR_NONE>
- AGENTS.override.md: <FOUND_PATH_OR_NONE>
- Codex config: <FOUND_PATH_OR_NONE>
- Project docs read: <LIST>
- Stable rules found: <SUMMARY>
- Missing rules worth codifying: <LIST_OR_NONE>
```
