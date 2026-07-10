---
name: agent-orchestration
description: Use when the user asks for agy/Gemini external review or research, or when coordinating Codex work across roles, threads, subagents, repositories, branches, worktrees, callbacks, status polling, recurring automations, project autopilot, QA/review/release gates, external-task quality logs, or multi-project handoffs. Also use for requests to keep work moving until a goal is met, inspect or message another Codex thread, verify a branch through QA/review, or run delayed check-backs. Chinese triggers include Gemini/agy 代码审查, agy 代码审查, 外部模型审查, Gemini 调研, agy 调研, 外部模型调研, 并行调研, 调研质量日志, 另一个对话/进程在改, 另一个 agent 接手, 分给 QA 验证, 多个分支/仓库收口, 稍后巡检/回调/合并, 持续推进, 一直做到目标效果, 定时自动继续, 创建/继续/读取/转交线程.
---

# Agent Orchestration

Use this skill to run a Codex conversation as a coordinator for a small role-based agent team. Prefer it when a task spans multiple projects, multiple roles, long-running threads, or handoffs that need explicit status tracking.

When this skill mentions `Gemini`, it means Gemini models invoked through local `agy`. Do not substitute the standalone `gemini` CLI.

If the user mentions `agy`, `Gemini`, `Antigravity`, external review, or external research, load this skill before running shell commands. Do not probe the standalone `gemini` CLI with `command -v gemini`, `gemini --version`, or `gemini --help`.
Negative cue: if your first impulse is to inspect `gemini` CLI, stop and return to the `agy` workflow instead.

## Do Not Use For

- Single-file edits, one-shot questions, or code explanations that fit cleanly in the current conversation.
- Debugging that needs one continuous execution context and would lose signal if split across roles.
- Parallel editing of the same files when branches, worktrees, or clear ownership boundaries are missing.
- Broad brainstorming where the user has not asked for execution, tracking, verification, or handoff.

## Core Workflow

