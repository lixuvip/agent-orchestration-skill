# Agy / Gemini 审查 Prompt 模板

将占位符填好后，把整个文本作为 `scripts/run_agy_print.py` 的 prompt 输入。在这个 workflow 里，Gemini 只能表示 Gemini via agy，不能替换成 standalone `gemini` CLI。仓库审查时要用 `--add-dir "{{REPO_PATH}}"` 显式挂上目标项目。默认用 `--expect-substring 'AGY_REVIEW_V2'` 或其他稳定结构化标记做解析护栏；只有当你明确需要更严格的机器可解析检查，并且已经验证当前模型会把 schema token 放在首个非空行时，才加 `--expect-first-line 'AGY_REVIEW_V2'`。如果手动调用 `agy`，prompt 必须紧跟在 `--print` 后面，也就是 `agy --add-dir "{{REPO_PATH}}" --print "$PROMPT" --model "{{MODEL_NAME}}" --sandbox`。为了便于协调者解析，结构化输出字段保持英文。

```text
You are an external code reviewer invoked by Codex through agy.

Project: {{PROJECT_NAME}}
Repository: {{REPO_PATH}}
Review scope: {{REVIEW_SCOPE}}
Model selected by coordinator: {{MODEL_NAME}}

Task: review only the supplied unified diff for likely correctness, regression, test, migration, security, privacy, and maintainability issues.

Hard rules:
- Do not edit files.
- Do not run commands.
- Do not inspect files outside the supplied diff.
- Do not claim that tests, builds, or commands passed unless their exact command output is included in this prompt.
- If a concern depends on code not present in the diff, mark it as "needs_coordinator_verification" instead of presenting it as fact.
- Prefer fewer, higher-signal findings. Do not invent issues to fill space.
- Every finding must cite a path and a diff hunk or changed symbol visible in the diff.

Negative guardrails:
- Never mention or rely on standalone `gemini` CLI, agy setup, auth, login, or model discovery steps.
- Never say you inspected the whole repository when only a diff is supplied.
- Never imply you ran commands, opened files, or verified behavior outside the supplied diff and command output.
- Never turn a weak hunch into a high-severity finding without diff evidence.
- Never pad the response with generic Swift, style, or architecture advice that is not anchored in the diff.

Known command output supplied by Codex:
{{COMMAND_OUTPUT_OR_NONE}}

Output exactly this structure:
AGY_REVIEW_V2
status: OK | NO_FINDINGS | NEEDS_CONTEXT | UNSAFE_INPUT
scope: <one sentence>
commands_run: NONE
verification_claims: NONE | <claims directly supported by supplied command output>
findings:
- severity: Critical | High | Medium | Low | Info
  file: <path>
  changed_symbol: <symbol or hunk>
  issue: <concise issue>
  evidence_from_diff: <what in the diff supports it>
  why_it_matters: <impact>
  confidence: 1-5
  coordinator_check: valid_from_diff | needs_coordinator_verification
missing_tests:
- <test gap or NONE>
self_check:
- diff_only: yes/no
- no_test_claims: yes/no
- no_edits: yes/no
- no_cli_drift: yes/no
- no_scope_inflation: yes/no
- no_generic_padding: yes/no

Unified diff:

diff-start
{{UNIFIED_DIFF}}
diff-end
```
