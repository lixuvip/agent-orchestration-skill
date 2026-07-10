# 自动化并发与生命周期

heartbeat 或 cron 可能重叠、崩溃重试或在多个 worker 上运行时，使用本规则。

提示词里的“避免重复”不等于并发控制。任何会更新 memory、发消息或执行工作的 tick，都必须先取得带 fencing token 的租约。

## 租约状态

租约文件默认放在目标仓库外：

```text
${CODEX_HOME:-$HOME/.codex}/automations/<automation-id>/state
```

使用 `scripts/automation_lease.py`。helper 使用独占文件锁、原子状态替换、随机 lease token、过期时间和单调递增 fencing token。

```bash
python3 scripts/automation_lease.py acquire \
  --state-dir "$STATE_DIR" \
  --automation-id "$AUTOMATION_ID" \
  --owner-id "$TICK_ID" \
  --ttl-seconds 900
```

结果含义：

- `LEASE_ACQUIRED`：本 tick 可以继续。
- `LEASE_ALREADY_HELD`：相同 owner ID 已有活动进程；安静 no-op 退出，活动 token 不会返回。
- `LEASE_BUSY`：另一个未过期 tick 正在执行；安静 no-op 退出。
- `LEASE_EXPIRED`：当前 owner 已过期，必须停止，不能续租或写回。
- `LEASE_NOT_OWNER`：token 不匹配或已经被接管；停止且不能产生副作用。

## Tick 租约协议

1. 每次 tick 生成唯一 tick ID，在读取可变 automation memory 前取得租约。
2. 只有 `LEASE_ACQUIRED` 会返回新的 `lease_token`。把它与 `fencing_token`、过期时间仅保存在本次 tick 上下文中；不要把 token 持久化或转交为可复用凭据。
3. TTL 应大于预计运行时间加收尾余量，且不超过 helper 的一天上限。
4. 合法长任务在过期前续租。
5. 发用户消息、外部写入、提交 memory、回调或清理 automation 前立即运行 `verify`。
6. 把 fencing token 写入 memory；如果 memory 里的 token 更大，禁止覆盖。
7. 在 finally 等价的收尾路径释放。相同 owner/token 重复释放是成功 no-op。

过期 tick 可以继续做本地计算，但必须丢弃结果。只有当前租约持有者能发布、写 memory 或改变 automation 生命周期。

worker 崩溃后，只能等租约过期再接管。新持有者会得到更大的 fencing token；旧持有者恢复后也不能续租、释放或关闭新租约。

租约状态应使用本地文件系统。不要把锁文件放到 advisory lock 或原子 rename 语义未知的文件系统。

## Heartbeat 生命周期

Heartbeat 状态只能单向前进：

```text
ACTIVE -> DRAINING -> CLOSED
```

| 状态 | 含义 | 允许动作 |
| --- | --- | --- |
| `ACTIVE` | 至少一个角色未进入终态。 | 巡检、接收当前回调、发送已去重的状态请求。 |
| `DRAINING` | 所有角色已终态，或已经开始关闭。 | 停止新状态请求，只发一次最终汇总，然后请求暂停/删除并等待确认。 |
| `CLOSED` | 清理已确认。 | 永久 no-op，不能重复汇总或重新创建 heartbeat。 |

巡检终态为 `DONE`、`DONE_WITH_CONCERNS`、`BLOCKED`、`NEEDS_CONTEXT`、`CANCELLED`。这些只是监控终态。Heartbeat 最终汇总会把完成项送入协调者验收，不能把角色 `DONE` 直接变成协调者 `ACCEPTED`。

使用 `scripts/heartbeat_lifecycle.py` 根据当前生命周期、角色状态、最终汇总状态和清理确认计算下一步。

## 幂等键

Automation memory 必须保留：

- 已处理的编排 `event_id`；
- 每个 task attempt 和 dispatch nonce 的状态请求键；
- 每个 heartbeat generation 的最终汇总键；
- cleanup request ID 以及 automation 工具是否确认暂停/删除；
- 最新 lease fencing token。

如果最终汇总已经发送，但 tick 在更新 memory 前崩溃，应先比较目标位置的 latest effective update，不能重复发送。如果清理失败，保持 `DRAINING`，保留“汇总已发送”，只重试 cleanup。

禁止：在 `LEASE_BUSY` 时继续执行、让过期 tick 关闭新持有者、未收到工具确认就写 `CLOSED`、因旧回调重新创建已关闭 heartbeat，或用进程内锁处理跨进程调度。
