# Quickstart

## Choose the skill

Use `$agent-orchestration` for Codex delegation, task visibility, worktrees, gates, or recurring continuation.

Use `$agy-second-opinion` only when an `agy`/Gemini external pass is explicitly requested.

## Small delegation

```text
Use $agent-orchestration. Have one internal subagent inspect the parser read-only and return the likely failure path here.
```

Expected behavior:

- no new sidebar task;
- no coordination reference or protocol files;
- one bounded owner and one returned result;
- coordinator verifies the evidence before accepting it.

## Visible task

```text
Use $agent-orchestration. Create a separate task for the release checklist so I can follow up there.
```

Expected behavior:

- the coordinator announces that a sidebar task will appear;
- the user-owned task owns direct follow-up;
- worktree, fork, or handoff is used only if its distinct semantics are needed.

## Formal gate

```text
Use $agent-orchestration. Coordinate implementation and one independent review against the exact candidate commit.
```

The coordination reference is loaded in one language. Targeted checks run during implementation and one final relevant suite runs on the candidate artifact.

Before dispatch, preflight the owner's required read, write, execute, network, browser, and connector capabilities. During active work, classify new user input as replace, add, or status; superseded output is stale until revalidated.

Before final delivery, map every request and follow-up to current evidence and audit active agents, tasks, background commands, monitors, and automations.

## Recurring continuation

```text
Use $agent-orchestration to check this release every weekday until it is published, staying quiet when nothing changes.
```

The automation reference routes this through native automation tools with a clear stop condition and cleanup.

## External second opinion

```text
Use $agy-second-opinion for one bounded read-only agy review of these files.
```

Only the review reference is loaded. Context disclosure stays bounded, and Codex verifies accepted findings.
