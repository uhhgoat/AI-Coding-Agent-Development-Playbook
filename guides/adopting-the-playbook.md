# Adopting The Playbook

Use this guide when you want an AI coding agent to adapt the workflow playbook
to an existing repository.

## Recommended Process

1. Give the agent the main playbook file or the whole repository.
2. Ask it to inspect the target project before writing anything.
3. Have it identify the project type, build tools, language versions, protected
   directories, generated files, and existing documentation.
4. Ask it to create or update the durable instruction set:
   - `AGENTS.md`, or the repository's equivalent standing-instructions file
   - `docs/current-status.md`, or an existing roadmap/status area
   - `docs/command-guide.md`, or an existing runbook/procedure guide
   - `docs/architecture-baseline.md`, or an existing architecture reference
   - `docs/active-work.md`, or an equivalent ownership tracker, when multiple
     people or agents may work at once
5. Ask it to propose project skills only for recurring, durable tasks.
6. Ask it to add tool-specific shims only after there is one canonical skill
   body worth sharing across tools.
7. Review the resulting docs for project-specific facts, team names, private
   paths, secrets, and stale assumptions before committing.

## Adapt The Shape

The playbook describes responsibilities, not mandatory filenames. Keep the
roles, but adapt the structure to the target repository.

- `AGENTS.md` means the canonical standing instructions for agents. If the
  project already has an equivalent file, update that file or add a thin pointer.
- `docs/current-status.md` means the operational state that helps the next
  person or agent resume work. It may live in an existing planning, roadmap, or
  project-notes area.
- `docs/command-guide.md` means validated ways to operate the project. It is
  not limited to CLI commands or CLI applications. It can include editor
  workflows, build/test invocations, release steps, migration procedures,
  notebook runs, local services, game-engine batchmode commands, in-game debug
  console commands, admin panels, or known failure/recovery procedures.
- `docs/architecture-baseline.md` means durable system shape: boundaries,
  dependency direction, runtime layers, data ownership, and integration points.
- `docs/active-work.md` is most useful when several humans or agents may overlap.
  A small solo project may use a lighter status section instead.
- Skills should describe recurring project work. Do not create a skill for a
  one-time bug investigation unless that investigation revealed a reusable
  workflow.

## What To Preserve

- Keep one canonical source of truth for standing instructions.
- Keep progress out of architecture docs.
- Keep command syntax and validated workflows in a command guide or equivalent
  runbook.
- Keep active ownership and handoffs visible when people or agents overlap.
- Keep skills focused on repeatable tasks, not one-off debugging notes.

## Unity Example Direction

For a Unity project, the agent might create:

- a root `AGENTS.md` with Unity version, package constraints, asset boundaries,
  scene/loading conventions, UI framework rules, and serialization guidance
- a `docs/command-guide.md` with editor, test, build, and validation commands
- a `docs/current-status.md` with the current milestone and latest test result
- one or more Unity skills for recurring patterns such as manager singletons,
  ScriptableObject config maps, asset registration, UI Toolkit screens, or
  custom update dispatch

Do not copy Unity sample skills verbatim unless the target project actually
uses the same pattern. Treat them as examples of how to write a skill.
