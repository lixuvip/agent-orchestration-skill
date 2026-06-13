# Role Reply Template

所有角色完成任务后都应按此格式回复。

```text
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT

Summary:
- <WHAT_WAS_DONE_OR_INSPECTED>

Changed files / Files inspected:
- <PATH>: <WHY_IT_WAS_CHANGED_OR_INSPECTED>

Verification run:
- <COMMAND_OR_CHECK>: PASS | FAIL | NOT RUN
  Result / reason: <DETAIL>

Risks / concerns:
- <NONE_OR_SPECIFIC_RISK>

Recommended next role:
- <Coordinator | Product Designer | Technical Engineer | QA Tester | Code Reviewer | Release / Docs>
```

## 回复要求

- 不允许只回复“完成了”。
- `NOT RUN` 必须说明原因。
- 如果有失败，必须写出失败命令、失败现象和建议下一步。
- 如果有风险，使用 `DONE_WITH_CONCERNS`，不要假装 `DONE`。

