# Texture Bake Contract

## Required inputs

Before baking, define:

- source objects and evaluated modifier state;
- target object;
- target UV layer;
- image resolution, file format, bit depth, and output directory;
- selected map type;
- ray distance or cage object;
- margin or dilation;
- tangent-space versus object-space normal intent;
- color-space treatment;
- material and smoothing state;
- deterministic render engine and sampling settings.

Stop if these are ambiguous.

## Manifest

Write one manifest for the bake set containing:

- source `.blend` fingerprint and Blender version;
- source and target object names;
- target mesh counts and UV layer;
- cage or ray settings;
- map name, semantic, resolution, format, bit depth, color space, and output path;
- normal-space and channel convention as configured;
- margin, samples, seed, and bake timestamp;
- warnings and validation result.

Do not infer a normal-map green-channel convention. Record the configured convention and verify it in Unity.

## Map handling

- Base Color is color data and should not contain baked lighting unless that is explicitly the deliverable.
- Roughness, Metallic, Ambient Occlusion, Height, masks, and normal maps are data maps; configure them as non-color data in Blender and with matching Unity import settings.
- Emission color is color data; emission masks are data.
- Normal maps require the correct Normal Map node and strength for Blender preview.
- Height may need higher bit depth when precision matters.

## Bake isolation

- Bake one semantic at a time to a clearly named image node.
- Ensure the intended image node is active on the target material.
- Hide unrelated objects from ray visibility or place them outside the bake set.
- Do not silently reuse a dirty image from a previous run.
- Save outputs to a new bake directory or versioned filename.

For several objects sharing one atlas, do not assume repeated bake operators
will preserve the prior object's pixels. A reliable deterministic route is:

1. bake each object and semantic to a fresh temporary image;
2. derive or bake an explicit occupancy/coverage mask per object;
3. verify those masks do not overlap after the configured dilation;
4. composite into the shared atlas against the semantic's correct background;
5. validate the composite before packing or assigning it.

Set the target image node active only after temporary override nodes have been
created. Record object order and per-object coverage in the manifest. Check
island spacing against two-sided dilation, not only raw UV polygon overlap.

Cycles may return valid RGB in a generated bake buffer while leaving alpha at
zero. Before PNG output, explicitly define alpha semantics. Use opaque alpha
for ordinary Base Color, data, normal, and AO maps; use `CHANNEL_PACKED` or an
equivalent non-premultiplied path when alpha carries data. Never trust a black
saved PNG merely because the in-memory RGB statistics were non-flat: reopen
or render the exact saved pixels.

## Cage, ray, and margin checks

- Inspect for missed rays, projection through nearby surfaces, hard-edge seams, skew, gradients, and cage intersections.
- Use a cage for difficult silhouettes or close overlapping parts.
- Make margin large enough for target mip levels and texture filtering.
- Test UV islands near image borders and mirrored or stacked UVs intentionally.

## Validation views

Produce:

- each map shown as a channel-appropriate diagnostic;
- the baked material on the target under fixed lighting;
- seam and high-curvature close-ups;
- a destination-engine import test using the actual renderer and material
  path.

A visually acceptable Blender preview does not validate Unity tangent basis, channel packing, compression, normal convention, or import color space.

## Output safety

- Never overwrite source texture images unless explicitly requested.
- Verify every expected output exists, has nonzero size, and matches its manifest dimensions.
- Verify saved files are finite and non-flat where variation is expected;
  compare their fingerprints with the manifest rather than validating only
  the temporary in-memory image.
- Report partial bake sets as incomplete rather than successful.
