# Agent Orchestration Capability Map

Use progressive disclosure. Select a route first, load one language, then open only the capability pack and templates required by the task.

## Runtime Packs

| Route / modifier | Load |
| --- | --- |
| Lite | No core pack. Use the current conversation and normal verification. |
| Standard | `COORDINATION_RUNBOOK.md` or `COORDINATION_RUNBOOK.zh-CN.md` |
| Durable | Standard pack plus `PROJECT_AUTOPILOT.md` or `PROJECT_AUTOPILOT.zh-CN.md` |
| Agy review | `AGY_GEMINI_REVIEW.md` only; add Standard/Durable packs only if the surrounding task needs them |
| Agy research | `AGY_GEMINI_RESEARCH.md` only; add Standard/Durable packs only if the surrounding task needs them |

Never load both English and Chinese versions. The English filenames emitted by `route_orchestration.py` are logical defaults; substitute `.zh-CN.md` for Chinese execution.

Per-thread `thinking` is orthogonal to Lite/Standard/Durable. Before creating a user-visible thread, use the selected coordination runbook to choose the best-fit supported effort, using latency/cost only as a tie-breaker, and record requested/applied/rationale fields; no separate capability pack is required.

## Optional Project Context

- `PROJECT_CONTEXT.template.md`: use only when repository, branch, commands, contracts, or prohibited areas are missing.
- `ROLE_REGISTRY.template.md`: use only when persistent role-to-thread mapping is needed.
- `TASK_BOARD.template.md`: use for two or more active tasks or recoverable manual polling.
- `REQUIREMENT_WRITING_GUIDE.md`: use when acceptance criteria or task boundaries need formalization.

## Deterministic Helpers

| Helper | Purpose |
| --- | --- |
| `scripts/route_orchestration.py` | Compute minimum/selected route and exact load pack. |
| `scripts/orchestration_event.py` | Validate, deduplicate, classify stale events, and check accepted delivery. |
| `scripts/automation_lease.py` | File-locked lease, expiry, takeover, verify, renew, and release. |
| `scripts/heartbeat_lifecycle.py` | Compute `ACTIVE -> DRAINING -> CLOSED` actions. |
| `scripts/run_agy_print.py` | Fixed sandboxed `agy --print` execution with timeout/output guards. |
| `scripts/build_agy_context_bundle.py` | Create bounded allowlisted external-model context. |
| `scripts/ensure_agy_review_agents_guidance.py` | Check stable AGY project guidance; write only with explicit authorization. |
| `scripts/append_agy_review_quality_log.py` | Append deduplicated review/research quality records outside the project by default. |

## Template Selection

Do not load the whole template directory.

| Need | English / Chinese template |
| --- | --- |
| Short route confirmation | `orchestration_intake.template.md` / `orchestration_intake.zh-CN.template.md` |
| Dispatch and human reply | `task_dispatch.template.md`, `role_reply.template.md` / `.zh-CN` variants |
| Async callback or status | `coordinator_callback.template.md`, `status_request.template.md` / `.zh-CN` variants |
| QA/review/merge gate | `qa_report.template.md`, `review_findings.template.md`, `merge_readiness.template.md` / `.zh-CN` variants |
| Finite heartbeat | `monitoring_heartbeat.template.md` / `monitoring_heartbeat.zh-CN.template.md` |
| Durable Autopilot | `project_goal_contract`, `automation_plan`, `automation_tick`, `automation_memory`, `escalation_report` template families |
| Stable project guidance | `agents_guidance_snippet.template.md` / `agents_guidance_snippet.zh-CN.template.md` |
| Agy review/research | Open only the prompt, quality, quality-log, and report family for the selected mode/language |

Role profiles under `roles/` are optional initialization material, not mandatory runtime context. Filled files under `examples/` are examples, not protocol sources.

Exact bilingual template index (select one language; do not preload):

```text
task_dispatch.template.md | task_dispatch.zh-CN.template.md
orchestration_intake.template.md | orchestration_intake.zh-CN.template.md
coordinator_callback.template.md | coordinator_callback.zh-CN.template.md
status_request.template.md | status_request.zh-CN.template.md
merge_readiness.template.md | merge_readiness.zh-CN.template.md
role_reply.template.md | role_reply.zh-CN.template.md
qa_report.template.md | qa_report.zh-CN.template.md
review_findings.template.md | review_findings.zh-CN.template.md
monitoring_heartbeat.template.md | monitoring_heartbeat.zh-CN.template.md
project_goal_contract.template.md | project_goal_contract.zh-CN.template.md
automation_plan.template.md | automation_plan.zh-CN.template.md
automation_tick.template.md | automation_tick.zh-CN.template.md
automation_memory.template.md | automation_memory.zh-CN.template.md
escalation_report.template.md | escalation_report.zh-CN.template.md
agents_guidance_snippet.template.md | agents_guidance_snippet.zh-CN.template.md
agy_gemini_review_prompt.template.md | agy_gemini_review_prompt.zh-CN.template.md
agy_gemini_review_quality.template.md | agy_gemini_review_quality.zh-CN.template.md
agy_gemini_review_quality_log.template.md | agy_gemini_review_quality_log.zh-CN.template.md
agy_gemini_review_report.template.md | agy_gemini_review_report.zh-CN.template.md
agy_gemini_research_prompt.template.md | agy_gemini_research_prompt.zh-CN.template.md
agy_gemini_research_quality.template.md | agy_gemini_research_quality.zh-CN.template.md
agy_gemini_research_quality_log.template.md | agy_gemini_research_quality_log.zh-CN.template.md
agy_gemini_research_report.template.md | agy_gemini_research_report.zh-CN.template.md
```

## Minimal Load Examples

```text
One local review
-> Lite
-> no core reference

Engineer + async QA
-> Standard
-> COORDINATION_RUNBOOK.zh-CN.md
-> task_dispatch + coordinator_callback + qa_report templates

Two-hour issue/PR progress
-> Durable
-> COORDINATION_RUNBOOK.zh-CN.md + PROJECT_AUTOPILOT.zh-CN.md
-> goal/plan/tick/memory/escalation templates

One read-only agy review
-> Lite + AGY review modifier
-> AGY_GEMINI_REVIEW.md only
```
