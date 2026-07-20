# Examples

## 1. Bounded internal subagent

```text
Use $agent-orchestration. Delegate a read-only dependency map to one internal subagent. No sidebar task is needed; return the evidence here.
```

The coordinator keeps implementation ownership and does not create task boards, callback envelopes, or heartbeat state.

## 2. Parallel owners with isolated files

```text
Use $agent-orchestration. Let one owner update backend validation and another update independent docs. State file ownership before dispatch and combine their results here.
```

Load `references/COORDINATION.md`. Overlapping writes are serialized or isolated.

## 3. User-owned worktree task

```text
Use $agent-orchestration. Create a visible worktree task for the risky refactor. I want to continue directly in that task.
```

Announce the new sidebar task, isolated write surface, result location, and follow-up owner.

## 4. Formal review gate

```text
Use $agent-orchestration. Accept the implementation only after one independent review and the final relevant test suite pass on the same candidate commit.
```

Intermediate owners use targeted checks. The final suite is not duplicated unless a code change invalidates evidence.

## 5. Quiet recurring monitor

```text
Use $agent-orchestration. Check the deployment each hour until healthy. Notify me only on a state change or blocker, then remove the automation.
```

Load `references/AUTOMATION.md` and use native automation tools.

## 6. Explicit agy review

```text
Use $agy-second-opinion to review the bounded diff through agy. Do not attach the repository. Verify accepted findings against the source.
```

This does not load `agent-orchestration`. Use the review reference and the sandboxed print helper.

## 7. Explicit agy research

```text
Use $agy-second-opinion for an independent agy research pass over the allowlisted architecture files, then compare it with Codex's own analysis.
```

Load only the research reference. External output remains a second opinion.

## 8. Capability preflight before dispatch

```text
Use $agent-orchestration. Before delegating browser QA, confirm that the owner can access the authenticated browser, run the required checks, and remain read-only. If not, keep QA in the current task.
```

The coordinator changes the execution surface before dispatch rather than accepting a result that could never inspect the real state.

## 9. Mid-flight requirement replacement

```text
Use $agent-orchestration. The original export format is cancelled; replace it with JSONL. Interrupt or redirect affected owners and do not merge late CSV work.
```

Late output from superseded scope is recorded as stale and can only be reused after revalidation against the new requirement.

## 10. Requirement closure and active-work audit

```text
Use $agent-orchestration. Before final, map every request and follow-up to current evidence, then check that no subagent, background command, monitor, or automation is still able to change the result.
```

Every item ends as `done`, `waived`, or `blocked`; unaccounted running work prevents a completion claim.

## 11. Correction versus independent review

```text
Use $agent-orchestration. Return the failed edge case to the implementer with the exact test output. After correction, give a fresh reviewer only the requirements, candidate commit, and raw evidence.
```

The implementer retains useful context for correction; the reviewer does not inherit the implementer's conclusions as facts.

## 12. Recovery capsule

```text
Use $agent-orchestration. Before handing this task to a worktree, preserve the latest objective, constraints, baseline, verified evidence, decisions, pending work, active processes, blocker, and exact next action.
```

Use native task history for the capsule unless the repository genuinely needs a durable handoff artifact.

## 13. Optional Best-of-N

```text
Use $agent-orchestration. Try three isolated implementations of the parser. Fix the correctness/performance/maintenance rubric before results arrive, reject all candidates if needed, and run the full suite only on the integrated winner.
```

Best-of-N is an explicit high-cost route, not the default for ordinary implementation.
