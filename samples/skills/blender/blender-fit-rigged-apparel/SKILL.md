---
name: blender-fit-rigged-apparel
description: Fit, split, mirror, or diagnose armature-bound Blender apparel while preserving rigs, bones, weights, vertex groups, shape keys, transforms, and deformation behavior. Use for Character Creator or other known character rigs, armor fitting, body-region splits, weight transfer, clipping diagnosis, accessory bones, or mirrored-part correction.
---

# Blender Fit Rigged Apparel

Treat rigged apparel editing as a high-risk preservation workflow. Never make
the only source file the working file.

## Workflow

1. Read [the shared Blender contract](../blender-validate-asset/references/shared-contract.md)
   and [rig-preservation requirements](references/rig-preservation.md).
2. Inspect the source and create a pre-change manifest of armatures, bones,
   parents, Armature modifiers, vertex groups, shape keys, mesh counts,
   transforms, and material slots.
3. Confirm the rig is known and the requested operation has an explicit
   preservation strategy.
4. Create a staged copy. Never apply object transforms or modifiers
   reflexively on armature-bound or shape-key meshes.
5. Perform one bounded fit, split, mirror, transfer, or cleanup operation.
6. Preserve or deliberately map every required bone, vertex group, shape key,
   and modifier target.
7. Reinspect and compare the pre/post manifests.
8. Render neutral and representative pose sweeps from multiple views to check
   clipping, seams, normals, and deformation.
9. Record visual limitations separately from structural preservation.
10. Stop before export until `blender-validate-asset` passes.

## Generated-source boundary

- Use imported or AI-generated apparel only as visual coverage/fit reference
  and as input to Blender-side fitting diagnostics unless its provenance
  establishes a stronger authoring claim.
- Do not reproduce generated topology, segmentation, UVs, material graphs, or
  textures as project pipeline patterns.
- Treat modifiers, armature binding, rigs, weights, shape keys, mesh splits,
  transforms, and deformation as pipeline-valid evidence.

## Stop Conditions

- Unknown or mismatched armature.
- Missing required bones, groups, shape keys, or modifier targets.
- Negative determinant or mirrored topology whose equivalence is unproven.
- Shape-key or weight loss, unexplained vertex-count changes, or invalid seams.
- No representative poses with which to evaluate deformation.
