# 快速开始

## 先选 skill

Codex 委派、任务可见性、worktree、门禁或周期继续，使用 `$agent-orchestration`。

只有明确要求 `agy` / Gemini 外部第二意见时，才使用 `$agy-second-opinion`。

## 小型委派

```text
使用 $agent-orchestration。让一个内部子 Agent 只读检查解析器，把最可能的失败链路返回这里。
```

预期行为：

- 不创建侧边栏新任务；
- 不加载协调参考，不生成协议文件；
- 一个有边界的 owner 返回一个结果；
- 协调者验证证据后再接受结论。

## 用户可见任务

```text
使用 $agent-orchestration。为发布清单创建一个独立任务，我要在那个任务里继续跟进。
```

预期行为：

- 协调者提前说明会出现侧边栏任务；
- 用户自有任务负责直接后续交流；
- 只有确实需要对应语义时才使用 worktree、fork 或 handoff。

## 正式门禁

```text
使用 $agent-orchestration。协调实现和一次独立 Review，证据绑定到准确的候选 commit。
```

只加载一个语言版本的协调参考。实现阶段做定向检查，候选产物上只跑一次最终相关测试套件。

派发前，预检 owner 需要的读取、写入、执行、网络、浏览器和 connector 能力。活跃工作期间，新用户消息分为替换、追加或状态；旧范围结果未经重验都属于过期结果。

最终交付前，把每条请求和后续补充映射到当前证据，并盘点活跃 Agent、任务、后台命令、monitor 和 automation。

## 周期继续

```text
使用 $agent-orchestration。每个工作日检查这次发布，发布完成后停止，没有变化时保持安静。
```

自动化参考会使用 Codex 原生 automation，明确停止条件和清理方式。

## 外部第二意见

```text
使用 $agy-second-opinion，通过 agy 对这些文件做一次有边界的只读审查。
```

只加载审查参考，披露范围保持最小，采纳结论由 Codex 再验证。
