---
name: blender-style-clean-stylized
description: Apply a general-purpose clean stylized or toon-readable style to Blender assets through deliberate exaggeration, simplified secondary construction, designed planes, broad material blocks, and restrained microdetail. Use for props, characters, armor, weapons, buildings, environments, or game assets where silhouette impact and immediate readability intentionally lead literal realism.
---

# Blender Style Clean Stylized

Use this only when stylization is an explicit target. Low polygon count alone
does not trigger this style.

## Contract

1. Read `style-contract.json` from `blender-define-asset-style`.
2. Name the dominant readability element and intended view distance.
3. Record every proportion departure: enlarged, shortened, thickened,
   tapered, simplified, rounded, sharpened, or flattened.
4. Preserve functional openings, attachments, articulation, support, and
   handling even when outer contours are exaggerated.
5. Author a small set of deliberate planes and contour changes. Do not use
   arbitrary Decimate output as style design.
6. Simplify secondary transitions and hardware according to screen size.
   Enlarge only the features that serve the declared hierarchy.
7. Use broad material/value blocks, compact roughness ranges, sparse graphic
   wear, and quiet normal response.
8. Keep macro identity legible. Reduce mid and micro detail before reducing
   the primary silhouette.
9. Review flat/neutral, grazing, gameplay-distance, and silhouette-only views.
10. State that the asset is stylized even if individual materials remain
    physically plausible.

## Material starting point

Use the `GP_CleanStylized_*` presets from
`blender-author-procedural-materials`. Keep `Micro Amount` near zero unless a
specific close-review requirement justifies it. Let color grouping,
silhouette, designed planes, and selective edge response do most of the work.

## Guardrails

- Do not infer stylization from missing detail.
- Do not enlarge every component.
- Do not let large bevels erase designed points or terminals.
- Do not use uniform noise as a substitute for a material identity.
- Do not close body or mechanism openings for a cleaner silhouette.
- Do not present stylized proportions as historical or physically measured.

## Deliverables

- Style contract with hierarchy, explicit exaggerations, plane language,
  material blocks, frequency limits, and review distance.
- Silhouette, flat-light, grazing-light, orthographic, perspective, and
  gameplay views.
- Separate readability, construction, reference-fidelity, and surface claims.
