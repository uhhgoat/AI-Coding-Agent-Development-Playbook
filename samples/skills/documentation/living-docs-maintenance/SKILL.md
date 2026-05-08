---
name: living-docs-maintenance
description: Maintain living project documentation when workflows, architecture, validation, ownership, or next steps change. Use when a task changes durable context that future humans or agents need.
---

# Living Docs Maintenance

Use this skill when a change affects the durable project record.

## Required Checks

1. Identify whether the task changed operating procedures, architecture,
   ownership, safety, validation, or next steps.
2. Find the project's canonical place for that information.
3. Update the smallest relevant document.
4. Prefer append-only progress notes for meaningful discoveries, failed
   attempts, handoffs, and validations.
5. Keep architecture docs stable and current-state docs operational.
6. Record skipped validation and remaining uncertainty.

## Documentation Targets

- Current-status or roadmap docs for phase, latest validation, risks, clues, and
  next intended move.
- Active-work docs, issue trackers, or plan ownership blocks for overlapping
  work and handoffs.
- Command guides or runbooks for scripts, flags, setup, expected output, editor
  workflows, debug-console actions, release procedures, and failure modes.
- Architecture-baseline docs for durable boundaries and dependency direction.
- Feature or module plans for local implementation state.

## Progress Note Shape

```markdown
### Update: <short title>

- Actor:
- Timestamp:
- Scope:
- Status:
- Files/areas touched:
- Summary:
- Verification:
- Next intended move:
```
