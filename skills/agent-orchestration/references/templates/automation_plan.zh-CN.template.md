# 自动化计划模板

调用 automation 工具前，用本模板准备 heartbeat 或 cron 自动化。

```text
自动化计划

名称: <AUTOMATION_NAME>
目标 ID: <GOAL_ID>
自动化类型: <heartbeat | cron>
目标位置: <thread | local | worktree>
工作区: <CWD_LIST_OR_NONE>
目标线程 ID: <THREAD_ID_OR_NONE>
频率: <自然语言频率；内部再转换为工具调度格式>
推理强度: <minimal | low | medium | high>

已有自动化检查:
- 匹配自动化 ID: <ID_OR_NONE>
- 更新而不是重复创建: <YES_OR_NO>

目标契约:
- <PATH_OR_INLINE_SUMMARY>

记忆:
- 记忆路径: <AUTOMATION_MEMORY_PATH>
- 最新有效更新键: <KEY>

提示词职责:
- 读取 AGENTS.md、AGENTS.override.md、已配置 fallback 指令文件和相关项目文档。
- 行动前读取 automation memory。
- 检查实时 git、issue、PR、测试、线程或发布状态。
- 每次 tick 只执行一个安全下一步。
- 每次 tick 都更新 memory。
- 完成、阻塞或缺少权限时暂停、删除或升级给用户。

保存前需要用户确认:
- <如果涉及 worktree 环境设置或高风险权限则 YES，否则 NO>
```
