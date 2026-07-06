# Usage Examples

For copy-ready scenario files, see:

- [Simple research task](../examples/simple-research-task.md)
- [Coding and review workflow](../examples/coding-review-workflow.md)
- [Multi-agent product planning](../examples/multi-agent-product-planning.md)
- [Bug fix with QA](../examples/bugfix-with-qa.md)
- [Multi-project finalization](../examples/multi-project-finalization.md)
- [Release preparation](../examples/release-prep.md)
- [Branch callback controller loop](../examples/branch-callback-controller-loop.md)
- [Continuous project autopilot](../examples/continuous-project-autopilot.md)

## Example 1: Bug Fix With QA Gate

```text
Use $agent-orchestration to coordinate a bug fix.

Create:
- one engineering role that can edit the smallest needed files;
- one QA role that is read-only and runs regression tests.

Goal:
Fix the issue where an export option is requested but the final report does not include the expected fields.

Done when:
- engineering explains root cause and changed files;
- QA runs the relevant regression tests;
- coordinator confirms the fix is scoped and verified.
```

## Example 2: Parallel Research Before Implementation

```text
Use $agent-orchestration.

Split this feature into parallel preparation:
- Product Designer: define acceptance criteria and user flow.
- Technical Engineer: inspect implementation options without editing files.
- QA Tester: propose the regression matrix.

After all three reply, merge their outputs into one engineering task.
```

## Example 3: Multi-Repository Commit Finalization

```text
Use $agent-orchestration to finalize three repositories.

Projects:
- /path/to/service
- /path/to/app-one
- /path/to/app-two

For each project thread:
- inspect git status;
- document service API contract changes;
- run tests;
- create focused commits if ready;
- report branch, commits, verification, and risks.

Create a 5-minute heartbeat monitor.
```

## Example 4: Release Preparation

```text
Use $agent-orchestration for release preparation.

Roles:
- Release Docs: summarize changes and migration notes.
- QA Tester: verify critical paths.
- Code Reviewer: inspect high-risk diffs.

Do not publish release notes until QA and review have terminal statuses.
```

## Example 5: Callback-Required Long Task

```text
Use $agent-orchestration.

Dispatch this long-running migration to a separate engineering thread.
Require the role to callback to this coordinator thread when complete.
If callback fails, require CALLBACK_FAILED in the role's final reply.
Also create a heartbeat monitor that checks the role every 5 minutes.
```

## Example 6: Branch Callback Controller Loop

```text
Use $agent-orchestration to coordinate branch work with direct callback to the main coordinator thread.

Create or continue a dedicated engineering branch/worktree.
Keep QA read-only.
Require every role to callback to the coordinator thread.
Create heartbeat monitoring if the work is long-running.
Run merge readiness before merging, pushing, or telling the user the branch is ready.
```

## Example 7: Continuous Project Autopilot

```text
Use $agent-orchestration to create a project autopilot loop for this repository.

Read AGENTS.md, AGENTS.override.md, project docs, and the release checklist first.
Create a goal contract with done criteria, allowed autonomous actions, confirmation gates, cadence, memory path, and stop conditions.
Use cron automation for workspace progress and heartbeat only for coordinator-thread callbacks.
Each tick should compare the latest effective update, take one safe next action, run verification, update automation memory, and escalate if merge/push/deploy or scope expansion is needed.
```
