---
name: blender-model-armor
description: Model staged body-worn armor in Blender around a declared body-fit envelope, with functional plate segmentation, believable overlaps, usable openings, and style-controlled proportions and topology. Use for grounded, historical-fantasy, low-poly, heroic, or toon armor including cuirasses, pauldrons, helmets, belts, faulds, cuisses, greaves, sabatons, or matching sets before rig fitting, surfacing, baking, or engine export.
---

# Blender Model Armor

Treat low polygon count, toon shape language, body fit, articulation, and
historical plausibility as separate decisions.

## Workflow

1. Read [the shared Blender contract](../blender-validate-asset/references/shared-contract.md),
   [the style skill](../blender-define-asset-style/SKILL.md),
   [the hard-surface skill](../blender-model-hard-surface/SKILL.md),
   [the armor workflow](references/armor-construction.md), and
   [the research ledger](references/research-sources.md).
2. Create or update `style-contract.json`. Select a separate style skill:
   `blender-style-grounded-realism` or `blender-style-clean-stylized`.
   Add `blender-model-low-poly-assets` only when an evaluated geometry budget
   is part of the task. Record reference fidelity, proportions, topology,
   construction plausibility, surface frequency, and review distance
   independently.
3. Establish a scaled body-fit reference before armor geometry. Prefer the
   target character; otherwise create a clearly labelled generic static body
   cage with declared measurements and clearance.
4. Break the design into functional zones: underlayer, torso shell, neck and
   arm openings, shoulder articulation, waist closure, hip defense, thigh,
   knee, shin, foot, straps, and hardware as applicable.
5. Block out the body-following primary masses with the smallest topology that
   preserves the required silhouette, cross-sections, openings, and intended
   facets. Match the base topology to the anatomy: use radial sphere/egg or
   revolved rings for cranial bowls and limb shells, not a rectangular
   extrusion whose corners survive smoothing. Mirror only genuinely bilateral
   forms.
6. Build close-fitting plates from controlled surfaces. Use Shrinkwrap,
   Solidify, Bevel, and normal treatment only in an order justified by the
   source surface and intended final facets.
7. Build articulated lames as successive plates along the joint or limb axis.
   Preserve the opening and overlap direction; do not create several
   coincident full-size shells.
8. Make straps, belts, collars, and trim follow the complete surface they bind.
   Confirm their side and back continuity before adding buckles or rivets.
9. Keep broad planes and silhouette breaks intentional at every budget. Spend
   polygons at joints, curved openings, sharp terminals, and profile changes
   rather than distributing them uniformly.
10. Save and review preserved blockout, construction, and detail stages.
    Render clean front, back, side, three-quarter, body-overlay, and X-ray fit
    views. Include an intended gameplay-distance view.
11. Run the hard-surface and style validation checks. Continue autonomous,
    reversible correction passes until no known high-impact fit, silhouette,
    layer-order, or construction error remains.
12. Route known-character weighting and pose sweeps through
    `blender-fit-rigged-apparel`. Route materials, bakes, final validation, and
    export through their dedicated skills.

## Guardrails

- Do not infer toon proportions from a low polygon budget.
- Do not call automatic Decimate output a designed low-poly result.
- Do not use a rounded box as a torso merely because it clears the body.
- Do not treat smooth shading, bevel, weighted normals, or subdivision as a
  substitute for anatomy-following shell geometry. If grazing-light,
  silhouette, or wireframe evidence still reads as a box or planar end cap,
  rebuild the base surface.
- Do not close or substantially occupy the arm, neck, waist, hip, knee, or
  ankle opening with decorative plates.
- Do not model shoulder lames as a vertical pile of near-identical shells.
- Do not model a belt as a front plaque with hidden or missing side/back
  continuation.
- Do not add subdivision merely to remove all visible faceting when the style
  contract calls for broad planes, and do not preserve arbitrary facets when
  grounded curvature is the target.
- Do not claim pose-safe fit from a neutral silhouette or static body cage.
- Do not claim historical accuracy without appropriate historical sources.

## Deliverables

- Preserved `.blend` stages with `BODY_FIT_REFERENCE`, `SOURCE`, `CONTROLS`,
  `OUTPUT`, and `PREVIEW` collections as applicable.
- Style contract, body-envelope dimensions, shell/clearance targets, operation
  manifest, and source-provenance notes.
- Component inventory naming each plate's protected region, overlap direction,
  attachment assumption, and material role.
- Clean, overlay, X-ray, topology, and gameplay-distance previews.
- Validation and iteration records with fit class, known limitations, and the
  explicit boundary between static modeling and later rig fitting.
