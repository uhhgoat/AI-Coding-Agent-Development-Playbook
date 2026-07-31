# Medieval Houses and Castle Kits

## Define the artifact

Choose one:

- **hero building:** one composed asset; may use reusable submodules;
- **building kit:** parts intended to generate several houses;
- **fortification kit:** walls, corners, towers, gates, stairs, and trims;
- **assembly:** a placed village, castle, arena, street, or ruin;
- **shell:** exterior only;
- **playable building:** exterior, interior, circulation, collision, and
  gameplay openings.

Record the style and period/region references separately. “Medieval fantasy”
is not a specific construction system.

## Human and gameplay scale

Use a human proxy and explicit measurements for:

- door height and width;
- window sill and head height;
- floor-to-floor height;
- stair rise, run, width, and headroom;
- wall, parapet, and battlement thickness;
- walkway and doorway combat clearance;
- ceiling and beam clearance;
- gate and portcullis clearance;
- roof pitch, eave depth, and ridge height;
- tower and wall relationship.

Stylized proportions may push doors, roofs, towers, or upper stories, but the
departure belongs in the style contract. Test player scale in both exterior
and playable interior spaces.

## House grammar

Build in this order:

1. footprint and ground contact;
2. floor masses;
3. wall thickness and major divisions;
4. roof pitch, ridge, eaves, and overhang;
5. door and window openings;
6. structural frame or masonry logic;
7. stairs, balcony, chimney, porch, dormer, or bay;
8. trims and roof covering;
9. controlled variants and damage;
10. props, vegetation, and set dressing only after the building passes.

### Timber-frame house

Distinguish load-bearing or visually structural timbers from plaster, wattle,
brick, or stone infill. Beams should meet, carry, brace, or terminate
deliberately. Avoid a flat wall with arbitrary dark strips.

For stylized houses:

- push the roof and major timber rhythm first;
- use a few controlled beam-width and sag variants;
- keep windows and doors aligned to a readable structural pattern;
- vary silhouettes between building modules, not every individual board;
- preserve believable ground contact and gravity.

After placing structural framing, run an opening-clearance review independently
from the silhouette review. Check every door and window in a view normal to the
opening and in three-quarter perspective. A brace may terminate at or frame an
opening, but it must not cross glass, a door leaf, or required clearance unless
it is intentionally modeled and named as a mullion, grille, shutter, or other
opening component. If the wall bay is too narrow for both a brace and an
opening, relocate the brace to a solid panel instead of squeezing it into the
glass.

### Roofs

Separate roof structure from roof covering.

Keep in geometry when visible:

- eaves and ridge silhouette;
- tile, shingle, slate, or thatch course edges;
- dormers, chimneys, gutters, and large damage;
- thick stylized roof layers.

Use instances, Array, Geometry Nodes, or a small variant set for repeated
covering. Apply controlled positional, rotational, scale, and color variation
without breaking drainage direction or course overlap.

Before surface detail, require the covering to pass four construction reads:

- every course has an upslope head and an exposed downslope edge;
- the upslope course overlaps the course below it;
- adjacent seams are staggered between rows;
- eave, ridge, end, valley, chimney, and damage transitions terminate
  deliberately.

Broad raised bands do not become shingles merely through a clay material. At
hero distance, use closed tile/shingle geometry or instances for the overlap,
seams, thickness, and exposed ends. Consolidating disconnected pieces into one
editable mesh per roof side is acceptable when it preserves per-piece material
variation and makes the output cheaper to organize.

At distant scales, bake or simplify interior courses while retaining a
silhouette row at eaves, ridge, and broken edges.

## Castle grammar

A minimal fortification kit usually needs:

- straight wall bay;
- inner and outer corners;
- end caps;
- wall base and top/parapet;
- crenellated and plain variants;
- tower wall and roof/top variants;
- gate or arch bay;
- stairs or ramp to the wall walk;
- floor, platform, and transition pieces;
- pillar/buttress/trim pieces;
- damaged variants;
- collision counterparts.

Build the blockout as circulation and defense-shaped massing, even for fantasy:

