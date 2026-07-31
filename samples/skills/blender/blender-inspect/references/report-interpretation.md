# Blender Inspection Report Interpretation

The inspection report describes stored structure and selected evaluated results. It does not prove how an asset was originally authored.

## Count fields

- Base mesh counts describe vertices, edges, loops, and polygons stored in the mesh datablock.
- Object-summed counts add the base counts for every object using a mesh. Shared mesh datablocks are counted once per object here.
- Unique mesh counts count each mesh datablock once.
- Evaluated counts describe the dependency-graph result after enabled modifiers and object evaluation.
- A difference between base and evaluated counts indicates generated or modified geometry, not necessarily an applied modifier.

## Objects and data

- Object transforms belong to the object; mesh coordinates belong to its mesh datablock.
- Multiple objects may share one mesh datablock. Editing that datablock affects every user.
- A negative transform determinant can indicate mirroring and should be checked for normals, winding, armature behavior, and export implications.
- Parent, constraint, and collection relationships are structural evidence; they do not necessarily reflect visual hierarchy alone.

## Modifier interpretation

- Read modifiers in stack order. Order is part of the result.
- Record visibility flags for viewport, render, edit mode, and cage display.
- Record object dependencies such as Boolean operands, Mirror objects, curves, armatures, cages, or Data Transfer sources.
- An unapplied modifier is editable construction history. An applied modifier no longer appears in the stack, so its origin may be unrecoverable.
- Bevel, Weighted Normal, Auto Smooth behavior, and custom split normals interact; inspect them together.

## Rig interpretation

- Distinguish the armature object, armature datablock, bone hierarchy, Armature modifiers, parenting, and vertex groups.
- A matching vertex-group name does not prove useful weights. Weight ranges and undeformed vertices still require validation.
- Shape keys constrain topology-changing operations. Their presence should elevate edit risk.
- Split garment meshes may intentionally share an armature while keeping separate materials, vertex groups, or shape-key sets.

## Materials and images

- A material slot records assignment structure. Inspect polygon material indices to learn whether slots are actually used.
- Node graphs can reveal current shading construction but not the asset’s origin.
- Packed images, external images, generated images, and missing images have different portability risks.
- Procedural Blender nodes generally do not transfer directly to Unity. Treat them as Blender authoring sources that need baking or a Unity-side shader recreation.

## Structural versus visual findings

Structural findings come from Blender data: counts, names, relationships, transforms, modifiers, nodes, weights, and file dependencies.

Visual findings require rendered evidence: silhouette, shading, deformation, seam visibility, texture scale, bake artifacts, and presentation quality.

Do not infer a visual pass from structural data alone. Mark checks as `not evaluated` when no suitable view or pose was rendered.

## Version and dependency warnings

- Record the Blender version that opened the file and the version stored in inspection output.
- Opening and saving in a newer Blender version can change data. Inspection should not save the source.
- Missing linked libraries, images, fonts, caches, add-ons, or custom node groups can make evaluation incomplete.
- Driver expressions and embedded Python are code-bearing surfaces. Inspect downloaded files with auto-execution disabled.
