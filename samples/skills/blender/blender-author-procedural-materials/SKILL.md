---
name: blender-author-procedural-materials
description: Author and reuse project-neutral, parameterized procedural Blender materials and node groups with explicit coordinates, physical scale, causal masks, style presets, and preview validation. Use for wood, forged or polished metal, leather, cloth, masonry, plaster, dirt, wear, moisture, color variation, normal/height response, or Blender-native shader workflows that must remain editable or later be baked for a game engine.
---

# Blender Author Procedural Materials

Author independent task/project-owned node graphs. Do not derive material
architecture from generated-model textures or copy a tutorial's final graph.

## Workflow

1. Read [the shared Blender contract](../blender-validate-asset/references/shared-contract.md)
   and [procedural-material guidance](references/procedural-materials.md).
   For armor, weapons, houses, castles, or medieval environments, also read
   [the medieval material recipes](references/medieval-material-recipes.md)
   and [the material research ledger](references/research-sources.md).
2. For style-sensitive work, read the asset `style-contract.json` created
   through `blender-define-asset-style`, then use
   `blender-style-grounded-realism` or `blender-style-clean-stylized`.
   Keep geometry style, material realism, and reference fidelity separate.
3. Define the material brief, physical scale, target objects, coordinate
   strategy, required exposed parameters, preview conditions, and target-engine
   path.
4. For wood, metal, leather, cloth, masonry, or plaster, read
   [the reusable node library](references/node-library.md). Append a group from
   the bundled `.blend` or generate a fresh library with the bundled script,
   then duplicate/version it before asset-specific edits.
5. Create named node groups for reusable layers and masks.
6. Keep coordinate, scale, color, roughness, metallic, normal/height, and mask
   responsibilities identifiable in the graph.
7. Connect one explicit Principled BSDF output path and label non-obvious
   nodes, frames, and parameters.
8. Separate material identity, object-scale structure, contact/use masks,
   optional damage/wear, and micro response. Do not let one Noise texture drive
   every channel.
9. Test the material on a standard preview object and an in-context asset at
   more than one scale and at the contract's intended viewing distance.
10. Render fixed neutral, grazing, representative, and close evidence views.
11. Write `material-manifest.json` with node groups, parameters, coordinates,
   assignments, Blender version, and provenance.
12. Run `blender-validate-asset` on node graphs, slots, images, and previews.
13. Use `blender-bake-texture-maps` when the target engine cannot consume the
    graph directly.

## Guardrails

- Do not silently depend on unpacked absolute-path images.
- Do not use generated coordinates when stable UV/object coordinates are
  required without documenting the choice.
- Do not hide scale corrections in arbitrary Mapping nodes; expose or record
  them.
- Do not copy generated-model UV layouts, node graphs, map resolutions, or
  channel conventions as the reusable architecture.
- Do not copy tutorial node graphs or paid material groups. Reconstruct the
  transferable process independently and record source influence.
- Keep visual complexity proportional to the eventual bake and runtime budget.
- Treat low-poly as a geometry budget, not a synonym for toon materials.
- Do not add high-frequency normals or scratches merely to make a stylized
  model sound realistic. Match the declared surface frequency and review
  distance.
- Do not use displacement for a silhouette-critical feature unless the render
  engine, subdivision, bake path, and target-engine result are explicitly
  validated.

## Deliverables

- Staged `.blend` containing named materials and reusable node groups.
- Material manifest and fixed-lighting previews.
- Explicit statement of whether the graph remains Blender-only, will be baked,
  or must be rebuilt in the target engine.
