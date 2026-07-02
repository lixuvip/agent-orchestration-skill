# Orchestration Intake Template

Use this when the coordinator needs a short route confirmation before creating branches, threads, worktrees, automations, or merge/push actions.

```text
I can coordinate this in a few ways. Ask only if the answer changes execution, write authority, callback, automation, merge, or push behavior.

Execution surface:
- <current thread only | internal subagent | user-visible Codex thread | existing thread | branch/worktree>

Callback behavior:
- <final answer only | role callback to coordinator thread | callback plus heartbeat | manual task board>

Merge/push permission:
- <summarize only | commit allowed | push branch allowed | merge allowed | PR allowed>

Questions:
1. <QUESTION_ABOUT_EXECUTION_SURFACE>
2. <QUESTION_ABOUT_CALLBACK_BEHAVIOR>
3. <QUESTION_ABOUT_MERGE_OR_PUSH_PERMISSION>
```

