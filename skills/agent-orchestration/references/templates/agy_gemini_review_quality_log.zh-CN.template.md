# Agy / Gemini 审查质量日志模板

每次外部模型审查完成后，先准备一个 JSON 对象，再用 `scripts/append_agy_review_quality_log.py` 追加到：

```text
<PROJECT_ROOT>/.codex/agent-orchestration/agy-review-quality.jsonl
```

使用 JSONL：每一行是一个紧凑 JSON 对象。不要记录密钥、token、cookie、私有 vault 正文、客户数据、完整 diff 或原始专有文档。只记录路径、哈希、findings 摘要和审查质量信号。

如果目标仓库禁止写入，或用户明确要求只读审查，就在协调者回复中展示这条 JSONL 记录，并说明为什么没有写入文件。

写入命令：

```bash
python3 <SKILL_DIR>/scripts/append_agy_review_quality_log.py --project-root "{{PROJECT_ROOT}}" <<'JSON'
{{QUALITY_LOG_JSON_OBJECT}}
JSON
```

只有 stdout 出现 `LOG_WRITTEN <path>` 才能声明质量日志已写入。如果脚本输出 `LOG_NOT_WRITTEN` 或非 0 退出，不要声称已经落盘。

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
