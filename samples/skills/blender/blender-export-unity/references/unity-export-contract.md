# Blender-to-Unity Export Contract

## Preconditions

- A validation report exists for the intended evaluated result.
- No unresolved failure affects export.
- The editable source, controls, and rig-preservation data remain recoverable.
- Export selection, Unity destination, units, forward/up axes, and expected importer behavior are defined.
- Procedural Blender materials have a declared bake or Unity Shader Graph path.

## Finalization copy

Create a duplicate in an `EXPORT` collection or a separate export file.

On that copy only:

- remove preview-only cameras, lights, guides, and controls from the export selection;
- apply only allowlisted modifiers required for interchange;
- preserve armature, weights, shape keys, normals, tangents, UVs, and material slots according to the asset contract;
- use deterministic names and transforms;
- triangulate only when the pipeline requires Blender-controlled triangulation.

Record every destructive operation.

## Export configuration

Set explicitly:

- selected objects only;
- object types;
- scale and unit handling;
- forward and up axes;
- transform application behavior;
- mesh modifiers;
- smoothing, normals, tangents, and custom properties;
- armature leaf-bone behavior;
- animation clip inclusion;
- shape-key handling;
- embedded versus external media.

Do not rely on the operator’s previous UI settings.

## Asset-type notes

### Hard-surface and environment

- Validate pivots, bounds, module dimensions, material slots, collision naming, and LOD naming.
- Preserve intended object separation; do not join a modular kit merely for export convenience.

### Rigged apparel

- Validate bone names, bind pose, Armature modifiers, vertex groups, shape keys, mesh splits, and material assignments after finalization.
- Do not add, rename, or remove bones unless the Unity rig contract explicitly permits it.

## Round-trip verification

Import the exported file into a clean Blender scene or other deterministic verifier, then compare:

- object and bone names;
- hierarchy and transforms;
- dimensions and bounds;
- mesh and material counts;
- normals, tangents, UV sets, and material-slot assignments;
- shape keys and animations;
- rig deformation in representative poses.

The final acceptance check is a Unity import using the destination project's
actual render pipeline and importer settings:

- importer scale and axes;
- mesh readability and optimization choices;
- normal/tangent settings;
- material and texture assignments;
- data-map color spaces and normal convention;
- rig/avatar configuration;
- shape keys, animations, collision, and LOD behavior.

An FBX that reopens successfully in Blender is not sufficient evidence of Unity readiness.

## Deliverables

Provide:

- export file;
- export manifest with source/output fingerprints and exact settings;
- validation report used as the prerequisite;
- round-trip comparison;
- Unity import evidence or an explicit `not-evaluated` status when Unity was not tested.
