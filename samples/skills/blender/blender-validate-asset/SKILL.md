---
name: blender-validate-asset
description: Validate Blender modeling, rigging, procedural-material, baked-texture, and export stages using explicit pass, warning, and failure evidence without modifying approved sources. Use before accepting or exporting `.blend` assets, when comparing revisions, or when checking geometry, modifiers, rigs, UVs, node graphs, image dependencies, normal maps, texture channels, and destination-engine budgets.
---

# Blender Validate Asset

Validation is a report-only boundary. Do not repair the asset unless the user
separately requests a change through the applicable authoring skill.

## Workflow

1. Read [the shared contract](references/shared-contract.md) and
   [validation checklist](references/validation-checklist.md).
2. Identify the asset type, accepted baseline/stage, intended downstream use,
   and explicit project thresholds. For appearance-sensitive work, also load
   the versioned `style-contract.json`.
3. Run `blender-inspect` and collect fixed geometry/material/channel previews.
   For unrigged hard-surface output parented to one assembly object, also run
   the report-only [`../shared/scripts/validate_hard_surface.py`](../shared/scripts/validate_hard_surface.py).
   When an operation manifest declares calibrated 2D landmarks, also run
   [`../shared/scripts/validate_reference_silhouette.py`](../shared/scripts/validate_reference_silhouette.py).
4. Compare the candidate with its baseline, manifests, fixed-view previews,
   and iteration log. Confirm that the previews were inspected rather than
   merely generated.
5. Classify each check as `pass`, `warn`, `fail`, or `not-evaluated`.
6. Fail on broken protected invariants, missing required dependencies, unsafe
   transforms, unexplained rig/morph changes, or invalid bake inputs/results.
7. Warn rather than invent thresholds when a visual or budget requirement is
   not yet agreed.
8. Write `validation.json` and a concise Markdown summary with direct evidence.
9. Compare reference fidelity, proportions/construction, shape language,
   visual hierarchy, and surface treatment independently. Keep structural
   validity separate from human judgments such as silhouette, style fit,
   historical accuracy, material appeal, and deformation quality.
10. Do not accept a modeling stage as visually ready while its iteration log
    contains an unresolved high-impact mismatch. A structural pass does not
    close the visual-review loop.
11. Require a passing result before the applicable export skill. Use
    `blender-export-unity` only when Unity is the declared destination.

## Required Evidence

- Source/version/stage lineage and manifests used.
- Style contract version, selected profile/axes, decisive ratios, intended
  review distance, and unresolved human acceptance questions when applicable.
- Base, unique, object-summed, and evaluated geometry.
- Modifier order, settings, and dependency targets.
- Transforms, determinant, dimensions, normals, UVs, and material slots.
- Rig, bone, vertex-group, weight, shape-key, and split preservation where
  applicable.
- Node graphs, external/packed images, formats, dimensions, color spaces, and
  missing paths.
- Bake source/target, UV, cage/ray, margin, channel, and normal convention.
- Fixed previews, evidence that each was inspected, the ranked iteration log,
  stage-to-stage comparison, and explicit human-review items.

## Guardrails

- Do not mutate, save, apply, repack, relink, rebake, or export during
  validation.
- Do not mark AI-generated or third-party topology or texture architecture as
  a project pattern.
- Do not turn `not-evaluated` into `pass`.
- Do not mark an asset realistic because its materials pass while its
  proportions or construction remain deliberately stylized.
