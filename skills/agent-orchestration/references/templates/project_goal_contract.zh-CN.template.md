# 项目目标契约模板

创建周期性项目 Autopilot 自动化前使用本模板。

```text
项目目标契约

目标 ID: <GOAL_ID>
编排模式: DURABLE
项目 / 工作区: <PATH_OR_REPOSITORY>
协调者线程 ID: <THREAD_ID_OR_NONE>

目标:
- <一句话说明最终效果>

完成条件:
- <验收条件 1>
- <验收条件 2>
- <验收条件 3>

指令来源:
- AGENTS.md / AGENTS.override.md: <PATH_OR_NONE>
- .codex/config.toml: <PATH_OR_NONE>
- 项目文档: <README_OR_DOCS>
- Issue / PR / Release 来源: <URL_OR_ID_OR_NONE>

可自动执行:
- <安全动作 1>
- <安全动作 2>
- <安全动作 3>

必须确认:
- merge、push、deploy、publish、删除数据、轮换密钥、产生费用、改变公开 API 契约、扩大产品范围
- <项目特定确认规则>

写入权限:
- <只读 | 限定文件编辑 | 仅测试/文档 | 允许 commit | 确认后允许 push>

验证命令:
- <COMMAND_1>
- <COMMAND_2>

频率和预算:
- 自动化类型: <heartbeat | cron>
- 频率: <自然语言频率>
- 最大尝试次数 / 运行时长: <LIMIT>
- 成功后停止: <YES_OR_NO>

记忆路径:
- <AUTOMATION_MEMORY_PATH>

并发与生命周期:
- 租约状态目录: <AUTOMATION_STATE_DIRECTORY>
- 租约 TTL / tick 最长运行时间: <SECONDS> / <SECONDS>
- Fencing 规则: 低 token 或无效 token 不能发消息、写 memory 或执行清理
- 初始 lifecycle: <ACTIVE>
- 清理策略: 最终汇总只发一次，工具确认后 <PAUSE | DELETE>

幂等键:
- <issue/pr/branch/test-state/latest-effective-update>

停止条件:
- <阻塞或失败次数限制>
- <缺少权限规则>
- <范围变化规则>
```
