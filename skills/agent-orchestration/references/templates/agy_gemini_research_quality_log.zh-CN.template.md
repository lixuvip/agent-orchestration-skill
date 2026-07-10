# Agy / Gemini 调研质量日志模板

每次外部模型调研完成后，先准备一个 JSON 对象，再用 `scripts/append_agy_review_quality_log.py` 追加到：

```text
<PROJECT_ROOT>/.codex/agent-orchestration/agy-review-quality.jsonl
```

这个文件现在作为外部只读任务的统一账本使用。调研场景请把 `"task_type"` 设为 `"research"`，方便后续把调研和审查分开复盘。

不要记录密钥、token、cookie、私有 vault 正文、客户数据、完整 diff 或原始专有文档。只记录路径、范围摘要、质量信号和精简后的结论。

如果目标仓库禁止写入，或用户明确要求只读调研，就在协调者回复中展示这条 JSONL 记录，并说明为什么没有写入文件。

```bash
python3 <SKILL_DIR>/scripts/append_agy_review_quality_log.py --project-root "{{PROJECT_ROOT}}" <<'JSON'
{{QUALITY_LOG_JSON_OBJECT}}
JSON
```

只有 stdout 出现 `LOG_WRITTEN <path>` 才能声明质量日志已写入。

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
  "mode": "run_agy_print.py -> agy --add-dir <project_root> --print <prompt> --sandbox",
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
