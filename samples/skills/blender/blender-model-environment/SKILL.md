---
name: blender-model-environment
description: Build and revise modular Blender environment kits with deterministic dimensions, pivots, reusable geometry, procedural assemblies, and validation-ready organization. Use for arena walls, gates, towers, stairs, fences, circular layouts, snap-together modules, collision sources, or LOD candidates.
---

# Blender Model Environment

Treat a module kit and an assembled environment as separate artifacts.

Use
[the medieval-architecture skill](../blender-model-medieval-architecture/SKILL.md)
for houses, cottages, castles, towers, gates, fortifications, roofs, ruins, or
village kits. It adds human-scale, structural, roof, circulation, and
medieval-material boundaries on top of this generic environment workflow.

## Workflow

1. Read [the shared Blender contract](../blender-validate-asset/references/shared-contract.md),
   [the hard-surface skill](../blender-model-hard-surface/SKILL.md), and
   [the modular-environment reference](references/modular-environment.md).
2. Define world units, module dimensions, grid increments, pivot convention,
   forward/up axes, contact surfaces, and evaluated budgets.
3. Create semantic collections for `MODULES`, `CONTROLS`, `ASSEMBLIES`,
   `COLLISION`, `LOD`, and `PREVIEW` as applicable.
4. Author one reusable module before building an assembly.
5. Prefer shared mesh data, collection instances, or retained Array/Curve
   construction when repeated objects should remain linked.
6. Name offset empties, curve paths, cutters, sockets, collision sources, and
   assemblies by role.
7. Render each module in isolation and the assembled result from fixed views.
8. Validate dimensions, pivots, seams, repetition, determinant, base/evaluated
   growth, and duplicate-versus-instance intent.
9. Keep collision and LOD candidates explicit; do not generate or export them
   merely because the render mesh exists.
10. Route materials, bakes, final validation, and export through their
    dedicated skills.

## Guardrails

- Do not join reusable modules into one opaque mesh during authoring.
- Do not apply an Array or Curve merely to obtain a preview.
- Do not mix experimental pieces with approved modules without collection and
  naming boundaries.
- Stop when grid, pivot, collision, or LOD requirements are unknown.

## Deliverables

- Reusable module collection and separate assembly collection.
- Module dimension/pivot manifest and operation manifest.
- Isolated-module and assembled previews.
- Validation evidence for seams, budgets, transforms, and instancing.
