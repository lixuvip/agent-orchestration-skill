# GitHub Issue And PR Autopilot

```text
Use $agent-orchestration to run a GitHub issue/PR project autopilot.

Goal:
Keep the tracked issue and implementation PR moving until the acceptance checklist is complete.

Channels:
- Issue is the coordination channel.
- PR is the implementation channel.
- Do not stop just because there is no open PR; inspect issue body, labels, comments, and status first.

Read first:
- AGENTS.md and AGENTS.override.md.
- CONTRIBUTING.md, PR template, issue template, and test docs.
- Existing automation memory.

Every tick:
- Run gh auth status.
- Read the tracked issue body, labels, comments, and timeline.
- Read linked/open PR body, comments, commits, files, checks, review state, and draft/ready status if present.
- Determine the latest effective update, not just updatedAt.
- Compare with memory and existing codex-auto-review / codex-next-action markers.
- If unchanged and already covered, do not post another GitHub comment; update memory only.
- If changed, take one safe next action: status request, read-only review, test summary, docs-only update, or coordinator summary.

Allowed autonomously:
- read issue/PR state;
- run non-destructive checks;
- post one idempotent status or review comment when the latest effective update changed;
- update automation memory.

Requires confirmation:
- commit, push, merge, close issue, mark release ready, deploy, change public API contract, or expand scope.

Done when:
- issue acceptance checklist is complete;
- PR is merged or explicitly not needed;
- checks are passing or blockers have owners;
- final summary has been posted.
```
