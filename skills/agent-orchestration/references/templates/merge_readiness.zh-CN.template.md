# 中文合并就绪模板

在合并、推送、发布或告诉用户某分支已就绪之前使用。

```text
合并就绪检查：<TASK_ID>

Goal ID: <GOAL_ID>
Attempt: <当前有效_ATTEMPT>
Dispatch nonce: <当前有效_DISPATCH_NONCE>
Coordinator epoch: <当前有效_COORDINATOR_EPOCH>
仓库：<REPO_PATH>
分支 / 工作区：<BRANCH_OR_WORKTREE>
基准分支：<BASE_BRANCH>
目标分支：<TARGET_BRANCH>
Expected head SHA: <EXPECTED_HEAD_SHA>
Observed head SHA: <OBSERVED_HEAD_SHA>

工作区：
- 是否干净：<YES_OR_NO>
- 未跟踪文件：<NONE_OR_LIST>
- 未提交改动：<NONE_OR_LIST>

范围：
- 预期修改文件：
- 非预期修改文件：
- 是否触碰禁止范围：<YES_OR_NO>

绑定到 observed head SHA 的门禁：
- 工程验证：PASS | FAIL | BLOCKED | WAIVED | NOT_APPLICABLE
- QA：PASS | FAIL | BLOCKED | WAIVED | NOT_APPLICABLE
- 代码审查：PASS | FAIL | BLOCKED | WAIVED | NOT_APPLICABLE
- 证据 SHA 是否一致：<YES_OR_NO>

冲突：
- 是否已同步基准分支：<YES_OR_NO>
- 是否预计有合并冲突：<YES_OR_NO_OR_UNKNOWN>

风险和豁免：
- <无_具体风险_或明确豁免原因>

推送权限：
- <NOT_REQUESTED | COMMIT_ONLY | PUSH_BRANCH | MERGE_TO_TARGET | CREATE_PR>

Coordinator state:
- <IN_REVIEW | RETURNED | ACCEPTED | ESCALATED | CANCELLED>

结论：
- <READY | NEEDS_FIX | NEEDS_USER_CONFIRMATION | BLOCKED>
```

只有精确 SHA 一致、必需门禁通过或明确豁免、且 coordinator state 为 `ACCEPTED` 时才能写 `READY`。分支名本身不是充分证据。
