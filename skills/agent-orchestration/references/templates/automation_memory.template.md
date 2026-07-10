# Automation Memory Template

Use this for the durable state file written by project autopilot automations.

```markdown
# Automation Memory

Goal ID: <GOAL_ID>
Automation ID: <AUTOMATION_ID>
Workspace: <PATH_OR_REPOSITORY>
Last updated: <ISO_TIMESTAMP>

## Concurrency Lease

- State directory: <AUTOMATION_STATE_DIRECTORY>
- Last owner ID: <TICK_ID_OR_NONE>
- Latest fencing token: <NON_NEGATIVE_INTEGER>
- Lease expires at: <ISO_TIMESTAMP_OR_NONE>
- Last lease result: <ACQUIRED | ALREADY_HELD | BUSY | EXPIRED | NOT_OWNER | RELEASED | NONE>

Never overwrite this file from a lower fencing token.

## Lifecycle

- State: <ACTIVE | DRAINING | CLOSED>
- Heartbeat generation: <GENERATION_ID_OR_NOT_APPLICABLE>
- Final summary key: <KEY_OR_NONE>
- Final summary posted: <YES_OR_NO>
- Cleanup request ID: <ID_OR_NONE>
- Cleanup confirmed: <YES_OR_NO>

## Goal

<ONE_SENTENCE_GOAL>

## Done Criteria

- <CRITERION_1>
- <CRITERION_2>

## Latest Effective Update

- Source: <issue | pr | branch | tests | thread | release | none>
- Value: <UPDATE_SUMMARY_OR_HASH>
- Covered by Codex action: <YES_OR_NO>

## Last Tick

- Observed state: <SUMMARY>
- Action taken: <ONE_ACTION_OR_NONE>
- Verification: <COMMAND_OR_CHECK_AND_RESULT>
- Result: <DONE | IN_PROGRESS | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>
- Risks: <NONE_OR_RISK>
- Fencing token: <INTEGER>

## Next Safe Action

<ONE_ACTION_OR_NONE>

## Blocker History

- <TIMESTAMP>: <BLOCKER_OR_NONE>

## Posted Messages

- <TIMESTAMP_OR_ID>: <WHERE_AND_SUMMARY>

## Processed Events And Actions

- Event IDs: <EVENT_ID_LIST_OR_NONE>
- Status request keys: <TASK_ATTEMPT_NONCE_KEY_LIST_OR_NONE>
- Action idempotency keys: <ACTION_KEY_LIST_OR_NONE>
- Escalation keys: <ESCALATION_KEY_LIST_OR_NONE>
```
