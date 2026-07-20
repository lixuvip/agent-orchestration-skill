# Agy / Gemini Research Report Template

Use this template as the coordinator-facing display after the background `agy` research pass, quality evaluation, and Codex synthesis are complete.

```text
**Agy External Research Report**

Status: `DONE | DONE_WITH_CONCERNS | BLOCKED`
Model: `{{MODEL_NAME}}`
Mode: `{{COMMAND_SHAPE}}` (expected: `agy --add-dir <allowlisted_context> --print <prompt> --sandbox`)
Timeout: `{{PRINT_TIMEOUT}}`
Scope: {{RESEARCH_SCOPE}}

Research inputs:
- {{INPUT_1}}
- {{INPUT_2_OR_NONE}}

Preflight:
- Consent: {{EXPLICIT_REQUEST_OR_ONCE_ONLY_OPT_IN_OR_CODEX_ONLY}}
- Availability cache: {{UNKNOWN_OR_AVAILABLE_OR_AGY_UNAVAILABLE_OR_AGY_UNHEALTHY}}
- User notice: {{NOTICE_SENT_ONCE_OR_NOT_NEEDED}}
- Fallback: {{CODEX_ONLY_OR_NONE}}
- `agy models`: {{MODELS_CHECK_RESULT}}
- Health check: {{HEALTH_CHECK_RESULT}}
- Scope attachment: {{SCOPE_ATTACHMENT_RESULT}}
- Context manifest / disclosure exception: {{CONTEXT_MANIFEST_OR_EXCEPTION}}
- Repository mutation: {{MUTATION_RESULT}}
- Quality log: {{LOG_WRITTEN_OUTPUT_OR_NOT_WRITTEN_REASON}}

**Agy Research Points**
1. {{CATEGORY}}: {{POINT_TITLE}}
   Agy claim: {{POINT_CLAIM}}
   Coordinator classification: `accepted | partially_accepted | speculative | rejected`

**Parallel Research Comparison**
- Codex research status: `{{CODEX_RESEARCH_STATUS_OR_NOT_RUN}}`
- Gemini research status: `{{GEMINI_RESEARCH_STATUS}}`
- Agreed points: {{AGREED_POINTS_OR_NONE}}
- Gemini-only points: {{GEMINI_ONLY_POINTS_OR_NONE}}
- Codex-only points: {{CODEX_ONLY_POINTS_OR_NONE}}
- Rejected / speculative points: {{REJECTED_POINTS_OR_NONE}}
- Follow-up questions: {{FOLLOW_UP_QUESTIONS_OR_NONE}}

**Quality Evaluation**
Score: `{{QUALITY_SCORE}}/5`

- Strong points: {{QUALITY_STRONG_POINTS}}
- Weak points: {{QUALITY_WEAK_POINTS}}
- Unsupported claims: {{UNSUPPORTED_CLAIMS}}
- Missed angles: {{MISSED_ANGLES_OR_NONE}}

**Codex Synthesis**
- {{SYNTHESIS_POINT_1}}
- {{SYNTHESIS_POINT_2_OR_NONE}}

**Recommended Next Steps**
1. {{NEXT_STEP_1}}
2. {{NEXT_STEP_2_OR_NONE}}
3. {{NEXT_STEP_3_OR_NONE}}
```