1. Read `references/ORCHESTRATION_INTAKE.md` when branch, thread, callback, automation, merge, or push permissions are ambiguous.
2. Read `references/ORCHESTRATION_ROUTING.md` and select the minimum safe `LITE`, `STANDARD`, or `DURABLE` mode. Use `scripts/route_orchestration.py` when a repeatable routing decision helps. External-model work is a modifier, not an automatic upgrade.
3. Read `references/PROJECT_CONTEXT.template.md` if project context is missing, or ask the user for the missing project facts.
4. Read `references/ROLE_REGISTRY.template.md` when role-to-thread IDs need to be created, recorded, or updated.
5. Read `references/ORCHESTRATION_PROTOCOL.md` before minting a dispatch identity, accepting a callback, deduplicating an event, or evaluating commit-pinned evidence. Use `scripts/orchestration_event.py` to validate machine-readable callbacks when stale or duplicate messages could change delivery.
6. Read `references/COMMUNICATION_PROTOCOL.md` before dispatching work to other threads.
7. Read `references/CONTROLLER_LOOP.md` when coordinating child-thread callbacks, branch handoffs, status requests, heartbeat automation, or merge readiness.
8. Read `references/PROJECT_AUTOPILOT.md` when the user wants recurring automation to keep a project moving until a goal, checklist, issue, PR, release, or branch state is complete.
9. Read `references/AUTOMATION_TOOLING.md` before creating, updating, viewing, or deleting heartbeat or cron automations.
10. Read `references/AUTOMATION_CONCURRENCY.md` before enabling any recurring automation that may overlap or retry. Use `scripts/automation_lease.py` for fenced tick ownership and `scripts/heartbeat_lifecycle.py` for monotonic heartbeat shutdown.
11. Read `references/PROJECT_INSTRUCTIONS_DISCOVERY.md` when recurring work depends on `AGENTS.md`, `AGENTS.override.md`, fallback instruction files, `.codex/config.toml`, or target-repo docs.
12. Read `references/STATE_MACHINE.md` when tracking more than one task, thread, role, gate, heartbeat, or automation tick.
13. Read `references/AGY_GEMINI_REVIEW.md` when the user asks to use `agy`, Gemini, Antigravity, or an external model as a review pass or review-quality log; in this workflow Gemini must run through `agy`, never through the standalone `gemini` CLI. Use `scripts/run_agy_print.py` for a sandboxed read-only call, use `scripts/build_agy_context_bundle.py` when repository source context is needed, and write quality logs to the Codex external-review ledger by default. Treat target-repository `AGENTS.md` changes and project-local quality logs as separate writes that require explicit authorization.
14. Read `references/AGY_GEMINI_RESEARCH.md` when the user asks for parallel Codex + Gemini research, idea expansion, repository survey, architecture option comparison, or an external-model research-quality log; here too Gemini must run through `agy`, never through the standalone `gemini` CLI. Keep the external pass read-only, minimize attached context through the allowlisted bundle helper, compare Codex findings with external-model findings before adopting them, and do not make target-repository writes merely to prepare the research pass.
15. Read `references/WORKFLOWS.md` and choose the narrowest workflow that fits the task.
16. Use `references/templates/task_dispatch.template.md` for every role task. Fill in dispatch identity, scope, branch/worktree, merge policy, stop conditions, verification, callback, and monitoring fields.
17. Require role replies to match `references/templates/role_reply.template.md` or `references/templates/coordinator_callback.template.md` when replying directly to the coordinator thread.
18. Before final delivery, inspect role output, diff scope, verification evidence, exact artifact SHA, gate verdicts, and unresolved risks yourself. Only coordinator state `ACCEPTED` is delivery.

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
- Mint and record the goal ID, attempt, dispatch nonce, coordinator epoch, base SHA, and expected head SHA for every asynchronous dispatch.
- Ask each role to callback to the coordinator thread on completion when thread messaging tools are available.
- If callback is unavailable, require `CALLBACK_FAILED: <reason>` in the role's final reply.
- When two or more role threads are active, create a recurring heartbeat automation if automation tools are available.
- The default heartbeat interval is 5 minutes.
- Use `references/templates/monitoring_heartbeat.template.md` as the automation prompt.
- When all tracked roles reach `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`, or `CANCELLED`, move completed work to coordinator review, summarize terminal outcomes, and disable or delete the heartbeat automation.
- For recurring project work beyond status monitoring, read `references/PROJECT_AUTOPILOT.md` and create a goal contract, automation plan, tick prompt, memory file, and escalation rule before enabling cron automation.
- Before creating a recurring automation, inspect existing automations when tools allow and update instead of duplicating.
- Every recurring tick that can write memory, post a message, or perform work must acquire a fenced lease. `LEASE_ALREADY_HELD`, `LEASE_BUSY`, expired, or replaced ticks are quiet no-ops.
- Heartbeats close monotonically through `ACTIVE -> DRAINING -> CLOSED`; post one final summary, wait for tool-confirmed cleanup, and never recreate a closed monitor from a late callback.
- Treat target project `AGENTS.md` / `AGENTS.override.md` as persistent repository guidance, and automation memory as temporary task state. Do not silently put live task state into `AGENTS.md`.

For Chinese-only teams, use the matching Chinese templates in `references/templates/*.zh-CN.template.md`.

## Status Semantics

- Role execution status says what the role claims about its work.
- Gate verdict says whether verification, QA, or review evidence passes for the exact observed SHA.
- Coordinator state says whether work is dispatched, under review, returned, accepted, escalated, or cancelled.

Do not collapse these dimensions. Role `DONE` means ready for inspection, not accepted delivery. `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`, and `CANCELLED` are terminal for monitoring but never automatic success. Read `references/ORCHESTRATION_PROTOCOL.md` for the accepted-delivery predicate.

## Delivery Rules

Final coordinator delivery should include:

- What was done.
- Which roles or threads participated.
- Verification that actually ran.
- Commits, branches, or changed files when relevant.
- Remaining risks or follow-up decisions.

Keep project-specific shared service or remote API contracts inside the target repo documentation. The coordinator may ask roles to document those contracts, but should not let later app updates silently change the remote service contract.
