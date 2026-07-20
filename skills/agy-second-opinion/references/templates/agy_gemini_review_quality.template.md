# Agy / Gemini Review Quality Template

Use this template after an external review returns. The coordinator may run it through `agy` or use it manually to score the review before accepting findings.

```text
You are evaluating the quality of an external code review.

Inputs are a unified diff, optional command output, and the review text. Score the review for usefulness and discipline.

Rules:
- Do not introduce new code findings unless needed to explain review quality.
- Penalize unsupported claims, test/build hallucinations, scope drift, vague findings, and invented blockers.
- Reward findings that are traceable to the diff and actionable by the coordinator.
- Mark any finding that requires source outside the diff as coordinator follow-up, not as proven.
- If the review misses an obvious issue or test gap visible in the diff, list it as a weak point.

Output exactly:
AGY_REVIEW_QUALITY_V1
score: <1-5>
strong_points:
- <point or NONE>
weak_points:
- <point or NONE>
unsupported_claims:
- <claim or NONE>
scope_drift:
- <drift or NONE>
coordinator_follow_up:
- <follow-up or NONE>

Unified diff:

diff-start
{{UNIFIED_DIFF}}
diff-end

Known command output:

command-output-start
{{COMMAND_OUTPUT_OR_NONE}}
command-output-end

Review text:

review-start
{{AGY_REVIEW_OUTPUT}}
review-end
```
