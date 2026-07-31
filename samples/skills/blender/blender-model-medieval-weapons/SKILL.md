---
name: blender-model-medieval-weapons
description: Model staged medieval or fantasy melee weapons in Blender with reference-calibrated profiles, explicit cross-sections, plausible haft/tang/socket assembly, controlled edge geometry, grip pivots, and style-aware proportions. Use for swords, axes, polearms, maces, war hammers, shields, or matching weapon sets before surfacing, baking, rig attachment, or game-engine export.
---

# Blender Model Medieval Weapons

Make the weapon's silhouette, cross-section, assembly, and handling proportions
agree before adding decoration.

## Workflow

1. Read [the shared Blender contract](../blender-validate-asset/references/shared-contract.md),
   [the style skill](../blender-define-asset-style/SKILL.md),
   [the hard-surface skill](../blender-model-hard-surface/SKILL.md),
   [the weapon workflow](references/weapon-construction.md), and
   [the research ledger](references/research-sources.md).
2. Classify the target as historically grounded, historically inspired,
   grounded fantasy, heroic, or toon-readable. Record any claim of historical
   accuracy as a separate evidence requirement.
3. Recap every reference before geometry: view and perspective, real versus
   apparent symmetry, total length, component ratios, decisive silhouette
   points, inferred depth, and unknown construction.
4. Establish local forward/up/side axes, the centerline, intended grip point,
   pivot, and destination-project scale.
5. Block out total length, balance of visual mass, head/blade reach, grip
   length, and handling clearance with simple components.
6. Build the primary profile from a calibrated image or deliberate dimensions.
   Build the cross-section independently; a convincing side silhouette does
   not determine thickness, taper, fuller, ridge, eye, socket, or edge wedge.
7. Separate functional parts while iterating: blade or striking head,
   sharpened edge, tang/eye/socket, haft, guard, grip, pommel/poll, langets,
   straps, rivets, wraps, and decoration as applicable.
8. Use Mirror only for real object-space symmetry. Use Array, radial object
   offset, or Geometry Nodes for repeated flanges, studs, or wrap segments
   while retaining the source element and controls.
9. Test construction: load path, attachment, grip clearance, edge direction,
   thickness, intersections, and whether the modeled assembly could plausibly
   be manufactured and held under the chosen style contract.
10. Save blockout, construction, and detail stages. Render the calibrated
    profile, opposite side, edge-on, top/bottom, three-quarter, in-hand proxy,
    and gameplay-distance views.
11. Continue reversible correction passes until no high-impact silhouette,
    proportion, point, cross-section, assembly, or symmetry discrepancy
    remains.
12. Assign only simple material roles during modeling. Route destination-owned
    wood, steel, iron, leather, wear, bakes, validation, and engine export
    through the relevant material, bake, validation, and export skills.

## Guardrails

- Do not reproduce perspective distortion as object-space asymmetry.
- Do not infer hidden thickness from one image without labelling it.
- Do not use one full-width slab plus a thin cosmetic edge when the intended
  cross-section is a blade wedge.
- Do not let a broad Bevel erase a requested tip, horn, beard, or cutting-edge
  terminal.
- Do not float an axe, hammer, or polearm head around a haft; model an eye,
  socket, straps, tang, wedge, or declared fantasy attachment.
- Do not call an oversized head, shortened haft, or enlarged hardware
  realistic because its materials look realistic.
- Do not model maker marks, etching, scratches, or painted graphics as deep
  relief unless the reference proves meaningful depth.
- Do not claim historical accuracy from a Blender tutorial alone.

## Deliverables

- Staged `.blend` files with semantic weapon components and editable controls.
- Style contract, dimension/ratio table, reference calibration, operation
  manifest, and material-role manifest.
- Construction note covering cross-section, edge, tang/eye/socket, grip,
  attachment, pivot, local axes, and inferred features.
- Fixed multiview, reference overlay, edge-on, in-hand proxy, topology, and
  gameplay-distance previews.
- Validation and iteration records with separate reference-fidelity,
  construction-plausibility, historical-evidence, and surface-status claims.
