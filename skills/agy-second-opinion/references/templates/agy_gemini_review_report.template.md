# Agy / Gemini Review Report Template

Use this template as the coordinator-facing display after the background `agy` review, quality evaluation, and Codex verification are complete.

```text
**Agy External Review Report**

Status: `DONE | DONE_WITH_CONCERNS | BLOCKED`
Model: `{{MODEL_NAME}}`
Mode: `{{COMMAND_SHAPE}}` (expected: `agy --add-dir <allowlisted_context> --print <prompt> --sandbox`)
Timeout: `{{PRINT_TIMEOUT}}`
Scope: {{REVIEW_SCOPE}}

Review scope:
- {{FILE_OR_MODULE_1}}
- {{FILE_OR_MODULE_2_OR_NONE}}

Preflight:
- Consent: {{EXPLICIT_REQUEST_OR_ONCE_ONLY_OPT_IN_OR_CODEX_ONLY}}
- Availability cache: {{UNKNOWN_OR_AVAILABLE_OR_AGY_UNAVAILABLE_OR_AGY_UNHEALTHY}}
- User notice: {{NOTICE_SENT_ONCE_OR_NOT_NEEDED}}
- Fallback: {{CODEX_ONLY_OR_NONE}}
- `agy models`: {{MODELS_CHECK_RESULT}}
- Health check: {{HEALTH_CHECK_RESULT}}
- Diff / whitespace check: {{DIFF_CHECK_RESULT}}
- Context manifest / disclosure exception: {{CONTEXT_MANIFEST_OR_EXCEPTION}}
- Repository mutation: {{MUTATION_RESULT}}
- Quality log: {{LOG_WRITTEN_OUTPUT_OR_NOT_WRITTEN_REASON}}

**Agy Findings**
1. {{SEVERITY}}: {{FINDING_TITLE}}
   Agy evidence: {{FINDING_EVIDENCE}}
   Coordinator classification: `valid | partially_valid | not_supported | needs_human_check`

**Dual Review Comparison**
- Codex reviewer status: `{{CODEX_REVIEWER_STATUS_OR_NOT_RUN}}`
- Gemini reviewer status: `{{GEMINI_REVIEWER_STATUS}}`
- Agreed findings: {{AGREED_FINDINGS_OR_NONE}}
- Gemini-only findings: {{GEMINI_ONLY_FINDINGS_OR_NONE}}
- Codex-only findings: {{CODEX_ONLY_FINDINGS_OR_NONE}}
- Rejected / unsupported findings: {{REJECTED_FINDINGS_OR_NONE}}
- Verification contrast: {{VERIFICATION_CONTRAST}}

**Quality Evaluation**
Score: `{{QUALITY_SCORE}}/5`

- Strong points: {{QUALITY_STRONG_POINTS}}
- Weak points: {{QUALITY_WEAK_POINTS}}
- Unsupported claims: {{UNSUPPORTED_CLAIMS}}
- Omissions: {{OMISSIONS_OR_NONE}}

**Codex Verification**
- {{FINDING_1_CLASSIFICATION_AND_REASON}}
- {{FINDING_2_CLASSIFICATION_AND_REASON_OR_NONE}}

**Recommended Next Steps**
1. {{NEXT_STEP_1}}
2. {{NEXT_STEP_2_OR_NONE}}
3. {{NEXT_STEP_3_OR_NONE}}
```
