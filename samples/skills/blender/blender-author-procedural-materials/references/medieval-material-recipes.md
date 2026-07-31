# Procedural Materials for Medieval Assets

Use these as independent design recipes, not fixed node graphs. Every material
still needs a physical scale, style contract, preview, manifest, and
target-engine bake or shader decision.

## Shared layer model

Build reusable materials from named responsibilities:

1. **coordinates:** UV, object, generated, or world space with an explicit
   reason;
2. **macro identity:** boards, rings, blocks, large forged variation, broad
   folds, or plaster regions;
3. **mid structure:** grain, hammering, mortar, leather cells, weave, chips;
4. **micro response:** pores, fine scratches, fibers, pits, roughness breakup;
5. **contact/use masks:** edges, cavities, upward faces, grip/contact zones,
   water paths, soot, sharpening;
6. **optional damage:** sparse and art-directed, never uniform;
7. **PBR outputs:** Base Color, Roughness, Metallic, Normal/Height, and any
   explicit mask channels.

Expose scale, rotation, seed, colors, roughness range, normal strength, wear,
and style controls only when they have stable meanings.

## Toon-readable metal

Goal: strong value separation and edge readability with little micro noise.

- Set Metallic from material identity, normally near the metallic end for bare
  metal.
- Use one broad color/value gradient or low-frequency variation.
- Use a compact roughness range that distinguishes main plate, trim, and
  polished edge.
- Add sparse broad dents or hammering only when visible at the intended
  distance.
- Keep scratches rare, longer, and grouped rather than evenly distributed.
- Use bevel geometry or a bake for reliable edge catch-light; do not depend on
  noisy color edges.

For toon armor, surface detail must not erase authored planes. Preview with
both flat neutral light and grazing light.

## Forged, rough, or hammered iron

Separate:

- broad manufacturing variation;
- irregular shallow hammered cells;
- sparse pits;
- finer roughness breakup;
- contact or edge polish.

Possible procedural building blocks:

- low-scale Noise or Musgrave-equivalent fractal structure for broad change;
- Voronoi distance or layered noise, heavily softened and distorted, for
  irregular hammer impressions;
- thresholded sparse noise for pits;
- a separate fine noise for roughness;
- Geometry/normal-derived or authored masks for edges and contact zones.

Drive normal/bump more strongly than Base Color for shallow hammering. Avoid a
uniform crater field. Keep pits sparse and do not place corrosion under a
freshly polished sharpening band without a wear narrative.

## Polished blade or sharpened edge

Treat the edge as a semantic region:

- higher smoothness/lower roughness than the forged body;
- subtle longitudinal grinding or sharpening direction;
- weak color variation;
- shallow, segmented scratches parallel to plausible finishing or use;
- optional edge-contact wear mask.

Use UV or object coordinates aligned with the blade. Directional Wave bands or
stretched patterns need a breakup mask so they do not become continuous
wallpaper lines.

Keep the cutting-edge wedge in geometry. The material describes finish, not
thickness or sharpness.

## Rusted, dirty, or worn metal

Build from causal masks:

- cavities and moisture traps for corrosion;
- exposed edges and contact areas for polish or paint loss;
- downward water paths for streaking;
- upward surfaces for settled dust;
- random interruption to avoid perfect curvature masks.

Rust is primarily nonmetallic. When blending exposed metal and corrosion,
blend metallic and roughness with the same identity mask rather than darkening
Base Color alone.

Use one wear amount to modulate several subordinate masks, but keep their
scales independently tunable. Stylized assets may use larger, fewer patches.

## Long-grain timber and polished wood

Do not identify wood with distorted parallel Noise alone.

Separate:

- virtual-log growth structure;
- longitudinal fibers/vessels;
- slow heartline drift or board-specific warp;
- plank/board boundaries when relevant;
- pores and finish response;
- end grain versus long grain;
- handling, polish, dirt, and cut masks.

For recognizable cut grain:

1. Define a virtual log axis in object or UV space.
2. Derive radial or elliptical distance around a slowly drifting center.
3. Distort it weakly for growth-ring variation.
4. Use the rings for broad color and subtle height/roughness.
5. Add weaker longitudinal vessels with directional Wave/noise.
6. Vary individual boards with deterministic object or UV masks.

