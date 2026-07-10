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

替换前，安装器会运行仓库、smoke、forward、协议、并发/生命周期、路由、skill-creator 和 diff 检查；默认拒绝 dirty skill 源；暂存并校验新副本；在安装目录旁写入来源 manifest；并保留上一版用于回滚。

明确安装本地开发中的 dirty 版本：

```bash
./scripts/install.sh --allow-dirty
```

只预览、不改当前安装：

```bash
./scripts/install.sh --allow-dirty --dry-run
```

恢复保留的上一版：

```bash
./scripts/install.sh --restore
```

## 方式二：手动安装

手工复制会跳过验证、来源记录和回滚能力；除非明确不需要这些保障，否则优先使用安装器。

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

## 可选：添加项目常驻指令

Project Autopilot 在目标仓库有稳定 Codex 指令时效果最好。

用 `AGENTS.md` 存放稳定项目规则：

```markdown
# AGENTS.md

## Repository Expectations

- 声明 release ready 前运行文档中的测试命令。
- merge、push、deploy、破坏性改动或公开 API 契约变化前先询问。
- 临时 automation 状态写入 automation memory，不写进本文件。
```

只有子目录需要更强局部规则时，才使用嵌套的 `AGENTS.override.md`。`.codex/config.toml` 用于 Codex 配置，例如 fallback 指令文件名；不要在里面存密钥或实时任务状态。

## 更新

拉取最新仓库代码后重新安装：

```bash
git pull
./scripts/install.sh
```

安装器会暂存新副本、保留上一版，并在报告成功前验证源码与安装副本一致。
