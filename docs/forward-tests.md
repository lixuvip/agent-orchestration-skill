# Forward-test scenarios

These scenarios test routing decisions rather than custom protocol serialization.

## bounded_subagent

Prompt: ask one internal subagent for a bounded read-only result that returns to the current task.

Expected:

- no sidebar task;
- no coordination or automation reference;
- no task board, callback JSON, heartbeat, lease, or status file;
- coordinator inspects the returned evidence.

## visible_user_task

Prompt: ask for a separate task that the user can see and continue directly.

Expected:

- announce that a sidebar task will appear;
- state where results live and who owns follow-up;
- use create/continue/fork/worktree/handoff according to their native semantics.

## formal_gate

Prompt: coordinate implementation and independent review of one candidate artifact.

Expected:

- load one language version of the coordination reference;
- define owners and non-overlapping scope;
- run targeted checks during implementation;
- run one final relevant suite on the exact candidate artifact;
- rerun only invalidated checks after changes.

## recurring_work

Prompt: monitor a changing state until a defined completion condition.

Expected:

- load one automation reference;
- use native automation tools;
- make unchanged ticks a quiet no-op;
- stop and clean up when the condition is satisfied.

## explicit_external_pass

Prompt: explicitly request an `agy` review or research pass.

Expected:

- trigger `agy-second-opinion`, not `agent-orchestration`;
- load exactly one of REVIEW or RESEARCH;
- keep the pass read-only with bounded disclosure;
- verify accepted external claims with Codex evidence.

## capability_preflight

Prompt: delegate work that needs a specific authenticated browser, connector, network path, or write/execute capability.

Expected:

- verify the required capabilities before dispatch;
- keep genuinely ambiguous planning read-only in the current task;
- do not assume a child inherits the parent's plan/read-only restrictions;
- change the surface or scope if the owner cannot inspect the real artifact.

## midflight_steering

Prompt: replace or extend a requirement while owners are still active.

Expected:

- classify the message as replace, add, or status;
- update or interrupt affected owners;
- preserve the latest effective scope in the current task;
- treat late superseded output as stale until revalidated.

## correction_vs_review

Prompt: an implementation fails one check and then needs independent review.

Expected:

- return the failure evidence and delta to the same implementation owner;
- give the independent reviewer fresh context, requirements, candidate artifact, and raw evidence;
- do not preload the implementer's conclusions as facts.

## requirement_closure

Prompt: finish a task with multiple follow-ups and mixed code/operational deliverables.

Expected:

- reconstruct the complete request including corrections;
- map each item to an action, current evidence, and `done`, `waived`, or `blocked`;
- do not use passing tests as proof for requirements the tests do not cover.

## active_work_audit

Prompt: prepare the final response after parallel or background work.

Expected:

- inspect native status for subagents, user-owned tasks, commands, monitors, and automations;
- wait for, cancel, or explicitly report every active item;
- never claim the whole objective is complete while unaccounted work can change it.

## bounded_retry

Prompt: a delegated check repeatedly hits the same blocker.

Expected:

- each retry adds evidence, narrows the failure, or changes approach;
- identical blockers do not produce an indefinite loop;
- ask, escalate, or report when no new progress is possible.

## recovery_capsule

Prompt: fork, hand off, or pause a context-sensitive task.

Expected:

- preserve objective, latest constraints, baseline, evidence, decisions, pending work, active work, blocker, and next action;
- use native task history unless the project needs a durable artifact.

## optional_best_of_n

Prompt: explicitly request several implementations or present a genuinely high-ambiguity design.

Expected:

- use only 2-3 isolated candidates;
- fix the rubric before candidate results;
- compare equivalent evidence and permit rejecting every candidate;
- run the full final suite only on the selected integrated candidate.

## Failure signals

The revision fails if ordinary delegation probes `agy`, if the main skill creates manual lifecycle files, if an internal subagent is described as a user-owned sidebar task, if formal verification is duplicated without invalidated evidence, if superseded work is accepted as current, or if final delivery leaves active work unaccounted.
