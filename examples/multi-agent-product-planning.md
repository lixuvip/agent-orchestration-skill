# Example Prompt: Multi-Agent Product Planning

```text
Use $agent-orchestration to plan a product feature before implementation.

Goal:
Design a first version of a team dashboard for monitoring long-running AI coding tasks.

Roles:
- Product Designer: define user workflow, screen states, and acceptance criteria.
- Technical Engineer: inspect likely implementation surfaces and integration risks.
- QA Tester: propose a regression matrix and manual test plan.
- Release Docs: draft user-facing release notes and migration notes.

Callback:
Each role must report findings, assumptions, risks, and recommended next steps.

Heartbeat:
Use a 5-minute heartbeat if role work is split across multiple Codex threads.

Final output:
Coordinator should merge the role outputs into one implementation-ready product brief.
```
