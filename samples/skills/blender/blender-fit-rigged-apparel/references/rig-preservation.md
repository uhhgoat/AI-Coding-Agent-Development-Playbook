# Rigged Apparel Preservation Contract

Rigged apparel edits are high-risk because topology, weights, armature relationships, shape keys, and mesh splits can all affect deformation.

## Capture invariants before editing

Record:

- armature object and datablock names;
- bone names, hierarchy, deform flags, and rest transforms;
- mesh object names and parent relationships;
- Armature modifier targets and stack positions;
- vertex-group names and weight statistics;
- shape-key names, order, relative-key relationships, and vertex counts;
- material slots and polygon assignments;
- mesh datablock users and intentional splits;
- object transforms, dimensions, determinant, and unit assumptions.

Save this as the pre-edit manifest. Compare it to a post-edit manifest.

## Safe fitting sequence

1. Work on a copy.
2. Confirm the body and apparel use the intended rest pose and scale.
3. Fit broad volume before local detail.
4. Preserve seam and split boundaries intentionally.
5. Transfer or adjust weights only through an explicit source/target mapping.
6. Validate neutral pose and a representative pose sweep.
7. Compare manifests and investigate every unexpected difference.

## Mesh splits

Separate meshes may be intentional for:

- material or equipment swapping;
- rigid versus deforming pieces;
- different weight-transfer strategies;
- corrective shape keys;
- draw-call or authoring boundaries.

Do not join or split meshes without documenting the runtime reason. Joining can change material indices, shape-key compatibility, vertex groups, object transforms, and export paths.

## Shape keys

- Topology-changing modifiers and destructive edits are usually incompatible with existing shape keys.
- Never assume shape keys can be recreated from names alone.
- Keep vertex count and vertex order stable when preserving shape keys.
- Test every key at meaningful values and in combination where the asset relies on combinations.
- Treat lost relative-key relationships or changed basis data as failures.

## Weight transfer

- Choose the transfer source, mapping method, mix mode, and group-selection policy explicitly.
- Data Transfer results depend on spatial proximity, topology, transforms, and modifiers.
- Normalize and limit influences only when that matches the target rig/export contract.
- Check for unweighted vertices, unintended bone groups, extreme weights, and left/right leakage.
- Rigid armor pieces may need deliberate rigid weighting instead of surface interpolation.

## Pose sweep

Include poses that stress:

- shoulders and elbows;
- hips and knees;
- spine twist and bend;
- crouch or deep flexion;
- weapon-ready or combat silhouettes relevant to the asset;
- mirrored motion when asymmetry might hide a problem.

Render consistent angles and inspect clipping, collapse, stretching, rigid-part drift, seam separation, and normal artifacts. A neutral-pose fit is not sufficient evidence.

## Generated-source boundary

For AI-generated or third-party apparel, do not learn or reproduce its base
topology, UV construction, generated material graph, or source textures as the
project modeling method unless provenance explicitly permits that use.

It remains valid to preserve or study:

- armature and modifiers;
- vertex groups and weights;
- shape keys;
- Blender-side mesh splits;
- object transforms and fitting;
- Data Transfer or cleanup decisions added after generation.
