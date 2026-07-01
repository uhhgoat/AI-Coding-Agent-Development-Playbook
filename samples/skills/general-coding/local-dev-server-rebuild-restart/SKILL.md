---
name: local-dev-server-rebuild-restart
description: Rebuild, restart, or recover a local development server or multi-process application stack. Use when Codex needs to stop a running app before building, recover from locked build outputs, restart a web/API/background service after a pull, resolve local port conflicts, start dependent local services, or verify a local dev URL with health checks or smoke tests.
---

# Local Dev Server Rebuild Restart

## Overview

Use this skill when local runtime state blocks development: stale processes, locked files, occupied ports, missing dependent services, or a dev URL that should be online after a build. Prefer documented project scripts over inventing a new lifecycle.

## Workflow

1. Discover the stack.
   - Read the project's runbook, package scripts, launch settings, compose files, process manager config, or IDE launch profile.
   - Identify the app entry point, build command, start command, ports, health URL, environment variables, and dependent services.
   - Check current Git status before commands that generate outputs or change local config.

2. Inspect current runtime state.
   - List processes by executable path, command line, package script, service name, or port.
   - Prefer precise process matching over broad names. Many machines run several `node`, `dotnet`, `python`, `java`, or `ruby` processes.
   - Check port listeners before starting a new server.
   - If the server writes logs, locate the current log file before restart.

3. Stop only the intended processes.
   - Stop the app process before full rebuilds when build outputs can be locked.
   - Do not kill database servers, Docker Desktop, system services, IDEs, or unrelated local apps unless the user explicitly asks.
   - If a process manager is used, stop through that manager when possible.

4. Rebuild using the narrowest command that is meaningful.
   - Use the documented command, such as `npm run build`, `dotnet build`, `mvn test`, `gradle build`, `cargo build`, `go test`, `docker compose build`, or a project script.
   - Clean only when stale outputs, dependency changes, or locked-file errors make it useful.
   - Preserve environment-specific local files unless the project documents they are generated.

5. Start dependencies, then the app.
   - Bring up required local services such as databases, queues, caches, proxy backends, or asset dev servers.
   - Pass documented environment variables explicitly.
   - For background starts, keep the process attached when logs are needed; otherwise use the platform's normal background service pattern.
   - Avoid leaving duplicate servers running on the same app or port.

6. Validate the running stack.
   - Check the port is listening.
   - Hit a health endpoint, root URL, API route, or CLI smoke command.
   - Confirm the response shape, status code, redirect, or log line that indicates success.
   - If validation fails, inspect logs before retrying.

## Common Diagnostics

- Windows port owner: `Get-NetTCPConnection -LocalPort <port> -State Listen`
- Cross-platform port owner: `lsof -i :<port>` or `netstat`
- HTTP smoke check: `curl -i http://localhost:<port>/health`
- Node scripts: `npm run`, `pnpm run`, or `yarn run`
- Docker stack: `docker compose ps`, `docker compose up -d`, `docker compose logs`

## Guardrails

- Do not change production, shared, or remote services while recovering a local server.
- Do not overwrite `.env`, secrets, databases, or local user config without explicit approval.
- Do not run destructive cleanup commands such as removing volumes, deleting caches, or pruning Docker resources unless asked.
- If a command needs long-lived background execution, make sure the chosen execution context will not immediately clean up child processes.

## Handoff

Report the stopped processes, build command, start command, validation URL or check, final status, and any services still required for the user to keep running.
