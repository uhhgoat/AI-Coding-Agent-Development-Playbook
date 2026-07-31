# Modular Environment Construction

## Establish the module contract

Define before modeling:

- Blender units and Unity scale expectation;
- grid increment and allowed dimensions;
- local forward and up directions;
- pivot placement and snapping face;
- naming convention;
- material and texel-density strategy;
- whether the asset is a reusable module or a placed assembly.

Treat walls, corners, pillars, gates, floors, and trims as reusable modules. Treat an arena ring or room layout as an assembly of those modules.

## Pivots and dimensions

- Put pivots where designers will snap or rotate the module.
- Use exact numeric dimensions for grid-critical surfaces.
- Keep decorative overhangs from silently changing logical module dimensions.
- Render orthographic views with a scale reference for review.

## Repetition choices

- Use linked duplicates or collection instances when repeated objects should share source data.
- Use independent copies when a piece needs unique geometry or UV edits.
- Use Array for linear repetition with inspectable count and spacing.
- Use Curve for controlled arcs only after confirming deformation axis, transforms, curve tilt, and radius.
- Use Geometry Nodes when variation or rule-driven placement materially improves the workflow; expose the important controls.

For a repeated piece positioned from a contact plane, such as a merlon on a
parapet, put the source pivot on that plane before creating linked copies.
Applying source location after copies exist can shift every shared mesh in a
surprising way; record the source pivot and the placed bottom/top elevations
as separate evidence.

## Modules versus assemblies

Do not join a complete environment early.

- Keep modules individually inspectable and exportable.
- Build preview assemblies in a separate collection.
- Use instances to exercise corner joins, repeating spans, stairs, gates, and elevation changes.
- Preserve a small seam test that reveals gaps, overlaps, normal discontinuities, and texture-scale changes.

## Surface detail

- Prefer reusable trim, decal, normal, and material systems over unique high-poly geometry for small repeated detail.
- Keep silhouette-defining damage or ornament in geometry when it matters at gameplay distance.
- Parameterize procedural variation with deterministic seeds.
- Ensure procedural material scale is consistent across differently sized modules.

## Tower and wall-walk interfaces

Treat a tower as both an asset and a junction in a fortification kit.

- Model an upper door as a true opening with a measurable threshold, not as a
  leaf pasted onto the exterior.
- Expose a landing or wall-walk socket with width, elevation, forward axis,
  and snapping face. Support an exterior landing with corbels, brackets, or
  another construction-readable load path.
- Keep the tower shell hollow when interior access or an opening reveal is
  part of the claim, even when interior rooms and stairs are deferred.
- Separate parapet, deck, and merlon responsibilities. Keep one merlon source
  linked across the circular placement and validate bottom/top elevation after
  rotation.
- State whether a door leads to a modeled interior, a future curtain wall, or
  only a placeholder connection. Do not imply complete circulation from an
  unsupported floating doorway.

## Collision and LOD

Collision and LOD are explicit deliverables, not automatic side effects.

- Define whether Unity will generate collision or Blender will author it.
- Keep authored collision simple, closed, named, and separate from render geometry.
- Define LOD naming and thresholds in the Unity-side asset contract.
- Validate pivots, bounds, and material slots on every exported LOD.

## Review views

At minimum produce:

- orthographic front, side, and top views with a scale reference;
- a perspective assembly preview;
- a seam or corner close-up;
- a simple material-scale view;
- wireframe or topology evidence when geometry quality matters.
