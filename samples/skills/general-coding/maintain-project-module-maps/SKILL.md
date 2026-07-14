---
name: maintain-project-module-maps
description: Load and maintain scoped project module maps for complex code analysis or edits. Use when selecting the smallest relevant source set, recording semantic relationships, tracking branch or module mapping status, or reconciling destination-branch instructions and maps during merges, rebases, or cherry-picks.
---

# Maintain Project Module Maps

Use this skill when a repository has adopted a module-map registry. Maps guide
source discovery but never replace authoritative code, configuration, schemas,
or assets.

## Workflow

1. Read repository instructions and the map registry.
2. Select and load only the smallest map that contains the task.
3. Open its named sources of truth and verify the relationships affected by the
   requested change.
4. Load another map only when the task crosses a declared boundary, source
   evidence reveals an undeclared dependency, or validation requires the other
   side of a contract.
5. Update affected maps in the same change when nodes, relationships,
   boundaries, coverage, or verification baselines change.
6. Record connections as directed semantic statements: source, target,
   relationship kind, and concise behavior, ownership, timing, or constraint.
7. Update branch and module statuses honestly. Use a review/reconciliation
   status when current source has not been verified.

## Branch Integration

Before merging, rebasing, or cherry-picking, inspect the destination branch's
current instructions, skill pointers, registry, and applicable maps. Reconcile
the combined map set against the integrated source. Preserve relevant maps that
exist on only one side and never resolve map conflicts by blindly choosing
`ours` or `theirs`.

## Validation And Reporting

- Check map paths, links, semantic relationships, statuses, and baselines.
- Report the initial maps loaded, any later map expansion and why, source files
  discovered outside the maps, and corrections made.
- Keep project-specific facts in project maps, not in this reusable workflow.

Follow the full
[project module mapping guide](../../../../guides/project-module-mapping.md)
and adapt its [sample registry](../../../module-maps/README.md) to the target
repository.
