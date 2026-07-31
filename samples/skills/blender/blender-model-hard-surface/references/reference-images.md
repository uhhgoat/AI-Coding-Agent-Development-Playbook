# Calibrated 2D Reference Images

Use an orthographic or low-perspective image to constrain a declared view.
Do not claim that one view determines hidden construction.

## Recap before geometry

Before tracing, write a short reference recap:

- identify the declared view, likely lens/perspective strength, and which axes
  the image actually constrains;
- decide whether apparent asymmetry belongs to the object or to perspective
  foreshortening. If a nominally symmetric object is merely shown in three
  quarters, author one canonical side and mirror it;
- name the primary impact/readability element and the strongest silhouette
  landmarks;
- record decisive ratios such as head-to-handle, blade-to-socket,
  thickness-to-width, grip taper, and fitting size;
- separate requested style from observed image fidelity through
  `blender-define-asset-style`.

Do not begin from a list of primitives alone. A correct primitive vocabulary
can still produce the wrong proportions and style.

## Calibrate before modeling

1. Record the source path, pixel dimensions, checksum, and rights/provenance
   note.
2. Decide whether the image is orthographic enough for direct measurement.
   If perspective is meaningful, rectify it or use multiple views.
3. Choose a visible landmark as the image/world origin.
4. Derive one uniform `meters_per_pixel` value from an agreed real dimension.
5. Convert every traced landmark with the same mapping. Do not independently
   scale pieces until they appear to fit.
6. Record which dimensions are image-measured and which are physical
   inferences.

## Blender setup

- Copy the image into the ignored task artifact directory.
- Load and pack it into the staged `.blend`.
- Add an Image Empty in a `REFERENCE` collection, aligned to the declared
  orthographic view, with reduced opacity and `BACK` depth.
- Keep the reference outside `OUTPUT` and `EXPORT`.
- When rendered evidence is required, create a separate image-textured
  `PREVIEW` plane. Hide it from ordinary renders and export.
- Store the image size, origin pixel, scale, view axis, and image object name
  as manifest data and custom properties.

## Model and validate

- Sample intentional silhouette landmarks rather than tracing compression,
  shadows, texture edges, or one-pixel noise.
- Preserve sharp functional landmarks; smooth incidental jaggedness.
- Use the 2D profile to drive the measured axes. Infer depth from plausible
  construction, real dimensions, or another view.
- Render an exact-aspect overlay with a translucent high-contrast model over
  the source image.
- Render perspective and edge-on views without the image to inspect depth,
  intersections, and construction.
- Run
  [`../../shared/scripts/validate_reference_silhouette.py`](../../shared/scripts/validate_reference_silhouette.py)
  with landmark targets
  and an explicit meter tolerance. Treat structural proximity as evidence,
  not as a human visual pass.

## Body-envelope fit references

For armor or another body-worn hard-surface form, use a body reference before
accepting proportions:

1. Prefer the known target character. When none is available, create a clearly
   labelled generic diagnostic silhouette and three-dimensional torso cage.
   Record its dimensions and provenance; never present it as a verified
   anatomical standard or project-character fit.
2. Align front and side references to one height, origin, and uniform world
   scale. Pack the front silhouette as an Image Empty in `REFERENCE`, and keep
   any rendered plane or cage in `PREVIEW` or `BODY_FIT_REFERENCE`, outside
   `OUTPUT` and `EXPORT`.
3. Define shell thickness and minimum/preferred clearance before reshaping.
   Sample at the waist, flank, lower rib cage, chest, upper chest, neckline,
   shoulder, and arm opening. Compare the armor's inner surface with the body
   envelope, not the armor's outer silhouette.
4. Reject both intersections and excessive empty volume. Armor should remain
   outside the body by the declared shell, garment, and motion allowance while
   still tracking the chest-to-waist and front-to-back shape closely.
5. Render a clean front view, a flat silhouette overlay without diagnostic
   shadows/cavity, and side/three-quarter X-Ray views of the three-dimensional
   cage. A hidden body cage or a clearance number without inspected images is
   insufficient evidence.
6. Treat static fit as a modeling proportion gate only. A silhouette cannot
   establish hidden depth, and a neutral cage cannot establish pose clearance,
   skinning, shoulder articulation, or deformation. Route known-character and
   pose-sweep work through `blender-fit-rigged-apparel`.

## Style and evidence labels

Report these independently:

- `reference fidelity`: approximate, landmark-matched, or overlay-matched for
  the declared view;
- `construction realism`: stylized, plausible inference, or verified from
  additional evidence;
- `surface realism`: placeholder, procedural, baked, or reference-matched.
- `body fit`: untested, generic-static-envelope, known-body-neutral, or
  known-body-pose-swept.

For example, the first double-battleaxe fixture is stylized and only
approximately reference-matched even though its later procedural materials
are more realistic. Its enlarged head and blades, shortened haft, oversized
hardware, broad bevels, and smooth low-frequency surface response remain
heroic/toon-styled. Do not shorten that to "realistic axe."

The side felling-axe fixture instead uses a calibrated side view, restrained
physical ratios, plausible inferred depth and assembly, and multi-scale wood
and forged-metal response. Its realistic reading comes from agreement between
geometry, construction, and surfaces, not from shader detail alone.

## Decal boundary

Log logos, maker marks, painted graphics, labels, engravings, and local damage
as future decal/material tasks. Do not permanently emboss them into the model
unless the physical reference proves they have meaningful depth.

A future `blender-author-decals` skill should decide among:

- UV or mesh decals baked into texture maps;
- floating decal geometry for Blender previews;
- height/normal decals for shallow physical marks;
- target-engine decal projectors, deferred overlays, or equivalent runtime
  decal systems.

It must record source rights, mapping, color/normal/roughness channels,
z-fighting and draw-call implications, bake behavior, and Unity validation.
