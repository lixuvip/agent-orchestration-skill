# Automation Memory Template

Use this for the durable state file written by project autopilot automations.

```markdown
# Automation Memory

Goal ID: <GOAL_ID>
Automation ID: <AUTOMATION_ID>
Workspace: <PATH_OR_REPOSITORY>
Last updated: <ISO_TIMESTAMP>

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

## Next Safe Action

<ONE_ACTION_OR_NONE>

## Blocker History

- <TIMESTAMP>: <BLOCKER_OR_NONE>

## Posted Messages

- <TIMESTAMP_OR_ID>: <WHERE_AND_SUMMARY>
```
