---
name: blender-export-unity
description: Finalize approved Blender stages into Unity-ready exports using disposable duplicates, allowlisted modifier application, explicit axes/scale, selected-object export, and round-trip comparison. Use only after modeling, rigging, materials, texture bakes, and validation are accepted and an FBX or other Unity-facing artifact is requested.
---

# Blender Export Unity

Export is a guarded write boundary. Apply destructive finalization only to a
disposable duplicate linked to an approved source stage.

## Workflow

1. Read [the shared Blender contract](../blender-validate-asset/references/shared-contract.md)
   and [the Unity export contract](references/unity-export-contract.md).
2. Require a passing `validation.json`, approved source-stage path, intended
   export selection, material/bake manifests, scale, axes, animation policy,
   and output path.
3. Create `finalize.blend` from the approved stage without replacing it.
4. Duplicate only approved export objects into an explicit `EXPORT` collection.
5. Apply only allowlisted modifiers and transforms on those duplicates.
6. Reinspect geometry, rigs, shape keys, materials, and image references.
7. Export selected objects with recorded settings to a new artifact path.
8. Reimport the artifact into a disposable Blender file.
9. Compare object hierarchy, dimensions, transforms, triangle counts, normals,
   rig/bones, material slots, and expected animation data.
10. Write `export-manifest.json`, preserve logs/previews, and report any Unity
    import checks still required.

## Guardrails

- Never export implicitly from an ordinary modeling/material request.
- Never apply modifiers or transforms to the accepted source stage.
- Stop when validation is missing, stale, or contains unresolved failures.
- Stop when an armature/shape-key modifier is not explicitly allowlisted.
- Do not assume Blender procedural nodes transfer to Unity; require baked maps
  or an explicitly planned Unity shader.
- Do not overwrite an existing export without explicit authorization.

## Deliverables

- `finalize.blend`, exported artifact, and round-trip inspection file.
- Export manifest containing source-stage lineage and exact settings.
- Pre/post counts, fixed previews, and remaining Unity import actions.
