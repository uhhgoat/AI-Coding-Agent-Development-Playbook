# Project Instructions

This file is the canonical standing-rules document for this repository. It is
for humans and AI coding agents.

## Purpose

- State what this repository contains.
- State the main product, library, service, game, app, or research goal.
- State important non-goals.

## Project Metadata

- Primary language:
- Runtime or engine version:
- Package manager or build system:
- Supported operating systems:
- Last dependency inventory refresh:

## Protected Areas

Treat these areas as read-only unless the user explicitly approves edits:

- vendored dependencies
- generated code
- build outputs
- external SDKs
- migration snapshots
- credentials or secret stores

Prefer adapters, wrappers, or first-party modules over direct upstream edits.

## Repository Direction

Suggested shape:

```text
docs/
src/ or modules/
apps/
tools/
tests/
configs/
logs/
exports/
```

Adjust this to match the target project. Document any local convention here.
If the project already has equivalent docs, link to them instead of duplicating
their contents.

## Architecture Rules

- Keep reusable logic separate from app-specific orchestration.
- Keep framework, engine, vendor, or cloud APIs behind adapter boundaries.
- Keep runtime configuration explicit.
- Avoid broad refactors during narrow tasks.
- Do not introduce new architecture layers without a concrete need.

## Collaboration And Ownership

- Check `git status --short` before editing.
- Assume uncommitted changes may belong to another person or agent.
- Read `docs/current-status.md` or the project's equivalent status note before
  non-trivial work.
- Read `docs/active-work.md` or the equivalent ownership tracker when it
  exists.
- Do not edit files owned by another active work stream without handoff,
  review scope, coordination, or explicit approval.
- Durable progress updates should include actor, timestamp, scope, summary,
  verification, and next intended move.

## Documentation Rules

Update docs in the same change when behavior, workflows, architecture, safety,
or durable project rules change.

| Change | Required documentation |
| --- | --- |
| New command, script, launch workflow, debug console action, editor procedure, or flag | `docs/command-guide.md` or equivalent |
| New module, integration, or staged feature | feature or module plan |
| Active owner, paused task, blocked task, or handoff | `docs/active-work.md` or plan ownership block |
| Architecture boundary or dependency direction change | `docs/architecture-baseline.md` or equivalent |
| Validated milestone, failed live test, important clue, or changed next step | `docs/current-status.md` or equivalent |
| New standing project rule | `AGENTS.md` |
| New recurring agent recipe | project skill |

## Testing Expectations

- Run the narrowest meaningful validation first.
- Expand tests when the blast radius is larger.
- Document skipped tests or blocked validation.
- Do not treat a passing build as complete validation for high-risk behavior.

## Safety Rules

Treat a task as high-risk if it can affect production, user data, money,
credentials, legal or medical outcomes, physical systems, destructive files, or
irreversible external state.

High-risk changes need explicit gates, dry-runs or simulations where possible,
operator-visible reporting, rollback or recovery paths, and documented
validation.

## Skills

Project skills should live in a documented canonical location, such as
`.skills/<skill-name>/SKILL.md`, with tool-specific shims only when needed.

Add a skill only for recurring, durable work that future agents are likely to
repeat.
