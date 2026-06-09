---
name: codex-local-automations
description: Create, review, or update local Codex app automation definitions, including cron schedules, prompts, model settings, cwd scopes, and safety rules. Use when an agent needs to document or modify Codex automation TOML files without relying on machine-specific paths, private user data, auth files, or unsupported backend calls.
---

# Codex Local Automations

Use this skill when creating or maintaining local Codex app automations from
the filesystem.

## Storage Layout

Prefer the Codex app UI when it is available. For manual edits, use the local
automation registry:

```text
$CODEX_HOME/automations/<automation-id>/automation.toml
```

If `CODEX_HOME` is unset, use the default Codex home:

```text
Windows: %USERPROFILE%\.codex\automations\<automation-id>\automation.toml
macOS/Linux: ~/.codex/automations/<automation-id>/automation.toml
```

Do not edit scheduler-internal files such as `.run-jitter-salt`. Do not inspect
or modify Codex auth/session files, browser cookies, tokens, or undocumented
backend endpoints.

## Workflow

1. Choose a stable lowercase automation id using letters, digits, and hyphens.
2. Back up the existing automations directory or the target automation folder.
3. Create or edit `<automation-id>/automation.toml`.
4. Use a conservative prompt for unattended work. State allowed actions,
   forbidden actions, repository boundaries, and review gates explicitly.
5. Set the schedule with `rrule`. Treat times as local to the machine unless the
   app documents otherwise.
6. Update `updated_at` when changing an automation. Use millisecond Unix
   timestamps for `created_at` and `updated_at`.
7. Refresh or restart the Codex app if the automation list does not update.
8. Verify in the Codex app, or by checking that the TOML still contains the
   intended id, status, schedule, model, reasoning effort, and cwd.

## TOML Template

```toml
version = 1
id = "project-daily-status-digest"
kind = "cron"
name = "Project daily status digest"
prompt = "Create a read-only project status digest. Inspect project docs and git status. Report blockers, pending user actions, uncommitted or unpushed work, dependency update availability, and the next safest action. Do not edit files, commit, push, install software, delete files, or read credentials. If nothing important changed, archive the run."
status = "ACTIVE"
rrule = "FREQ=DAILY;INTERVAL=1;BYHOUR=22;BYMINUTE=45"
model = "gpt-5.3-codex-spark"
reasoning_effort = "medium"
execution_environment = "local"
cwds = ["<absolute-project-path>"]
created_at = 1780000000000
updated_at = 1780000000000
```

Use `status = "ACTIVE"` only when the automation is ready to run unattended.
Keep `cwds` narrow and absolute so the automation opens the intended project.

## Schedule Examples

```toml
# Daily at 22:45 local time
rrule = "FREQ=DAILY;INTERVAL=1;BYHOUR=22;BYMINUTE=45"

# Every three hours
rrule = "FREQ=HOURLY;INTERVAL=3"

# Weekdays at 18:00 local time
rrule = "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=18;BYMINUTE=0"
```

## Safety Notes

- Keep manual editing focused on `automation.toml`.
- Treat any mirrored SQLite database or app state as internal implementation
  detail unless the Codex app documents it as an API.
- Default new automations to read-only behavior until the user approves a write
  workflow.
- Include explicit "do not commit" and "do not push" instructions when review
  confirmation is required.
- For automations that may update dependencies, require dry-run reporting when
  the working tree is dirty or when a pull would conflict with local work.
