# Lightweight Automation

Load this only for recurring or delayed work that must continue beyond the current turn.

- Use the product's automation tools; do not emulate scheduling with shell loops, heartbeat files, custom leases, or chat polling.
- Inspect existing automations before creating one. Reuse or update the matching goal instead of duplicating it.
- Put outcome, scope, authority, verification, cadence, and stop conditions in the automation prompt.
- Keep each run small: inspect current state, take one safe useful step, verify it, and record a concise result.
- Compare the latest effective state before external writes or messages. If nothing substantive changed, perform a quiet no-op.
- Do not let recurrence grant merge, push, deploy, publish, spending, destructive, secret, or scope-expansion authority.
- Stop, pause, delete, or archive the automation when done or when the user asks. Confirm cleanup through the native tool.
- Use a heartbeat attached to the current task for short follow-up; use a scheduled local/worktree automation for durable project work.

Report the automation name, target, cadence in human terms, authority limits, next run, and cleanup state. Do not expose raw scheduler syntax unless requested.
