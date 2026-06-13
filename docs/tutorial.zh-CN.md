# 教程：协调一次多项目发布

这份教程模拟一个真实任务：一个协调者要求三个项目线程分别完成收尾工作，并把结果回报给协调者。

## 场景

你有三个项目：

- `Service API`：共享后端服务。
- `Web Client`：使用共享服务的浏览器客户端。
- `Mobile Client`：使用共享服务的移动客户端。

你希望每个项目完成改动、创建提交、记录远程接口契约，并返回清晰的最终状态。

## 第 1 步：从协调者提示开始

```text
Use $agent-orchestration.

Coordinate final delivery across Service API, Web Client, and Mobile Client.

For each project:
- inspect current git status;
- ensure shared service API documentation is clear;
- run relevant verification;
- create focused commits if the work is ready;
- return branch, commits, verification, and remaining risks.

Create a 5-minute heartbeat monitor and close it when every project reaches a terminal status.
```

## 第 2 步：登记角色

协调者记录一张角色表：

| Role | Project | Thread ID | Scope |
| --- | --- | --- | --- |
| API Engineer | Service API | `<thread-id>` | backend service and docs |
| Web Client Engineer | Web Client | `<thread-id>` | browser client and integration docs |
| Mobile Client Engineer | Mobile Client | `<thread-id>` | mobile client, API bridge, and docs |

如果这是一个会重复使用的协作设置，可以使用 `references/ROLE_REGISTRY.template.md`。

## 第 3 步：分发任务

每个角色都会收到基于 `references/templates/task_dispatch.template.md` 的提示。

关键字段包括：

- `Task ID`
- `Coordinator thread ID`
- `This role thread ID`
- `Editable scope`
- `Read-only scope`
- `Verification`
- `Callback`
- `Stop and report if`

## 第 4 步：创建心跳监控

协调者使用 `references/templates/monitoring_heartbeat.template.md` 创建一个 recurring automation。

建议间隔：

```text
Every 5 minutes
```

监控器读取每个被跟踪线程，并且只接受明确的终态：

- `DONE`
- `DONE_WITH_CONCERNS`
- `BLOCKED`
- `NEEDS_CONTEXT`

## 第 5 步：汇总结果

当所有角色完成后，协调者生成简洁的最终汇总：

```text
All three project threads reached terminal status.

Service API:
- Status: DONE_WITH_CONCERNS
- Commits: ...
- Verification: ...
- Risk: untracked dist/ left untouched

Web Client:
- Status: DONE_WITH_CONCERNS
- Commits: ...
- Verification: ...
- Risk: end-to-end browser tests were skipped because no test account was available

Mobile Client:
- Status: DONE
- Commits: ...
- Verification: ...
- Risk: none reported
```

## 第 6 步：关闭循环

协调者在发布 all-complete 汇总后，禁用或删除心跳监控。

任务已经到达终态后，不要让过期的监控继续运行。
