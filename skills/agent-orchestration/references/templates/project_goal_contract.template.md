# Project Goal Contract Template

Use this before creating a recurring project autopilot automation.

```text
Project goal contract

Goal ID: <GOAL_ID>
Project / workspace: <PATH_OR_REPOSITORY>
Coordinator thread ID: <THREAD_ID_OR_NONE>

Goal:
- <ONE_SENTENCE_OUTCOME>

Done when:
- <ACCEPTANCE_CRITERION_1>
- <ACCEPTANCE_CRITERION_2>
- <ACCEPTANCE_CRITERION_3>

Instruction sources:
- AGENTS.md / AGENTS.override.md: <PATH_OR_NONE>
- .codex/config.toml: <PATH_OR_NONE>
- Project docs: <README_OR_DOCS>
- Issue / PR / release source: <URL_OR_ID_OR_NONE>

Allowed autonomously:
- <SAFE_ACTION_1>
- <SAFE_ACTION_2>
- <SAFE_ACTION_3>

Requires confirmation:
- merge, push, deploy, publish, delete data, rotate secrets, spend money, change public API contracts, or expand product scope
- <PROJECT_SPECIFIC_CONFIRMATION_RULE>

Write authority:
- <read-only | scoped edits | tests/docs only | commit allowed | push allowed with confirmation>

Verification commands:
- <COMMAND_1>
- <COMMAND_2>

Cadence and budget:
- Automation type: <heartbeat | cron>
- Cadence: <NATURAL_LANGUAGE_INTERVAL>
- Max attempts / runtime: <LIMIT>
- Stop after success: <YES_OR_NO>

Memory path:
- <AUTOMATION_MEMORY_PATH>

Idempotency key:
- <issue/pr/branch/test-state/latest-effective-update>

Stop conditions:
- <BLOCKER_OR_FAILURE_LIMIT>
- <MISSING_PERMISSION_RULE>
- <SCOPE_CHANGE_RULE>
```
