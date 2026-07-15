---
name: agent-orchestration
description: Coordinate Codex work across roles, threads, subagents, repositories, branches, worktrees, callbacks, QA/review/release gates, recurring automation, project autopilot, or multi-project handoffs; also use for agy/Gemini external review or research and external-task quality logs. Trigger for requests to delegate, inspect/message another Codex thread, verify a branch through QA/review, run delayed check-backs, or keep work moving until a goal is met. Chinese triggers include 外部模型审查/调研, Gemini/agy 审查或调研, 并行调研, 另一个对话/agent 接手, 分给 QA, 多分支/多仓库收口, 巡检/回调, 持续推进, 定时自动继续, 创建/读取/转交线程.
---

# Agent Orchestration

Coordinate only when the task benefits from independent ownership, async recovery, formal gates, or recurrence. Keep simple work simple.

## Route First

- `LITE`: one-shot current-context work without async callbacks or recurrence. LITE: load no core reference; do not create task boards, event envelopes, heartbeats, cron, or memory.
- `STANDARD`: finite multi-role, async/user-visible thread, cross-repo, long-running, or formal gate work. STANDARD: load one language version of `COORDINATION_RUNBOOK.md` and only the templates used.
- `DURABLE`: recurring work or recovery across ticks. DURABLE: load the same runbook plus one language version of `PROJECT_AUTOPILOT.md`.
- Never load both language versions. For Chinese work use the `.zh-CN.md` pack; otherwise use English.
- Use `scripts/route_orchestration.py` only when the route is not obvious. Never downgrade below its minimum safe mode.
- External-model review/research is an independent modifier, not an automatic upgrade. Load only `AGY_GEMINI_REVIEW.md` or `AGY_GEMINI_RESEARCH.md` for the requested mode.

## Core Contract

- Respect user/project scope and authority. Ask only when a missing choice materially changes execution, writes, visible threads, automation, merge, or push.
- Give each delegated task one owner and explicit editable/read-only/out-of-scope boundaries. Isolate or serialize overlapping edits.
- User-visible threads require explicit user intent. Use subagents only when the user explicitly asks for delegation/parallel agent work and ownership does not overlap.
- Before creating a user-visible thread, choose the best-fit supported thinking effort independently from orchestration mode; prioritize expected quality and risk coverage, use lower latency/cost only as a tie-breaker, honor explicit user overrides, never set `model` unless requested, and record fallbacks per the coordination runbook.
- Never infer completion from silence. Require actual verification and inspect role output before acceptance.
- For Standard/Durable async work, use versioned callbacks, stale/duplicate rejection, exact artifact gates, and coordinator-owned acceptance from the selected coordination runbook.
- Role `DONE` is ready for coordinator review, not delivery. Do not merge, push, deploy, publish, or claim readiness without current evidence and authority.
- Use `PROJECT_CONTEXT.template.md` or `ROLE_REGISTRY.template.md` only when those facts are genuinely missing; do not preload them.
- Select templates directly: dispatch/reply for roles, QA/review for gates, heartbeat for finite monitoring, and goal/plan/tick/memory/escalation for Durable work.

## Agy / Gemini Boundary

`Gemini` means Gemini through local `agy`, never the standalone `gemini` CLI. If the user did not request an external pass, ask once before probing or invoking `agy`; without confirmation, continue Codex-only. After opt-in, check `agy` once per goal and host, cache unavailable/unhealthy results, notify once, and do not retry until the goal or environment changes or the user explicitly requests a recheck. Use the selected AGY pack's sandboxed helpers and bounded context; target-repository guidance writes and project-local quality logs require separate authorization.

## Capability Fallbacks

- Prefer thread tools for user-visible role conversations and callbacks.
- Use automation tools for actual heartbeat/cron creation and lifecycle changes.
- If a required capability is absent, use manual task-board polling or keep coordination in the current conversation; state the limitation instead of pretending independent work is running.

## Delivery

Report work done, participants, real verification, changed files/branches/commits, automation cleanup, waivers, and remaining risk. Keep project-specific service/API contracts in the target repository rather than this generic skill.
