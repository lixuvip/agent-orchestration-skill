# Agy / Gemini External Research

Use this reference when the coordinator wants a parallel Codex + Gemini research workflow: Codex does its own research while `agy` / Gemini runs an independent read-only research pass in parallel. In this workflow, `Gemini` means Gemini through local `agy`, not the standalone `gemini` CLI. Treat the external pass as a second research stream, not as an authoritative answer.

Mandatory start: if the user asks for `agy`, `Gemini`, `Antigravity`, or an external research pass, load this workflow before running shell commands. Do not inspect `gemini` CLI first.

## Negative Guardrails

If any of these feels like the next step, stop and return to the documented preflight:

- `command -v gemini`, `gemini --version`, or `gemini --help`
- opening standalone `gemini` CLI to inspect auth, models, or workspace behavior
- attaching the entire repository when a bounded problem statement or allowlisted context bundle is sufficient
- writing target-repository guidance or logs merely to prepare a read-only research pass
- padding the research prompt with generic ideation language that ignores the supplied repository scope

## When To Use

- The user explicitly asks to use `agy`, Gemini, Antigravity, or another external model for research, repo understanding, idea expansion, or option comparison.
- The coordinator wants an independent architecture or implementation-options pass before choosing a plan.
- A repository is broad enough that a second read-only perspective may surface additional risks, migration edges, or missed alternatives.

## Do Not Use

- Do not send secrets, tokens, cookies, private vault contents, customer data, or proprietary large documents.
- Do not use `agy` as an editing agent for research. Keep the external pass read-only.
- Do not replace the coordinator's own repository reading, source-backed web research, or acceptance decision with `agy` output.
- Do not ask `agy` to claim current external facts unless those facts are already included in the prompt. Time-sensitive ecosystem claims still need Codex verification from primary sources.
- Do not probe the standalone `gemini` CLI with `command -v gemini`, `gemini --version`, or `gemini --help`. Discovery for this workflow is `agy` only.
- Do not invoke the standalone `gemini` CLI for this workflow. If a process does that and receives a `403`, classify it as `WRONG_EXECUTION_SURFACE` and rerun through `agy`.
- Do not modify target `AGENTS.md` or create a project-local quality log unless the user explicitly authorized that separate repository write.

## Availability And Consent Gate

Apply this gate before model discovery, health checks, context bundling, or any `agy` invocation:

1. Check the current goal's capability state for this host and environment. Use `UNKNOWN`, `AVAILABLE`, `AGY_UNAVAILABLE`, or `AGY_UNHEALTHY`; record the check time, host/PATH context, consent, and whether the user was notified. Keep this state in coordinator context for Lite, `TASK_BOARD.md` for Standard, or automation memory for Durable.
2. If the user explicitly requested `agy`, Gemini, Antigravity, or an external model, treat that as consent for a bounded read-only pass. It is not consent for whole-repository disclosure or repository writes.
3. If the user requested research but did not request an external model, ask once whether to use `agy` as an auxiliary research stream. Continue Codex research while waiting. If the user declines or does not confirm, record Codex-only for this goal and do not probe or invoke `agy`; do not ask again in the same goal.
4. When consent is present and state is `UNKNOWN`, run `command -v agy` once per goal and host. If it is absent, cache `AGY_UNAVAILABLE`, give a user-facing notice once, continue Codex-only, and do not run `agy models`, the health check, or `run_agy_print.py`.
5. If the binary exists, run `agy models` once and then the small health check below. If model discovery or health fails, cache `AGY_UNHEALTHY` with the specific failure detail, give a user-facing notice once, and continue Codex-only without retrying the external pass.
6. Reuse `AVAILABLE`, `AGY_UNAVAILABLE`, and `AGY_UNHEALTHY` during the same goal on the same host. Recheck only for a new goal, a changed host or `PATH`, or an explicit user request to recheck after installation or repair.

Suggested unavailable notice: `未检测到 agy，本轮改用 Codex-only，后续不再重试；安装后可要求重新检测。`

## Preflight

1. Read target project instructions such as `AGENTS.md` and obey privacy, branch, and verification rules.
2. Keep preflight read-only by default. The installed skill already contains the command-safety rules. Check project guidance only when it is relevant:

```bash
python3 <SKILL_DIR>/scripts/ensure_agy_review_agents_guidance.py --project-root "$PROJECT_ROOT"
```

The helper is check-only unless `--write` is explicitly supplied. Missing guidance does not block a one-shot research pass. Only after the user separately authorizes a durable repository instruction change may the coordinator run it with `--write`.

