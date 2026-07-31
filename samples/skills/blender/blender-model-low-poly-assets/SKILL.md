---
name: blender-model-low-poly-assets
description: Model or optimize Blender assets to an explicit low-polygon budget while preserving silhouette, cross-section, deformation, openings, modular seams, and stable shading. Use alongside either grounded-realism or stylized style skills when a real-time prop, character, armor set, weapon, building, environment module, or LOD needs deliberate topology rather than automatic decimation.
---

# Blender Model Low-Poly Assets

Treat low-poly as topology allocation and evaluated cost, not an art style.

## Workflow

1. Read the asset style contract and the relevant domain modeling skill.
2. Record target platform, camera distance, on-screen size, base/evaluated
   triangles, material slots, UV/bake path, rig/deformation needs, and LOD role.
3. Preserve a source or high-detail stage. Work on a recoverable low stage.
4. Establish silhouette, major cross-sections, joints, openings, hard/soft
   transitions, modular seams, and material boundaries before reducing loops.
5. Spend geometry where it changes silhouette, motion, shading, or connection.
   Remove hidden, planar, redundant, and sub-pixel structure first.
6. Use clean retopology, controlled dissolve, limited planar reduction, or a
   manually reviewed Decimate starting point. Never accept automatic output
   without silhouette and normal review.
7. Use smoothing groups, marked sharp edges, weighted/custom normals, and
   restrained bevel geometry deliberately. Do not use normal tricks to hide a
   broken silhouette.
8. Bake high-frequency form when it survives the target texel density. Keep
   silhouette, deep seams, cutting edges, plate thickness, roof edges, and
   joint openings in geometry.
9. Review object-space and camera-space silhouettes, wireframe density,
   grazing highlights, UV distortion, rig pose sweep if applicable, and engine
   import.
10. Compare each LOD at its transition distance and remove detail only when
    the transition remains stable.

## Geometry versus maps gate

Before modeling repeated construction detail, ask whether it changes the
silhouette, creates a deep opening, affects motion/collision, or needs a true
material boundary. If none apply at the intended distance, keep it in UVs,
shading, normals, height, or baked maps.

For simple rotational props such as barrels, drums, jars, pipes, and capped
containers:

- start from one cylinder or revolved profile and spend loop cuts only on the
  silhouette-changing taper, bulge, neck, or shoulder;
- inset and extrude end faces from that same shell when separate lid/head
  volumes do not change the runtime silhouette;
- consolidate repeated rings or bands into one mesh and keep their radial and
  vertical thickness subordinate;
- move plank seams, board divisions, fasteners, shallow joints, scratches, and
  small edge rounding to the later UV/material/normal stage;
- do not add Bevel, Subdivision, or Weighted Normal modifiers by habit. Compare
  the unmodified smooth/flat face assignment first and add geometry only when a
  fixed close or gameplay view proves it necessary.

Preserve a detailed construction stage when it remains useful as a bake source
or design reference, but do not treat that source as the runtime mesh by
default. Record object, base-triangle, evaluated-triangle, modifier, and
material-slot reductions between stages.

## Style composition

- With `blender-style-grounded-realism`, preserve realistic proportions,
  plausible curvature, restrained bevels, and smooth but not inflated forms.
- With `blender-style-clean-stylized`, preserve designed planes,
  exaggerations, and primary contour breaks.

The same triangle count can support either style. Do not flatten grounded
anatomy into boxes, and do not smooth away intentional stylized facets.

## Deliverables

- Source/high and low or LOD stages with evaluated triangle counts.
- Per-component topology budget and reduction notes.
- Silhouette, wireframe, grazing-light, normal, UV, and intended-distance
  previews.
- Bake/geometry boundary and any deformation or modular-seam evidence.
