# Project Autopilot

Use this reference when the user wants Codex to keep a project moving across repeated automation runs until an explicit goal is reached.

Project autopilot is not just heartbeat monitoring. A heartbeat checks child-thread status. Autopilot maintains a goal contract, reads persistent project guidance, chooses one safe next action per tick, records memory, and stops or escalates when authority is missing.

## When To Use

Use autopilot when the user asks for:

- continuous project progress until a goal is met;
- recurring checks that may perform safe follow-up work;
- ongoing issue, PR, branch, QA, release, or backlog coordination;
- a Codex thread or workspace that should wake up later and continue from memory;
- Chinese equivalents such as `持续推进`, `一直做到目标效果`, `定时巡检并继续处理`, `自动收口`, or `保持项目继续工作`.

Do not use autopilot for a one-shot edit, a short answer, or an automation that only reminds the user.

## Persistent Guidance Sources

Before creating or updating an autopilot automation, read `PROJECT_INSTRUCTIONS_DISCOVERY.md` and identify durable project guidance:

- `AGENTS.md`: Codex project instructions. Use repository-level and nested files as the first source for build, test, review, and safety conventions.
- `AGENTS.override.md`: stronger local override when present.
- fallback instruction files configured by `project_doc_fallback_filenames` in Codex config, if known.
- `.codex/config.toml`: Codex configuration such as project-scoped settings or agent profiles. Do not store task state, secrets, or project memory here.
- existing project docs such as `README.md`, `CONTRIBUTING.md`, `docs/`, issue templates, and PR templates.

Put stable repository rules in `AGENTS.md`. Put temporary goal state in automation memory. Do not edit `AGENTS.md` unless the user asks, or unless recurring feedback clearly needs to be codified and the user has allowed documentation updates.

## Automation Types

Choose the narrowest automation surface:

| Type | Use for | Notes |
| --- | --- | --- |
| Heartbeat | Current-thread follow-up, role-thread polling, short delayed checks, callback collection. | Prefer for sub-hour follow-up tied to the coordinator thread. |
| cron | Workspace or worktree work that should recur independently, such as issue/PR polling, tests, backlog triage, or release readiness. | Use for durable project autopilot. |
| Suggested create/update | Worktree automations or local-environment setup that the user should review before saving. | Use when environment setup or workspace destination is material. |

When automation tools are available, use `AUTOMATION_TOOLING.md` and the app automation tool rather than writing raw automation directives. For existing automations, inspect the current automation before creating a duplicate, and prefer updating it while preserving fields that the user did not ask to change.

## Goal Contract

Before enabling autopilot, create or infer `templates/project_goal_contract.template.md`:

- goal and done criteria;
- allowed autonomous actions;
- actions requiring confirmation;
- verification commands and evidence;
- target workspace, branch, issue, PR, or release;
- cadence, runtime budget, and stop conditions;
- memory path and idempotency key.

If the user says "fully autonomous" or "keep working until done", still keep destructive or external actions gated: merge, push, deploy, delete data, rotate secrets, spend money, change public API contracts, or broaden product scope.

## Tick Loop

Each automation tick should:

1. Read the goal contract, project guidance, and automation memory.
2. Inspect live state: git status, branch, issue/PR activity, role callbacks, test results, build state, logs, and known blockers.
3. Compare the latest effective update against the stored memory to avoid duplicate comments or repeated work.
4. Choose one smallest safe next action.
5. Execute it only if it is inside the allowed autonomous actions.
6. Run or record the relevant verification.
7. Update automation memory with timestamp, observed state, action, evidence, and next step.
8. If done, post a final summary and pause or delete the automation.
9. If blocked or authority is missing, post `templates/escalation_report.template.md` and pause or wait according to the goal contract.

Do not use raw freshness alone as a trigger. A timestamp changed by metadata is not necessarily a new effective update.

## Memory Rules

Use `templates/automation_memory.template.md` for durable memory. Store it in the automation's own state directory when available, for example:

```text
${CODEX_HOME:-$HOME/.codex}/automations/<automation-id>/memory.md
```

If `CODEX_HOME` is unset in the automation shell, resolve the path through `$HOME/.codex` rather than expanding to `/automations`.

Memory should record:

- goal ID and automation ID;
- latest effective update;
- last action taken;
- verification evidence;
- blocker history;
- next safe action;
- what user-facing comments or callbacks have already been posted.

## AGENTS.md Feedback Loop

Use `templates/agents_guidance_snippet.template.md` when a project lacks persistent guidance for repeated automation work.

Suggest an `AGENTS.md` update when:

- the same mistake or assumption recurs;
- automation repeatedly has to rediscover the same build/test command;
- review feedback repeats across runs;
- the project needs clearer branch, merge, or deployment rules.

Keep `AGENTS.md` small. It should contain stable rules, not a live task board.

## Completion And Escalation

Autopilot may declare the goal reached only when the goal contract's done criteria and verification pass. If the result is partial, use `DONE_WITH_CONCERNS` and preserve the risk.

Pause or escalate when:

- required confirmation is missing;
- verification fails repeatedly;
- the same blocker appears across the configured limit;
- the next action would exceed scope, budget, permissions, or safety limits;
- a merge, push, deploy, external notification, or public release is needed without explicit permission.