3. Inspect `git status --short`, the relevant repository paths, and any provided docs so the research scope is explicit.
4. Redact unsafe content before sending it to an external model.
5. After the availability and consent gate permits the pass, confirm the models:

```bash
agy models
```

If `gemini` CLI is also installed on the machine, ignore it for this workflow. The execution surface is `agy`.

Do not run `command -v gemini`, `gemini --version`, or `gemini --help` as discovery. The presence of the standalone CLI is irrelevant and counts as wrong-surface probing for this workflow.

6. Run a small health check before the real research pass:

```bash
python3 <SKILL_DIR>/scripts/run_agy_print.py \
  --print-timeout 20s \
  --model 'Gemini 3.5 Flash (High)' \
  --expect-substring 'READY' \
  --prompt 'Reply exactly: READY'
```

If the health check fails, returns empty stdout, or misses the expected token, cache `AGY_UNHEALTHY`, report the detailed state as `HEALTH_CHECK_FAILED` or `NO_STRUCTURED_OUTPUT`, and continue with Codex-only research without another external attempt in this goal. If a role probes or opens standalone `gemini` CLI, or reports a `403` from that CLI, classify that as `WRONG_EXECUTION_SURFACE` and rerun the pass through `agy` instead of treating it as a research result.

7. Send the minimum necessary repository context. Prefer a bounded prompt. When source files are required, build an allowlisted bundle outside the project and attach that bundle:

```bash
CONTEXT_PARENT="$(mktemp -d)"
python3 <SKILL_DIR>/scripts/build_agy_context_bundle.py \
  --project-root "$PROJECT_ROOT" \
  --output-dir "$CONTEXT_PARENT/context" \
  --include src/relevant_subsystem \
  --include docs/relevant_design.md

python3 <SKILL_DIR>/scripts/run_agy_print.py \
  --add-dir "$CONTEXT_PARENT/context" \
  --print-timeout 20s \
  --model 'Gemini 3.5 Flash (High)' \
  --expect-substring 'AGY_RESEARCH_V1' \
  --prompt-file /tmp/agy-research-prompt.txt
```

Attach the full project root only when the user explicitly approved whole-repository disclosure and the privacy rules allow it. Record the context-bundle manifest or the whole-repository exception in the final report.

## Model Selection

Use `Gemini 3.5 Flash (High)` as the standard external research model for this skill. Keep the workflow on that model unless the user explicitly asks to experiment outside the default route.

## Parallel Codex + Gemini Research

When the user wants Gemini involved in research rather than only in review, run a parallel research workflow instead of forcing the question into a review prompt:

1. Codex reads the repository, docs, and any required external primary sources itself.
2. `agy` / Gemini receives the same bounded problem statement as a read-only research prompt.
3. Keep the two research passes independent until both return or one reaches a terminal failure state.
4. The coordinator then compares:
   - agreed points;
   - Gemini-only points;
   - Codex-only points;
   - speculative or rejected points;
   - follow-up questions;
   - concrete next actions worth carrying into engineering.
5. If the task depends on current external facts, Codex must still browse primary sources and mark which Gemini claims were actually verified.

## Command Shape

Prefer the bundled helper for every `agy --print` invocation. It guarantees that the prompt argument appears immediately after `--print`, which is required by the `agy` CLI. For research, use normal read-only print mode with `--sandbox` as the default path.

Do not substitute `gemini` CLI for `agy`, even if both are installed.

```bash
python3 <SKILL_DIR>/scripts/run_agy_print.py \
  --add-dir "$CONTEXT_PARENT/context" \
  --prompt-file /tmp/agy-research-prompt.txt \
  --print-timeout 3m0s \
  --expect-substring 'AGY_RESEARCH_V1' \
  --model 'Gemini 3.5 Flash (High)'
```

If invoking `agy` manually, this exact argument order is required:

```bash
agy --add-dir "$CONTEXT_PARENT/context" --print-timeout 3m0s --print "$PROMPT" --model 'Gemini 3.5 Flash (High)' --sandbox
```

Never put flags between `--print` and the prompt. If a run says the workspace is missing, confirm the bounded prompt or allowlisted bundle before expanding scope. If a run exits 0 but stdout is empty, misses `AGY_RESEARCH_V1` when `--expect-substring` is used, or places narration before the schema token when `--expect-first-line` is used, treat it as `NO_STRUCTURED_OUTPUT`. `--expect-first-line` is an optional strict mode, not the default path, because some runs can still prepend narration before the schema token.

## Scope Budget

For a single research prompt, prefer:

- one decision topic or architecture question at a time;
- prompt plus pasted context under roughly 20 KB;
- a focused list of files, docs, or symbols instead of the entire repository unless the task is explicitly a full-project baseline survey.

