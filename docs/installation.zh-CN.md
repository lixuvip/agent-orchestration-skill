# 安装说明

本仓库提供一个 Codex skill：

```text
skills/agent-orchestration
```

Codex skill 是一个包含 `SKILL.md` 的目录，也可以附带 references、scripts、assets 和 UI metadata 等资源。这个 skill 提供多角色线程协调所需的参考文档和模板。

当前 Codex skill 的结构和支持的安装位置，请参考官方 [Agent Skills documentation](https://developers.openai.com/codex/skills)。

## 方式一：从 Git 安装

```bash
git clone https://github.com/lixuvip/agent-orchestration-skill.git
cd agent-orchestration-skill
./scripts/install.sh
```

安装脚本会把 skill 安装到：

```text
${CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}/agent-orchestration
```

## 方式二：手动安装

```bash
git clone https://github.com/lixuvip/agent-orchestration-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R agent-orchestration-skill/skills/agent-orchestration "${CODEX_HOME:-$HOME/.codex}/skills/"
```

如果你的 Codex 环境扫描 `$HOME/.agents/skills`，可以运行：

```bash
CODEX_SKILLS_DIR="$HOME/.agents/skills" ./scripts/install.sh
```

## 方式三：按仓库安装

如果只想让这个 skill 在某一个项目仓库中生效，可以把它复制到该仓库的 `.agents/skills` 目录：

```bash
mkdir -p /path/to/your/repo/.agents/skills
cp -R skills/agent-orchestration /path/to/your/repo/.agents/skills/
```

这种方式适合团队把 skill 和项目一起版本化管理。

## 验证安装

启动一个新的 Codex 会话，然后输入：

```text
Use $agent-orchestration to create a two-role plan for a small bug fix.
```

如果 Codex 没有检测到这个 skill，重启 Codex，并确认下面的文件存在：

```text
${CODEX_HOME:-$HOME/.codex}/skills/agent-orchestration/SKILL.md
```

如果安装到 `$HOME/.agents/skills`，检查：

```text
$HOME/.agents/skills/agent-orchestration/SKILL.md
```

## 更新

拉取最新仓库代码后重新安装：

```bash
git pull
./scripts/install.sh
```

安装脚本会替换已安装的 `agent-orchestration` 目录。
