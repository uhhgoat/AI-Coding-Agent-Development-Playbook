---
name: blender-style-grounded-realism
description: Apply a general-purpose grounded-realism style to Blender assets using realistic proportions, plausible construction, restrained physically legible materials, and performance-aware detail rather than hyperreal rendering. Use for armor, characters, weapons, props, vehicles, buildings, or environments that should feel believable and cohesive while remaining practical for real-time games.
---

# Blender Style Grounded Realism

Use this as a style layer over the relevant modeling or material skill.

## Contract

1. Read `style-contract.json` from `blender-define-asset-style`.
2. Set proportions to realistic or reference-measured unless the request names
   a specific controlled exaggeration.
3. Require plausible thickness, assembly, support, articulation, load path,
   openings, and manufacturing appropriate to the asset.
4. Preserve real-world scale. Label reference measurements, inferred hidden
   dimensions, and design choices separately.
5. Allocate topology to silhouette, curvature, joints, openings, cross-section,
   deformation, and stable shading. Low polygon count is acceptable when those
   reads survive; it is not permission for blocky or toon proportions.
6. Use restrained bevels at plausible physical widths. Keep edge quality
   consistent with camera distance and bake resolution.
7. Separate macro identity, characteristic mid structure, and subtle micro
   response in materials. Fine detail should usually affect roughness and
   normal more than Base Color.
8. Place wear by cause: contact, sharpening, handling, bending, moisture,
   ground proximity, soot, drainage, or manufacturing.
9. Review under neutral and grazing light at close, representative, and
   gameplay distance. Reduce detail that aliases, dominates, or disappears
   below the intended texel/mip budget.
10. Record intentional departures from physical realism. Do not relabel
    heroic, chunky, cute, or exaggerated geometry as grounded because its
    shader is realistic.

## Realistic, not hyperreal

- Favor coherent form and material identity over pore-level density.
- Do not add scratches, pits, pores, fuzz, or displacement merely because a
  close render can resolve them.
- Keep normals shallow unless the source surface genuinely has relief.
- Prefer a few causal masks over many independent noises.
- Stop increasing shader complexity when it will be baked below the feature's
  useful texel size or will not survive the target engine.
- Validate actual gameplay lighting and distance before adding more detail.

## Material starting point

Use the `GP_Grounded_*` presets from
`blender-author-procedural-materials`. Align material coordinates, then tune
species, manufacturing method, finish, age, scale, and causal masks for the
asset. The preset is a starting point, not a claim that the result is already
reference-matched.

## Deliverables

- Style contract with real-world scale, proportion, construction, material,
  frequency, wear, budget, and review-distance decisions.
- Fixed reference, orthographic, perspective, edge/grazing, and intended
  gameplay views.
- Separate geometry-fidelity, construction-plausibility, surface-realism, and
  performance findings.
- Explicit list of any stylized exceptions.
