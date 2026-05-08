# Module Instructions

This file applies to the current module or subtree. It supplements the root
`AGENTS.md`.

## Scope

- State what this module owns.
- State what this module must not own.
- Link to the root project instructions and relevant architecture docs.

## Boundaries

- Keep module-internal types private unless callers need them.
- Keep external API contracts small and explicit.
- Do not reach across module boundaries when an interface or adapter should be
  used instead.
- Document any dependency direction that must not be reversed.

## Local Workflow

- Read this file before editing files in this subtree.
- Read the module plan, if one exists.
- Update the module plan when implementation direction, validation, ownership,
  or next steps change.
- Add or update module-specific commands, editor workflows, debug-console
  actions, setup steps, or validation procedures in the command guide or the
  project's equivalent runbook.

## Verification

- List the narrow tests for this module.
- List integration tests or smoke workflows.
- State any environment setup required before running validation.

## Handoff

When pausing or completing module work, record:

- actor
- timestamp
- files touched
- what changed
- validation run
- residual risk
- next intended move