On a weapon haft, align the grain with the haft and keep it continuous through
the visible length. On a timber-frame building, vary boards deliberately while
preserving consistent physical scale. Polished wood narrows roughness and may
add a weak clear-coat response; it does not remove grain structure.

For coopered barrels and other repeated boards, do not stamp one identical
cathedral symbol into every cell. Vary each stave or board's virtual-log
heartline, ring phase, apparent width, and vertical origin within restrained
ranges. Keep earlywood/latewood Base Color contrast lower than the first
readable draft and place more of the distinction in roughness and shallow
normal response. Review the asset at gameplay distance: if the grain reads as
inked outlines before the barrel silhouette and hoops, reduce ring contrast,
frequency, or bump. End grain needs a different radial construction and board
layout; rotating long grain onto a cap is not a substitute.

Treat finish and dryness as separate from albedo. An attractive wood color can
still read as plastic when the roughness floor is too low or a generic coat is
left enabled. For dry, unfinished barrel timber, start with a broad high
roughness range, remove coat unless the asset narrative calls for varnish, and
add a weak fine-fiber roughness layer that is independent of the visible growth
rings. Let recessed seams and porous end grain become rougher still. Validate
the scalar map under grazing light and regenerate any packed
metallic/smoothness texture after changing roughness; otherwise a target engine
can continue sampling stale smoothness from the packed alpha channel.

## Leather

Use several weak scales:

- broad folds, compression, or stretched regions;
- mid-scale irregular cells/grain;
- fine pores;
- edge darkening or polish;
- bend and grip wear;
- optional cracks only for aged/dry leather.

Chain bump stages from large to small rather than using one texture for every
channel. Let grain and pores affect normal and roughness more than Base Color.
Use UVs when stitch lines, straps, borders, or directional stretching need
art direction.

For toon leather, simplify to a broad color, one gentle grain response, and
selective edge/contact wear.

## Cloth and woven underlayers

Separate cloth body from visible weave:

- broad color and roughness;
- fiber direction;
- crossing warp/weft or knitted structure;
- weak fuzz/sheen where appropriate;
- folds and seams from geometry, bake, or a separate larger-scale layer.

Use two perpendicular directional patterns for a simple weave, with a mask or
phase relation that suggests over/under crossings. Keep thread-scale normal
weak at game distance. If threads would exceed the bake resolution, omit them
or author a controlled mip-safe pattern.

Chain mail is not generic woven cloth. Use actual low-cost geometry,
alpha/normal cards, or a baked repeating link pattern based on distance and
silhouette requirements; validate moiré and mip behavior.

## Masonry, stone blocks, and mortar

Separate block layout from stone surface:

- brick/block cell layout and bond;
- mortar mask and depth;
- per-block color/roughness variation;
- chipped edges and large damage;
- stone grain and pores;
- dirt, moss, soot, or moisture.

Use a Brick Texture, Voronoi-derived cells, UV-authored layout, or Geometry
Nodes depending on required bond and silhouette. Mortar belongs between
blocks, not as a global noise color. Large protruding blocks and broken edges
need geometry or a bake with enough parallax/normal support.

Maintain constant material scale across modular wall sizes. Use object or UV
coordinates that do not resize with every module's bounds.

### Cylindrical towers and curved masonry shells

Do not feed an ordinary planar brick layout directly into the surface of a
round tower and call the result wrapped masonry. Planar projection compresses
or mirrors the bond around the flanks and makes openings expose inconsistent
courses.

For a cylindrical shell with a stable assembly origin:

1. derive angle with `atan2(Y, X)`;
2. shift the angle into a continuous positive range;
3. multiply by a recorded nominal radius to recover circumferential arc
   length in meters;
4. divide arc length by nominal block width;
5. derive course coordinate independently from world/assembly `Z` divided by
   course height;
6. offset alternating integer courses by half a block;
7. derive vertical and horizontal mortar from distance to cell boundaries;
8. keep per-block variation keyed by integer block/course coordinates.

Use the same assembly-relative coordinate source for every contributing shell
object when courses must line up. Record the nominal radius and acknowledge
that deep reveals at a meaningfully different radius may need a separate
mapping or UV treatment.

