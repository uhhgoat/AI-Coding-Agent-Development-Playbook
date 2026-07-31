---
name: blender-define-asset-style
description: Define and record an explicit Blender asset style contract before modeling or surfacing. Use when choosing or reviewing stylized, heroic, grounded, realistic, reference-faithful, or hybrid proportions; deciding visual hierarchy and detail density; interpreting perspective or symmetry in references; or explaining why an asset reads as toon-styled versus realistic.
---

# Blender Define Asset Style

Freeze visual intent before proportion-sensitive modeling or material work.
Treat style as several independent decisions, not one `realistic` flag.

## Workflow

1. Read [the shared Blender contract](../blender-validate-asset/references/shared-contract.md)
   and [the style profiles and axes](references/style-profiles.md).
2. Recap each reference before authoring: declared view, perspective strength,
   actual versus apparent symmetry, primary silhouette, functional
   construction, visible materials, and uncertain or hidden dimensions.
3. Copy [the style-contract template](assets/style-contract.template.json) into
   the task artifact directory as `style-contract.json`.
4. Select a named profile or a custom hybrid. Record reference fidelity,
   proportions, construction plausibility, shape language, visual hierarchy,
   material response, detail frequency, wear, and presentation independently.
   Apply `blender-style-grounded-realism` or
   `blender-style-clean-stylized`; add `blender-model-low-poly-assets` only
   when topology budget is part of the task. Apply a separate project overlay
   when one exists.
5. Record decisive ratios and landmarks in measurable units. Label every value
   `measured`, `reference-estimated`, `physically-inferred`, or `stylized`.
6. Name the primary impact/readability element and state what may be
   exaggerated, simplified, or kept physically plausible.
7. Define separate macro, mid-frequency, and micro-detail targets for geometry,
   color, roughness, and normal/height. State the expected gameplay and
   close-review distances.
8. List fixed review views, phase gates, mismatch severities, and human
   acceptance questions. State which reference-supported corrections may
   continue autonomously without changing the contract. Do not convert
   subjective approval into an automated pass.
9. Give the contract to `blender-model-hard-surface`,
   `blender-author-procedural-materials`, and `blender-validate-asset`.
10. Revise the contract explicitly when feedback changes the intended style;
    preserve the prior contract with its matching stage.

## Guardrails

- Do not infer object-space asymmetry from perspective foreshortening.
- Do not let realistic shaders relabel exaggerated geometry as realistic.
- Do not let exact silhouette matching imply verified hidden construction.
- Do not add microdetail merely because a close render can resolve it.
- Do not mix a style change into a fidelity correction without recording both.
- Do not treat a human acceptance question as a reason to stop when a visible
  discrepancy has an objective, reference-supported correction inside the
  current contract.

## Deliverables

- A versioned `style-contract.json` beside the stage manifests.
- A concise reference recap and measured-versus-inferred ratio table.
- Fixed views that make the chosen hierarchy, proportions, and surface detail
  reviewable at their intended distances.
