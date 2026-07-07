---
name: agent-orchestration
description: Use when coordinating Codex work across roles, threads, subagents, repositories, branches, worktrees, callbacks, status polling, recurring automations, project autopilot, QA/review/release gates, or multi-project handoffs. Also use for requests to keep work moving until a goal is met, inspect or message another Codex thread, verify a branch through QA/review, or run delayed check-backs. Chinese triggers include 另一个对话/进程在改, 另一个 agent 接手, 分给 QA 验证, 多个分支/仓库收口, 稍后巡检/回调/合并, 持续推进, 一直做到目标效果, 定时自动继续, 创建/继续/读取/转交线程.
---

# Agent Orchestration

Use this skill to run a Codex conversation as a coordinator for a small role-based agent team. Prefer it when a task spans multiple projects, multiple roles, long-running threads, or handoffs that need explicit status tracking.

## Do Not Use For

- Single-file edits, one-shot questions, or code explanations that fit cleanly in the current conversation.
- Debugging that needs one continuous execution context and would lose signal if split across roles.
- Parallel editing of the same files when branches, worktrees, or clear ownership boundaries are missing.
- Broad brainstorming where the user has not asked for execution, tracking, verification, or handoff.

## Core Workflow

1. Read `references/ORCHESTRATION_INTAKE.md` when branch, thread, callback, automation, merge, or push permissions are ambiguous.
2. Read `references/PROJECT_CONTEXT.template.md` if project context is missing, or ask the user for the missing project facts.
3. Read `references/ROLE_REGISTRY.template.md` when role-to-thread IDs need to be created, recorded, or updated.
4. Read `references/COMMUNICATION_PROTOCOL.md` before dispatching work to other threads.
5. Read `references/CONTROLLER_LOOP.md` when coordinating child-thread callbacks, branch handoffs, status requests, heartbeat automation, or merge readiness.
6. Read `references/PROJECT_AUTOPILOT.md` when the user wants recurring automation to keep a project moving until a goal, checklist, issue, PR, release, or branch state is complete.
7. Read `references/AUTOMATION_TOOLING.md` before creating, updating, viewing, or deleting heartbeat or cron automations.
8. Read `references/PROJECT_INSTRUCTIONS_DISCOVERY.md` when recurring work depends on `AGENTS.md`, `AGENTS.override.md`, fallback instruction files, `.codex/config.toml`, or target-repo docs.
9. Read `references/STATE_MACHINE.md` when tracking more than one task, thread, role, heartbeat, or automation tick.
10. Read `references/WORKFLOWS.md` and choose the narrowest workflow that fits the task.
11. Use `references/templates/task_dispatch.template.md` for every role task. Fill in scope, branch/worktree, merge policy, stop conditions, verification, callback, and monitoring fields.
12. Require role replies to match `references/templates/role_reply.template.md` or `references/templates/coordinator_callback.template.md` when replying directly to the coordinator thread.
13. Before final delivery, inspect role output, diff scope, verification evidence, and unresolved risks yourself.

## Thread And Tool Handling

- When the user asks to create, continue, inspect, or message Codex threads, discover the relevant thread tools first.
- Use new threads only when the user explicitly wants user-visible conversations. For internal parallel work, prefer available subagent tools.
- Record every role thread ID in the coordinator notes or task board before leaving the dispatch step.
- Never infer completion from silence. Completion requires an explicit terminal status or an unambiguous final delivery message.

## Capability Fallbacks

- If thread tools are available, use them for user-visible role conversations and callbacks.
- If subagent tools are available, prefer them for internal parallel role work that does not need user-owned threads.
- If automation tools are available, create a heartbeat for two or more active role threads, any long-running role, or current-thread follow-up; create a cron automation for durable workspace/project autopilot.
- If callbacks or automation are unavailable, maintain a manual task board from `references/TASK_BOARD.template.md` and poll unresolved roles before final delivery.
- If none of these capabilities are available, keep orchestration in the current conversation, make the limitation explicit, and avoid pretending that independent roles are running.

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
- For recurring project work beyond status monitoring, read `references/PROJECT_AUTOPILOT.md` and create a goal contract, automation plan, tick prompt, memory file, and escalation rule before enabling cron automation.
- Before creating a recurring automation, inspect existing automations when tools allow and update instead of duplicating.
- Treat target project `AGENTS.md` / `AGENTS.override.md` as persistent repository guidance, and automation memory as temporary task state. Do not silently put live task state into `AGENTS.md`.

For Chinese-only teams, use the matching Chinese templates in `references/templates/*.zh-CN.template.md`.

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
