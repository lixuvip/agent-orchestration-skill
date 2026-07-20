# Lightweight Coordination

Load this only for multiple owners, cross-repository/worktree work, or formal QA/review/release gates.

## Choose The Surface

| Need | Surface |
| --- | --- |
| One owner with shared context | Current task |
| Bounded independent exploration, test, triage, or summary | Internal subagent; result returns to coordinator |
| User wants separate visibility or direct continuation | New or existing user-owned thread |
| New direction needs completed source history | Forked thread |
| Parallel writes need checkout isolation | Worktree thread |
| Same task must move between Local and Worktree | Handoff |

Treat words such as “agent”, “subprocess”, or “child conversation” as clues, not tool names. Before dispatch, state whether a new sidebar task appears, where the result returns, and who owns follow-up.

## Finite Flow

1. Define outcome, boundaries, owner, write scope, evidence, return surface, and stop conditions.
2. Preflight required read, write, execute, network, browser, and connector capabilities. If the approach is genuinely ambiguous, keep planning read-only in the current task until the direction is accepted. A parent's plan/read-only state does not prove a child is read-only.
3. Split only independent work; isolate or serialize overlapping writes. Keep the delegation tree flat unless nested delegation is explicitly useful and still auditable.
4. Dispatch through native subagent or thread tools. Give the owner only the minimum inputs and capability needed.
5. Wait through native agent/thread status. Do not create callback envelopes, task boards, heartbeat automation, leases, or polling files for finite work.
6. Inspect the result, artifact, diff, commands, and unresolved risks.
7. Return work for correction or accept it. Role completion is evidence to inspect, not automatic delivery.

## Dispatch And Evidence Contract

A concise dispatch states:

- outcome and current artifact/baseline;
- minimum required inputs and capabilities;
- editable, read-only, and out-of-scope boundaries;
- expected evidence and where the result returns;
- follow-up owner and stop/escalation conditions.

Match evidence to the task. Research returns sources, observed facts, and labeled inferences. Implementation returns the diff and targeted tests. Review returns finding, location, impact, and evidence. QA returns candidate, scenario, expected result, actual result, and raw output location when useful.

If a task lacks a required capability, change the surface or scope before dispatch. Do not discover after completion that the owner could not inspect the real artifact or run the required check.

## Steering And Stale Results

When the user writes during active work, classify the message as:

- **replace**: interrupt or redirect work that no longer matches;
- **add**: preserve the current objective and extend affected owners;
- **status/question**: answer without silently changing scope.

Record the latest effective scope in the current task. A late result from superseded scope is stale: it may be useful background, but must not be merged, accepted, or presented as current without revalidation.

Corrections normally return to the same owner with the failed evidence and requested delta. An independent reviewer receives the candidate artifact, requirements, and raw evidence with fresh context; do not preload the implementer's conclusions as facts.

## Verification Budget

- During implementation, run targeted tests and cheap static checks first.
- Form a candidate artifact before independent review.
- Use one independent reviewer when risk or user intent justifies it; avoid nested reviewers by default.
- Run the full relevant suite once on the final candidate. If code changes afterward, rerun affected checks and any project-mandated final gate.
- Do not rerun an identical expensive suite on the same artifact merely to duplicate another agent's proof; inspect its raw output or run a smaller independent check.
- Before acceptance, build a closure checklist from the complete user request, including follow-ups and corrections. Map each item to an action, current evidence, and `done`, `waived`, or `blocked`; tests are not a substitute for uncovered requirements.

Retries are bounded. Each retry must add evidence, narrow the failure, or change the approach. After the same blocker repeats without new information, stop the loop and ask, escalate, or report the blocker instead of spending indefinitely.

## Optional Best Of N

Use 2-3 isolated candidates only when the user explicitly asks for alternatives or when high ambiguity justifies the extra cost. Define the evaluation rubric before results arrive, isolate all write candidates, compare the same evidence, and allow rejecting every candidate. Run the final full suite only on the selected candidate after integration.

## Formal Gates

For merge, push, deploy, release, security-sensitive changes, or explicit QA/review:

- identify the exact candidate commit or non-Git artifact;
- require current test/review evidence for that artifact;
- treat later changes as invalidating affected evidence;
- keep merge/push/deploy authority separate from implementation authority;
- report blockers and waivers plainly.

Use natural concise handoffs. Include owner, scope, artifact, verification, risks, and requested next action; no machine envelope is required unless an external system explicitly requires one.

Before a fork, handoff, long pause, or context-sensitive continuation, leave a recovery capsule with the objective, latest user constraints, artifact baseline, verified evidence, decisions, pending work, active background work, blocker, and exact next action. Use native task history as storage; do not create a project file unless the project needs a durable artifact.

Before final delivery, audit native status for active subagents, user-owned tasks, background commands, monitors, and automations. Wait for, cancel, or explicitly report each one. Never imply the whole objective is complete while unaccounted work can still change the result.

## Communication

Use native activity UI as the primary progress surface. Add commentary only for meaningful transitions, blockers, approvals, changed risk, or completed evidence. Do not repeat “still running” or unchanged safety boundaries.

If a native capability is unavailable, keep work in the current task or use a concise manual handoff. State the limitation instead of simulating an independent worker.
