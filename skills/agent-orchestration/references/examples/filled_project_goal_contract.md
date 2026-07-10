# Filled Project Goal Contract

```text
Project goal contract

Goal ID: release-readiness-2026-07
Project / workspace: /path/to/product
Coordinator thread ID: 019f-example-coordinator

Goal:
- Keep the repository moving until the release-readiness checklist is complete.

Done when:
- The release checklist issue has no unchecked blocking items.
- Unit tests and documented smoke checks pass, or blocked checks have an owner and reason.
- Release notes mention the API contract and known risks.

Instruction sources:
- AGENTS.md / AGENTS.override.md: /path/to/product/AGENTS.md
- .codex/config.toml: /path/to/product/.codex/config.toml
- Project docs: README.md, CONTRIBUTING.md, docs/release.md
- Issue / PR / release source: GitHub issue #42

Allowed autonomously:
- Inspect git status, issues, PRs, checks, and release docs.
- Run non-destructive validation commands from AGENTS.md.
- Post one idempotent status request when latest effective update changed.
- Make docs-only checklist updates if already authorized by the user.

Requires confirmation:
- merge, push, deploy, publish, delete data, rotate secrets, spend money, change public API contracts, or expand product scope
- changing CI configuration or release branch policy

Write authority:
- tests/docs only; commit allowed after coordinator review; push requires confirmation

Verification commands:
- npm test
- npm run lint

Cadence and budget:
- Automation type: cron
- Cadence: every 2 hours on weekdays
- Max attempts / runtime: 12 ticks or until release checklist is complete
- Stop after success: YES

Memory path:
- /Users/example/.codex/automations/release-readiness/memory.md

Concurrency and lifecycle:
- Lease state directory: /Users/example/.codex/automations/release-readiness/state
- Lease TTL / max tick runtime: 900 / 600 seconds
- Fencing rule: a lower or invalid token cannot post, write memory, or clean up
- Initial lifecycle: ACTIVE
- Cleanup policy: PAUSE after one final summary and tool confirmation

Idempotency key:
- issue #42 latest effective update + PR head SHA + check conclusions

Stop conditions:
- same verification failure appears twice
- push, merge, deploy, publish, or public API contract change is needed
- issue scope changes beyond release readiness
```
