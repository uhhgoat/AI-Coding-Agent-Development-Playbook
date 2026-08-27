# Hard-Surface Modifier Stack Patterns

Modifier order is an authored decision. Build and validate the stack from the intended form-generation sequence.

## Contents

- [Transform discipline](#transform-discipline)
- [Common stack shapes](#common-stack-shapes)
- [Boolean controls](#boolean-controls)
- [Bevel and normals](#bevel-and-normals)
- [Array, mirror, and curve dependencies](#array-mirror-and-curve-dependencies)
- [Finalization](#finalization)

## Transform discipline

- Establish dimensions, origin, and object scale before bevel widths, array offsets, mirror tolerances, or procedural texture scale depend on them.
- Apply scale only when doing so is safe for the current stage and dependencies.
- Keep a recoverable source or construction copy before destructive application.
- Use explicit object-space versus world-space assumptions in scripts.

## Common stack shapes

### Symmetric manufactured part

1. Base low-poly form
2. Mirror
3. Boolean features
4. Bevel
5. Normal treatment

Place topology-generating operations before bevel when the bevel must affect their new edges. Exceptions are valid but must be intentional.

### Repeated element

1. Source element
2. Array or Geometry Nodes repetition
3. Curve deformation when needed
4. Weld/merge only when a continuous mesh is required
5. Bevel and normal treatment appropriate to the final form

Keep the source element accessible. Do not apply repetition merely to make the object look finished.

### Panel or shell

1. Surface form
2. Mirror
3. Solidify
4. Boolean openings or panel lines
5. Bevel
6. Normal treatment

Check whether Solidify should occur before or after openings; the result and topology differ.

### Anatomy-following rigid shell

1. Choose a primitive whose loop flow already follows the target volume:
   UV-sphere/egg rings for a cranial bowl, revolved rings for a limb, or a
   sparse body-following patch for a torso plate.
2. Establish the complete curved volume before cutting or deforming openings.
3. Reshape entire rings or weighted vertex regions to control breadth,
   flattening, asymmetry, and local extensions while preserving continuous
   curvature.
4. Build paired inner/outer surfaces or Solidify only after the source surface
   and opening boundary are stable.
5. Add edge rolls, hardware, bevel, and normal treatment after the shell passes
   silhouette, wireframe, and grazing-light review.

A rounded extrusion and an anatomy-following shell may share the same outer
dimensions but not the same curvature. Do not preserve planar end-cap topology
and expect subdivision or normals to create the missing volume.

### Planar blade or weapon head

1. Establish the asset's local axes and decide whether apparent asymmetry is
   object-space design or camera perspective. For a symmetric head shown in a
   three-quarter view, author one canonical side and mirror it.
2. Read the style contract before choosing reach, thickness, curvature,
   socket scale, hardware scale, or bevel width. These construction decisions
   establish style before materials do.
3. Infer a clean two-dimensional silhouette from the reference.
4. Use sampled curves for intentional arcs rather than tracing every image
   irregularity into dense topology.
5. Extrude the profile to an explicit physical thickness.
6. Keep a separate cutting-edge insert when it improves editability, material
   separation, or later bake control.
7. Add a bevel sized to the declared style and physical scale after the
   profile and thickness are stable.
8. Validate front, back, edge-on, perspective, and intended-distance views.
   When symmetry is an
   acceptance requirement, also compare mirrored base and evaluated vertex
   coordinates within an explicit tolerance.

Keep the dark blade body and bright edge as separate closed components during
early iteration when their shapes are still changing. Decide whether they
must be joined, welded, or baked together only at finalization. A visually
correct front silhouette is insufficient; the edge-on view must confirm
usable blade, socket, grip, and haft thickness.

Treat upper and lower cutting-edge terminals as explicit silhouette
landmarks. Do not let a broad Bevel erase a requested horn or beard point.
Compare the evaluated terminal coordinates with the authored base landmark;
a visually small bevel can still shorten a sword or spear point outside its
dimension tolerance.
When the edge is a tapered wedge, stop the blade body at the wedge's inner
seam and let the edge component own the outer arc. A full-width blade body
behind a thinner wedge will occlude the edge in front/back views and does not
represent the intended cross-section.

## Boolean controls

- Put cutters in a dedicated `CONTROLS` collection and name them for the feature they create.
- Make solver choice, operand type, and self-intersection assumptions explicit.
- Avoid nearly coplanar cutter surfaces and microscopic overlaps.
- Validate non-manifold edges, interior faces, thin slivers, and shading after evaluation.
- Keep cutters hidden from render/export without deleting them.

For arched openings through a faceted cylindrical shell, do not assume a clean
render proves clean evaluated topology. A cutter vertex exactly on the shell's
centerline or a radial segment boundary can produce a microscopic zero-area
face. Preserve the cutter, enable modifiers incrementally, and report the
first modifier that introduces a degeneracy. Offset the intersection
topologically—an odd arch sample count can avoid a centerline apex—without
silently changing the declared opening dimensions.

Be cautious with a global Bevel after several shell openings. If it produces
slivers, keep the main shell smoothly shaded and move visible edge softness to
separate dressed frames, trims, or local bevel-weighted regions.

## Bevel and normals

- Define whether bevel width is absolute, percentage-based, or driven by bevel weights/attributes.
- Set segment counts appropriate to the target asset and preview distance.
- Do not assume a Weighted Normal modifier is always needed. Validate shading with the active Blender version and intended export path.
- Record custom split normals and sharp-edge strategy because export can change them.

## Array, mirror, and curve dependencies

- Mirror merge distance depends on object-space scale and centerline placement.
- Array relative offsets depend on source bounds; constant offsets are more stable when exact module spacing matters.
- Curve deformation depends on deformation axis, origin, transforms, and curve tilt/radius.
- A bevelled curve that looks capped can still become an open mesh after
  dependency-graph evaluation or `new_from_object` conversion. After
  conversion, count connected boundary components on the actual mesh. For an
  intended closed rail or swept beam, fill each endpoint loop independently,
  then validate base and evaluated non-manifold edges. Do not assume
  `use_fill_caps`, one global holes-fill operation, or a clean render proves
  that both ends closed.
- Shared mesh data and linked duplicates reduce memory but propagate edits. Choose this deliberately.

## Finalization

Apply only the modifiers required by the downstream interchange format or tool.

Before applying:

- duplicate into an `EXPORT` collection or file;
- preserve the editable source and controls;
- record the original stack and settings;
- validate the evaluated result;
- ensure shape keys, rigs, or data links will not be invalidated.
