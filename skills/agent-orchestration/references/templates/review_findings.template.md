# Review Findings Template

```text
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT

Findings:
- [P0 | P1 | P2 | P3] <TITLE>
  File: <PATH:LINE>
  Problem: <WHAT_IS_WRONG>
  Impact: <WHY_IT_MATTERS>
  Suggested fix: <HOW_TO_FIX_OR_DIRECTION>

Open questions:
- <QUESTION_OR_NONE>

Test gaps:
- <GAP_OR_NONE>

Merge recommendation:
- APPROVE | APPROVE_WITH_CONCERNS | REQUEST_CHANGES | BLOCKED

Recommended next role:
- <Technical Engineer | QA Tester | Coordinator>
```

## 审查重点

- 正确性。
- 回归风险。
- 并发、权限、数据一致性、边界条件。
- 测试是否覆盖关键行为。
- 是否有无关重构或越权改动。

