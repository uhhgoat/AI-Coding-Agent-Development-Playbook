# Iterative Visual Review for Hard-Surface Modeling

Technical validity is necessary but does not establish visual success. Use a
preserved, evidence-backed iteration loop whenever shape, style, or reference
fidelity matters.

## Stage loop

For every substantial pass:

1. Save a new named `.blend` stage. Never overwrite the only preceding stage.
2. Run the structural checks appropriate to that stage.
3. Render the same fixed front, back, side, and three-quarter views. Include
   the intended gameplay or presentation distance when it differs.
4. For a calibrated image match, render an aligned overlay from each constrained
   reference view.
5. For a curved shell, add a wireframe view and a grazing-light view that makes
   highlight flow legible. Smooth beauty shading alone can conceal ruled
   surfaces, planar end caps, pinching, and rectangular cross-sections.
6. Inspect the images, compare them with the reference and preceding stage,
   and write a ranked self-critique.
7. Correct the highest-impact discrepancy that is unambiguous and within the
   current style contract.
8. Repeat until the stop conditions below are satisfied.

Useful stage names are:

- `stage-00-blockout`: overall envelope, silhouette, proportions, and axes.
- `stage-01-construction`: thickness, layering, intersections, and attachment
  logic.
- `stage-02-detail`: bevel hierarchy, functional hardware, panel breaks, and
  other secondary geometry.
- `stage-03-correction` or later: any additional pass needed to clear a
  high-impact mismatch found in review.

The names describe intent, not a mandatory three-pass limit.

## Review order

Review in this order so detail does not hide a bad foundation:

1. Reference framing, projection, orientation, and actual symmetry.
2. Macro silhouette, total proportions, mass distribution, and negative space.
3. Construction plausibility, depth, thickness, layer order, contact, and
   intersections.
4. Secondary forms, fasteners, straps, sockets, seams, and readable functional
   hierarchy.
5. Bevel hierarchy, shading continuity, and only then decorative geometry.

Do not optimize low-impact details while a higher-impact issue is still visible.

For a multi-level assembly, inspect every change in floor or deck elevation
from both travel directions. Side support does not prove that the transverse
step face is enclosed; an absent bulkhead or riser can make an otherwise
closed slab read as a floating shelf.
After adding the support, use a focused transition crop to compare its exposed
face with the terminal plane of the upper level. Look for a half-thickness
projection, a dark open edge, a floating top beam, or an unsupported side
gap. If the wall carries doors or windows, keep their frames and hardware
separate enough to read at the intended distance and verify that they sit on
the visible face rather than intersecting the deck lip.

For masts, antennae, spars, cables, or sails, preserve and review a bare-support
checkpoint before adding the suspended surfaces. Compare mast stations,
heights, rake, spar spans, taper, and deck clearance from both broadsides, bow,
stern, top, and a three-quarter silhouette. After adding sails, repeat those
views and add a near-edge view: a convincing face-on sail can still hide
excessive billow, intersecting courses, an unclosed shell, or a yard that no
longer appears to support its upper edge. Treat rigging/ropes as a separate
scope decision rather than silently using them to rescue weak mast or sail
placement.

For annular, revolved, or radially repeated work, make full-circumference
continuity part of macro review. Inspect front, rear, both side views, top,
and grazing light; then isolate the first/last angular boundary. A clean front
silhouette does not excuse a rear gap, overlapping end segment, tangent break,
or local thickness jump.

When the same high-impact volume error survives a smoothing, bevel, normal, or
subdivision pass, stop tuning the modifier stack. Compare the base wireframe
to the target volume and replace the primitive or loop flow. A successful
topology correction must be visibly different before shading is considered.

## Self-critique record

Record each discrepancy with:

- `severity`: `high`, `medium`, or `low`;
- `contract_axis`: such as reference fidelity, proportions, construction,
  shape language, or visual hierarchy;
- `observation`: what is visibly wrong, without prescribing the answer first;
- `evidence_view`: the preview or overlay that demonstrates it;
- `intended_fix`: the bounded geometric or modifier correction;
- `result`: fixed, improved, unchanged, or blocked;
- `residual`: any remaining limitation after the pass.

Severity means:

- `high`: wrong identity, silhouette, proportions, symmetry, major depth, major
  layer order, or visibly implausible construction.
- `medium`: secondary construction, local contour, attachment, hardware scale,
  or shading issue that affects quality but not identity.
- `low`: small bevel, spacing, or decorative refinement visible mainly nearby.

## Autonomous continuation

Continue without asking the user when the correction:

- is clearly supported by the supplied reference and style contract;
- remains inside the requested modeling scope;
- is reversible because the prior stage is preserved; and
- does not touch protected rigs, weights, shape keys, source assets, or
  destructive finalization.

Ask for direction only when references conflict, hidden construction has
multiple materially different solutions, a subjective choice would revise the
style contract, or authorization is required for a risky or expanded action.

Do not use a screenshot handoff as a pause point when the screenshot itself
shows an objectively fixable high-impact mismatch.

## Stop conditions

A modeling pass is ready for user review only when:

- no known high-impact discrepancy remains;
- medium discrepancies are fixed or identified as reference limitations;
- required structural checks pass or have explicit non-blocking warnings;
- every required fixed view has been rendered and inspected;
- the previous recoverable stage and its evidence remain available; and
- the final self-critique states residual limitations honestly.

Human taste and appeal remain human judgments, but that does not excuse
stopping before objective reference and construction errors are addressed.

## Common armor failure example

A cuirass can be watertight and symmetrical while still reading incorrectly.
Horizontal wing-like shoulder plates, a boxy torso, floating collar shards,
and unsupported fasteners are high-impact visual failures. Correct shoulder
drape and overlap, chest and waist curvature, arm-opening shape, and attachment
logic before refining rivets, bevels, materials, or surface wear.

Rounded bevels do not make a rectangular shell anatomical. Review torso
cross-sections around the complete front-side-back perimeter, not only the
front silhouette. A form-fitting male cuirass should communicate a sternum
transition, paired pectoral volume, rib-cage breadth, side wrap, scapular/back
curvature, and chest-to-waist taper without copying a body as one smooth blob.

Layered shoulder armor should advance along an imaginary upper-arm axis like
roof shingles. Each lame owns a successive segment, partially overlaps its
neighbor, and preserves the arm aperture beneath the assembly. Four nearly
coincident full-size shells are a stack, even if their vertical offsets look
layered from one view.

Waist reinforcement and belts must be reviewed from side and back. A flat
front panel with buckle hardware is not a wraparound belt; author a continuous
perimeter band or explicit connected front, side, and back segments.

Do not judge body-worn proportions in isolation. Compare the shell with a
scaled body silhouette and, when depth matters, a three-dimensional body cage.
The inner armor surface should follow the body envelope with explicit
clearance: intersections fail fit, while a large unexplained gap produces the
same stretched or oversized reading as an excessively broad chest. Inspect a
clean front view, a flat body-silhouette overlay, and side/three-quarter X-Ray
views. Keep a generic static check separate from known-character neutral fit
and rigged pose clearance.

For a rigid head-worn prop, declare the seating plane and measure the actual
proxy-mesh cross-section at that plane. Do not infer clearance from an
ellipsoid's nominal object dimensions or from duplicated custom properties:
primitive tessellation and an offset seating plane can change the usable
width or depth. Compare the crown, circlet, or helmet inner boundary with the
measured proxy envelope on both principal axes. Correct a mismatched
non-export proxy before changing already-approved output geometry when the
proxy, rather than the asset, violates the declared envelope.
