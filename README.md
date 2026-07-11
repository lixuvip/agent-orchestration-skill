# Agent Orchestration Skill for Codex

[![Validate](https://github.com/lixuvip/agent-orchestration-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/lixuvip/agent-orchestration-skill/actions/workflows/validate.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/lixuvip/agent-orchestration-skill)](https://github.com/lixuvip/agent-orchestration-skill/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="docs/images/logo.svg" alt="Agent Orchestration logo" width="120">
</p>

<p align="center">
  <strong>Turn Codex into a coordinator for role threads, branch handoffs, callbacks, automations, QA/review gates, and project autopilot loops.</strong>
</p>

<p align="center">
  <a href="README.zh-CN.md">中文说明</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#unreleased-reliability-pass">Reliability Pass</a> ·
  <a href="#demo-workflow">Demo Workflow</a> ·
  <a href="docs/examples.md">Examples</a> ·
  <a href="docs/installation.md">Installation</a>
</p>

<p align="center">
  <a href="https://github.com/lixuvip/agent-orchestration-skill/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/lixuvip/agent-orchestration-skill"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/lixuvip/agent-orchestration-skill"></a>
  <a href="https://github.com/lixuvip/agent-orchestration-skill/actions"><img alt="Validate" src="https://github.com/lixuvip/agent-orchestration-skill/actions/workflows/validate.yml/badge.svg"></a>
  <a href="https://github.com/lixuvip/agent-orchestration-skill/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/lixuvip/agent-orchestration-skill?style=social"></a>
</p>

![Agent orchestration workflow overview](docs/images/workflow-overview.svg)

`agent-orchestration` is a Codex skill that scales from a Lite one-shot workflow to Standard multi-role coordination and Durable project autopilot. It helps one coordinator conversation split complex work across planner, researcher, coder, reviewer, release docs, QA, and monitor roles without forcing heavyweight machinery onto simple tasks.

Instead of asking one agent to handle everything in a long linear thread, this skill gives Codex a repeatable orchestration layer for scoped delegation, versioned callbacks, commit-pinned QA/review evidence, fenced recurring ticks, heartbeat lifecycle management, and final coordinator acceptance.

It is especially useful when another Codex thread or branch is doing work and the main thread needs a reliable way to receive callbacks, request status, verify QA/review output, and decide whether a branch is ready to merge or push. It can also pair Codex automations with `AGENTS.md` project guidance so recurring work keeps moving toward a clear goal instead of becoming a loose reminder.

It can also add a read-only `agy` / Gemini review or research pass as an external second opinion. The coordinator still owns the final decision: every external finding or idea must be checked against the diff, repo context, or actual evidence before it affects planning, QA, repair, merge readiness, or delivery.

External-task quality is logged outside the target repository by default under `${CODEX_HOME:-$HOME/.codex}/external-review-ledger/`. Review entries use `task_type=review`; research entries use `task_type=research`. The workflow does not modify target `AGENTS.md` or create a project-local ledger merely to prepare a read-only pass. Those repository writes require separate authorization.

## Quick Links

- [Install the skill](docs/installation.md)
- [Start in 3 minutes](docs/quickstart.md)
- [Coordinate a multi-project release](docs/tutorial.md)
- [Copy example prompts](docs/examples.md): [research](examples/simple-research-task.md), [coding + review](examples/coding-review-workflow.md), [branch callback](examples/branch-callback-controller-loop.md), [project autopilot](examples/continuous-project-autopilot.md), [GitHub issue/PR autopilot](examples/github-issue-pr-autopilot.md), [product planning](examples/multi-agent-product-planning.md)
- [Review forward-test scenarios](docs/forward-tests.md)
- [Read the v0.1.4 release notes](docs/releases/v0.1.4.md)
- [Read the Chinese docs](README.zh-CN.md)
- [Publish or fork your own version](docs/publishing.md)

## Unreleased Reliability Pass

The current unreleased branch focuses on safe real-world operation. It does not publish, merge, or push anything automatically.

| Area | What changed | Operational effect |
| --- | --- | --- |
| Mode routing | Adds deterministic Lite, Standard, and Durable routing through `route_orchestration.py` and compact capability packs. | A one-shot task loads no core reference; Standard loads one runbook; Durable adds one Autopilot pack. |
| Context budget | Consolidates 14 overlapping core references into four bilingual capability-pack files and caps `SKILL.md` at 70 lines through `scale_test.py`. | New and existing safety features share one runtime path without making every request preload protocol, monitoring, and automation prose. |
| Callback protocol | Adds `ORCHESTRATION_EVENT_V1` with attempt, dispatch nonce, coordinator epoch, event ID, and artifact SHA. | Duplicate and stale callbacks become no-ops; role `DONE` cannot masquerade as coordinator acceptance. |
| Commit-pinned gates | Separates role execution status, gate verdict, and coordinator state. QA and review evidence names the exact candidate SHA. | A new code commit invalidates old QA/review evidence instead of silently reusing it. |
| Automation concurrency | Adds file-locked leases, expiry, and monotonic fencing tokens. | Overlapping cron or heartbeat ticks elect one owner; stale ticks cannot post, write memory, or close a newer automation. |
| Heartbeat lifecycle | Adds `ACTIVE -> DRAINING -> CLOSED` with one final summary and confirmed cleanup. | Shutdown is idempotent and late callbacks cannot recreate a closed monitor. |
| External-pass safety | Keeps `agy` sandboxed and bounded, uses allowlisted context bundles, and moves quality logs outside target repositories by default. | One-shot external review/research remains read-only unless a separate repository write is authorized. |
| Install safety | Adds clean-source enforcement, staged replacement, provenance, retained previous install, dry-run, and restore. | Local skill updates are auditable and recoverable. |
| Behavior tests | Adds protocol, concurrency/lifecycle, routing, and scale-budget tests in addition to static validation, smoke tests, and forward tests. | CI checks real stale-event, duplicate, lease-takeover, shutdown, route-selection, and context-budget behavior. |

## What v0.1.4 Adds

`v0.1.4` hardens the Project Autopilot workflow from `v0.1.3` with CI-backed forward tests and clearer visual documentation.

| Area | What changed | Why it helps |
| --- | --- | --- |
| Forward-test guard | Adds `scripts/forward_test.py` and runs it in GitHub Actions. | Trigger coverage for heartbeat callbacks, cron Autopilot, no-op GitHub polling, and missing `AGENTS.md` guidance is checked before release. |
| Project Autopilot | Keeps the goal-driven recurring automation workflow for project progress. | Codex can continue checking and taking safe next steps until done criteria are met. |
| Automation memory | Keeps templates for memory, idempotency, latest effective updates, blockers, and posted messages. | Cron runs avoid duplicate comments, repeated status requests, and repeated work. |
| Escalation gates | Keeps explicit stop rules for merge, push, deploy, destructive changes, public API contract changes, and scope expansion. | Automation can move quickly without taking authority it does not have. |
| Visual docs | Adds Project Autopilot loop diagrams. | Users can understand the runtime loop before copying automation prompts. |

## Project Autopilot

Project Autopilot is a pattern for recurring Codex automation. It is for prompts like "keep working on this project until the checklist is complete" or "check every hour and take the next safe step."

![Project Autopilot loop](docs/images/project-autopilot-loop.svg)

Autopilot combines:

- `AGENTS.md` / `AGENTS.override.md` as persistent project guidance.
- A goal contract with done criteria, permissions, verification, cadence, and stop conditions.
- Heartbeat automation for current-thread follow-up and callback polling.
- Cron automation for durable workspace or worktree progress.
- Automation memory so each run compares the latest effective update, processed event IDs, and action keys before posting comments or repeating work.
- A file-locked lease and fencing token so overlapping ticks cannot both act or overwrite newer memory.
- `ACTIVE -> DRAINING -> CLOSED` heartbeat shutdown with one final summary and tool-confirmed cleanup.
- Escalation reports when merge, push, deploy, scope expansion, or repeated verification failure needs user input.
- Forward-test scenarios and filled examples for no-op ticks, escalation, goal contracts, and automation memory.

## Why This Exists

Codex is powerful, but complex projects often need more than one linear agent thread. Long-running AI coding tasks can fail because progress is hidden, context gets mixed, or subtasks are forgotten.

This skill adds a small coordination layer that makes Codex workflows more observable, modular, and reliable:

- Split one goal into multiple role-specific agents.
- Give every role explicit scope, stop conditions, verification, and callback rules.
- Route work through Lite, Standard, or Durable mode based on actual coordination and recovery needs.
- Confirm branch, thread, callback, merge, and push behavior before risky orchestration.
- Track role execution, QA/review gate verdict, and coordinator acceptance as separate states.
- Reject duplicate event IDs and stale attempt, nonce, epoch, or artifact-SHA callbacks without changing current state.
- Use heartbeat monitoring for long-running or asynchronous work.
- Use project autopilot for recurring automation that can continue a workspace toward a defined goal.
- Fence recurring ticks and close heartbeat monitors monotonically so crashes and overlaps remain recoverable.
- Add an optional read-only `agy` / Gemini review pass while guarding against scope drift and unsupported test claims.
- Run parallel Codex + Gemini research for repo surveys, option comparison, or idea expansion without forcing those tasks into review mode.
- Preserve per-task quality logs for later prompt, model, and scope tuning.
- Require the coordinator to inspect role output, risks, and verification before final delivery.
- Run merge-readiness checks before branch finalization.

## Best For

- Multi-agent coding workflows.
- Research plus implementation pipelines.
- Product planning with role-based AI agents.
- QA and code review gates for AI-assisted development.
- Optional external `agy` / Gemini review gates for high-risk diffs or second-opinion review.
- Optional external `agy` / Gemini research passes for implementation options, repo surveys, and idea expansion.
- Multi-repository release coordination.
- Long-running Codex tasks that need monitoring and callbacks.
- Branch/worktree handoffs that need status requests, QA gates, and merge readiness.
- Recurring project automation that should read `AGENTS.md`, keep memory, choose one safe next step per run, and stop when the goal is met.

## What It Solves

Use this skill when a task is too large or risky for one uninterrupted conversation:

- Multi-repository changes that need separate implementation and verification threads.
- Parallel work across product, engineering, QA, review, and release docs roles.
- Long-running Codex threads where the coordinator must poll status instead of relying on memory.
- Handoffs that require explicit changed files, verification commands, risks, and final status.
- Workflows where child threads should call back to the coordinator and a heartbeat automation should check status every 5 minutes.
- Branch or worktree workflows that need status requests, coordinator callbacks, and merge-readiness checks.
- Projects that need recurring cron automation to inspect issues/PRs/tests, act idempotently, and keep moving without losing project rules.

## Optional Agy / Gemini Review

When `agy` is installed locally, the coordinator can run a bounded external review after Codex implementation or before accepting a branch handoff. A one-shot second opinion remains Lite unless the wider task actually needs Standard or Durable coordination. This workflow uses `references/AGY_GEMINI_REVIEW.md` plus prompt, quality, and dedicated report templates under `references/templates/`.

The standard review model is `Gemini 3.5 Flash (High)`. For broad audits or user-requested comparisons, the workflow runs independent Codex and Gemini reviews, then compares agreed, model-only, rejected, and verified findings. Gemini always means Gemini through local `agy`, never the standalone `gemini` CLI. `scripts/run_agy_print.py` fixes the pass to sandboxed print mode, rejects unsafe edit-mode flags, enforces a host timeout and output limit, and treats empty or structurally invalid output as failure. Diff-only review needs no repository attachment; source-backed review uses an allowlisted bundle created by `scripts/build_agy_context_bundle.py`. Whole-repository disclosure, persistent `AGENTS.md` guidance, and project-local quality logging each require explicit authorization.

## Optional Agy / Gemini Research

When you want Gemini involved in research instead of only in review, the coordinator can run a parallel Codex + Gemini research pass. This workflow uses `references/AGY_GEMINI_RESEARCH.md` plus prompt, quality, log, and dedicated report templates under `references/templates/`.

The standard research model is also `Gemini 3.5 Flash (High)` for repo surveys and option framing. Codex still reads the repository and verifies current external facts from primary sources. The external stream receives a bounded prompt or allowlisted context bundle, never an automatically expanded whole-repository attachment. Results are shown as agreed points, Gemini-only points, Codex-only points, rejected or speculative points, and concrete next actions. Research-quality records use `task_type=research` in the same Codex-owned external-review ledger.

## Example: Branch Callback

```text
Use $agent-orchestration to coordinate branch work with direct callback to the main coordinator thread.

Create or continue a dedicated engineering branch/worktree.
Keep QA read-only.
Require every role to callback to the coordinator thread.
Create heartbeat monitoring if the work is long-running.
Run merge readiness before merging, pushing, or telling the user the branch is ready.
```

## Example: Project Autopilot

```text
Use $agent-orchestration to create a project autopilot loop.

Read AGENTS.md and project docs first.
Create a goal contract with done criteria, allowed autonomous actions, verification commands, cadence, and stop conditions.
Use cron automation for workspace progress and heartbeat only for coordinator-thread callbacks.
Maintain automation memory and compare the latest effective update before repeating work or posting comments.
Acquire a fenced lease for every tick, verify it before side effects and memory writes, and discard stale-owner results.
Escalate before merge, push, deploy, publish, destructive changes, public API contract changes, or scope expansion.
```

## Quick Start

Install:

```bash
git clone https://github.com/lixuvip/agent-orchestration-skill.git
cd agent-orchestration-skill
./scripts/install.sh
```

Use in Codex:

```text
Use $agent-orchestration to coordinate this bug fix with one engineering thread and one QA thread.

Goal:
Fix the failing export option in the report generation flow.

Constraints:
- Engineer may edit application and test code.
- QA is read-only and must run the regression tests.
- Both roles must report exact commands and results.
```

## Demo Workflow

```mermaid
flowchart TD
    A[User Request] --> B[Agent Orchestrator]
    B --> C[Planner Agent]
    B --> D[Research Agent]
    B --> E[Coder Agent]
    B --> F[Reviewer Agent]
    B --> G[Monitor Agent]
    C --> H[Task State]
    D --> H
    E --> H
    F --> H
    G --> I[Heartbeat Monitor]
    C --> J[Callback]
    D --> J
    E --> J
    F --> J
    H --> K[Final Output]
    I --> K
    J --> K
```

## Core Roles

| Role | Purpose |
| --- | --- |
| Coordinator | Breaks down the goal, dispatches role tasks, tracks status, and reviews final evidence. |
| Planner | Clarifies scope, acceptance criteria, and task order. |
| Researcher | Gathers context without changing files. |
| Coder | Implements scoped changes and reports exact files changed. |
| Reviewer | Checks quality, regressions, and risk areas. |
| QA Tester | Runs verification and reports exact commands and results. |
| Monitor | Polls long-running tasks, summarizes terminal role states into coordinator review, and closes its automation lifecycle. |

## Repository Layout

```text
.
├── skills/
│   └── agent-orchestration/
│       ├── SKILL.md
│       ├── agents/
│       │   └── openai.yaml
│       ├── scripts/
│       │   ├── automation_lease.py
│       │   ├── heartbeat_lifecycle.py
│       │   ├── orchestration_event.py
│       │   └── route_orchestration.py
│       └── references/
│           ├── AGY_GEMINI_REVIEW.md
│           ├── AGY_GEMINI_RESEARCH.md
│           ├── COORDINATION_RUNBOOK.md
│           ├── COORDINATION_RUNBOOK.zh-CN.md
│           ├── PROJECT_AUTOPILOT.md
│           ├── PROJECT_AUTOPILOT.zh-CN.md
│           ├── PROJECT_CONTEXT.template.md
│           ├── ROLE_REGISTRY.template.md
│           ├── TASK_BOARD.template.md
│           ├── examples/
│           ├── roles/
│           └── templates/
├── docs/
│   ├── installation.md
│   ├── installation.zh-CN.md
│   ├── quickstart.md
│   ├── quickstart.zh-CN.md
│   ├── tutorial.md
│   ├── tutorial.zh-CN.md
│   ├── examples.md
│   ├── examples.zh-CN.md
│   ├── forward-tests.md
│   ├── images/
│   ├── releases/
│   ├── publishing.md
│   └── publishing.zh-CN.md
├── examples/
├── scripts/
│   ├── install.sh
│   ├── install_skill.py
│   ├── automation_test.py
│   ├── protocol_test.py
│   ├── routing_test.py
│   ├── scale_test.py
│   ├── smoke_test.py
│   ├── forward_test.py
│   └── validate.py
└── .github/workflows/validate.yml
```

## Install

Clone the repository and run the installer:

```bash
git clone https://github.com/lixuvip/agent-orchestration-skill.git
cd agent-orchestration-skill
./scripts/install.sh
```

The installer copies `skills/agent-orchestration` into:

```text
${CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}/agent-orchestration
```

The installer validates first, refuses a dirty source tree by default, stages replacement atomically, records source provenance, and retains the previous install for rollback. Use `./scripts/install.sh --dry-run` to preview, `--allow-dirty` only for an intentional local snapshot, and `./scripts/install.sh --restore` to restore the retained previous copy.

Restart Codex if the skill does not appear immediately.

Manual copying bypasses provenance and rollback. If you still need it:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/agent-orchestration "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Some Codex installations scan `$HOME/.agents/skills` for user-scoped skills. If that is your setup, install with:

```bash
CODEX_SKILLS_DIR="$HOME/.agents/skills" ./scripts/install.sh
```

## Usage

Invoke it explicitly in Codex:

```text
Use $agent-orchestration to split this task across engineering, QA, and code review threads. Create a 5-minute heartbeat monitor and summarize the final status when all roles finish.
```

Or describe a matching task and let Codex select it implicitly:

```text
Coordinate this release across three repositories. Have each project thread finish commits, document API contracts, and report verification results back to this coordinator thread.
```

## Minimal Workflow

1. The coordinator chooses the minimum safe Lite, Standard, or Durable route.
2. Standard or Durable work creates scoped dispatch identities and selects isolated role threads/worktrees where needed.
3. Each asynchronous role receives a versioned dispatch using `task_dispatch.template.md` and replies with `ORCHESTRATION_EVENT_V1`.
4. The coordinator validates, deduplicates, and rejects stale callbacks before updating state.
5. Long-running Standard work uses a leased heartbeat; Durable work uses a goal contract, memory, cron, and fencing.
6. Terminal role status moves work to `IN_REVIEW`. The coordinator accepts delivery only after current artifact-pinned gates pass.

## Search Keywords

Codex skill, Codex skills, Agent Skills, OpenAI Codex, AGENTS.md, AGENTS.override.md, AI agent orchestration, multi-agent workflow, project autopilot, Codex automations, cron automation, heartbeat automation, GitHub issue automation, PR automation, parallel agents, parallel coding, git worktrees, subagents, task orchestration, role-based agents, callback workflow, heartbeat monitoring, structured handoff, coding agent, QA workflow, code review automation, agy Gemini review, Antigravity review, external model review, release management, developer tools.

## Documentation

- Installation: [English](docs/installation.md) | [中文](docs/installation.zh-CN.md)
- Quickstart: [English](docs/quickstart.md) | [中文](docs/quickstart.zh-CN.md)
- Tutorial: [English](docs/tutorial.md) | [中文](docs/tutorial.zh-CN.md)
- Usage examples: [English](docs/examples.md) | [中文](docs/examples.zh-CN.md)
- Forward tests: [docs/forward-tests.md](docs/forward-tests.md)
- Publishing guide: [English](docs/publishing.md) | [中文](docs/publishing.zh-CN.md)

## Validate

Run the repository validator:

```bash
python3 scripts/validate.py
python3 scripts/smoke_test.py
python3 scripts/forward_test.py
python3 scripts/protocol_test.py
python3 scripts/automation_test.py
python3 scripts/routing_test.py
python3 scripts/scale_test.py
git diff --check
```

If you also have Codex's built-in `skill-creator` validator available, run it against the skill folder:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/agent-orchestration
```

## Requirements

- Codex with skill support.
- Optional: Codex thread tools for creating, reading, and messaging role conversations.
- Optional: Codex automation tools for recurring heartbeat monitoring and workspace cron autopilot.
- Recurring lease helpers require a local POSIX-style filesystem with advisory locks and atomic rename semantics.
- Optional: local `agy` CLI with Gemini models for external read-only review or research passes.
- Optional: Project `AGENTS.md` / `AGENTS.override.md` guidance for durable repository rules.

## Related Codex Documentation

- [Agent Skills](https://developers.openai.com/codex/skills)
- [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
- [Save workflows as skills](https://developers.openai.com/codex/use-cases/reusable-codex-skills)
- [Codex automations](https://developers.openai.com/codex/app/automations)

## License

MIT License. See [LICENSE](LICENSE).
