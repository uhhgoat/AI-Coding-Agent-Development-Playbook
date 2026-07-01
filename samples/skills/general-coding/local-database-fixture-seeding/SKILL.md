---
name: local-database-fixture-seeding
description: Create, repair, refresh, clean, or validate local-only database fixture data for development and tests. Use when Codex needs repeatable seed scripts, ORM seeders, fake scenario records, local database cleanup, fixture logs, predicate-based validation, or idempotent test data setup without touching production or deployable migrations.
---

# Local Database Fixture Seeding

## Overview

Use this skill to create useful local test data without turning workstation-only state into a deployable migration. The goal is coherent fake scenarios, guarded writes, repeatability, and validation that mirrors the product behavior being tested.

## Local-Only Rules

- Confirm the target is local, disposable, or explicitly approved for test data before writing.
- Do not create real personal, customer, financial, medical, credential, or production-like data. Use clearly fake names, addresses, emails under reserved domains such as `example.test`, and non-routable identifiers.
- Keep local fixture scripts separate from deployable migrations unless the user explicitly asks for a deployable seed.
- Add an obvious seed marker, such as `LOCAL-SEED-YYYYMMDD-<scenario>`, to safe text fields, metadata, or separate tracking tables so the data can be found and cleaned later.
- Use transactions, idempotent upserts, and target guards. For SQL scripts, prefer `SET XACT_ABORT ON` or the engine equivalent when supported.
- Do not update generated ORM mappings just to seed existing tables.

## Workflow

1. Understand the scenario.
   - Identify the UI, API, report, job, or test that needs data.
   - Trace the code or query predicates before designing rows.
   - Write a small scenario matrix with the expected outcome for each fixture.

2. Inventory existing data.
   - Query by stable keys, seed marker, date range, owning user, tenant, or feature flag.
   - Check for previous fixture rows that can be reused, repaired, or safely removed.
   - Inspect schema constraints, defaults, foreign keys, required columns, and enum values from the database or ORM metadata.

3. Design coherent records.
   - Seed every relationship the product path actually needs, not just the visible row.
   - Prefer the smallest set of records that proves the behavior.
   - Use deterministic values for dates, identifiers, and names unless randomness is part of the test.
   - Avoid brittle assumptions about auto-increment values; capture generated IDs in variables or query by stable keys.

4. Write the script or seeder.
   - Put local-only artifacts in the repository's scratch, tools, test, or documented local workflow area.
   - Guard the target database using database name, host, tenant, environment, or an explicit `ALLOW_LOCAL_SEED` style flag.
   - Use `INSERT ... WHERE NOT EXISTS`, `MERGE`, `ON CONFLICT`, ORM upserts, or clear delete-and-reinsert logic when appropriate.
   - Include cleanup logic only when it is safe and clearly scoped to the seed marker.

5. Validate like the product.
   - Run row counts, but do not stop there.
   - Run validation SQL, ORM queries, tests, or API checks that mirror the product predicates.
   - Re-run the seed when practical to prove idempotency.
   - Record the script path, seed marker, scenarios, validation output, and cleanup approach.

## Safety Checks

Before any write, verify:

- database name and host
- current user or connection role
- environment or tenant
- number of rows that will be inserted, updated, or deleted
- rollback or cleanup path

Stop and ask for direction if the target appears shared, production-like, regulated, or unclear.

## Handoff

Report the seed marker, files changed, target environment, scenarios created, validation performed, whether idempotency passed, and how to clean up the fixtures.
