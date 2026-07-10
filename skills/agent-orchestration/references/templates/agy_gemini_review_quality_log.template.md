# Agy / Gemini Review Quality Log Template

Prepare one JSON object per completed external review and append it with `scripts/append_agy_review_quality_log.py` to:

```text
<PROJECT_ROOT>/.codex/agent-orchestration/agy-review-quality.jsonl
```

Use JSONL: each line is one compact JSON object. Do not store secrets, tokens, cookies, private vault note contents, customer data, full diffs, or raw proprietary documents. Store paths, hashes, summarized findings, and review-quality signals only.

If the target repository forbids writes or the user requested a read-only pass, display the JSONL entry in the coordinator reply and record why it was not written.

Write command:

```bash
python3 <SKILL_DIR>/scripts/append_agy_review_quality_log.py --project-root "{{PROJECT_ROOT}}" <<'JSON'
{{QUALITY_LOG_JSON_OBJECT}}
JSON
```

Success requires `LOG_WRITTEN <path>` in stdout. If the helper prints `LOG_NOT_WRITTEN` or exits non-zero, do not claim the log was written.

```json
{
  "timestamp": "{{ISO_8601_LOCAL_OR_UTC}}",
  "project": "{{PROJECT_NAME}}",
  "repository": "{{REPO_PATH}}",
  "thread_id": "{{THREAD_ID_OR_UNKNOWN}}",
  "coordinator_thread_id": "{{COORDINATOR_THREAD_ID_OR_UNKNOWN}}",
  "review_id": "{{STABLE_REVIEW_ID}}",
  "model": "{{MODEL_NAME}}",
  "mode": "run_agy_print.py -> agy --add-dir <project_root> --print <prompt> --sandbox",
  "timeout": "{{PRINT_TIMEOUT}}",
  "scope": "{{REVIEW_SCOPE}}",
  "diff_summary": "{{DIFF_STAT_OR_SCOPE_SUMMARY}}",
  "status": "DONE | DONE_WITH_CONCERNS | BLOCKED",
  "quality_score": {{QUALITY_SCORE_INTEGER_OR_NULL}},
  "strong_points": ["{{POINT}}"],
  "weak_points": ["{{POINT}}"],
  "unsupported_claims": ["{{CLAIM_OR_NONE}}"],
  "scope_drift": ["{{DRIFT_OR_NONE}}"],
  "omissions": ["{{OMISSION_OR_NONE}}"],
  "accepted_findings": ["{{FINDING_ID_OR_SUMMARY}}"],
  "rejected_findings": ["{{FINDING_ID_OR_SUMMARY}}"],
  "needs_human_check": ["{{FINDING_ID_OR_SUMMARY}}"],
  "coordinator_notes": ["{{NOTE}}"],
  "template_tuning_suggestions": ["{{SUGGESTION}}"],
  "next_review_scope": "{{NEXT_SCOPE_OR_NONE}}"
}
```
