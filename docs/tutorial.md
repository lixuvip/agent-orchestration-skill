# Tutorial

## 1. Start from ownership

Keep a single-owner deliverable in the current task. Delegation is useful only when an independent result can proceed without overlapping writes.

## 2. Pick the native surface

Use an internal subagent when the result should return to the coordinator. Use a user-owned task when the user wants sidebar visibility or direct follow-up. Fork carries completed history; worktree isolates writes; handoff moves the same task between Local and Worktree.

## 3. Announce visibility

Before delegating, say whether a sidebar task will appear, where the result returns, and who owns follow-up.

## 4. Load detail only when needed

A bounded internal subagent needs only `SKILL.md`. Multiple owners, worktrees, cross-repo work, or formal gates load one coordination reference. Recurring work loads one automation reference.

## 5. Verify once at the right level

Use targeted checks while implementing. Bind review and QA to the exact candidate artifact, then run one final relevant suite. Do not duplicate verification unless a change invalidates it.

## 6. Close the request, not just the tests

Map every original request, follow-up, and correction to an action, current evidence, and `done`, `waived`, or `blocked`. Audit active work before final. If the user changes direction mid-flight, update or interrupt affected owners and treat old-scope output as stale.

## 7. Keep AGY separate

An external second opinion is a different skill. Only an explicit request activates `$agy-second-opinion`; ordinary orchestration never probes or invokes it.
