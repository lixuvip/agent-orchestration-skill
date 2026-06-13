# Example Prompt: Coding And Review Workflow

```text
Use $agent-orchestration to coordinate a coding task with review and QA gates.

Goal:
Add a safe retry option to the export command.

Roles:
- Technical Engineer: implement the smallest scoped change and run unit tests.
- Code Reviewer: inspect the diff for regressions and maintainability risks.
- QA Tester: run the documented command path and report exact output.

Callback:
Every role must reply with DONE, DONE_WITH_CONCERNS, BLOCKED, or NEEDS_CONTEXT.

Heartbeat:
Create a 5-minute heartbeat monitor if any role is dispatched to a separate long-running thread.

Final output:
Coordinator should summarize changed files, commits, verification commands, review findings, and unresolved risks.
```
