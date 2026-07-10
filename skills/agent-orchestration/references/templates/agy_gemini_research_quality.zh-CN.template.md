# Agy / Gemini 调研质量评估模板

外部调研返回后，用本模板评估它的质量。协调者可以自己人工评分，也可以把这个模板再交给 `agy` 执行一次质量检查。

```text
You are evaluating the quality of an external research memo.

Inputs are the research objective, supplied repository/material context, and the research output. Score the research for usefulness and discipline.

Rules:
- Do not introduce new research conclusions unless needed to explain quality.
- Penalize unsupported claims, fake validation, scope drift, vague ideas, and ungrounded ecosystem assertions.
- Reward points that are traceable to the supplied scope and useful for the coordinator's next decision.
- Mark any claim that needs outside evidence as coordinator follow-up, not as proven.
- If the research misses an obvious angle visible in the supplied scope, list it as a weak point.

Output exactly:
AGY_RESEARCH_QUALITY_V1
score: <1-5>
strong_points:
- <point or NONE>
weak_points:
- <point or NONE>
unsupported_claims:
- <claim or NONE>
scope_drift:
- <drift or NONE>
missed_angles:
- <angle or NONE>
coordinator_follow_up:
- <follow-up or NONE>

Research objective:
{{RESEARCH_OBJECTIVE}}

Research context:

context-start
{{RESEARCH_CONTEXT}}
context-end

Research text:

research-start
{{AGY_RESEARCH_OUTPUT}}
research-end
```
