# Codex Agent Orchestration Skills

This repository now ships two independent Codex skills:

- `agent-orchestration`: lightweight, native-first coordination for Codex tasks, internal subagents, user-owned tasks, worktrees, formal gates, and recurring automation.
- `agy-second-opinion`: an explicit opt-in, read-only external review or research pass through local `agy`.

They do not load or depend on each other. Ordinary delegation never probes `agy`; an external pass never activates the orchestration workflow.

[简体中文](README.zh-CN.md)

## Why the main skill is lightweight

The installable `agent-orchestration` runtime contains only six files: one entrypoint, UI metadata, and concise English/Chinese coordination and automation references.

Its default route is:

1. Keep one-owner work in the current task.
2. Use one internal subagent for a bounded result that returns to the coordinator.
3. Create a user-owned task only when separate sidebar visibility or direct follow-up is useful.
4. Load the coordination reference only for multiple owners, cross-repo/worktree work, or formal QA/review/release gates.
5. Load the automation reference only for recurring work that must survive the current turn.

It relies on native Codex lifecycle and status. There are no callback JSON envelopes, task boards, custom heartbeats, leases, role catalogs, or routing scripts.

## Reliability additions in v0.3.0

- Preflight the real capabilities and authority required by each owner before dispatch.
- Keep delegation flat by default and make mid-flight user steering invalidate superseded results.
- Use typed evidence contracts, requirement-to-evidence closure, bounded retries, and a final active-work audit.
- Resume corrections with the same owner, but give independent reviewers fresh context and raw artifacts.
- Preserve a compact recovery capsule before a fork, handoff, long pause, or context-sensitive continuation.
- Use Best-of-N only for explicit or genuinely high-ambiguity work, with isolated candidates and permission to reject them all.

The [v0.3.0 design notes](docs/design-notes-v0.3.0.md) map each addition to the exact Grok Build material that inspired it and explain how the behavior was redesigned for Codex's native tasks, subagents, worktrees, and automations. The release does not vendor Grok Build code or prompts.

## Surface selection

| Need | Surface |
| --- | --- |
| One owner, one deliverable | Current task |
| Bounded independent analysis returning here | Internal subagent |
| Separate sidebar visibility or direct user follow-up | User-owned task |
| Same completed history in a new task | Fork |
| Isolated repository writes | Worktree task |
| Move the same task between Local and Worktree | Handoff |
| Recurring or delayed continuation | Native automation |
| Explicit external-model second opinion | `agy-second-opinion` |

Before delegation, the coordinator states whether a sidebar task will appear, where the result returns, and who owns follow-up.

## Install

```bash
git clone https://github.com/lixuvip/codex-agent-orchestration-skill.git
cd codex-agent-orchestration-skill
./scripts/install.sh
```

The default installer validates and installs only the lightweight orchestration skill:

```bash
./scripts/install.sh --allow-dirty
```

Install the independent AGY skill explicitly:

```bash
./scripts/install.sh --skill agy-second-opinion --allow-dirty
```

Manual install can also copy either skill separately from `skills/`.

## Examples

Use the lightweight orchestration skill:

```text
Use $agent-orchestration. Ask one internal subagent to inspect the authentication flow read-only, then return the evidence here.
```

Request a visible Codex task:

```text
Use $agent-orchestration. Create a separate user-owned task for the release audit and tell me where follow-up should happen.
```

Explicitly request an external second opinion:

```text
Use $agy-second-opinion to run a bounded read-only agy review of this diff, then verify every accepted finding with Codex.
```

## Development checks

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

See [Quickstart](docs/quickstart.md), [Examples](docs/examples.md), [Installation](docs/installation.md), [Forward tests](docs/forward-tests.md), and [v0.3.0 design provenance](docs/design-notes-v0.3.0.md).
