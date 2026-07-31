# General Procedural Node Library

Use the bundled library as an editable starting point, not as an immutable
black box.

## Contents

The library ships seven project-neutral signal groups:

| Group | Material-space contract |
|---|---|
| `GP_Surface_WoodGrain_v1` | Local `Z` follows long grain; `XY` crosses a virtual log |
| `GP_Surface_ForgedMetal_v1` | Object/material meters; explicit mask supplies contact polish |
| `GP_Surface_PolishedMetal_v1` | Local `Z` follows brushing, grinding, or scratch direction |
| `GP_Surface_Leather_v1` | UVs for straps/stitches; object space is acceptable for seamless hide |
| `GP_Surface_WovenCloth_v1` | Local `X/Y` follow warp and weft |
| `GP_Surface_Masonry_v1` | Meter-scale UV/object coordinates stay constant across modules |
| `GP_Surface_Plaster_v1` | Meter-scale object coordinates; authored masks drive loss or damp |

Every group exposes:

- `Vector`
- `Scale (1/m)`
- `Macro Amount`
- `Mid Amount`
- `Micro Amount`
- `Normal Strength`
- `Wear Mask`
- `Wear Amount`
- material-specific colors, roughness, and characteristic frequencies
- `Base Color`, `Roughness`, `Metallic`, `Normal`, `Height`, and `Wear` outputs

The `Wear Mask` is intentionally not guessed from generic Noise. Supply a
painted, geometric, curvature-derived, contact, cavity, sharpening, moisture,
or baked mask appropriate to the asset.

## Bundled files

- `assets/general-procedural-material-library-v1.blend`
- `assets/material-library-manifest.json`
- `assets/material-library-preview.png`
- `scripts/build_material_library.py`
- `scripts/validate_material_library.py`

Append/link the `.blend` for interactive work. Rebuild it when testing the
script itself:

```powershell
& blender --background --factory-startup `
  --python scripts/build_material_library.py -- `
  --output artifacts/general-procedural-material-library-v1.blend `
  --manifest artifacts/material-library-manifest.json `
  --preview artifacts/material-library-preview.png
```

Validate the result:

```powershell
& blender --background --factory-startup `
  artifacts/general-procedural-material-library-v1.blend `
  --python scripts/validate_material_library.py -- `
  --manifest artifacts/material-library-manifest.json `
  --preview artifacts/material-library-preview.png `
  --report artifacts/material-library-validation.json
```

## Style presets

The `.blend` includes two parameter families:

- `GP_Grounded_*`: realistic scale, restrained multi-frequency detail, weak
  normals, and plausible roughness. This targets game-ready grounded realism,
  not hyperreal close-up rendering.
- `GP_CleanStylized_*`: broader color/value groups, reduced mid detail, almost
  no micro response, and quiet normals.

These are not geometry labels. A clean-stylized material does not make
exaggerated geometry grounded, and a grounded material does not make low-poly
geometry toon-styled.

## Adaptation rules

1. Duplicate and version a group before changing socket meanings.
2. Align material space before tuning frequencies.
3. Apply transforms or compensate explicitly so `Scale (1/m)` is meaningful.
4. Tune macro, mid, and micro independently at intended review distance.
5. Use separate causal masks for edge polish, grip wear, sharpening, dirt,
   moisture, soot, and damage.
6. Treat `Height` as a bake/debug signal; retain real geometry for silhouette,
   cutting edges, deep mortar, stitching, and construction seams.
7. Bake approved channels for game engines. Procedural Blender nodes do not
   transfer through FBX.

## Provenance

The graphs are original implementations of general procedural-shading
principles. They contain no external images and do not reproduce a tutorial or
paid material graph. Keep this provenance statement and add project-specific
source influences when extending the library.
