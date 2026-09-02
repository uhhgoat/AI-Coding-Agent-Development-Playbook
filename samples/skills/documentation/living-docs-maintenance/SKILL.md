---
name: living-docs-maintenance
description: Maintain living project documentation when workflows, architecture, validation, ownership, or authorized plan state changes. Use when a task changes durable context that future humans or agents need.
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
7. For planned work, update the smallest applicable plan slice and its
   completion state before changing global status. Do not create a successor
   slice or label an agent-discovered idea as the next move without explicit
   authorization.

## Plan Closure

The applicable milestone or feature plan controls the next move for planned
work. Keep documentation aligned with that authority:

- Continue the smallest incomplete authorized slice; do not skip to a later
  phase or expand scope because it seems useful.
- When the slice succeeds, mark it complete and record its verification,
  residual uncertainty, and ownership state.
- Keep out-of-scope discoveries as deferred observations, risks, or open
  questions only when they matter to recovery. They are not active work.
- A `Next intended move` must name an existing authorized item. When a slice
  has closed and no authorized work remains, write `No active next move — await
  direction.`

## Documentation Targets

- Current-status or roadmap docs for phase, latest validation, risks, clues,
  slice closure, and the authorized next intended move.
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
- Next intended move: <authorized plan item, or `No active next move — await direction.`>
```