For large repos, split the work by subsystem and merge the conclusions in the coordinator synthesis.

## Prompt And Quality Templates

Use `templates/agy_gemini_research_prompt.template.md` for the external research prompt.
Use `templates/agy_gemini_research_quality.template.md` to evaluate the returned research output.
Use `templates/agy_gemini_research_report.template.md` or the Chinese version for the dedicated research display in the coordinator reply.
Use `templates/agy_gemini_research_quality_log.template.md` or the Chinese version to prepare the durable research-quality record, then run `scripts/append_agy_review_quality_log.py` to append it.

Chinese-only teams may use the `*.zh-CN.template.md` versions; keep the structured keys unchanged so the coordinator can parse them.

## Quality Log

Default log location:

```text
${CODEX_HOME:-$HOME/.codex}/external-review-ledger/<project-id>/agy-review-quality.jsonl
```

This file now acts as the durable ledger for external read-only tasks. Set `"task_type": "research"` for research entries so later tuning can distinguish them from review runs.

```bash
python3 <SKILL_DIR>/scripts/append_agy_review_quality_log.py --project-root "$PROJECT_ROOT" <<'JSON'
{
  "task_type": "research",
  "project": "example",
  "repository": "/absolute/path/to/project",
  "model": "Gemini 3.5 Flash (High)",
  "mode": "run_agy_print.py -> agy --add-dir <allowlisted_context> --print <prompt> --sandbox",
  "timeout": "3m0s",
  "scope": "repository research on retry architecture",
  "context_summary": "retry coordinator, queue adapters, existing failure handling docs",
  "status": "DONE_WITH_CONCERNS",
  "quality_score": 4,
  "strong_points": ["surfaced one viable repo-backed option Codex had not prioritized"],
  "weak_points": ["one architecture claim still needs primary-source verification"],
  "unsupported_claims": [],
  "scope_drift": [],
  "omissions": ["did not compare migration cost for the existing retry path"],
  "accepted_findings": ["keep retries inside the existing coordinator boundary"],
  "rejected_findings": [],
  "agreed_points": ["shared view that queue ownership should stay local"],
  "external_only_points": ["suggested explicit retry-budget configuration surface"],
  "codex_only_points": ["identified current telemetry contract that constrains retries"],
  "valuable_takeaways": ["external pass was useful for option framing, not for final choice"],
  "follow_up_questions": ["does the current deployment environment allow per-job retry metadata?"],
  "coordinator_notes": [],
  "template_tuning_suggestions": ["ask for migration-cost comparison explicitly next time"]
}
JSON
```

Treat the log as written only when the script exits 0 and prints `LOG_WRITTEN <path>`. Project-local logging requires an explicitly selected project path plus `--allow-project-write`; the normal read-only pass writes only to the Codex-owned ledger.

## Failure States

Report one of these terminal states instead of treating a failed run as research coverage:

| State | Meaning |
| --- | --- |
| `AGY_UNAVAILABLE` | `agy` is not installed or not on `PATH`. |
| `AGY_UNHEALTHY` | `agy` exists, but model discovery or the one-time health check failed; do not retry automatically in the same goal. |
| `HEALTH_CHECK_FAILED` | The tiny health check failed or did not return the expected token. |
| `TIMED_OUT` | The research pass exceeded the selected timeout. |
| `HOST_TIMEOUT` | The wrapper terminated a stalled process at its host-side deadline. |
| `INTERACTIVE_CONFIRMATION_REQUIRED` | The run asked for user input and could not proceed non-interactively. |
| `UNSAFE_INPUT` | The supplied context includes private or secret material that should not be sent. |
| `SCOPE_DRIFT` | The output reasoned outside the supplied repo/context boundary. |
| `NO_STRUCTURED_OUTPUT` | The output did not follow the required research structure, returned only narration, or exited 0 with empty stdout. |
| `WRONG_EXECUTION_SURFACE` | The process probed or invoked standalone `gemini` CLI, or used another non-`agy` Gemini surface; rerun through `agy`. |

## Coordinator Acceptance

After `agy` returns, classify each point:

- `accepted`: supported by the supplied scope and useful for the decision.
- `partially_accepted`: useful, but needs narrowing or further verification.
- `speculative`: plausible, but not yet supported by the supplied scope.
- `rejected`: contradicted, low-signal, or outside scope.

Final delivery should include the model used, timeout, command shape, context-bundle manifest or disclosure exception, which points were accepted, which were rejected, what Codex verified separately, and the quality-log path or why the log was not written.
