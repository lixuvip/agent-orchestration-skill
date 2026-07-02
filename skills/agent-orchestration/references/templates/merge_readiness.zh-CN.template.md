# 中文合并就绪模板

在合并、推送、发布或告诉用户某分支已就绪之前使用。

```text
合并就绪检查：<TASK_ID>

仓库：<REPO_PATH>
分支 / 工作区：<BRANCH_OR_WORKTREE>
基准分支：<BASE_BRANCH>
目标分支：<TARGET_BRANCH>

工作区：
- 是否干净：<YES_OR_NO>
- 未跟踪文件：<NONE_OR_LIST>
- 未提交改动：<NONE_OR_LIST>

范围：
- 预期修改文件：
- 非预期修改文件：
- 是否触碰禁止范围：<YES_OR_NO>

测试：
- <COMMAND_OR_CHECK>: PASS | FAIL | NOT RUN
  结果 / 原因：<DETAIL>

冲突：
- 是否已同步基准分支：<YES_OR_NO>
- 是否预计有合并冲突：<YES_OR_NO_OR_UNKNOWN>

风险：
- <无或具体风险>

推送权限：
- <NOT_REQUESTED | COMMIT_ONLY | PUSH_BRANCH | MERGE_TO_TARGET | CREATE_PR>

结论：
- <READY | NEEDS_FIX | NEEDS_USER_CONFIRMATION | BLOCKED>
```
