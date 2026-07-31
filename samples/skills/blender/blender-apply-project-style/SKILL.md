---
name: blender-apply-project-style
description: Apply a repository's own art-direction, performance, renderer, and export constraints to otherwise project-neutral Blender skills. Use when adapting general modeling, materials, reference matching, texture baking, or engine-export workflows to a specific game's or visualization project's documented style contract.
---

# Blender Apply Project Style

Keep general modeling and material logic in portable Blender skills. Use this
skill as a thin repository-owned overlay.

## Required selection

1. Locate the project's canonical art-direction and graphics-pipeline
   documentation. Stop if no authoritative source exists and the missing
   choice would materially change the result.
2. Select the closest portable style layer, such as
   `blender-style-grounded-realism` or
   `blender-style-clean-stylized`.
3. Apply `blender-model-low-poly-assets` only when the asset has an explicit
   performance, LOD, topology, or platform budget.
4. Record project-specific renderer, unit, scale, naming, material, bake,
   preview-distance, collision, LOD, and export requirements in the asset's
   style contract.
5. Keep project rules here or in project documentation. Do not fork the
   general modeling skills merely to change one project's aesthetic.

## Project boundaries

- Keep geometry style, reference fidelity, material realism, and topology
  budget as separate decisions.
- Do not infer that low-poly means toon-styled or that realism means
  hyperreal/cinematic fidelity.
- Define the target renderer and transfer path explicitly. Blender procedural
  nodes rarely transfer directly through interchange formats.
- Validate at the project's intended review distance and under representative
  destination lighting.
- Keep generated, downloaded, or externally derived asset rights and
  provenance explicit.

## Deliverable

Add a `project_profile` section to the versioned style contract:

```json
{
  "project_profile": {
    "name": "example-project-style",
    "render_target": "Example Engine / Renderer",
    "unit_scale": "1 unit = 1 meter",
    "default_style": "grounded-realism",
    "low_poly_allowed_when_form_preserved": true,
    "procedural_material_transfer": "bake approved PBR channels"
  }
}
```

Replace every example value with repository-owned decisions before using the
contract as acceptance evidence.
