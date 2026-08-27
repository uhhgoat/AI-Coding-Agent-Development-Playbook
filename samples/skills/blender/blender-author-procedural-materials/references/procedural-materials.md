# Procedural Material Authoring

## Contents

- [Define the material contract](#define-the-material-contract)
- [Coordinates and scale](#coordinates-and-scale)
- [Node-group design](#node-group-design)
- [Physically meaningful outputs](#physically-meaningful-outputs)
- [Style-scaled material response](#style-scaled-material-response)
- [Performance and maintainability](#performance-and-maintainability)
- [Realistic multi-scale surface patterns](#realistic-multi-scale-surface-patterns)
- [Blender-to-game-engine boundary](#blender-to-game-engine-boundary)
- [Generated-model boundary](#generated-model-boundary)

## Define the material contract

Record:

- intended surface and gameplay context;
- physical scale and reference dimensions;
- coordinate source and mapping space;
- exposed parameters and allowed ranges;
- Principled BSDF channels driven;
- preview lighting and color management;
- bake requirements and target-engine destination.

## Coordinates and scale

- Use UV coordinates when placement must be art-directed or exported predictably.
- Use object coordinates for stable object-local procedural detail.
- Use generated coordinates only when their bounds-dependent behavior is acceptable.
- World coordinates can align surfaces across objects but may make moved assets appear to slide through a texture.
- Apply or compensate for object scale so pattern size is measurable and consistent.

Expose a real-world or project-unit scale control when the material will be reused.

## Node-group design

- Put reusable logic in named node groups.
- Expose a small, meaningful interface: color, scale, roughness range, normal strength, wear amount, edge treatment, seed, and similar controls.
- Use clear node and socket names.
- Keep units and expected ranges in labels or documentation.
- Avoid hiding asset-specific object references inside a supposedly reusable group.
- Make deterministic noise or variation the default.

## Physically meaningful outputs

Connect through a Principled BSDF unless the effect needs a justified alternative.

- Base Color should avoid baked lighting.
- Roughness should stay within the material’s plausible range.
- Metallic should normally represent material identity rather than generic darkness.
- Height and normal detail need an explicit scale and strength.
- Alpha and emission require a documented target-engine shader path.

## Style-scaled material response

Read `style-contract.json` before choosing contrast, frequency, or normal
strength.

For a stylized heroic or toon-readable asset:

- use broad material and value blocks that reinforce the primary silhouette;
- keep roughness transitions legible and comparatively smooth;
- use sparse, selective scratches, pores, and pits;
- keep fine normal response restrained so it does not compete with the shape;
- use wear as a graphic cue, not uniform high-frequency noise.

For grounded reference-matched realism:

- combine coherent macro structure, characteristic mid-frequency pattern, and
  subtle micro roughness/normal response;
- keep every scale physically plausible for the asset;
- differentiate manufacturing and use, such as forged iron versus a polished
  cutting edge or growth rings versus weaker vessels;
- place wear where sharpening, contact, gripping, moisture, and grain direction
  would cause it.

Material realism supports geometry; it does not repair exaggerated
head-to-handle ratios, oversized hardware, implausible thickness, or simplified
construction. Report those axes separately.

## Performance and maintainability

- Prefer the simplest graph that produces the required visual result.
- Reuse intermediate calculations instead of duplicating large branches.
- Separate large-form breakup from fine normal detail.
- Keep preview-only nodes and controls out of production outputs.
- Provide fixed close, medium, and gameplay-distance previews.
- Render a multi-view preview batch in one Blender process when possible.
  Eevee shader compilation can dominate startup time; reusing the compiled
  graphs makes additional fixed views inexpensive and keeps iteration
  deterministic.
- Review exposed colors and roughness on neutral, two-scale swatches before
  judging the in-context asset under representative key/fill/rim lighting.
  This separates material response from lighting-driven color bias.
- For a long narrow surface such as a sword blade, a whole-asset or
  whole-blade render may allocate too few pixels across the material to prove
  scratches, brushing, or roughness breakup. Add a localized blade-section
  crop and a grazing-light crop while retaining the full and gameplay views.
- Very thin nonmetallic relief such as leather cord can catch one bright
  dielectric highlight and read as metal even when Metallic is correctly
  zero. Review the assigned asset, not only a sphere: raise plausible
  roughness, remove unjustified coat, reduce Specular IOR Level when the
  material supports it, and keep enough color response outside the highlight
  to preserve identity.

## Realistic multi-scale surface patterns

Treat realism as several weak, physically distinct layers instead of one
high-contrast noise texture:

- separate broad form or manufacturing variation from characteristic
  mid-frequency structure and fine roughness/normal detail;
- expose scale, rotation, color, roughness, distortion/detail, and normal or
  bump strength where the group will be reused;
- use a directional primitive such as distorted Wave bands for timber fibers,
  brushed metal, or scratches. Stretching isotropic Noise can elongate a
  pattern, but by itself tends to produce blur rather than legible fibers;
- do not use distorted parallel bands as the primary identity of cut timber
  when the reference calls for recognizable rings, cathedrals, or end loops.
  Derive the broad grain from radial or elliptical distance around a virtual
  log axis, let that heartline drift slowly along the object, and reserve
  directional noise or Wave bands for weaker vessels and fibers. Preview the
  result on the asset and on rounded two-scale swatches so a coherent cut
  structure is not mistaken for arbitrary squiggles;
- break directional scratches into irregular segments with a second mask.
  Keep their color, roughness, and shallow recessed normal responses separate
  from forged macro variation and sparse pitting;
- build leather from chained low-strength bump stages: broad folds first,
  characteristic cells or grain second, and fine pores last. Do not force one
  texture to drive every frequency and channel;
- reserve strong color contrast for material identity. Fine pores, scratches,
  and machining marks normally belong more strongly in roughness and normal
  than in Base Color;
- add cropped material-specific evidence views when the full asset cannot
  resolve the authored pattern. Whole-asset, close-up, and two-scale swatch
  views answer different validation questions.

These principles were cross-checked against Ryan King Art's own
[procedural wood overview](https://ryankingart.gumroad.com/p/how-to-make-procedural-wood-in-blender-three-materials),
[scratched-metal tutorial page](https://ryankingart.wordpress.com/2021/06/18/procedural-scratched-metal-blender-tutorial/),
[procedural metal overview](https://ryankingart.wordpress.com/2024/09/14/procedural-metal-materials-blender-tutorial/),
and [procedural leather material listing](https://superhivemarket.com/products/3-leather).
Use the transferable construction ideas; author project node graphs
independently and record source influence in the material manifest rather than
copying a tutorial graph.

## Blender-to-game-engine boundary

Blender procedural node graphs generally do not transfer through FBX into game
engines.

Choose one:

- bake the relevant channels to textures;
- recreate the logic in the target engine's shader system;
- use both, with baked base detail and engine-side runtime variation.

Do not label a procedural material engine-ready until the chosen path has been
tested on an imported asset using the destination project's actual renderer.

## Generated-model boundary

Do not treat an AI-generated or third-party material graph or texture set as a
template for this authoring pipeline. It may be inspected for current asset
compatibility and channel assignment, but reusable procedural materials must
have independent, documented construction and provenance.
