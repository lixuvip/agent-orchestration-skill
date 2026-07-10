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
- 使用有界 prompt 或 build_agy_context_bundle.py；默认不要挂载整个仓库。
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
角色终态只进入 IN_REVIEW；只有 QA/Review 证据绑定当前 commit SHA 且协调者为 ACCEPTED，才算发布就绪。
```

## 示例 6：需要回调的长任务

```text
Use $agent-orchestration.

Dispatch this long-running migration to a separate engineering thread.
Require the role to callback to this coordinator thread when complete.
If callback fails, require CALLBACK_FAILED in the role's final reply.
Also create a heartbeat monitor that checks the role every 5 minutes.
重叠 tick 使用 fenced lease，并按 ACTIVE -> DRAINING -> CLOSED 关闭；最终汇总只发一次，等待工具确认清理。
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
Each tick should acquire a fenced lease, compare the latest effective update and idempotency keys, take one safe next action, verify the lease before side effects and memory writes, and escalate if merge/push/deploy or scope expansion is needed.
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
Run python3 scripts/forward_test.py, scripts/protocol_test.py, scripts/automation_test.py, and scripts/routing_test.py with the normal validation suite.
Report any missing trigger coverage before preparing release notes.
```

## 示例 11：可选 Agy / Gemini 审查

```text
Use $agent-orchestration to add an agy/Gemini external review pass for the current branch diff.

Treat agy as a read-only second opinion.
在这个 workflow 里，Gemini 只能表示 Gemini via agy，不能直接使用 standalone `gemini` CLI。
For broad or full-project review, run a dual Codex + Gemini review: keep a Codex reviewer role independent from the agy pass, then compare agreed findings, Gemini-only findings, Codex-only findings, rejected findings, and verification evidence.
默认保持只读；只有目标项目的稳定规则写入被单独授权时才修改 AGENTS.md。
这个 workflow 的探测命令只允许 `command -v agy` 和 `agy models`，不要去跑 `command -v gemini`、`gemini --version` 或 `gemini --help`。
使用审查 prompt 模板里的反向护栏：不要漂移到 CLI/auth 叙述，不要声称执行过命令，不要把范围扩到 diff 之外，也不要塞泛泛建议。
通过 run_agy_print.py 走固定 sandboxed 模式；需要源码时挂载 allowlist bundle，不直接挂项目根目录。需要自动拦截 0 输出或 narration-only 输出时，加上 --expect-substring READY 或 Status:。
如果某个进程误开 `gemini` CLI 并返回 403，按 `WRONG_EXECUTION_SURFACE` 处理并改回 `agy` 重跑。
Do not let agy edit files or claim tests passed unless exact command output is supplied.
After the review returns, evaluate review quality and classify each finding as valid, partially_valid, not_supported, or needs_human_check before deciding the next role.
Show the result as a dedicated review report with Agy findings, dual-review comparison, quality evaluation, Codex verification, and recommended next steps.
把质量记录写入默认 Codex external-review ledger，只有出现 LOG_WRITTEN 或 LOG_ALREADY_PRESENT 才声明已持久化。
```

## 示例 12：从 Lite 逐步升级到 Durable

```text
Use $agent-orchestration，并在每个阶段选择最低安全模式。

阶段 1：对当前 diff 获取一次只读 agy 第二意见，并在当前线程综合。保持 Lite，不创建额外线程或 recurring automation。
阶段 2：如果需要修复，异步协调一个隔离工程角色和一个只读 QA 角色。升级到 Standard，使用版本化回调、task board、commit 固定门禁和带租约 heartbeat。
阶段 3：只有我要求每两小时继续检查 issue/PR 时，升级 Durable，加入目标契约、cron、automation memory、fenced lease 和 lifecycle 规则。

说明所选模式和原因，不要把后续重流程提前带进前一阶段。
```

## 示例 13：拒绝过期回调

```text
Use $agent-orchestration 判断这些回调。

当前有效任务是 attempt 2，dispatch nonce 为 dispatch-2，coordinator epoch 为 epoch-7，expected commit 为 bbbbbbb。
这时晚到一个 attempt 1、commit aaaaaaa 的 DONE 回调。
随后 bbbbbbb 的 QA event 用相同 event ID 到达两次。
最后工程根据 review 反馈产生 ccccccc。

分类 stale 和 duplicate，不能改变当前状态。不能把角色 DONE 当成交付。产生 ccccccc 后，使 bbbbbbb 的 QA/Review 证据失效，并对新精确 SHA 重新派发门禁。
```

## 示例 14：重叠 Autopilot Tick

```text
Use $agent-orchestration 的 Durable 模式运行每两小时一次的 issue/PR autopilot。

假设两个 cron tick 可能重叠，或旧 tick 在租约过期后恢复。
读取可变 memory 前取得文件锁租约。
LEASE_ALREADY_HELD 和 LEASE_BUSY 都安静 no-op。
发消息、写 memory 或 cleanup 前验证当前 owner token。
保存最新 fencing token，拒绝更低 token 写入。
heartbeat 全员终态后按 ACTIVE -> DRAINING -> CLOSED 收尾，最终汇总只发一次，并等待 automation 工具确认清理。
```
