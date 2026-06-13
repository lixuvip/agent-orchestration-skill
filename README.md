# Agent Orchestration Skill for Codex

[中文说明](README.zh-CN.md)

`agent-orchestration` is a reusable Codex skill for coordinating multi-role work across Codex threads, subagents, repositories, or worktrees.

It helps one Codex conversation act as the coordinator while other conversations or subagents take roles such as engineering, QA, code review, release notes, and product design. The skill includes dispatch templates, role reply templates, workflow gates, callback rules, and recurring heartbeat monitoring for long-running asynchronous work.

## What It Solves

Use this skill when a task is too large or risky for one uninterrupted conversation:

- Multi-repository changes that need separate implementation and verification threads.
- Parallel work across product, engineering, QA, review, and release docs roles.
- Long-running Codex threads where the coordinator must poll status instead of relying on memory.
- Handoffs that require explicit changed files, verification commands, risks, and final status.
- Workflows where child threads should call back to the coordinator and a heartbeat automation should check status every 5 minutes.

## Repository Layout

```text
.
├── skills/
│   └── agent-orchestration/
│       ├── SKILL.md
│       ├── agents/
│       │   └── openai.yaml
│       └── references/
│           ├── AUTOMATION_MONITORING.md
│           ├── COMMUNICATION_PROTOCOL.md
│           ├── PROJECT_CONTEXT.template.md
│           ├── ROLE_REGISTRY.template.md
│           ├── TASK_BOARD.template.md
│           ├── WORKFLOWS.md
│           ├── roles/
│           └── templates/
├── docs/
│   ├── installation.md
│   ├── quickstart.md
│   ├── tutorial.md
│   ├── examples.md
│   └── publishing.md
├── examples/
├── scripts/
│   ├── install.sh
│   └── validate.py
└── .github/workflows/validate.yml
```

## Install

Clone the repository and run the installer:

```bash
git clone https://github.com/lixuvip/agent-orchestration-skill.git
cd agent-orchestration-skill
./scripts/install.sh
```

The installer copies `skills/agent-orchestration` into:

```text
${CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}/agent-orchestration
```

Restart Codex if the skill does not appear immediately.

For manual installation:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/agent-orchestration "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Some Codex installations scan `$HOME/.agents/skills` for user-scoped skills. If that is your setup, install with:

```bash
CODEX_SKILLS_DIR="$HOME/.agents/skills" ./scripts/install.sh
```

## Use

Invoke it explicitly in Codex:

```text
Use $agent-orchestration to split this task across engineering, QA, and code review threads. Create a 5-minute heartbeat monitor and summarize the final status when all roles finish.
```

Or describe a matching task and let Codex select it implicitly:

```text
Coordinate this release across three repositories. Have each project thread finish commits, document API contracts, and report verification results back to this coordinator thread.
```

## Minimal Workflow

1. The coordinator reads the project context and chooses a workflow.
2. The coordinator creates or selects role threads.
3. Each role receives a scoped task using `task_dispatch.template.md`.
4. Role threads reply using `role_reply.template.md`.
5. Long-running multi-thread work gets a callback rule and a 5-minute heartbeat monitor.
6. The coordinator reads every terminal result, checks verification, and delivers a final summary.

## Documentation

- [Installation](docs/installation.md)
- [Quickstart](docs/quickstart.md)
- [Tutorial](docs/tutorial.md)
- [Usage examples](docs/examples.md)
- [Publishing guide](docs/publishing.md)

## Validate

Run the repository validator:

```bash
python3 scripts/validate.py
```

If you also have Codex's built-in `skill-creator` validator available, run it against the skill folder:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/agent-orchestration
```

## Requirements

- Codex with skill support.
- Optional: Codex thread tools for creating, reading, and messaging role conversations.
- Optional: Codex automation tools for recurring heartbeat monitoring.

## Related Codex Documentation

- [Agent Skills](https://developers.openai.com/codex/skills)
- [Save workflows as skills](https://developers.openai.com/codex/use-cases/reusable-codex-skills)
- [Codex automations](https://developers.openai.com/codex/app/automations)

## License

MIT License. See [LICENSE](LICENSE).