- wall walks need access and width;
- parapets need thickness and height;
- towers need believable junctions to walls;
- gates need depth and closure space;
- stairs and ramps must land on actual platforms;
- openings should not remove the support that visually carries the mass above.

Do not overfit a kit to one finished castle. Test at least two wall lengths,
both turn directions, a height change, a gate, a tower junction, and a compact
alternate layout.

### Round wall towers

Define the outer diameter, inner diameter, shell thickness, wall-walk
threshold, parapet height, merlon height, and curtain-wall connection before
adding dressed stone or surface breakup.

- Use a closed annular shell when doorways or arrow slits must show real wall
  depth.
- Keep the ground entrance and upper wall-walk entrance human-scaled even when
  the tower silhouette is visually dominant.
- Give an upper entrance a supported landing or explicit curtain-wall socket;
  a door leaf floating above the ground is not a circulation solution.
- Treat a continuous parapet, top deck, and repeated merlons as separate
  construction roles.
- Use one linked merlon source with a bottom-center pivot and verify the placed
  bottom and top elevations numerically.
- Let true openings, crenellations, string courses, and a few large dressed
  frames carry the modeling-stage identity. Reserve mortar, ordinary block
  joints, pits, lichen, and small erosion for materials, decals, or bakes.
- Validate curved-shell Boolean openings at evaluated topology, not only in
  beauty renders. Centerline-coincident arch vertices and shell-wide bevels
  can create microscopic sliver faces.

## Stylized low-poly shape language

Use a small hierarchy:

1. skyline: roof pitch, tower height, wall profile, gate, or keep;
2. major masses: floors, bays, towers, roof blocks;
3. structural rhythm: beams, buttresses, arches, crenellations;
4. surface and props.

Purposeful stylization can use:

- tapered walls or towers;
- slightly bowed beams;
- nonuniform roof ridges;
- chunky eaves and trims;
- larger doors/windows for gameplay readability;
- grouped rather than uniform stone breakup;
- limited planar faceting.

Keep deformation coherent. If a building leans, show how floors, roof, and
attachments respond. Independent random rotations create noise instead of
design.

## Modularity and variation

Build an `ASSET_ZOO` containing:

- every base module;
- each allowed size;
- material variants;
- damage or age variants;
- collision and LOD candidates;
- labels or metadata;
- one human-scale proxy.

Build a seam test containing:

- two straight bays;
- internal and external corners;
- a door/window transition;
- a floor or wall-height change;
- a roof valley/ridge or end cap;
- a stair/platform junction;
- a material-scale comparison.

Use:

- linked mesh data for identical geometry;
- collection instances for composed modules;
- Array for exact linear repetition;
- curves for deliberate paths;
- Geometry Nodes when rule-driven placement or exposed variation pays for its
  complexity.

Keep deterministic seeds and inspectable controls. Do not realize instances or
apply arrays solely for preview.

## Material and geometry boundary

| Feature | Usually geometry | Usually material/decal/bake |
|---|---|---|
| Timber | Major beams, splintered silhouette | Grain, pores, fine cracks, stains |
| Masonry | Wall mass, corner blocks, large broken stones | Mortar, pits, color variation, small cracks |
| Plaster | Wall plane, large missing chunks | Grain, hairline cracks, dirt, small chips |
| Roof | Eave/ridge silhouette, visible courses | Fine grain, pores, soot, lichen |
| Metal | Hinges, straps, grilles, large fasteners | Scratches, oxidation, micro dents |
| Ground | Curbs, large stones, terrain silhouette | Dirt, mud, moss, small gravel |

The correct boundary depends on viewing distance, silhouette, bake plan, and
runtime budget. Document exceptions.

## Review checklist

- Human and player scale is credible in all required spaces.
- The full silhouette works before material or vegetation.
- Structural parts meet and appear supported.
- Roof covering overlaps and drains consistently.
- Modules snap without gaps, double faces, or shading discontinuities.
- Material scale remains stable across differently sized modules.
- Repetition is visible only where intentional.
- An alternate assembly proves the kit is not a disguised one-off model.
- Street, roof, interior, and top-down gameplay views reveal no major failure.
- Collision, LOD, interior, and damage status are explicit.
- Historical confidence is reported independently from visual quality.
