# Agy / Gemini External Review

Use this reference when the coordinator adds an optional `agy` / Gemini review pass after Codex implementation or before accepting a branch handoff. In this workflow, `Gemini` means Gemini through local `agy`, not the standalone `gemini` CLI. Treat it as a second opinion, not as the authoritative reviewer.

Mandatory start: if the user asks for `agy`, `Gemini`, `Antigravity`, or an external reviewer, load this workflow before running shell commands. Do not inspect `gemini` CLI first.

## Negative Guardrails

If any of these feels like the next step, stop and return to the documented preflight:

- `command -v gemini`, `gemini --version`, or `gemini --help`
- opening standalone `gemini` CLI to inspect auth, models, or workspace behavior
- attaching the entire repository when a bounded diff or allowlisted context bundle is sufficient
- writing target-repository guidance or logs merely to prepare a read-only review
- padding the reviewer prompt with generic "find anything useful" language instead of bounded diff-only scope

## When To Use

- The user explicitly asks to use `agy`, Gemini, Antigravity, or another external model for code review.
- A change is broad, risky, storage-related, migration-related, or hard to review from one model perspective.
- The coordinator wants an independent read-only review before QA, merge readiness, or final delivery.

## Do Not Use

- Do not send secrets, tokens, cookies, private vault contents, customer data, or proprietary large documents.
- Do not use `agy` as an editing agent for review gates. Use read-only review prompts.
- Do not replace the coordinator's own diff inspection, tests, and acceptance decision with `agy` output.
- Do not run on huge diffs in one prompt. Split by ownership or risk area.
- Do not probe the standalone `gemini` CLI with `command -v gemini`, `gemini --version`, or `gemini --help`. Discovery for this workflow is `agy` only.
- Do not invoke the standalone `gemini` CLI for this workflow. If a process does that and receives a `403`, classify it as `WRONG_EXECUTION_SURFACE` and rerun through `agy`.
- Do not modify target `AGENTS.md` or create a project-local quality log unless the user explicitly authorized that separate repository write.

## Preflight

1. Read target project instructions such as `AGENTS.md` and obey privacy, branch, and verification rules.
2. Keep preflight read-only by default. The installed skill already contains the command-safety rules. Check project guidance only when it is relevant:

```bash
python3 <SKILL_DIR>/scripts/ensure_agy_review_agents_guidance.py --project-root "$PROJECT_ROOT"
```

The helper is check-only unless `--write` is explicitly supplied. Missing guidance does not block a one-shot review. Only after the user separately authorizes a durable repository instruction change may the coordinator run it with `--write`. Do not write live task state, findings, scores, or temporary review status into `AGENTS.md`.

3. Inspect `git status --short` and `git diff --stat` so the review scope is explicit.
4. Redact unsafe content before sending it to an external model.
5. Confirm the tool and models:

```bash
command -v agy
agy models
```

If `gemini` CLI is also installed on the machine, ignore it for this workflow. The execution surface is `agy`.

Do not run `command -v gemini`, `gemini --version`, or `gemini --help` as discovery. The presence of the standalone CLI is irrelevant and counts as wrong-surface probing for this workflow.

6. Run a small health check before the real review:

```bash
python3 <SKILL_DIR>/scripts/run_agy_print.py \
  --print-timeout 20s \
  --model 'Gemini 3.5 Flash (High)' \
  --expect-substring 'READY' \
  --prompt 'Reply exactly: READY'
```

If the health check fails, returns empty stdout, or misses the expected token, report `AGY_UNAVAILABLE`, `HEALTH_CHECK_FAILED`, or `NO_STRUCTURED_OUTPUT` and continue with normal Codex review. The helper emits `AGY_PRINT_EMPTY_OUTPUT` for exit-0 zero-byte stdout, `AGY_PRINT_FIRST_LINE_FAILED ...` when narration appears before the required schema token, and `AGY_PRINT_EXPECTATION_FAILED ...` when `--expect-substring` is not satisfied. If a role probes or opens standalone `gemini` CLI, or reports a `403` from that CLI, classify that as `WRONG_EXECUTION_SURFACE` and rerun the pass through `agy` instead of treating it as a reviewer result.

7. Send the minimum necessary source context. For diff-only review, place the bounded diff in the prompt and do not attach the repository. When source files are required, build an allowlisted bundle outside the project and attach that bundle:

```bash
CONTEXT_PARENT="$(mktemp -d)"
python3 <SKILL_DIR>/scripts/build_agy_context_bundle.py \
  --project-root "$PROJECT_ROOT" \
  --output-dir "$CONTEXT_PARENT/context" \
  --include src/relevant_module.py \
  --include tests/test_relevant_module.py

python3 <SKILL_DIR>/scripts/run_agy_print.py \
  --add-dir "$CONTEXT_PARENT/context" \
  --print-timeout 20s \
  --model 'Gemini 3.5 Flash (High)' \
  --expect-substring 'READY' \
  --prompt 'Reply exactly: READY'
```

