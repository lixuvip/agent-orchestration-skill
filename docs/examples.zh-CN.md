# 示例

## 1. 有边界的内部子 Agent

```text
使用 $agent-orchestration。让一个内部子 Agent 只读梳理依赖关系；不需要侧边栏任务，把证据返回这里。
```

协调者保留实现 owner，不创建 task board、回调信封或 heartbeat 状态。

## 2. 文件互不重叠的并行 owner

```text
使用 $agent-orchestration。一个 owner 修改后端校验，另一个 owner 修改独立文档。派发前说明文件归属，结果回到当前任务汇总。
```

加载 `references/COORDINATION.zh-CN.md`。重叠写入必须串行或隔离。

## 3. 用户自有 Worktree 任务

```text
使用 $agent-orchestration。为高风险重构创建一个可见的 worktree 任务，我要直接在那个任务继续。
```

提前说明侧边栏任务、隔离写入面、结果位置和后续 owner。

## 4. 正式 Review 门禁

```text
使用 $agent-orchestration。实现只有在一次独立 Review 和同一候选 commit 的最终相关测试通过后才能接受。
```

中间 owner 只跑定向检查；代码未变化时，不重复最终套件。

## 5. 安静的周期巡检

```text
使用 $agent-orchestration。每小时检查部署，直到健康。只有状态变化或阻塞时通知，完成后删除 automation。
```

加载 `references/AUTOMATION.zh-CN.md`，使用 Codex 原生 automation。

## 6. 明确要求 agy 审查

```text
使用 $agy-second-opinion，通过 agy 审查这个有限 diff，不挂载整个仓库；采纳项必须回到源码验证。
```

不会加载 `agent-orchestration`。只读取审查参考，并使用 sandbox print helper。

## 7. 明确要求 agy 调研

```text
使用 $agy-second-opinion，对 allowlist 中的架构文件做一次独立 agy 调研，再和 Codex 自己的分析比较。
```

只加载调研参考，外部输出始终只是第二意见。

## 8. 派发前能力预检

```text
使用 $agent-orchestration。委派浏览器 QA 前，确认 owner 能访问已有登录态浏览器、运行必要检查并保持只读；如果不能，就把 QA 留在当前任务。
```

协调者会在派发前改变执行面，而不是最后才接受一个从未检查真实状态的结果。

## 9. 中途替换需求

```text
使用 $agent-orchestration。取消原 CSV 导出，改为 JSONL。中断或改派受影响 owner，不要合并迟到的 CSV 工作。
```

旧范围的迟到结果标记为过期；只有按新需求重新验证后才能复用。

## 10. 需求闭环与活跃工作盘点

```text
使用 $agent-orchestration。最终回复前，把每条请求和后续补充映射到当前证据，再确认没有子 Agent、后台命令、monitor 或 automation 仍可能改变结果。
```

每项最终为 `done`、`waived` 或 `blocked`；存在未盘点的运行中工作时，不能宣称整体完成。

## 11. 修正与独立 Review 分流

```text
使用 $agent-orchestration。把失败边界场景和准确测试输出交回实现者修正；修好后，只把需求、候选 commit 和原始证据交给新的 Reviewer。
```

实现者保留修正所需上下文；Reviewer 不把实现者结论预设成事实。

## 12. 恢复胶囊

```text
使用 $agent-orchestration。把任务 handoff 到 worktree 前，保存最新目标、约束、baseline、已验证证据、决策、待办、活跃进程、阻塞和精确下一步。
```

默认使用原生任务历史保存恢复胶囊；只有仓库确实需要长期交接产物时才写文件。

## 13. 可选 Best-of-N

```text
使用 $agent-orchestration。对解析器尝试 3 个隔离实现；结果返回前固定正确性、性能和可维护性标准；必要时全部拒绝；只对集成后的胜出候选运行完整套件。
```

Best-of-N 是显式高成本路径，不是普通实现的默认方式。
