---
name: sql-migration-script-runner
description: Run, rerun, diagnose, or verify database migration scripts for local, development, or test databases. Use when Codex is asked to execute ordered SQL files, framework migrations, schema changes, seed/config migrations, rollback-and-rerun requests, failed migration recovery, or post-migration verification for tools such as SQL Server, PostgreSQL, MySQL, SQLite, Flyway, Liquibase, Rails, Django, EF, or similar migration systems.
---

# SQL Migration Script Runner

## Overview

Use this skill to run database migrations with evidence instead of hope. Prefer the repository's existing migration runner and conventions over ad hoc SQL execution.

## Workflow

1. Identify the exact target.
   - Locate the migration file, migration class, or ordered migration range.
   - Read any repository or folder instructions before execution.
   - Confirm whether the task is read-only verification, first execution, rerun, failed-script recovery, or rollback-and-rerun.
   - Preserve migration ordering. Do not skip prerequisite migrations unless the user explicitly directs it and the risk is understood.

2. Confirm the environment and safety level.
   - Determine the database engine, database name, host, account, and migration tool from documented local config, environment variables, or the user's explicit instruction.
   - Do not print secrets. Redact passwords, tokens, and connection-string credentials in responses.
   - Treat shared development, staging, production, customer, billing, medical, financial, or regulated data as high-risk. Require explicit user approval before writes.
   - Prefer local or disposable test databases for first runs.

3. Inspect before writing.
   - Read the migration contents.
   - Check whether the target objects or rows already exist.
   - For schema changes, inspect catalog tables such as `information_schema`, `sys.tables`, `sys.columns`, `pg_catalog`, or the engine equivalent.
   - For data/config changes, query by stable keys before writing.
   - If the migration changes ORM-backed schema, check whether model snapshots, generated mappings, or entity metadata also need updates.

4. Execute through the project's normal path.
   - Prefer commands already documented in the repo, such as `dotnet ef database update`, `rails db:migrate`, `python manage.py migrate`, `flyway migrate`, `liquibase update`, `psql -f`, `sqlcmd -i`, `mysql <`, or a project script.
   - If raw SQL execution is necessary, use the database driver's safe execution API and a reasonable timeout.
   - For SQL Server-style scripts, split batches only on lines containing `GO` by itself. Do not split on the text `GO` inside comments or string literals.
   - Keep command output or result summaries sufficient to prove what happened.

5. Verify immediately.
   - Re-query the exact objects, columns, constraints, indexes, or rows the migration should create or change.
   - If idempotency is expected, rerun only when safe and verify the second run does not duplicate data or fail.
   - For failed runs, record the failed migration, error, last successful step, and database state before retrying.

## Rollback And Rerun

- Do not drop tables, columns, constraints, indexes, or data unless the user explicitly requested rollback/destructive repair.
- Inspect dependencies before removal.
- Back up or export affected data when practical before destructive local changes.
- Verify removal, rerun the intended migration, then verify restoration.

## Reporting

State:

- target database/environment, with secrets redacted
- script or migration identifiers executed
- execution method and command family
- verification queries or checks run
- whether idempotency was checked
- skipped validation and remaining risk
