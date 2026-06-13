---
name: agent-orchestration
description: Coordinate multi-role Codex work across threads, subagents, repositories, or worktrees. Use when a task needs agent orchestration, role-based task dispatch, conversation/thread IDs, coordinator handoffs, asynchronous Codex threads, status polling, completion callbacks, recurring automation monitoring, multi-project commits, QA/review/release gates, or reusable task templates.
---

# Agent Orchestration

Use this skill to run a Codex conversation as a coordinator for a small role-based agent team. Prefer it when a task spans multiple projects, multiple roles, long-running threads, or handoffs that need explicit status tracking.

## Core Workflow

1. Read `references/PROJECT_CONTEXT.template.md` if project context is missing, or ask the user for the missing project facts.
2. Read `references/ROLE_REGISTRY.template.md` when role-to-thread IDs need to be created, recorded, or updated.
3. Read `references/COMMUNICATION_PROTOCOL.md` before dispatching work to other threads.
4. Read `references/WORKFLOWS.md` and choose the narrowest workflow that fits the task.
5. Use `references/templates/task_dispatch.template.md` for every role task. Fill in scope, stop conditions, verification, callback, and monitoring fields.
6. Require role replies to match `references/templates/role_reply.template.md`.
7. Before final delivery, inspect role output, diff scope, verification evidence, and unresolved risks yourself.

## Thread And Tool Handling

- When the user asks to create, continue, inspect, or message Codex threads, discover the relevant thread tools first.
- Use new threads only when the user explicitly wants user-visible conversations. For internal parallel work, prefer available subagent tools.
- Record every role thread ID in the coordinator notes or task board before leaving the dispatch step.
- Never infer completion from silence. Completion requires an explicit terminal status or an unambiguous final delivery message.

## Callback And Monitoring

For asynchronous multi-thread tasks, read `references/AUTOMATION_MONITORING.md`.

Apply these rules:

- Include the coordinator thread ID and task ID in each dispatched role prompt.
- Ask each role to callback to the coordinator thread on completion when thread messaging tools are available.
- If callback is unavailable, require `CALLBACK_FAILED: <reason>` in the role's final reply.
- When two or more role threads are active, create a recurring heartbeat automation if automation tools are available.
- The default heartbeat interval is 5 minutes.
- Use `references/templates/monitoring_heartbeat.template.md` as the automation prompt.
- When all tracked roles reach `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT`, summarize results and disable or delete the heartbeat automation.

## Status Semantics

- `DONE`: Complete and verified.
- `DONE_WITH_CONCERNS`: Complete, but risk or coverage gaps remain; preserve those concerns in the final answer.
- `NEEDS_CONTEXT`: The role cannot continue without missing facts.
- `BLOCKED`: The role hit an environment, permissions, conflict, or safety blocker.

Do not treat `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT` as successful completion. They are terminal states for monitoring, not automatic acceptance.

## Delivery Rules

Final coordinator delivery should include:

- What was done.
- Which roles or threads participated.
- Verification that actually ran.
- Commits, branches, or changed files when relevant.
- Remaining risks or follow-up decisions.

Keep project-specific shared service or remote API contracts inside the target repo documentation. The coordinator may ask roles to document those contracts, but should not let later app updates silently change the remote service contract.
