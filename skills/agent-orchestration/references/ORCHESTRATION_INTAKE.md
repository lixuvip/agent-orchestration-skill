# Orchestration Intake

Use this reference before dispatch when the user's request may create branches, worktrees, child threads, callbacks, heartbeat automation, merges, commits, pushes, or handoffs between conversations.

## Decision Rule

Ask only when the answer changes execution surface, write authority, callback behavior, automation, merge, push, or user-visible thread creation.

Do not ask when the user already specified the route, such as "use another agent", "create a new thread", "分给 QA 验证", "20 minutes later merge and push", or "let the branch reply to the main thread". In those cases, execute the narrowest safe route and record the assumption.

## Confirmation Surfaces

- **Execution surface**: current thread, internal subagent, user-visible Codex thread, existing thread, branch, worktree, or read-only audit.
- **Write authority**: read-only, scoped edits, tests only, commit allowed, push allowed, merge allowed.
- **Callback behavior**: final answer only, callback to coordinator thread, callback plus heartbeat, or manual task-board polling.
- **Merge/push permission**: summarize only, prepare commit, commit only, push branch, merge to main, or create PR.

## Tool Handling

If a UI elicitation tool such as `request_user_input` is available, use it for 1-3 short questions when the choice is useful but not obvious. If no elicitation tool is available, ask concise plain-text questions. Do not simulate a UI control in text.

If the user asks for autonomous orchestration and the operation is non-destructive, default to safe automation: isolated branch or worktree, callback required, heartbeat for long-running or multi-thread work, no merge or push unless explicitly authorized.

## Intake Shortcut

Use `templates/orchestration_intake.template.md` or the Chinese version when asking the user to choose route, callback, and merge policy.

