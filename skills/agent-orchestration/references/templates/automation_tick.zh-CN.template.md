# 自动化 Tick 模板

将本模板作为项目 Autopilot 周期性自动化的提示词主体。

```text
你正在运行一次项目 Autopilot tick。

目标 ID: <GOAL_ID>
自动化 ID: <AUTOMATION_ID>
工作区: <PATH_OR_REPOSITORY>
协调者线程 ID: <THREAD_ID_OR_NONE>
记忆路径: <AUTOMATION_MEMORY_PATH>
租约状态目录: <AUTOMATION_STATE_DIRECTORY>
Tick ID: <UNIQUE_TICK_ID>
租约 TTL 秒数: <TTL_SECONDS>
生命周期状态: <ACTIVE | DRAINING | CLOSED>

目标契约:
<粘贴或引用目标契约>

每次 tick:
1. 生成 Tick ID，用 `scripts/automation_lease.py` 获取 fenced lease。收到 `LEASE_ALREADY_HELD` 或 `LEASE_BUSY` 时安静 no-op 退出。
2. 读取 AGENTS.md、AGENTS.override.md、已配置 fallback 指令文件和相关项目文档。
3. 读取 automation memory；如果 memory 的 fencing token 更大，立即停止。memory 不存在时在本 tick 后初始化。
4. 检查目标实时状态：git status、分支、issue/PR 活动、角色回调、测试、构建、日志和阻塞。
5. 识别最新有效更新，而不只看时间戳；校验并去重回调 event ID。
6. 和 memory 的状态及幂等键对比，避免重复评论、状态请求、汇总或工作。
7. 只选择一个属于可自动执行范围的安全下一步。
8. 动作前立即验证租约，再执行动作和最小相关验证。
9. 再次验证租约，并原子更新 memory：fencing token、观察状态、动作、证据、风险和下一步。
10. 完成条件满足时只发一次最终摘要并请求暂停/删除；工具确认后才能记录清理完成。
11. 阻塞、缺权限或超范围时只发一次已去重的升级报告，并按目标契约停止或等待。
12. 在 finally 等价的收尾路径释放租约。租约过期或被替换时丢弃结果，不写入、不发消息。

必需 tick 摘要:
Latest effective update: <SUMMARY_OR_UNCHANGED>
Lease result: <ACQUIRED | ALREADY_HELD | BUSY | EXPIRED | NOT_OWNER>
Fencing token: <INTEGER_OR_NONE>
Action taken: <ONE_ACTION_OR_NONE>
Verification: <COMMAND_OR_CHECK_AND_RESULT>
Memory updated: <YES_OR_NO>
Next safe action: <ACTION_OR_NONE>
Done: <YES_OR_NO>
Lifecycle state: <ACTIVE | DRAINING | CLOSED>
Cleanup confirmed: <YES_OR_NO_OR_NOT_APPLICABLE>
Escalation needed: <YES_OR_NO_AND_REASON>

除非目标契约明确允许，不要 merge、push、deploy、删除数据、轮换密钥、产生费用、改变公开 API 契约或扩大范围。
```
