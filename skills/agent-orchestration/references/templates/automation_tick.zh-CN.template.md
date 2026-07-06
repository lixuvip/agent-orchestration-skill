# 自动化 Tick 模板

将本模板作为项目 Autopilot 周期性自动化的提示词主体。

```text
你正在运行一次项目 Autopilot tick。

目标 ID: <GOAL_ID>
自动化 ID: <AUTOMATION_ID>
工作区: <PATH_OR_REPOSITORY>
协调者线程 ID: <THREAD_ID_OR_NONE>
记忆路径: <AUTOMATION_MEMORY_PATH>

目标契约:
<粘贴或引用目标契约>

每次 tick:
1. 读取 AGENTS.md、AGENTS.override.md、已配置 fallback 指令文件和相关项目文档。
2. 读取记忆路径中的 automation memory。如不存在，本次 tick 后按 memory 模板创建。
3. 检查目标的实时状态：git status、分支、issue/PR 活动、角色回调、测试、构建、日志和阻塞。
4. 识别最新有效更新，而不是只看最新时间戳。
5. 和 memory 对比，避免重复评论、重复状态请求或重复工作。
6. 只选择一个属于可自动执行范围的安全下一步。
7. 执行动作，并运行最小相关验证。
8. 更新 memory：观察到的状态、已执行动作、验证、风险、下一步。
9. 如果完成条件满足，发布最终摘要并暂停或删除本自动化。
10. 如果阻塞、缺权限或超范围，发布升级报告，并按目标契约停止或等待。

必需 tick 摘要:
Latest effective update: <SUMMARY_OR_UNCHANGED>
Action taken: <ONE_ACTION_OR_NONE>
Verification: <COMMAND_OR_CHECK_AND_RESULT>
Memory updated: <YES_OR_NO>
Next safe action: <ACTION_OR_NONE>
Done: <YES_OR_NO>
Escalation needed: <YES_OR_NO_AND_REASON>

除非目标契约明确允许，不要 merge、push、deploy、删除数据、轮换密钥、产生费用、改变公开 API 契约或扩大范围。
```
