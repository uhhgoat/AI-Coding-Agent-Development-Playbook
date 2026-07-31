# Blender Asset Style Profiles

Use profiles as starting points. The contract axes remain authoritative, and a
hybrid may deliberately mix them.

## Core axes

Record each axis independently:

| Axis | Questions |
|---|---|
| Reference fidelity | Is the result approximate, landmark-matched, overlay-matched, or unconstrained? |
| Proportion strategy | Are real ratios preserved, selectively pushed, or strongly exaggerated? |
| Construction plausibility | Would the parts plausibly fit, carry load, sharpen, fasten, and be manufactured? |
| Shape language | Is the form restrained, angular, rounded, chunky, delicate, or graphic? |
| Visual hierarchy | Which element must read first, and from what distance? |
| Geometry detail | Which features affect silhouette, planes, seams, and bevels? |
| Material realism | Are surfaces broad and illustrative, physically grounded, or reference-matched? |
| Surface frequency | How much macro, mid-frequency, and micro color/roughness/normal variation is allowed? |
| Wear narrative | Is wear absent, decorative, gameplay-readable, or caused by plausible use? |
| Presentation | Is the asset judged in orthographic matching, close beauty renders, or gameplay views? |

Do not collapse these into a single label. A model can be overlay-matched but
stylized in depth, or have realistic materials on heroic proportions.

## Stylized heroic / toon-readable

Choose this when silhouette impact and immediate recognition matter more than
literal construction.

- Make the dominant functional element carry the design. A battleaxe may use
  oversized blades and head mass, a shorter or thicker haft, enlarged collars,
  rivets, wraps, and sockets, and more dramatic blade curvature.
- Simplify secondary construction and reduce small offsets, fasteners, and
  transitions that would disappear at gameplay distance.
- Use broad, deliberate planes and larger bevels. Preserve a few strong points,
  not many small contour changes.
- Use clear color/material blocks, smooth shading, restrained roughness
  breakup, and sparse normal detail. Let silhouette and value separation do
  most of the work.
- Keep wear selective and graphic. Avoid uniform procedural noise.
- State that the result is stylized even if metal, wood, or leather becomes
  more physically convincing later.

The first double-battleaxe fixture is the project example: its mirrored
construction fixed a perspective-reading error, but the enlarged head/blades,
shorter shaft, oversized hardware, broad bevels, and smooth low-frequency
materials still make it heroic/toon-styled and only approximately matched to
the reference.

## Low-poly / toon medieval armor

Choose this when a body-worn set needs a small evaluated budget, broad
readable planes, and a deliberate cartoon or game-readable silhouette.

- Define low-poly and toon independently. Low-poly controls where geometry is
  spent; toon controls proportion, contours, facets, hierarchy, and surface
  response.
- Fit the inner armor envelope to a known body or labelled generic cage before
  exaggerating the outer silhouette.
- Concentrate geometry at the torso taper, neck and arm openings, joint
  clearances, overlap boundaries, helmet profile, knees, ankles, and other
  silhouette-critical changes.
- Use a few designed planes. Do not accept arbitrary Decimate facets as a
  finished style.
- Let one or two components dominate, such as helmet, shoulders, chest, or
  greaves. Keep the remaining hardware subordinate.
- Make shoulder, waist, hip, knee, and foot plates advance along the protected
  body or limb like articulated shingles rather than coincident stacks.
- Keep underlayers and material blocks simple: main metal, edge/trim, leather,
  cloth or mail, and sparse accents.
- Use quiet roughness variation and sparse surface normals. Preserve the
  geometry's broad planes and value grouping.

Report body-fit evidence separately as generic static, known-body neutral, or
known-body pose-swept. A toon proportion decision does not excuse body
intersections, closed joint openings, a front-only belt, or unsupported armor.

## Stylized low-poly medieval architecture

Choose this when houses, castles, or villages should read clearly at gameplay
distance with reusable low-cost modules.

- Establish human scale, footprint, floor masses, roof pitch, skyline,
  openings, and circulation before timber, stone, or prop detail.
- Push a small number of structural reads: roof mass, tower height, gate,
  timber rhythm, eaves, buttresses, or battlements.
- Use coherent taper, lean, bow, and asymmetry. Independent random deformation
  produces noise rather than authored charm.
- Repeat from a small variant set and preserve exact logical snap dimensions
  beneath decorative overhangs.
- Keep eaves, ridge, visible roof courses, major beams, crenellations, large
  stones, and broken silhouettes in geometry. Put grain, pores, mortar, small
  cracks, moss, soot, and stains into materials, decals, or bakes.
- Prefer restrained material palettes and grouped value changes. Surface
  contrast should reinforce the large building masses.

State whether the design is merely medieval-fantasy, historically informed, or
historically verified. A charming fantasy silhouette is not historical
evidence.

## Grounded reference-matched realism

Choose this when believable scale, function, and reference fidelity lead the
design.

- Calibrate the declared view and preserve measured head-to-handle,
  thickness-to-width, grip, taper, socket, and edge ratios.
- Separate image-measured dimensions from inferred depth. Infer hidden
  construction from real manufacturing and use, not from visual convenience.
- Keep exaggeration near zero unless the contract names a specific exception.
- Use restrained bevels and transitions at plausible physical scale.
- Build material identity from coherent structure at multiple weak
  frequencies: growth rings and vessels for cut wood; forged macro variation,
  pitting, directional scratches, roughness, and edge polish for iron.
- Tie wear to contact, sharpening, handling, moisture, grain direction, and
  manufacturing. Fine detail should live more strongly in roughness and normal
  than in high-contrast color.
- Review both the calibrated view and independent perspective/edge-on views.

The side felling-axe fixture is the project example: its roughly `0.902 m`
overall length, `0.192 m` head span, and inferred `0.048 m` depth are governed
by one calibrated side view and explicit landmarks. Its polished handle uses
a virtual-log growth-ring structure with weaker vessels; the head separates
rough hammered iron from a polished sharpened edge. Those material choices
support, rather than create, its grounded construction.

## Hybrid profiles

Name the hybrid by its leading decisions, for example:

- `reference-faithful-stylized`: match the declared silhouette closely but
  simplify depth, construction, and surface frequencies;
- `grounded-heroic`: preserve plausible assembly and material scale while
  selectively enlarging one gameplay-critical element;
- `realistic-geometry-clean-materials`: preserve physical proportions but use
  smooth, quiet surfaces for readability or budget.

For a hybrid, list the deliberate departures from the nearest base profile.
Review those departures as design choices, not modeling errors.
