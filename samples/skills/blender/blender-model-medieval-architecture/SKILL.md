---
name: blender-model-medieval-architecture
description: Build stylized or grounded medieval houses, castle kits, fortifications, and village assemblies in Blender from a declared modular grammar, human scale, structural layers, reusable variants, and material-scale rules. Use for timber houses, cottages, keeps, towers, gates, curtain walls, battlements, roofs, stairs, ruins, or medieval settlement kits before surfacing, baking, collision, LOD, and game-engine export.
---

# Blender Model Medieval Architecture

Treat a building, a modular kit, and an assembled settlement or castle as
different artifacts with different validation needs.

## Workflow

1. Read [the shared Blender contract](../blender-validate-asset/references/shared-contract.md),
   [the style skill](../blender-define-asset-style/SKILL.md),
   [the environment skill](../blender-model-environment/SKILL.md),
   [the medieval architecture workflow](references/medieval-architecture.md),
   and [the research ledger](references/research-sources.md).
2. Define the target: one hero building, reusable kit, playable assembly,
   exterior shell, or exterior-plus-interior. Record style, reference region
   and period if known, historical-confidence limits, camera distance, and
   runtime budget.
3. Establish units, human-scale proxy, floor heights, wall thickness, grid,
   pivots, axes, snapping faces, material scale, collision intent, and LOD
   intent.
4. Build a structural blockout before decoration. For houses, establish
   footprint, floors, wall masses, roof pitch, ridge, openings, and chimney.
   For castles, establish terrain relation, circulation, wall runs, towers,
   gates, parapets, stairs, and playable widths.
5. Define the kit grammar and allowed dimensions. Separate structural modules,
   trims, openings, roof parts, hero parts, damage variants, props, collision,
   and assemblies into semantic collections.
6. Author and validate one wall bay, corner, opening, floor/roof transition,
   and elevation change before multiplying the kit.
7. Use linked data, collection instances, retained Arrays, curves, or exposed
   Geometry Nodes for intentional repetition. Add deterministic variants where
   repetition becomes visually obvious.
8. Keep construction readable: timber frame and infill, roof support and
   covering, masonry mass and openings, parapet and stair access, gate and
   tower junctions. Stylization may bend forms but should not create accidental
   floating or unsupported parts.
9. Decide detail by screen scale. Keep silhouette, eaves, roof courses,
   crenellations, major beams, and large damage in geometry; route mortar,
   grain, pits, small cracks, soot, moss, and paint wear to materials, decals,
   or bakes when appropriate.
10. Build an `ASSET_ZOO` and seam-test assembly before the hero layout. Test
    mirrored/rotated corners, repeated spans, roof joins, stairs, gates,
    elevation changes, interiors if required, and collision clearances.
11. Save and review blockout, kit, and assembly stages. Render module
    orthographics, a scale view, seam close-ups, rooftop views, street/player
    views, and a full assembly.
12. Continue autonomous correction passes until no high-impact scale,
    silhouette, support, circulation, seam, repetition, or modularity error
    remains. Route surfaces, bakes, collision/LOD approval, final validation,
    and export through their dedicated skills.

## Guardrails

- Do not detail one facade before footprint, height, roof, openings, and
  circulation work from multiple views.
- Do not treat decorative overhangs as logical module dimensions.
- Do not join a whole house, castle, or village into one opaque authoring mesh.
- Do not use random distortion as a substitute for designed stylization.
- Do not make every timber, stone, tile, or crenellation unique; author a small
  controlled variation set.
- Do not use a shader to fake silhouette-critical roof tiles, thatch edges,
  battlements, beams, or damage.
- Do not add interiors, destructibility, collision, or LODs merely because an
  exterior render exists; each is an explicit deliverable.
- Do not claim a fantasy arrangement is historically accurate without
  appropriate architectural evidence.

## Deliverables

- Preserved `.blend` stages with `MODULES`, `VARIANTS`, `TRIMS`, `HERO`,
  `ASSEMBLIES`, `ASSET_ZOO`, `COLLISION`, `LOD`, and `PREVIEW` collections as
  applicable.
- Style contract, module grammar, dimension/pivot manifest, structural and
  circulation notes, material-role plan, and source provenance.
- Isolated module, scale, seam, roof, street/player, and assembly previews.
- Validation and iteration records covering modular fit, structural reading,
  repetition, playable clearance, evaluated budgets, and known historical or
  hidden-construction limits.