Attach the full project root only when the user explicitly approved whole-repository disclosure and the privacy rules allow it. Record the context-bundle manifest or the whole-repository exception in the final report.

## Model Selection

Use `Gemini 3.5 Flash (High)` as the standard external reviewer for this skill. Keep the workflow on that model unless the user explicitly asks to experiment outside the default route.

Coordinator rule: every finding from every model must be verified by Codex against the diff, source context, or test evidence before it affects the handoff decision.

## Dual Codex + Gemini Review

When the user asks to compare reviewers, requests a full-project audit, or a change is broad enough that one reviewer is likely to miss context, run a dual Codex + Gemini review instead of a standalone `agy` pass:

1. Start or use a Codex reviewer role thread with read-only scope, explicit stop conditions, and the standard role reply format.
2. Run `agy` / Gemini in parallel with the same scope and privacy limits.
3. Keep the two reviewers independent until both return or one reaches a terminal failure state.
4. The coordinator performs the only acceptance decision. Compare:
   - agreed findings;
   - Gemini-only findings;
   - Codex-only findings;
   - rejected or unsupported findings;
   - verification actually run by each reviewer;
   - review-quality self-scores and observed weaknesses.
5. For any P0/P1/high-severity item, require exact file/line evidence plus a falsification check. If the reviewer claims a call happens on a queue, through a dependency, before authentication, or across a trust boundary, the coordinator must inspect the exact source path that proves or disproves that claim.

Use the same `Gemini 3.5 Flash (High)` model for full-project baseline audits as well. Model variance is not part of the default workflow; the coordinator should tune prompt scope before tuning models.

## Command Shape

Prefer the bundled helper for every `agy --print` invocation. It guarantees that the prompt argument appears immediately after `--print`, which is required by the `agy` CLI. For review, use normal read-only print mode with `--sandbox` as the default path.

Do not substitute `gemini` CLI for `agy`, even if both are installed.

For reference, the invariant is still `agy --print <prompt> ...`: `--print` must be followed immediately by the prompt argument, even when an allowlisted context bundle appears earlier in the command.

```bash
python3 <SKILL_DIR>/scripts/run_agy_print.py \
  --add-dir "$CONTEXT_PARENT/context" \
  --prompt-file /tmp/agy-review-prompt.txt \
  --print-timeout 2m0s \
  --expect-substring 'Status:' \
  --model 'Gemini 3.5 Flash (High)'
```

If invoking `agy` manually, this exact argument order is required:

```bash
agy --add-dir "$CONTEXT_PARENT/context" --print-timeout 2m0s --print "$PROMPT" --model 'Gemini 3.5 Flash (High)' --sandbox
```

Never put flags or options between `--print` and the prompt. This is invalid:

```bash
agy --print --model 'Gemini 3.5 Flash (High)' "$PROMPT"
```

For slower models or high reasoning, use a longer timeout such as `3m0s`; the helper also enforces a host-side timeout. If a run fails because `--print` did not receive the prompt, retry once with `scripts/run_agy_print.py` before reporting the review as failed.
If a run says the workspace is missing, first confirm that the bounded prompt or allowlisted bundle contains the required context. Do not silently expand to the whole repository.
If a run exits 0 but stdout is empty, misses the required schema token when `--expect-substring` is used, or puts narration before the required schema token when `--expect-first-line` is used, treat it as `NO_STRUCTURED_OUTPUT` rather than as a successful review. `--expect-first-line` is an optional strict mode, not the default path, because some runs can still prepend narration before the schema token.

Never use these for review gates:

- hand-written command shapes where `--print` is not immediately followed by the prompt
- the standalone `gemini` CLI
- `--mode accept-edits`
- `--dangerously-skip-permissions`
- prompts that ask `agy` to modify files
- prompts that let `agy` claim tests passed without supplied command output

## Scope Budget

For a single review prompt, prefer:

- diff under 800 lines;
- prompt plus diff under roughly 20 KB;
- one feature, branch, or ownership area at a time.
- only the source files required to verify the bounded finding.

For larger changes, split the diff and run multiple reviews. The coordinator should merge findings and remove duplicates.

## Prompt And Quality Templates

Use `templates/agy_gemini_review_prompt.template.md` for the review prompt.
Use `templates/agy_gemini_review_quality.template.md` to evaluate the returned review.
Use `templates/agy_gemini_review_report.template.md` or the Chinese version for the final dedicated display in the coordinator reply.
Use `templates/agy_gemini_review_quality_log.template.md` or the Chinese version to prepare the durable per-review quality record, then run `scripts/append_agy_review_quality_log.py` to append it.

