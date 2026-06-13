# Example Prompt: Simple Research Task

```text
Use $agent-orchestration to run a small research workflow.

Goal:
Compare three implementation options for adding background job retries to this project.

Roles:
- Planner: define the decision criteria.
- Researcher: inspect the codebase and summarize available approaches.
- Reviewer: challenge risks, edge cases, and maintenance cost.

Callback:
Each role must report status, findings, evidence, and open questions.

Heartbeat:
No recurring monitor is needed unless any role expects the task to take more than 10 minutes.

Final output:
Coordinator should return one recommended approach, tradeoffs, and the next engineering task.
```
