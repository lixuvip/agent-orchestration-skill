# Agy / Gemini Research Quality Log Template

Prepare one JSON object per completed external research pass and append it with `scripts/append_agy_review_quality_log.py` to:

```text
${CODEX_HOME:-$HOME/.codex}/external-review-ledger/<project-id>/agy-review-quality.jsonl
```

This file is the shared ledger for external read-only tasks. Set `"task_type": "research"` so later tuning can separate research runs from review runs.

Do not store secrets, tokens, cookies, private vault note bodies, customer data, full diffs, or raw proprietary documents. Store paths, scope summaries, quality signals, and concise findings only.

The default ledger is outside the target repository. A project-local path requires explicit authorization and `--allow-project-write`.

```bash
python3 <SKILL_DIR>/scripts/append_agy_review_quality_log.py --project-root "{{PROJECT_ROOT}}" <<'JSON'
{{QUALITY_LOG_JSON_OBJECT}}
JSON
```

Only claim success when stdout contains `LOG_WRITTEN <path>` or `LOG_ALREADY_PRESENT <path>`.

```json
{
  "timestamp": "{{ISO_8601_LOCAL_OR_UTC}}",
  "task_type": "research",
  "project": "{{PROJECT_NAME}}",
  "repository": "{{REPO_PATH}}",
  "thread_id": "{{THREAD_ID_OR_UNKNOWN}}",
  "coordinator_thread_id": "{{COORDINATOR_THREAD_ID_OR_UNKNOWN}}",
  "review_id": "{{STABLE_RESEARCH_ID}}",
  "model": "{{MODEL_NAME}}",
  "mode": "run_agy_print.py -> agy --add-dir <allowlisted_context> --print <prompt> --sandbox",
  "timeout": "{{PRINT_TIMEOUT}}",
  "scope": "{{RESEARCH_SCOPE}}",
  "context_summary": "{{SCOPE_SUMMARY}}",
  "status": "DONE | DONE_WITH_CONCERNS | BLOCKED",
  "quality_score": {{QUALITY_SCORE_INTEGER_OR_NULL}},
  "strong_points": ["{{POINT}}"],
  "weak_points": ["{{POINT}}"],
  "unsupported_claims": ["{{CLAIM_OR_NONE}}"],
  "scope_drift": ["{{DRIFT_OR_NONE}}"],
  "omissions": ["{{OMISSION_OR_NONE}}"],
  "accepted_findings": ["{{ACCEPTED_POINT}}"],
  "rejected_findings": ["{{REJECTED_POINT_OR_NONE}}"],
  "agreed_points": ["{{AGREED_POINT_OR_NONE}}"],
  "external_only_points": ["{{EXTERNAL_ONLY_POINT_OR_NONE}}"],
  "codex_only_points": ["{{CODEX_ONLY_POINT_OR_NONE}}"],
  "valuable_takeaways": ["{{TAKEAWAY}}"],
  "follow_up_questions": ["{{QUESTION_OR_NONE}}"],
  "coordinator_notes": ["{{NOTE}}"],
  "template_tuning_suggestions": ["{{SUGGESTION}}"],
  "next_research_scope": "{{NEXT_SCOPE_OR_NONE}}"
}
```
