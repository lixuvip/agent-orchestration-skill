# AGENTS.md Guidance Snippet Template

Use this when a project needs persistent Codex guidance for recurring autopilot work.

```markdown
## Codex Project Autopilot

- Primary goal sources: <issues | PRs | roadmap | docs | release plan>.
- Required verification before declaring progress: <COMMANDS_OR_CHECKS>.
- Safe autonomous actions: <read-only checks | tests | docs edits | scoped fixes | comments>.
- Actions requiring confirmation: merge, push, deploy, publish, delete data, rotate secrets, spend money, change public API contracts, or expand product scope.
- Status memory: store temporary automation state under `${CODEX_HOME:-$HOME/.codex}/automations/<automation-id>/memory.md`; do not store live task state in this file.
- Idempotency rule: compare the latest effective update before posting comments or repeating work.
- Escalation rule: stop and ask when verification fails repeatedly, permissions are missing, or scope changes.
```
