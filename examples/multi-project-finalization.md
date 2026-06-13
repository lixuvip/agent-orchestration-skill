# Example Prompt: Multi-Project Finalization

```text
Use $agent-orchestration to finalize three project threads.

Projects:
- Service repository: /path/to/service
- Desktop app repository: /path/to/desktop-app
- Mobile app repository: /path/to/mobile-app

For each project:
- inspect git status;
- run the relevant tests;
- document any service API contract dependencies;
- create focused commits if the work is ready;
- report final branch, commit hashes, tests, and risks.

Create a recurring heartbeat monitor every 5 minutes.
Close the monitor after every project reaches DONE, DONE_WITH_CONCERNS, BLOCKED, or NEEDS_CONTEXT.
```

