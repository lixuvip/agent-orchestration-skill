# Changelog

## Unreleased

- Hardened installation with clean-source enforcement, explicit `--allow-dirty`, staged replacement, provenance manifests, retained previous installs, dry-run support, and rollback.
- Locked `run_agy_print.py` to sandboxed read-only execution, removed edit/no-sandbox bypasses, and added host-side timeout plus output limits.
- Added `build_agy_context_bundle.py` so source-backed external passes can attach an allowlisted bundle instead of disclosing the full repository by default.
- Made project guidance check-only by default; target `AGENTS.md` writes now require explicit `--write` authorization.
- Moved quality logging to the Codex-owned external-review ledger by default, with strict fields, sensitive-content limits, locked appends, and `review_id` deduplication. Project-local logs require `--allow-project-write`.
- Added a parallel Codex + Gemini research workflow for repository survey, idea expansion, and option comparison instead of forcing external-model research through the review path.
- Added `AGY_GEMINI_RESEARCH.md` plus English and Chinese research prompt, quality, quality-log, and dedicated report templates.
- Extended `scripts/append_agy_review_quality_log.py` so the same Codex-owned JSONL ledger can record both review entries and research entries with `task_type`.
- Expanded the optional durable `AGENTS.md` guidance snippet so explicitly authorized project rules cover read-only research passes as well as review passes.
- Updated examples, READMEs, and forward tests so the skill can be triggered for parallel Codex + Gemini research and later tuned from the shared quality ledger.
- Added an optional `agy` / Gemini external review workflow with read-only command guardrails, model-selection guidance, structured review prompts, quality evaluation templates, and coordinator acceptance rules.
- Added a dedicated Agy review report template for displaying external findings, quality evaluation, Codex verification, and recommended next steps directly in chat.
- Added dual Codex + Gemini review guidance for full-project audits or user-requested comparisons, including agreed/Gemini-only/Codex-only/rejected finding buckets and verification contrast in the report.
- Added an Agy review quality-log template that records per-review scores, weak points, unsupported claims, omissions, accepted/rejected findings, and template tuning suggestions in the external-review ledger.
- Added `scripts/append_agy_review_quality_log.py` so review-quality logging is a deterministic append step with a `LOG_WRITTEN` success signal instead of only a prose instruction.
- Added `scripts/run_agy_print.py` to enforce the required `agy --print <prompt> ...` argument order and avoid first-run failures caused by putting flags between `--print` and the prompt.
- Updated the external-review workflow to attach bounded allowlisted source bundles through `--add-dir`; whole-repository disclosure is an explicit exception.
- Updated the external-review workflow to standardize on `Gemini 3.5 Flash (High)` and treat empty or narration-only output as failure through `run_agy_print.py` plus optional schema checks.
- Hardened the agy/Gemini workflow so Gemini always means "Gemini via agy", never the standalone `gemini` CLI; added `WRONG_EXECUTION_SURFACE` guidance for accidental `gemini` CLI `403` failures and made `run_agy_print.py` reject `--agy-bin gemini`.
- Tightened agy/Gemini entry rules so one-shot passes remain read-only by default, while standalone `gemini` CLI probing such as `command -v gemini`, `gemini --version`, or `gemini --help` remains the wrong execution surface.
- Added explicit reverse-prompt guardrails to the AGY review/research prompt templates and target `AGENTS.md` snippet so the workflow now pushes back on CLI/auth narration, fake validation claims, scope inflation, and generic filler.
- Added `scripts/ensure_agy_review_agents_guidance.py` so coordinators can check stable command-safety guidance and persist it only after explicit project-write authorization.
- Added forward-test, smoke-test, and validation coverage for external review resources so the templates stay discoverable and include anti-hallucination fields.
- Updated README and examples to document external model review as a second opinion rather than an automatic replacement for Codex review or real test evidence.

## 0.1.4 - 2026-07-07

- Added a forward-test validation script and wired it into GitHub Actions.
- Added English and Chinese Project Autopilot loop diagrams to make the recurring automation flow easier to understand.
- Updated repository maintenance instructions, READMEs, examples, and forward-test docs so the new validation layer is visible before release.

## 0.1.3 - 2026-07-07

- Added Project Autopilot guidance for recurring Codex automation that keeps a workspace moving toward explicit done criteria.
- Added automation-tooling and project-instruction discovery references for heartbeat/cron selection, duplicate automation avoidance, and AGENTS.md boundaries.
- Added goal-contract, automation-plan, automation-tick, automation-memory, escalation-report, and AGENTS.md guidance snippet templates in English and Chinese.
- Added filled Autopilot examples, forward-test scenarios, and a GitHub issue/PR Autopilot scenario.
- Added repository-level `AGENTS.md` instructions for maintaining this skill repo.
- Documented how to combine `AGENTS.md`, `AGENTS.override.md`, `.codex/config.toml`, heartbeat automations, cron automations, and automation memory safely.
- Added a continuous project autopilot example and validator/smoke-test coverage for the new workflow.

## 0.1.2 - 2026-07-02

- Added orchestration intake rules for branch, thread, callback, automation, merge, and push decisions.
- Added controller-loop guidance for coordinator-to-role callbacks, status requests, heartbeat monitoring, and merge readiness.
- Added English and Chinese templates for orchestration intake, coordinator callbacks, status requests, and merge readiness checks.
- Expanded dispatch, role-reply, and heartbeat templates with branch/worktree, commit, callback, and status-request fields.
- Added a branch callback controller-loop example and strengthened validation for the new resources.

## 0.1.1 - 2026-06-13

- Added Chinese documentation for installation, quickstart, tutorial, examples, and publishing.
- Expanded README discovery keywords and GitHub topic guidance.
- Added project logo, workflow overview image, badges, quick links, and scenario examples.
- Simplified the README workflow overview image for better first-screen readability.
- Added a Chinese workflow overview image for the Chinese README.
- Added do-not-use guidance, capability fallbacks, and task state machine rules.
- Added Chinese dispatch, role reply, and heartbeat templates.
- Added filled dispatch and role reply examples.
- Strengthened repository validation with Markdown link, SVG XML, template field, and reference discovery checks.
- Added a static smoke test and included it in GitHub Actions.

## 0.1.0

- Initial public-ready release.
- Added the `agent-orchestration` Codex skill.
- Added role dispatch, role reply, QA, review, handoff, and heartbeat monitoring templates.
- Added installation, quickstart, tutorial, usage examples, validation script, and GitHub Actions workflow.
- Added English and Simplified Chinese README documentation.
