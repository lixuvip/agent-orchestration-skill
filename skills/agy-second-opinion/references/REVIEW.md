# Bounded Agy Review

Load this file only after the user explicitly requests an `agy`, Gemini-through-`agy`, Antigravity, or other external-model code review. The external pass is one read-only second opinion; Codex owns verification and the final decision.

## Default Fast Path

1. Read the target project's instructions and privacy rules.
2. Resolve the exact review baseline before invoking anything:
   - working-tree diff: state whether staged, unstaged, or both;
   - branch review: state `BASE...HEAD`;
   - supplied patch/file set: name it precisely.
   If the request does not identify the baseline and different choices would change the answer, ask instead of combining them silently.
3. Redact secrets and keep the prompt plus diff bounded. For a small diff, embed it in the prompt and attach no repository.
4. Check `command -v agy` once. If unavailable, report `AGY_UNAVAILABLE` and continue Codex-only.
5. Run one external pass with `scripts/run_agy_print.py`. Use agy's configured default model unless the user names a model. Do not run a separate health-check pass.
6. Codex inspects the source and real test evidence, accepts or rejects each external finding, and reports the result.

Do not invoke `agy` a second time to score its own answer. Quality evaluation is a local Codex responsibility.

## Minimal Prompt Contract

For an ordinary bounded diff, a short prompt is enough:

```text
You are a read-only external code reviewer.
Scope: <EXACT_BASELINE_AND_FILES>
Do not modify files or claim commands ran.
Return:
AGY_REVIEW_V2
Status: PASS | FINDINGS | BLOCKED
Findings: severity, file/line, evidence, consequence, smallest fix
Needs Codex verification: unsupported or context-dependent claims
<BOUNDED_DIFF_OR_SUMMARY>
```

Require `AGY_REVIEW_V2` with `--expect-substring`. Load `templates/agy_gemini_review_prompt.template.md` only when the review is large enough to need the full structured schema. Load report or quality templates only when the user explicitly requests that format.

## Command

```bash
python3 <SKILL_DIR>/scripts/run_agy_print.py \
  --prompt-file /tmp/agy-review-prompt.txt \
  --print-timeout 2m0s \
  --expect-substring 'AGY_REVIEW_V2'
```

The helper enforces `agy --print <prompt> ... --sandbox`, host timeout, non-empty output, output limits, and rejects the standalone `gemini` CLI. Use `--model '<EXACT_AGY_MODEL_NAME>'` only when the user selected one or current local configuration requires it.

Never use edit-acceptance mode, permission bypass flags, prompts asking the model to modify files, or claims of tests not included in the supplied evidence.

## Source Context

Prefer no attachment for diff-only review. If specific source files are necessary, create an allowlisted bundle outside the project:

```bash
python3 <SKILL_DIR>/scripts/build_agy_context_bundle.py \
  --project-root "$PROJECT_ROOT" \
  --output-dir "$CONTEXT_PARENT/context" \
  --include src/relevant.py \
  --include tests/test_relevant.py
```

Then pass that directory with `--add-dir`. Whole-repository disclosure requires explicit approval. Never include secrets, credentials, cookies, private vault content, customer data, or broad proprietary documents.

## Failure And Fallback

Treat missing binary, timeout, non-zero exit, empty output, missing schema token, or oversized output as a failed external pass. Report the specific state and continue Codex-only. Do not retry in the same goal unless the user changes the model, context, or environment and asks to retry.

If the standalone `gemini` CLI is invoked accidentally, classify it as `WRONG_EXECUTION_SURFACE`; do not treat its auth or 403 result as an `agy` review.

## Acceptance And Delivery

For every accepted finding, provide source or test evidence. Separate accepted, rejected, and unresolved items. State:

- exact review baseline;
- context disclosed to `agy`;
- external pass status;
- Codex verification performed;
- remaining risk.

Quality logging is off by default. Use `append_agy_review_quality_log.py` only when the user explicitly requests a durable log or an existing authorized project policy requires it. Target-repository guidance or project-local logs are separate writes and require explicit authority.