Perfectly straight procedural joints can make plausible stone read as molded
brick. Add only weak, low-frequency coordinate warp before cell masks. The
warp should interrupt ruler-straight seams without changing course spacing,
closing openings, or pretending to create silhouette damage.

Separate the construction families:

- the large shell may show the cylindrical bond and mortar;
- modeled frames, string courses, landings, and merlons generally need a
  quieter cut-stone material without a second unrelated mortar grid;
- deep chips, missing corners, and broken merlons remain geometry or bake
  responsibilities.

At the first realistic pass, reject these common failure modes:

- pale dressed stone that loses all quarry or granular response;
- a clean rectangular bond with no within-stone variation;
- mortar so dark or deep that it reads as inked toon outlines;
- high-contrast door grain that reads as decorative stripes;
- one light rig that is mistaken for proof that every side of the material was
  reviewed.

Inspect neutral, grazing, close, rear three-quarter, and gameplay-distance
views. A fixed rear beauty view may remain shadowed, but a second illuminated
angle must still verify material continuity.

## Plaster and damaged plaster

Build:

- broad warm/cool color drift;
- subtle sandy or fibrous roughness;
- weak pores and trowel variation;
- larger missing-plaster masks;
- exposed masonry or lath beneath only where construction supports it;
- dirt and moisture near ground, ledges, and leaks.

Large missing regions should change the wall edge or reveal an underlying
layer through geometry or a controlled layered material. Avoid uniform
cracking over every wall.

## Roof tile, slate, shingle, and thatch

Use geometry for eave, ridge, and broken silhouettes. Materials provide:

- per-piece color and roughness variation;
- clay pores, slate grain, wood grain, or straw fibers;
- dirt and moss;
- soot near chimneys;
- water and sun weathering.

A procedural “tile material” does not replace tile course geometry when the
camera sees the roof edge. At distant LODs, bake the interior courses and retain
silhouette geometry.

For hero roofs, decide the geometry/material split explicitly:

- geometry owns course overlap, staggered joints, exposed lower edges,
  thickness, end cuts, and broken silhouettes;
- the material owns restrained per-piece color, clay/slate/wood structure,
  fine pores or grain, roughness, soot, and weathering;
- a darker under-roof or underlayment may show narrowly through intentional
  gaps, but it must not become the primary pattern;
- keep color variants close enough that they read as firing or aging
  differences rather than randomly painted tiles.

Validate a roof close enough to see overlap and again at gameplay distance.
If it reads as horizontal strips close up or dissolves into high-frequency
noise far away, revise the geometry or frequency before adding more nodes.

For thatch, use layered cards, curves, or geometry at silhouette scale and a
fiber material for internal density. Check alpha overdraw if cards are used.

## Dirt, mud, moss, and environmental accumulation

Drive placement from cause:

- upward-facing and moisture-retaining surfaces for moss;
- ground proximity and foot/vehicle paths for dirt or mud;
- cavities and ledges for settled debris;
- roof drainage and wall runoff for streaks;
- contact/occlusion for grime.

Combine geometric masks with low-frequency breakup. World-space masks can keep
vertical placement stable but may slide when assets move; bake them or convert
to object/UV space before reuse if necessary.

## Reusable medieval material interface

Prefer a small consistent interface:

- `ScaleMeters`
- `Rotation`
- `Seed`
- `PrimaryColor`
- `SecondaryColor`
- `RoughnessMin`
- `RoughnessMax`
- `MacroAmount`
- `MidAmount`
- `MicroAmount`
- `NormalStrength`
- `WearAmount`
- `DirtAmount`
- `MoistureAmount`
- `StyleDetail` or separate declared preset

Do not expose every internal node value. Version the node group when socket
meaning changes.

## Preview and bake gates

For each material, render:

- neutral front light;
- grazing light;
- close crop;
- medium and gameplay distance;
- two differently scaled swatches;
- in-context assigned asset;
- a flat diagnostic view of important masks.

Before baking:

- confirm coordinate scale and object transforms;
- decide which details become Base Color, Roughness, Metallic, Normal, AO,
  Height, or packed masks;
- remove unsupported Blender-only displacement assumptions;
- verify normal strength at the target texel density;
- check tile seams, UV seams, and mip behavior;
- preserve the procedural source and bake manifest.
