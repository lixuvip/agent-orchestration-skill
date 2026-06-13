# Example Prompt: Bug Fix With QA

```text
Use $agent-orchestration to coordinate this bug fix.

Goal:
Fix the regression where a remote service receives a feature flag but the final user-facing result ignores it.

Roles:
- Technical Engineer: may edit the relay and worker code.
- QA Tester: read-only; run regression tests and inspect output artifacts.

Requirements:
- Engineer must explain root cause.
- Engineer must keep the diff scoped.
- QA must report exact commands and results.
- Coordinator must not deliver until QA reaches DONE or DONE_WITH_CONCERNS.
```

