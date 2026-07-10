# 编排模式路由

选择能安全保留职责、验证、恢复能力和用户权限的最轻模式。不要把每次 skill 调用都升级成多线程项目。

## 三档模式

| 模式 | 适用情况 | 必需产物 | 不要默认增加 |
| --- | --- | --- | --- |
| `LITE` | 当前上下文的一次性工作，通常只有一个活动角色，没有异步回调和 recurring 执行。 | 范围、停止条件、验证、简洁交付。 | Task board、heartbeat、cron、automation memory；没有异步边界时也不需要完整事件信封。 |
| `STANDARD` | 两个以上角色、异步或用户可见线程、跨仓库交接、merge/release 门禁，或有限期长任务。 | 明确派发和 owner、task board、异步交接用 `ORCHESTRATION_EVENT_V1`、协调者验收、重叠编辑时的分支/worktree 隔离。 | 当前协调周期内可以结束时，不要默认上 durable cron 和项目 memory。 |
| `DURABLE` | 周期性项目推进、必须跨多个 tick 恢复，或用户明确要求持久运行循环。 | Standard 所需内容，加目标契约、automation plan、持久 memory、cron、fenced lease、幂等键、生命周期和升级规则。 | 只看时间戳判断进展，或无并发租约运行。 |

Standard 只有在异步、长任务或使用用户可见角色线程时才需要 heartbeat。有限期同步 Standard 可以只维护 task board。任何 recurring heartbeat 或 cron tick 仍必须取得并发租约。

## 最低安全档位

出现以下任一情况，至少使用 `STANDARD`：

- 两个以上活动角色；
- 角色回调可能异步到达；
- 创建用户可见角色线程；
- 跨仓库或独立 worktree 交接；
- 需要协调 merge、release、QA 或 review 门禁；
- 任务足够长，需要可恢复巡检。

出现以下任一情况，使用 `DURABLE`：

- 调度会在当前协调者 turn 之后重复运行；
- 必须依赖 automation memory 安全恢复；
- 用户明确要求 project autopilot 或同类持久模式。

即使用户选择了更轻模式，也不能低于最低安全档位；简短说明原因即可。用户可以明确升级到更重模式。

## 独立修饰项

外部模型审查或调研只是修饰项，不会自动提高编排档位。一次性、只读的 `agy` 第二意见可以保持 `LITE`，同时遵守 `AGY_GEMINI_REVIEW.md` 或 `AGY_GEMINI_RESEARCH.md`。只有真实协调形态需要时才升级 Standard 或 Durable。

## 共享编辑安全

两个角色并行编辑相同文件或共享工作区时，路由本身不能保证安全。应使用分支/worktree 和不重叠 owner 隔离，或者串行执行。两者都做不到时，留在一个执行上下文。

## 路由 helper

```bash
printf '%s\n' '{
  "role_count": 2,
  "asynchronous": true,
  "recurring": false,
  "user_visible_threads": true,
  "requested_mode": "AUTO"
}' | python3 scripts/route_orchestration.py
```

helper 返回 `ORCHESTRATION_ROUTE`：最低和最终模式、用户请求是否被采纳、`NONE/HEARTBEAT/CRON`、所需协议/task board/目标契约/memory/lease/lifecycle，以及外部模型修饰项和共享编辑告警。

这是确定性的默认建议。项目指令和用户明确约束可以要求更重模式，但不能突破安全或授权硬边界。

## 工作中升级或收缩

- `LITE -> STANDARD`：出现第二个独立角色、异步回调、跨仓库交接或正式门禁。
- `STANDARD -> DURABLE`：需要 recurring tick 或持久恢复 memory。
- 升级时不能丢弃已有协议身份、event ledger 或门禁证据。
- 不能为了移除 lease 或 memory 而给运行中的 automation 降级；先按生命周期关闭。
- Durable automation 已 `CLOSED` 后，后续一次性跟进可以用新 goal identity 作为 Lite 新任务。

## 实际场景

| 场景 | 路由 |
| --- | --- |
| 当前线程审查一个本地 diff | Lite |
| 一次只读 `agy` 审查，再由协调者综合 | Lite + 外部模型修饰项 |
| 工程分支、QA 线程、Reviewer 门禁 | Standard；异步时使用 heartbeat |
| 收集两个有限期调研线程后一次综合 | Standard |
| 每两小时巡检 issue/PR 并执行安全下一步 | Durable cron |
| 持续推进 release readiness 直到目标契约通过 | Durable cron |
