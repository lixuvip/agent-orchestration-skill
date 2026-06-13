# Example Prompt: Release Preparation

```text
Use $agent-orchestration for release preparation.

Roles:
- Release Docs: draft release notes and migration notes.
- QA Tester: verify critical user paths.
- Code Reviewer: review high-risk diffs and missing tests.

Stop conditions:
- production deployment;
- destructive git commands;
- missing release scope;
- failed critical-path tests.

Final coordinator delivery must include version scope, verification, known issues, and remaining risks.
```

