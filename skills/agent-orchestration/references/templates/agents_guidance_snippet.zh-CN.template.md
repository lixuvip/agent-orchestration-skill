# AGENTS.md 指令片段模板

项目需要为周期性 Autopilot 工作保留持久 Codex 指令时使用。

```markdown
## Codex 项目 Autopilot

- 主要目标来源: <issues | PRs | roadmap | docs | release plan>。
- 声明进展前必须验证: <COMMANDS_OR_CHECKS>。
- 可自动执行的安全动作: <只读检查 | 测试 | 文档编辑 | 小范围修复 | 评论>。
- 必须确认的动作: merge、push、deploy、publish、删除数据、轮换密钥、产生费用、改变公开 API 契约、扩大产品范围。
- 状态记忆: 临时 automation 状态写入 `${CODEX_HOME:-$HOME/.codex}/automations/<automation-id>/memory.md`；不要把实时任务状态写进本文件。
- 幂等规则: 评论或重复工作前，先比较最新有效更新。
- 升级规则: 验证反复失败、缺少权限或范围变化时停止并询问。
```
