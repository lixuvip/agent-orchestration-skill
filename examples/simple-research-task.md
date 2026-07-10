# Example Prompt: Simple Research Task

```text
Use $agent-orchestration to run a small research workflow.

Goal:
Compare three implementation options for adding background job retries to this project.

Roles:
- Planner: define the decision criteria.
- Researcher: inspect the codebase and summarize available approaches.
- Reviewer: challenge risks, edge cases, and maintenance cost.
- External Researcher (Gemini via agy): run a read-only second research pass on the same repository and objective.

External agy/Gemini rule:
Keep the pass read-only by default. Do not modify AGENTS.md or create project-local logs unless those writes were separately authorized. Use a bounded prompt or an allowlisted context bundle, and do not probe command -v gemini, gemini --version, or gemini --help.
Use the research prompt negative guardrails too: no CLI/auth drift, no fake validation, no scope inflation, and no generic brainstorming filler.

Callback:
Each role must report status, findings, evidence, and open questions.

Heartbeat:
No recurring monitor is needed unless any role expects the task to take more than 10 minutes.

Final output:
Coordinator should return one recommended approach, tradeoffs, agreed points, Gemini-only points worth keeping, rejected speculative points, and the next engineering task.
```