Chinese-only teams may use the `*.zh-CN.template.md` versions; keep the structured output keys unchanged so the coordinator can parse them.

The quality evaluation is only a discipline check. It can miss omissions, so the coordinator must still inspect the diff for obvious gaps that the external reviewer did not mention.

## Quality Log

Default log location:

```text
${CODEX_HOME:-$HOME/.codex}/external-review-ledger/<project-id>/agy-review-quality.jsonl
```

After the coordinator classifies the external findings, append one JSON object for each completed or blocked review. This JSONL file is also reused by the parallel research workflow, so review entries should keep `"task_type": "review"` or omit the field and let the helper default it. Include the model, command mode, timeout, scope, quality score, strong points, weak points, unsupported claims, scope drift, omissions, accepted findings, rejected findings, human-check items, coordinator notes, and template_tuning_suggestions.

Use the bundled helper script so the write is deterministic:

```bash
python3 <SKILL_DIR>/scripts/append_agy_review_quality_log.py --project-root "$PROJECT_ROOT" <<'JSON'
{
  "project": "example",
  "repository": "/absolute/path/to/project",
  "model": "Gemini 3.5 Flash (High)",
  "mode": "run_agy_print.py -> agy --add-dir <allowlisted_context> --print <prompt> --sandbox",
  "timeout": "2m0s",
  "scope": "current diff",
  "status": "DONE_WITH_CONCERNS",
  "quality_score": 5,
  "strong_points": ["traceable findings"],
  "weak_points": [],
  "unsupported_claims": [],
  "scope_drift": [],
  "omissions": [],
  "accepted_findings": [],
  "rejected_findings": [],
  "needs_human_check": [],
  "coordinator_notes": [],
  "template_tuning_suggestions": []
}
JSON
```

Treat the quality log as written only when the script exits 0 and prints `LOG_WRITTEN <path>`. If it prints `LOG_NOT_WRITTEN` or exits non-zero, include the JSONL entry in the coordinator reply and state why the file was not written.

The script creates the Codex-owned ledger directory when missing, locks concurrent appends, deduplicates `review_id`, and rejects unsupported or sensitive fields. Do not store secrets, tokens, cookies, private vault note contents, customer data, full diffs, or raw proprietary documents. Store paths, hashes, summarized findings, and review-quality signals only.

Project-local logging is optional and requires both an explicitly selected project path and `--allow-project-write`. A read-only external pass never needs to modify the target repository.

Use the log for periodic tuning, not for noisy per-run churn. Revisit the log after a full-project baseline review, after about five entries, or when repeated weak points, unsupported claims, scope drift, or omissions appear. Direct callback to a coordinator thread is optional for active multi-thread coordination; the file log is the durable default.

## Failure States

Report one of these terminal states instead of treating a failed run as review coverage:

| State | Meaning |
| --- | --- |
| `AGY_UNAVAILABLE` | `agy` is not installed or not on `PATH`. |
| `HEALTH_CHECK_FAILED` | The tiny health check failed or did not return the expected token. |
| `TIMED_OUT` | The review exceeded the selected timeout. |
| `HOST_TIMEOUT` | The wrapper terminated a stalled process at its host-side deadline. |
| `INTERACTIVE_CONFIRMATION_REQUIRED` | The run asked for user input and could not proceed non-interactively. |
| `UNSAFE_INPUT` | The diff or context includes secrets or private content that should not be sent. |
| `SCOPE_DRIFT` | The output reviewed files, repos, or behavior outside the supplied scope. |
| `NO_STRUCTURED_OUTPUT` | The output did not follow the required review structure, returned only narration, or exited 0 with empty stdout. |
| `WRONG_EXECUTION_SURFACE` | The process probed or invoked standalone `gemini` CLI, or used another non-`agy` Gemini surface; rerun through `agy`. |

## Coordinator Acceptance

After `agy` returns, the coordinator must classify each item:

- `valid`: directly supported by supplied diff/source/test evidence.
- `partially_valid`: useful but needs narrowing or reframing.
- `not_supported`: speculative, false, or outside supplied scope.
- `needs_human_check`: product, privacy, legal, or release decision.

Final delivery should include the model used, timeout, command shape, context-bundle manifest or disclosure exception, whether the run succeeded, which findings were accepted, which were rejected, what verification actually ran, and the quality log path or why the log was not written.

For dual review, final delivery must also include the Codex reviewer status, the Gemini reviewer status, the cross-review comparison buckets, and the coordinator's final accepted finding list.

Default to showing the dedicated report in chat. Do not require the user to inspect the integrated terminal for review content.
