---
name: blender-model-hard-surface
description: Create or revise staged, non-destructive hard-surface Blender models with explicit topology, semantic controls, calibrated 2D reference-image matching, and editable modifier stacks. Use for props, armor plates, architectural modules, weapons, or other unrigged forms built from primitives, direct topology, `bmesh`, Mirror, Boolean, Bevel, Solidify, Array, Curve, Shrinkwrap, or Subdivision workflows.
---

# Blender Model Hard Surface

Keep source geometry and construction controls editable. Work only in a new
file or disposable stage.

Use [the armor skill](../blender-model-armor/SKILL.md) for body-worn armor and
[the medieval-weapons skill](../blender-model-medieval-weapons/SKILL.md) for
swords, axes, polearms, maces, hammers, or shields. Those skills add
domain-specific fit, construction, handling, and review rules on top of this
generic hard-surface workflow.

## Workflow

1. Read [the shared Blender contract](../blender-validate-asset/references/shared-contract.md),
   [primitive-decomposition guidance](references/primitive-decomposition.md),
   [modifier-stack guidance](references/modifier-stacks.md), and
   [the iterative visual-review loop](references/iterative-visual-review.md).
2. Inspect every input with `blender-inspect`; identify protected or
   reference-only data.
3. For style- or reference-sensitive work, use
   `blender-define-asset-style` to freeze separate reference-fidelity,
   proportion, construction, shape-language, visual-hierarchy, and surface
   targets before geometry. Do not use material realism as a geometry label.
4. Analyze the asset into the fewest continuous base masses before adding
   detail. Record each mass's topological class, best-fit primitive, local
   axis, modification method, attachment boundary, and continuity/seam
   requirement. Translate the result and style contract into dimensions,
   decisive ratios, symmetry, silhouette, thickness, repetition, bevel,
   topology, and evaluated-budget constraints.
5. When matching a supplied image, read
   [reference-image guidance](references/reference-images.md). Calibrate one
   image-to-world mapping, keep the image as a packed non-export reference,
   recap perspective and object-space symmetry, and label image-measured
   versus inferred dimensions. For body-worn hard-surface assets, also define
   a scaled body silhouette or cage and explicit static-clearance targets.
6. Create `SOURCE`, `CONTROLS`, `OUTPUT`, and `PREVIEW` collections in a new
   staged `.blend`.
7. Build geometry with direct data/RNA and `bmesh` where practical. Use
   `bpy.ops` only after explicitly setting mode, active object, selection, and
   context.
8. Name cutters, mirror controls, curve controls, and output objects by role.
9. Add one coherent topology or modifier change per stage. Preserve the prior
   `.blend`, name the new stage, and record exact stack order and settings in
   `operation-manifest.json`.
10. Reinspect base and evaluated geometry. For an unrigged assembly parent, run
    [`../shared/scripts/validate_hard_surface.py`](../shared/scripts/validate_hard_surface.py)
    to check closed geometry, loose
    or degenerate elements, transforms, materials, and modifier dependencies.
11. Render fixed front, back, side, perspective, and declared gameplay-distance
    views. For an image match, also render an aligned translucent silhouette
    overlay. Actually inspect every required view; generating an image is not
    visual-review evidence by itself.
12. Write a ranked self-critique against the reference, style contract, and
    preceding stage. Review macro silhouette and proportions before
    construction, layer order, secondary features, bevels, or fine detail.
13. When a high-impact mismatch is objectively visible and its correction is
    inside the declared style and scope, revise it autonomously in another
    preserved stage. Repeat steps 9-12 until no high-impact mismatch remains.
    Do not stop at the first technically valid model or ask for approval
    between normal, reversible modeling passes.
14. Record medium and low residuals honestly. Ask the user only when references
    conflict, a subjective choice would change the style contract, or the
    correction would expand scope or risk protected data.
15. Leave modifiers unapplied. Route approved finalization through the
   destination project's export skill; use `blender-export-unity` only when
   Unity is the declared target.

## Guardrails

- Never overwrite the only source or apply modifiers to it.
- Stop when a requested change touches an armature, skin weights, or shape
  keys; route that work through `blender-fit-rigged-apparel`.
- Do not use AI-generated or third-party topology, UVs, generated materials,
  or textures as a modeling recipe.
- Do not hide Boolean cutters or control objects in unlabelled collections.
- Do not infer visual success from a valid mesh or triangle count alone.
- Treat the first visually reviewable pass as a checkpoint, not a final
  deliverable.
- Resolve silhouette, proportion, depth, and construction mismatches before
  spending time on decorative hardware, materials, decals, or microdetail.
- Keep reference fidelity, construction realism, and surface realism as
  separate claims. A model may match a silhouette while its hidden depth is
  inferred, or have realistic materials on stylized proportions.
- Do not silently "improve realism" by changing the style contract. Correct
  fidelity errors and revise deliberate proportions as separate operations.
- Do not model logos, labels, scratches, or printed marks as permanent mesh
  relief merely because they appear in the reference. Record them for a
  future decal/material/bake stage.
- Do not approximate a continuous ring, shell, or revolved body with repeated
  disconnected panels when a torus, cylinder, sphere, revolved profile, or
  other matching base topology can own the form directly.

## Deliverables

- Staged `.blend` files with source-stage lineage.
- Named source/control/output collections and retained modifier stacks.
- Operation manifest, inspection report, validation report, and fixed views
  from each substantial review stage.
- An iteration log containing the ranked self-critique, evidence view, intended
  correction, result, and remaining limitations for each reviewed stage.
- Versioned style contract with decisive ratios and intended review distance
  when appearance is part of acceptance.
- Primitive-decomposition table with continuous masses, repeated parts,
  attachment boundaries, and mandatory seam/overlap checks.
- Reference image fingerprint, calibration, packed reference object, measured
  landmarks, inferred-depth notes, and overlay preview when applicable.
- For body-worn assets, a non-export body-fit silhouette or cage, sampled
  clearance evidence, clean views, and diagnostic overlay/X-ray views.
- A short list of unresolved visual decisions requiring human judgment.
