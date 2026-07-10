# Agy / Gemini 审查报告展示模板

后台 `agy` 审查、质量评估和 Codex 复核完成后，用本模板在对话中展示专属审查内容。不要要求用户查看底部终端。

```text
**Agy 外部审查报告**

Status: `DONE | DONE_WITH_CONCERNS | BLOCKED`
Model: `{{MODEL_NAME}}`
Mode: `{{COMMAND_SHAPE}}`（期望：`agy --add-dir <allowlisted_context> --print <prompt> --sandbox`）
Timeout: `{{PRINT_TIMEOUT}}`
Scope: {{REVIEW_SCOPE}}

审查范围：
- {{FILE_OR_MODULE_1}}
- {{FILE_OR_MODULE_2_OR_NONE}}

前置检查：
- `agy models`：{{MODELS_CHECK_RESULT}}
- 健康检查：{{HEALTH_CHECK_RESULT}}
- diff / 空白检查：{{DIFF_CHECK_RESULT}}
- Context manifest / 披露例外：{{CONTEXT_MANIFEST_OR_EXCEPTION}}
- 仓库变更：{{MUTATION_RESULT}}
- 质量日志：{{LOG_WRITTEN_OUTPUT_OR_NOT_WRITTEN_REASON}}

**Agy Findings**
1. {{SEVERITY}}：{{FINDING_TITLE}}
   Agy 依据：{{FINDING_EVIDENCE}}
   Codex 分类：`valid | partially_valid | not_supported | needs_human_check`

**双轨审查对比**
- Codex 审查状态：`{{CODEX_REVIEWER_STATUS_OR_NOT_RUN}}`
- Gemini 审查状态：`{{GEMINI_REVIEWER_STATUS}}`
- 共同命中：{{AGREED_FINDINGS_OR_NONE}}
- Gemini-only：{{GEMINI_ONLY_FINDINGS_OR_NONE}}
- Codex-only：{{CODEX_ONLY_FINDINGS_OR_NONE}}
- 驳回 / 无依据：{{REJECTED_FINDINGS_OR_NONE}}
- 验证对比：{{VERIFICATION_CONTRAST}}

**质量评估**
整体评分：`{{QUALITY_SCORE}}/5`

- 优点：{{QUALITY_STRONG_POINTS}}
- 弱点：{{QUALITY_WEAK_POINTS}}
- 无依据声明：{{UNSUPPORTED_CLAIMS}}
- 遗漏：{{OMISSIONS_OR_NONE}}

**Codex 复核结论**
- {{FINDING_1_CLASSIFICATION_AND_REASON}}
- {{FINDING_2_CLASSIFICATION_AND_REASON_OR_NONE}}

**建议下一步**
1. {{NEXT_STEP_1}}
2. {{NEXT_STEP_2_OR_NONE}}
3. {{NEXT_STEP_3_OR_NONE}}
```
