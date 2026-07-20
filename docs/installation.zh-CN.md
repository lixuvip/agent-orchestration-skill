# 安装说明

本仓库提供两个互相独立的 Codex skill：

```text
skills/agent-orchestration
skills/agy-second-opinion
```

## 使用安装器

```bash
git clone https://github.com/lixuvip/codex-agent-orchestration-skill.git
cd codex-agent-orchestration-skill
./scripts/install.sh
```

默认命令验证仓库并只安装 `agent-orchestration`，同时记录来源并校验一致性。外部 skill 单独安装：

```bash
./scripts/install.sh --skill agy-second-opinion
```

本地开发版本：

```bash
./scripts/install.sh --allow-dirty
./scripts/install.sh --allow-dirty --dry-run
./scripts/install.sh --skill agy-second-opinion --allow-dirty
```

分别恢复所选 skill 的旧副本：

```bash
./scripts/install.sh --restore
./scripts/install.sh --skill agy-second-opinion --restore
```

默认目标目录是 `${CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}`。

## 只手工安装一个 skill

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/agent-orchestration "${CODEX_HOME:-$HOME/.codex}/skills/"
```

也可以只复制 `skills/agy-second-opinion`。按仓库安装时，把需要的目录放到 `.agents/skills/`。

## 验证

新建 Codex 任务并明确调用：

```text
使用 $agent-orchestration 完成一次有边界的内部子 Agent 委派。
使用 $agy-second-opinion 完成一次明确要求的 agy 审查。
```

如果发现列表没有刷新，重启 Codex，并检查两个安装目录中的 `SKILL.md`。
