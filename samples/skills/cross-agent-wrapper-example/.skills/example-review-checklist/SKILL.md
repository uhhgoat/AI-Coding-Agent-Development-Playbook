---
name: example-review-checklist
description: Run a concise review checklist for small repository changes. Use when asked to review a change, prepare a PR, or verify that docs, tests, and risk notes line up before handoff.
---

# Example Review Checklist

Use this canonical skill as the single source of truth. Wrapper files in
`.codex/skills`, `.claude/skills`, and `.github/instructions` should point here
instead of duplicating the workflow.

## Workflow

1. Identify the change under review.
   - Inspect the diff, touched files, and surrounding code.
   - Note generated files, vendored folders, or protected paths.
   - Separate user changes from agent changes when the worktree is dirty.

2. Check behavior and risk.
   - Look for regressions, missing validation, incorrect assumptions, and unsafe
     writes before style feedback.
   - Verify that commands, migrations, deployments, or external calls are
     documented and appropriately guarded.
   - Confirm that user-facing text, docs, and examples match the implementation.

3. Validate with the narrowest meaningful checks.
   - Prefer existing test, lint, build, or format commands.
   - Run only the checks that are relevant to the touched surface.
   - Record skipped checks and why they were skipped.

4. Report clearly.
   - Lead with actionable findings, ordered by severity.
   - Include file and line references when possible.
   - Summarize validation and residual risk after the findings.

## Privacy Guardrails

Do not copy private issue text, credentials, customer data, local paths, hostnames,
or personal notes into reusable review examples. Replace specific identifiers with
neutral names before sharing the skill outside the source project.