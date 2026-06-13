# 中文角色回复模板

所有角色完成任务后都应按此格式回复。

```text
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT

Summary:
- <完成或检查了什么>

Changed files / Files inspected:
- <PATH>: <为什么修改或检查它>

Verification run:
- <COMMAND_OR_CHECK>: PASS | FAIL | NOT RUN
  Result / reason: <结果或未运行原因>

Risks / concerns:
- <无，或具体风险>

Recommended next role:
- <Coordinator | Product Designer | Technical Engineer | QA Tester | Code Reviewer | Release / Docs>
```

## 回复要求

- 不允许只回复“完成了”。
- `NOT RUN` 必须说明原因。
- 如果有失败，必须写出失败命令、失败现象和建议下一步。
- 如果有风险，使用 `DONE_WITH_CONCERNS`，不要假装 `DONE`。
