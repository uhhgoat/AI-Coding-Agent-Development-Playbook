# Procedural Material Research Ledger

Research passes: `2026-07-28`, `2026-07-30`.

This ledger records sources that informed the reusable process. It is not a
library of node graphs to copy.

## Blender fundamentals

- [Blender Studio: Procedural Shading — Fundamentals and Beyond](https://studio.blender.org/training/procedural-shading/5f07594bdf7b3cdd8937a945/)
  covers values/vectors, coordinate types, Noise, shape control, repetition,
  texture composition, space manipulation, PBR map generation, masks,
  randomization, semi-procedural workflows, parameterization, node groups, and
  worked wall/wood examples. It includes example scenes and shaders.
- [Blender Manual: Principled BSDF](https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html)
  is the authority for the current Principled material inputs and physically
  based response.
- [Blender Manual: Asset Libraries](https://docs.blender.org/manual/en/latest/files/asset_libraries/introduction.html)
  defines reusable material and node assets discoverable through the Asset
  Browser.
- [Blender Manual: Brick Texture](https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/brick.html)
  documents offset rows, frequency, mortar, brick width, and row height. Use
  those controls for procedural or baked interior course signals while
  retaining geometry for hero-distance shingle overlap and roof edges.

## Ryan King Art source map

Ryan King Art maintains more than a YouTube channel:

- [ArtStation profile and tutorial archive](https://ryanking.artstation.com/)
  indexes a large range of Blender procedural material tutorials.
- [Procedural Materials album](https://ryanking.artstation.com/albums/3476170)
  groups wood, stone, brick, cobblestone, metal, leather, fabric, plaster,
  dirt, moss, roof, and many other materials.
- [Gumroad storefront](https://ryankingart.gumroad.com/)
  offers tutorial-linked materials, Blender project files, material packs, and
  Asset Browser-ready libraries.
- [WordPress tutorial archive](https://ryankingart.wordpress.com/category/tutorials/)
  provides dated tutorial posts and direct material topics.

Relevant focused sources:

- [Three procedural wood materials](https://ryankingart.gumroad.com/p/how-to-make-procedural-wood-in-blender-three-materials)
  demonstrates that one “wood” label needs multiple authored structures and
  reusable variations.
- [Procedural metal materials](https://ryankingart.wordpress.com/2024/09/14/procedural-metal-materials-blender-tutorial/)
  surveys reusable metal material construction.
- [Procedural scratched metal](https://ryankingart.wordpress.com/2025/04/25/procedural-scratched-metal-material-blender-tutorial-2/)
  is relevant to segmented directional scratches and separate roughness/bump
  controls.
- [Procedural brushed metal](https://ryanking.artstation.com/projects/xYoKA4)
  is relevant to directional finish and cross-engine preview.
- [Procedural leather](https://ryanking.artstation.com/projects/9mLA8y)
  is relevant to layered grain and pores.
- [Stone material](https://ryanking.artstation.com/projects/3qbmRv)
  is relevant to separating rock identity from generic noise.
- [Ryan King Art metal material pack](https://ryankingart.gumroad.com/l/pro-metal-1)
  lists a wide range of metal identities and exposes recurring controls such
  as scale, rotation, color, metallic response, detail, noise/distortion,
  roughness, normal, bump, and displacement.
- [Ultimate material pack overview](https://ryankingart.gumroad.com/p/ultimate-blender-procedural-material-pack)
  documents custom thumbnails, sorted catalogs, customizable node groups, and
  Asset Browser organization.

The ArtStation archive also indexes directly relevant topics including stone
bricks, brick walls, cobblestone, white and damaged plaster, terracotta roof
tiles, tree bark, wood planks/floors, cast iron, hammered copper, battered and
worn metal, fabric, woven fabric, black leather, dirt, mud, moss, and stylized
shaders.

The `2026-07-30` cottage refinement used the terracotta-roof topic only as
layering and parameter evidence. Its three clay variants and node parameters
remain independently authored around the project-owned plaster signal group;
the visible shingle layout is original geometry rather than a copied tutorial
graph.

## Findings adopted by this skill

- Reusable material groups need a small, consistent control surface.
- One material identity requires separate macro, mid, and micro structures.
- Scale, rotation, color, roughness, detail/distortion, and normal/bump are
  recurring useful controls.
- Directional materials such as wood, brushed metal, scratches, and weave need
  an explicit coordinate axis.
- Material libraries benefit from curated preview thumbnails and catalogs.
- Project files are valuable for lawful structural comparison, but a tutorial
  graph should not become an undocumented project dependency.
- Cycles displacement and Eevee previews are not interchangeable; the intended
  engine and bake path must be explicit.

## Independent-authoring and rights rules

- Use the sources to understand visual layers, parameter categories, and
  validation strategy. Author destination-project node graphs independently.
- Record source influence in `material-manifest.json`.
- Do not redistribute paid `.blend` files, node groups, thumbnails, HDRIs, or
  renders.
- Verify the current license before importing a downloaded material.
- Do not use assets marked `NoAI` for automated graph extraction, reconstruction,
  or skill derivation.
- Prefer original creator pages and official Blender documentation over mirrors
  and tutorial-summary sites.
- If a Blender-version change alters a node or socket, validate against the
  current manual and update the project group rather than reproducing an old
  screenshot mechanically.
