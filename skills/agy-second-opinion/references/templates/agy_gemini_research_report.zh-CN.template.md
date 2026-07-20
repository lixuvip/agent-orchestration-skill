# Agy / Gemini 调研报告展示模板

后台 `agy` 调研、质量评估和 Codex 综合判断完成后，用本模板在对话中展示专属调研内容。不要要求用户查看底部终端。

```text
**Agy 外部调研报告**

Status: `DONE | DONE_WITH_CONCERNS | BLOCKED`
Model: `{{MODEL_NAME}}`
Mode: `{{COMMAND_SHAPE}}`（期望：`agy --add-dir <allowlisted_context> --print <prompt> --sandbox`）
Timeout: `{{PRINT_TIMEOUT}}`
Scope: {{RESEARCH_SCOPE}}

调研输入：
- {{INPUT_1}}
- {{INPUT_2_OR_NONE}}

前置检查：
- 使用授权：{{EXPLICIT_REQUEST_OR_ONCE_ONLY_OPT_IN_OR_CODEX_ONLY}}
- 能力缓存：{{UNKNOWN_OR_AVAILABLE_OR_AGY_UNAVAILABLE_OR_AGY_UNHEALTHY}}
- 用户提示：{{NOTICE_SENT_ONCE_OR_NOT_NEEDED}}
- 降级路径：{{CODEX_ONLY_OR_NONE}}
- `agy models`：{{MODELS_CHECK_RESULT}}
- 健康检查：{{HEALTH_CHECK_RESULT}}
- Scope attachment：{{SCOPE_ATTACHMENT_RESULT}}
- Context manifest / 披露例外：{{CONTEXT_MANIFEST_OR_EXCEPTION}}
- 仓库变更：{{MUTATION_RESULT}}
- 质量日志：{{LOG_WRITTEN_OUTPUT_OR_NOT_WRITTEN_REASON}}

**Agy Research Points**
1. {{CATEGORY}}：{{POINT_TITLE}}
   Agy 观点：{{POINT_CLAIM}}
   Codex 分类：`accepted | partially_accepted | speculative | rejected`

**并行调研对比**
- Codex 调研状态：`{{CODEX_RESEARCH_STATUS_OR_NOT_RUN}}`
- Gemini 调研状态：`{{GEMINI_RESEARCH_STATUS}}`
- 共同观点：{{AGREED_POINTS_OR_NONE}}
- Gemini-only：{{GEMINI_ONLY_POINTS_OR_NONE}}
- Codex-only：{{CODEX_ONLY_POINTS_OR_NONE}}
- 驳回 / 推测性观点：{{REJECTED_POINTS_OR_NONE}}
- 后续问题：{{FOLLOW_UP_QUESTIONS_OR_NONE}}

**质量评估**
整体评分：`{{QUALITY_SCORE}}/5`

- 优点：{{QUALITY_STRONG_POINTS}}
- 弱点：{{QUALITY_WEAK_POINTS}}
- 无依据声明：{{UNSUPPORTED_CLAIMS}}
- 遗漏角度：{{MISSED_ANGLES_OR_NONE}}

**Codex 综合判断**
- {{SYNTHESIS_POINT_1}}
- {{SYNTHESIS_POINT_2_OR_NONE}}

**建议下一步**
1. {{NEXT_STEP_1}}
2. {{NEXT_STEP_2_OR_NONE}}
3. {{NEXT_STEP_3_OR_NONE}}
```
