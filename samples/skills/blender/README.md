# Blender Skills

General-purpose Blender skills for inspection, style definition, staged
modeling, procedural surfacing, texture baking, validation, and Unity export.
They are designed for coding agents that can run Blender's Python API in
background mode and inspect rendered evidence.

The skills contain no repository-specific asset names, user names, local
machine paths, private references, or required commercial add-ons.

## Skill set

| Phase | Skills |
|---|---|
| Inspect and define intent | `blender-inspect`, `blender-define-asset-style`, `blender-apply-project-style` |
| Choose a visual profile | `blender-style-grounded-realism`, `blender-style-clean-stylized` |
| Model general assets | `blender-model-hard-surface`, `blender-model-low-poly-assets`, `blender-model-environment` |
| Model medieval assets | `blender-model-armor`, `blender-model-medieval-weapons`, `blender-model-medieval-architecture` |
| Preserve rigged apparel | `blender-fit-rigged-apparel` |
| Surface and bake | `blender-author-procedural-materials`, `blender-bake-texture-maps` |
| Validate and export | `blender-validate-asset`, `blender-export-unity` |

Use the smallest applicable combination. For example, a reference-matched
low-poly sword normally uses:

1. `blender-inspect`
2. `blender-define-asset-style`
3. one style skill
4. `blender-model-medieval-weapons`
5. `blender-model-low-poly-assets`
6. `blender-author-procedural-materials`
7. `blender-bake-texture-maps`
8. `blender-validate-asset`
9. the destination export skill

## Bundled resources

- `blender-author-procedural-materials/assets/` contains an original,
  general-purpose `.blend` material library, manifest, and preview.
- `blender-author-procedural-materials/scripts/` rebuilds and validates that
  library.
- `shared/scripts/` contains report-only inspection, rendering, reference,
  articulation, procedural-material, hard-surface, and bake validators.
- `examples/` contains three original fixture generators and a small visual
  gallery. The examples do not use downloaded meshes or reference images.

The procedural library targets Blender `4.3+` and was last validated with
Blender `4.5 LTS`. Revalidate before relying on it with another major version.

The current modeling guidance also incorporates forward-tested lessons for
continuous annular forms, anatomy-following headwear, evaluated weapon
landmarks, station-lofted hulls, supported deck transitions, and static
mast-and-sail assemblies. These are reusable construction and validation rules;
the private project fixtures and machine-local manifests are not included.

## Adapting the suite

- Copy the whole `blender/` directory when possible so cross-skill links and
  shared scripts remain intact.
- If copying only selected skills, also copy
  `blender-validate-asset/references/shared-contract.md` and every directly
  linked reference or shared script.
- Replace `blender-apply-project-style` with a thin repository-owned overlay
  that points to the project's actual art-direction documentation.
- Keep source images, downloads, manifests, and generated artifacts outside
  the skill folders unless they are intentionally reusable public assets.
- Never commit absolute local paths in manifests or examples.

See the [example gallery and commands](examples/README.md).
