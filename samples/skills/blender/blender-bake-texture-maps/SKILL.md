---
name: blender-bake-texture-maps
description: Bake approved Blender geometry or procedural materials into validated game texture maps with explicit source/target pairing, UVs, cages, margins, color spaces, and channel metadata. Use for tangent or object-space normal maps, ambient occlusion, base color, roughness, metallic, height, ID/custom masks, or packed Unity texture outputs.
---

# Blender Bake Texture Maps

Treat baking as a guarded derivative step. Never let a bake mutate the only
approved modeling or material stage.

## Workflow

1. Read [the shared Blender contract](../blender-validate-asset/references/shared-contract.md)
   and [the bake contract](references/bake-contract.md).
2. Require approved source and target objects, UV map, texture set, resolution,
   margin, samples, cage/ray settings, bit depth, color space, normal
   convention, and channel layout.
3. Create a disposable bake stage and deterministic output directory.
4. Validate source/target pairing, transforms, normals, UV bounds/overlaps,
   material slots, and cage or ray distance before invoking a bake.
5. Create images with explicit dimensions, format, bit depth, and color space.
6. Bake one map at a time through Cycles and save it immediately to a new path.
7. Generate channel/contact-sheet previews and inspect seams, skew, gradients,
   projection misses, padding, and unexpected values.
8. Pack channels only after every source map passes independently.
9. Write `bake-manifest.json` with every input and setting required to repeat
   the bake.
10. Validate the intended normal/tangent convention through a Unity import
    test before making it a project default.

## Stop Conditions

- Ambiguous high/low or source/target pairing.
- Missing, unsuitable, or unexpectedly overlapping UVs.
- Missing cage or unsafe ray distance.
- Undefined tangent basis or normal-map orientation.
- Projection artifacts, insufficient padding, or unapproved texture budget.
- An output path would overwrite source textures or an approved bake.

## Deliverables

- Individual maps, optional approved packed maps, and checksums.
- Bake manifest and channel previews.
- Pass/warn/fail result with unresolved projection or Unity-import risks.
