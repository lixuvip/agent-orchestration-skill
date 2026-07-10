# 使用示例

可以直接复制使用的场景文件：

- [简单研究任务](../examples/simple-research-task.md)
- [编码加审查工作流](../examples/coding-review-workflow.md)
- [多代理产品规划](../examples/multi-agent-product-planning.md)
- [带 QA 的 Bug 修复](../examples/bugfix-with-qa.md)
- [多项目收尾](../examples/multi-project-finalization.md)
- [发布准备](../examples/release-prep.md)
- [分支回调主线程控制循环](../examples/branch-callback-controller-loop.md)
- [持续项目 Autopilot](../examples/continuous-project-autopilot.md)
- [GitHub issue 和 PR Autopilot](../examples/github-issue-pr-autopilot.md)

## 示例 1：带 QA 门禁的 Bug 修复

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

## 示例 2：实现前的并行调研

```text
Use $agent-orchestration.

Split this feature into parallel preparation:
- Product Designer: define acceptance criteria and user flow.
- Technical Engineer: inspect implementation options without editing files.
- QA Tester: propose the regression matrix.

After all three reply, merge their outputs into one engineering task.
```

## 示例 3：并行 Codex + Gemini 调研

```text
Use $agent-orchestration to research this repository in parallel with Codex and Gemini.

Goal:
Figure out the best approach for adding background job retries without widening the architecture unnecessarily.

Research rules:
- Codex must do its own repo reading and final synthesis.
- Gemini via agy should run as a read-only second research stream.
- Use run_agy_print.py so the prompt stays immediately after --print.
- 不要使用 standalone `gemini` CLI；如果某个进程误开它并返回 403，按 `WRONG_EXECUTION_SURFACE` 处理并改回 `agy` 重跑。
- Attach the repository with --add-dir <project_root>.
- Add --expect-substring AGY_RESEARCH_V1 so narration-only output is rejected automatically.
- Compare agreed points, Gemini-only points, Codex-only points, and rejected/speculative points before choosing the next engineering task.
- Append a quality log entry with task_type=research after the run.
```

## 示例 4：多仓库提交收尾

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

## 示例 5：发布准备

```text
Use $agent-orchestration for release preparation.

Roles:
- Release Docs: summarize changes and migration notes.
- QA Tester: verify critical paths.
- Code Reviewer: inspect high-risk diffs.

Do not publish release notes until QA and review have terminal statuses.
```

## 示例 6：需要回调的长任务

```text
Use $agent-orchestration.

Dispatch this long-running migration to a separate engineering thread.
Require the role to callback to this coordinator thread when complete.
If callback fails, require CALLBACK_FAILED in the role's final reply.
Also create a heartbeat monitor that checks the role every 5 minutes.
```

## 示例 7：分支回调主线程控制循环

```text
Use $agent-orchestration to coordinate branch work with direct callback to the main coordinator thread.

Create or continue a dedicated engineering branch/worktree.
Keep QA read-only.
Require every role to callback to the coordinator thread.
Create heartbeat monitoring if the work is long-running.
Run merge readiness before merging, pushing, or telling the user the branch is ready.
```

## 示例 8：持续项目 Autopilot

```text
Use $agent-orchestration to create a project autopilot loop for this repository.

Read AGENTS.md, AGENTS.override.md, project docs, and the release checklist first.
Create a goal contract with done criteria, allowed autonomous actions, confirmation gates, cadence, memory path, and stop conditions.
Use cron automation for workspace progress and heartbeat only for coordinator-thread callbacks.
Each tick should compare the latest effective update, take one safe next action, run verification, update automation memory, and escalate if merge/push/deploy or scope expansion is needed.
```

## 示例 9：GitHub Issue 和 PR Autopilot

```text
Use $agent-orchestration to run a GitHub issue/PR project autopilot.

Issue is the coordination channel.
PR is the implementation channel.
Do not stop just because there is no open PR.
Do not comment if the latest effective update is unchanged and already covered by a previous codex-next-action comment.
Read issue body, labels, comments, linked PR commits, files, checks, and review state before deciding the next safe action.
```

## 示例 10：发布前前向测试审计

```text
Use $agent-orchestration to audit this skill release before publishing.

Check that the forward-test scenarios still cover heartbeat callbacks, cron project autopilot, GitHub issue/PR no-op polling, missing AGENTS.md guidance, automation memory, latest effective update comparison, and escalation gates.
Run python3 scripts/forward_test.py with the normal validation suite.
Report any missing trigger coverage before preparing release notes.
```

## 示例 11：可选 Agy / Gemini 审查

```text
Use $agent-orchestration to add an agy/Gemini external review pass for the current branch diff.

Treat agy as a read-only second opinion.
在这个 workflow 里，Gemini 只能表示 Gemini via agy，不能直接使用 standalone `gemini` CLI。
For broad or full-project review, run a dual Codex + Gemini review: keep a Codex reviewer role independent from the agy pass, then compare agreed findings, Gemini-only findings, Codex-only findings, rejected findings, and verification evidence.
On first use in this project, ensure the stable agy/Gemini command-safety guidance is present in AGENTS.md before any agy health check or model discovery.
这个 workflow 的探测命令只允许 `command -v agy` 和 `agy models`，不要去跑 `command -v gemini`、`gemini --version` 或 `gemini --help`。
使用审查 prompt 模板里的反向护栏：不要漂移到 CLI/auth 叙述，不要声称执行过命令，不要把范围扩到 diff 之外，也不要塞泛泛建议。
通过 run_agy_print.py 走普通只读 print + `--sandbox` 模式，保证 prompt 紧跟在 --print 后面；做全项目审查时，再显式传入 --add-dir <项目根目录> 把仓库挂进 agy workspace；需要自动拦截 0 输出或 narration-only 输出时，加上 --expect-substring READY 或 Status:。
如果某个进程误开 `gemini` CLI 并返回 403，按 `WRONG_EXECUTION_SURFACE` 处理并改回 `agy` 重跑。
Do not let agy edit files or claim tests passed unless exact command output is supplied.
After the review returns, evaluate review quality and classify each finding as valid, partially_valid, not_supported, or needs_human_check before deciding the next role.
Show the result as a dedicated review report with Agy findings, dual-review comparison, quality evaluation, Codex verification, and recommended next steps.
Append a quality log entry to .codex/agent-orchestration/agy-review-quality.jsonl with append_agy_review_quality_log.py, and only claim logging succeeded if it prints LOG_WRITTEN.
```
