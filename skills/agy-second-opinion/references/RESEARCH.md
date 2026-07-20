# Bounded Agy Research

Load this file only after the user explicitly requests an `agy`, Gemini-through-`agy`, Antigravity, or other external-model research pass. The external result is one independent idea stream; Codex owns evidence gathering and synthesis.

## Default Fast Path

1. Define one bounded question, the decision it informs, and the supplied evidence.
2. Read target project instructions and remove secrets or private data.
3. Check `command -v agy` once. If unavailable, report `AGY_UNAVAILABLE` and continue Codex-only.
4. Run one external pass with `scripts/run_agy_print.py`. Use agy's configured default model unless the user names one. Do not add a separate health-check or self-scoring pass.
5. Codex compares the result with repository evidence and verifies time-sensitive or external facts through primary sources before accepting them.

## Minimal Prompt Contract

```text
You are a read-only external research assistant.
Question: <BOUNDED_QUESTION>
Decision: <DECISION_THIS_INFORMS>
Evidence supplied: <FILES_FACTS_OR_NONE>
Do not modify files or claim unsupplied current facts are verified.
Return:
AGY_RESEARCH_V1
Options: concise alternatives with tradeoffs
Evidence: supplied support for each point
Unknowns: claims requiring Codex verification
Recommendation: conditional, not authoritative
```

Require `AGY_RESEARCH_V1` with `--expect-substring`. Load `templates/agy_gemini_research_prompt.template.md` only for a complex comparison needing the full schema. Report and quality templates are optional explicit formats, not default runtime dependencies.

## Command

```bash
python3 <SKILL_DIR>/scripts/run_agy_print.py \
  --prompt-file /tmp/agy-research-prompt.txt \
  --print-timeout 2m0s \
  --expect-substring 'AGY_RESEARCH_V1'
```

Use `--model '<EXACT_AGY_MODEL_NAME>'` only when explicitly selected or required by local configuration. Never substitute the standalone `gemini` CLI.

## Source Context

Keep repository context out unless the question needs it. When specific files are necessary, use `build_agy_context_bundle.py` with an allowlist and attach only that generated directory. Whole-repository disclosure requires explicit approval.

Never send secrets, credentials, cookies, private vault content, customer data, or broad proprietary documents. Do not ask the external model to edit files.

## Verification And Delivery

Codex must distinguish:

- points supported by supplied project evidence;
- external claims verified through current primary sources;
- useful but unverified ideas;
- rejected or out-of-scope suggestions.

Report the bounded question, disclosed context, external-pass status, accepted/rejected points, verification, and remaining uncertainty.

Quality logging is off by default. Use `append_agy_review_quality_log.py` only after explicit logging authority or under an existing authorized policy. Do not write target-project guidance or a project-local log merely to prepare a read-only pass.
