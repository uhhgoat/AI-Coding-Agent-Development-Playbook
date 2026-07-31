# Blender Asset Validation Checklist

Use the status values `pass`, `warn`, `fail`, and `not-evaluated`.

- `pass`: the check ran and met its defined criterion.
- `warn`: the result may be intentional but needs review.
- `fail`: the result violates the declared asset contract or blocks the next stage.
- `not-evaluated`: evidence or configuration was insufficient. This is not a pass.

## File and provenance

- Source fingerprint recorded and unchanged for read-only work.
- Blender version and external dependencies recorded.
- Asset origin classified as `pipeline-valid`, `reference-only`, or `unknown`.
- Missing images, libraries, fonts, caches, add-ons, node groups, and drivers reported.

## Geometry

- Object names, roles, transforms, dimensions, origins, determinant, and units match the contract.
- Base and evaluated mesh counts are recorded.
- Non-manifold edges, loose elements, degenerate faces, zero-area UVs, and invalid normals are checked.
- Material slots are used intentionally.
- Modifiers have valid dependencies, intended order, and expected visibility.
- Shared mesh datablocks and linked instances are intentional.
- Silhouette and shading are reviewed from fixed views.
- The current stage is compared with the preceding preserved stage; previews
  are inspected, not merely rendered.

## Style intent

- A versioned style contract exists when appearance is an acceptance
  criterion.
- Reference view, perspective strength, and object-space symmetry decisions
  are explicit.
- Reference fidelity, proportion/construction, shape language, material
  realism, and surface frequency are reported separately.
- Decisive dimensions, ratios, and landmarks are compared with their declared
  tolerance and evidence class.
- The primary impact element reads at the intended distance without
  accidentally distorting restrained elements.
- Macro, mid-frequency, and micro geometry/color/roughness/normal detail agree
  with the selected profile.
- A realistic material pass does not convert stylized proportions into a
  realistic-geometry pass.
- Human questions about appeal, realism, historical accuracy, or style fit
  remain `not-evaluated` until reviewed.
- The iteration log ranks discrepancies by impact and records evidence, fix,
  result, and residual limitation.
- Any unresolved high-impact mismatch prevents visual acceptance even when
  geometry and dependency checks pass.

## Calibrated image reference

- Source checksum, image dimensions, origin pixel, scale, and view axis are
  recorded.
- The reference image is packed and kept outside output/export hierarchies.
- Measured axes and inferred hidden dimensions are explicitly separated.
- Projected landmark distance is checked against an explicit meter tolerance.
- An aligned overlay and independent perspective/edge-on views are reviewed.
- Structural proximity does not automatically pass realism, historical
  accuracy, construction plausibility, or views the image does not constrain.
- For body-worn assets, body-reference provenance, world scale, shell
  thickness, sampled clearance zones, and fit-evidence class are recorded.
- Clean, flat silhouette-overlay, and side/three-quarter cage X-Ray views are
  inspected; neither a hidden cage nor a static clearance table alone passes
  fit.
- Generic-static-envelope, known-body-neutral, and known-body-pose-swept fit
  remain distinct claims.

## Modular environment

- Grid dimensions, pivots, snapping faces, and assembly seams pass.
- Array, Curve, instance, and Geometry Nodes controls remain inspectable.
- Collision and LOD deliverables are present or explicitly not required.
- Procedural material scale is consistent across modules.

## Stylized armor

- Low-poly budget and toon shape language are declared independently.
- Body-fit reference, inner shell, thickness, and clearance targets are
  recorded.
- Front, back, side, three-quarter, overlay, X-ray, wireframe, and
  gameplay-distance evidence is inspected.
- Torso form tracks chest, rib, side, back, and waist transitions rather than
  reading as a rounded box or unexplained inflated body.
- Arm, neck, waist, hip, knee, ankle, and foot openings remain usable.
- Shoulder and lower-body lames progress along the articulation axis, overlap
  consistently, and preserve the underlying aperture.
- Belts, collars, straps, and trims wrap their targets; front-only facades fail.
- Facets and segment density support silhouette and authored planes rather than
  arbitrary decimation.
- `generic-static-envelope`, `known-body-neutral`, and
  `known-body-pose-swept` remain distinct fit claims.

## Medieval weapons

- Total length, component ratios, local axes, grip point, and pivot match the
  contract.
- Reference projection and real object-space symmetry are explicit.
- Profile, opposite side, edge-on, top/bottom, three-quarter, and in-hand proxy
  views are inspected.
- Blade/head cross-sections, sharpened edge, distal or haft taper, and important
  points remain readable.
- Tang, eye, socket, langet, wedge, grip, guard, or other attachment logic is
  present or explicitly declared fantasy construction.
- A realistic surface does not upgrade heroic proportions to grounded
  construction or historical accuracy.
- Historical claims remain `not-evaluated` without appropriate authoritative
  evidence.

## Medieval architecture

- Artifact scope is explicit: hero building, kit, assembly, exterior shell, or
  playable interior.
- Human scale, floors, openings, stairs, wall thickness, roof, parapet, gate,
  and playable clearances meet the declared contract.
- Footprint, structural massing, roof support, timber/masonry logic, and
  circulation read before decorative detail.
- The asset zoo, seam test, and at least one alternate assembly validate the
  modular grammar.
- Repetition uses shared sources and controlled variants; deterministic
  controls remain inspectable.
- Geometry/material division preserves silhouette-critical roofs, beams,
  battlements, openings, and large damage.
- Interior, collision, LOD, damage, and historical-confidence status are
  explicit and not inferred from an exterior beauty render.

## Rigged apparel

- Bone hierarchy, Armature modifiers, parent relationships, and deform flags match the pre-edit manifest.
- Vertex groups, weight ranges, unweighted vertices, and influence limits are checked.
- Shape-key count, order, relationships, topology, and sample values match expectations.
- Mesh splits and material assignments remain intentional.
- Neutral pose and representative pose sweep are visually reviewed.

## Materials

- Material slots and polygon assignments are valid.
- Procedural material coordinate strategy, scale, exposed parameters, and output channels are documented.
- Compare each material and node group with its manifest-declared coordinate
  strategy; do not hard-code `object-local` when an assembly-relative,
  cylindrical, UV, or deliberately shared module space is documented.
- Require at least one meaningful metric control for a reusable physical
  surface, but accept explicit dimensions or frequencies such as
  `Block Width (m)`, `Course Height (m)`, or `Ring Frequency (1/m)` instead of
  requiring every group to expose one generic `Scale (1/m)` socket.
- Packed and external images are portable or intentionally referenced.
- Unity path is defined: baked textures, Shader Graph recreation, or both.

## Bakes

- Bake manifest is complete.
- Map dimensions, format, bit depth, color space, and semantic match the contract.
- Normal space and configured channel convention are recorded.
- Empty, flat, clipped, contaminated, or missing outputs fail.
- Seams, projection errors, margins, and Unity import behavior are reviewed.

## Export readiness

- Export selection is explicit.
- An editable source remains recoverable.
- Finalization occurs on a duplicate.
- Axes, scale, normals, tangents, animation, armature, materials, and object types are configured explicitly.
- Reimport or round-trip checks confirm names, hierarchy, bounds, transforms, mesh counts, materials, and rig behavior.

## Reporting

List failures first, then warnings, then passed checks. Include evidence paths and exact affected objects. Never mutate the asset while running the validation skill.
