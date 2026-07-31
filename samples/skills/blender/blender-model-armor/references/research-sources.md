# Armor Research Ledger

Research passes: `2026-07-28`, `2026-07-29`.

Use this ledger to understand transferable workflows. Do not reproduce a
source model, topology, texture, or tutorial node graph unless its license and
the current task explicitly permit that use.

## Primary and instructional sources

- [Blender Studio: Stylized Character Workflow](https://studio.blender.org/training/stylized-character-workflow/5d5c286ddbaeb3f9fb86e610/)
  separates goal definition, body and outfit basemeshes, stylization,
  retopology, UVs, textures, and turntable review. It also provides lesson
  `.blend` files. Transferable lesson: design the body/outfit relationship
  before polishing isolated clothing or armor surfaces.
- [Blender Studio: Low Poly Character Creation](https://studio.blender.org/training/low-poly-character-creation/chapter/5978699a8119172dda22c7cb/)
  shows a staged high/low workflow, low-poly body and clothing, UVs, bakes, and
  props. The timelapses have no narration, so treat them as process evidence,
  not complete instructions.
- [Behind the Scenes: The Cartoon Knight](https://www.blendernation.com/2020/06/19/behind-the-scenes-the-cartoon-knight/)
  documents direct poly modeling for topology and budget control, a duplicated
  detailed version, UVs, normal/AO baking, material separation, and the need to
  understand rig deformation.
- [Blender Manual: Shrinkwrap Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/shrinkwrap.html)
  is the authority for projection methods, target behavior, limits, and
  offsets.
- [Blender Manual: Solidify Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/solidify.html)
  is the authority for shell thickness, offsets, boundary behavior, and scale
  caveats.
- [Blender Manual: Mirror Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/mirror.html)
  is the authority for mirror axes, clipping, bisect, merge, and mirror-object
  behavior.
- [Blender Manual: Bevel Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html)
  is the authority for non-destructive edge treatment, limits, profiles, and
  shading options.
- [Blender Manual: Mesh Primitives](https://docs.blender.org/manual/en/latest/modeling/meshes/primitives.html)
  documents UV spheres as quad-ring meshes with pole triangle fans and
  distinguishes their latitude/longitude layout from the more isotropic
  Icosphere. Transferable lesson: prefer UV-sphere rings when an
  anatomy-following shell needs controlled horizontal loop deformation.
- [Blender Manual: Loop Cut and Slide](https://docs.blender.org/manual/en/5.0/modeling/meshes/editing/edge/loopcut_slide.html)
  documents adding parallel loops, sliding their position, and applying
  smoothness to preserve curvature. Transferable lesson: add or redistribute
  loops where silhouette or curvature changes rather than relying on uniform
  density.

## Downloadable structural samples

- [Fullplate Armor Knight by Luana Coppio](https://scoppio.itch.io/fullplate-armor-knight)
  is a small PSX-style low-poly/low-resolution character with a simple rig,
  `.blend`, textures, FBX, and GLB. The author labels it CC0 and states that no
  generative AI was used. It is a strong candidate for future licensed
  structural inspection.
- [RPG Low Poly Knight on OpenGameArt](https://opengameart.org/content/rpg-low-poly-knight)
  includes a downloadable `.blend` with removable armor, hair, and facial
  hair. It is offered under CC-BY 3.0 and CC-BY-SA 3.0; preserve attribution
  and do not silently mix license obligations.

Downloading a file does not make its authored topology the project default.
Fingerprint it, record the license and origin, open it with auto-execution
disabled, classify its evidence, and inspect it through `blender-inspect`.

## Findings adopted by this skill

- Low-poly style is designed through silhouette and plane placement, not a
  post-process Decimate modifier.
- Body and outfit/armor proportions must be reviewed together.
- Direct poly modeling can be preferable when exact topology and a small
  budget matter.
- A more detailed duplicate may be useful for normal/AO baking, but the low
  source remains recoverable.
- Static design and rig deformation are separate approval gates.
- Turntables and fixed multiview review reveal shading and proportion problems
  that a single hero image hides.
- A cranial plate should begin from radial sphere/egg or revolved loop flow.
  A smoothed longitudinal extrusion can remain visibly rectangular even when
  it is manifold and clears a head cage.
- Scripted `bmesh` or direct mesh generation permits deterministic
  vertex-by-vertex ring control; interactive selection granularity is not a
  blocker.

## Rights and exclusion rules

- Record author, URL, license, retrieval date, and any attribution obligation
  for every downloaded sample.
- Do not import or analyze assets marked `NoAI` for agent training, skill
  derivation, or automated reconstruction. A visible online image is not
  permission to use its underlying model.
- Do not treat marketplace display images as topology or rigging evidence.
- Do not redistribute paid or attribution-restricted project files.
- Extract general workflow principles in original wording; do not copy
  tutorial prose, node graphs, or proprietary assets.
