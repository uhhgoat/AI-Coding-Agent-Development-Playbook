# Body-Worn Armor Construction

## Keep fit, style, and budget separate

Low-poly describes an evaluated geometry budget and the placement of that
geometry. Toon or stylized describes proportion, contour, plane design,
material response, and visual hierarchy. They may occur together, but neither
implies the other.

Record:

- target platform and intended on-screen size;
- base and evaluated triangle budgets by component or set;
- flat, smooth, mixed, or authored-normal shading strategy;
- deliberate facet size and orientation;
- realistic, restrained, heroic, chunky, cute, graphic, or other proportion
  strategy;
- reference-fidelity class;
- static-fit or rigged-fit evidence class;
- permitted silhouette exaggerations;
- material frequency and contrast;
- whether the armor is historically informed, fantasy-plausible, or purely
  invented.

Do not invent a universal triangle count. Spend geometry where it changes the
silhouette, joint opening, major plane, or deformation behavior.

## Build around an envelope

Use a known target body when available. A generic body cage is diagnostic only.

At minimum, describe or sample:

- neck base and shoulder slope;
- chest breadth and depth;
- sternum and paired pectoral transition;
- rib-cage side wrap;
- scapular/back curvature;
- waist breadth and depth;
- armhole position and diameter;
- pelvis and upper-thigh envelope for lower armor;
- knee, calf, ankle, and foot envelope for greaves and sabatons.

Define the armor's inner surface, shell thickness, garment allowance, and
motion allowance separately. Reject both intersections and unexplained empty
volume. A stylized silhouette may exaggerate the outer surface while its inner
clearance remains disciplined. A grounded silhouette should follow plausible
anatomy and garment allowance without becoming an inflated body copy.

## Segment by function

Use functional articulation zones rather than arbitrary decorative cuts.

| Region | Modeling concern |
|---|---|
| Cuirass | Front, side, and back form; chest-to-waist taper; arm and neck openings; closure logic |
| Gorget/collar | Neck clearance, shoulder relation, front/back overlap |
| Pauldron | Shoulder cap plus successive lames advancing along the upper-arm axis |
| Rerebrace/vambrace | Tapered limb shell, elbow clearance, strap/hinge assumption |
| Belt/waist band | Continuous wrap, buckle or closure, no flat front-only plane |
| Fauld/tassets | Descending waist/hip plates, overlap direction, hip and thigh clearance |
| Cuisses | Thigh protection that follows the limb without filling the hip or knee joint |
| Poleyns | Knee cap plus side wings that preserve flexion clearance |
| Greaves | Calf and shin asymmetry, ankle opening, believable closure |
| Sabatons | Overlapping toe plates and ankle articulation |
| Underlayer | Cloth, leather, or mail gap coverage; separate from rigid plate |

Treat every plate as protecting a region while leaving adjacent joints usable.
Large gaps may be intentionally covered by cloth, leather, or mail rather than
sealed with rigid metal.

## Useful construction stacks

### Close-fitting plate

1. Start with a sparse, clean surface patch following the body cage.
2. Add only enough support geometry for the intended contour and facets.
3. Use Mirror for a genuinely bilateral starting form.
4. Use Shrinkwrap with an explicit method, axis, project limit, and offset when
   the surface must track a cage.
5. Add Solidify for controlled thickness, checking face normals and
   non-uniform scale.
6. Add restrained Bevel only where edge catch-light is part of the style.
7. Use flat, smooth, sharp-edge, or custom-normal treatment deliberately.

The exact order can change. A Boolean opening before Solidify behaves
differently from one after it. Record the reason.

### Helmet bowl, visor, and liner

1. Build the brow, crown, rear bowl, and tail as one continuous shell unless
   the reference shows a real plate boundary. Do not accept two overlapping
   closed shells merely because the silhouette hides their contact shadow.
2. Choose topology whose natural curvature matches the protected anatomy. For
   a cranial bowl, prefer a UV-sphere/egg layout, a revolved profile, or another
   radial ring structure over a rectangular extrusion or open section loft.
   Cut or deform the opening after the bowl exists; spread and reshape complete
   rings to control brow width, temple breadth, crown flattening, rear volume,
   and tail flow.
3. Preserve a monotonic, tangent transition across any sewn forehead/crown
   patches. Review it with smooth shading and wireframe; a mathematically
   closed seam can still produce a visible fold.
4. Inspect real geometry under grazing light. If the silhouette, wireframe, or
   highlight still reads as a box or end cap, replace the base topology.
   Bevels, weighted normals, subdivision, and smooth shading cannot repair the
   wrong volume.
5. Establish the visor pivot before adding arms, rolled edges, or hardware.
   Give every moving visor component the same origin and local axis.
6. Test closed, intermediate, and raised positions. Separate intentional
   arm-to-shell riding contact from visor-to-shell and visor-to-face clearance.
   Label a rotated duplicate as a diagnostic preview unless an actual rig or
   animation has been validated.
7. Build the liner as a head-following suspension boundary with declared body
   clearance. Terminate inferred attachment tabs against the evaluated inner
   shell, not at guessed lengths that can protrude through the steel.
8. Permit contact only at declared liner attachment regions. Test the liner
   separately against both shell and body cage, and keep hidden construction
   labeled as inferred when the references do not expose it.

For scripted construction, direct per-vertex ring control is not a selection
limitation. Parameterize azimuth and latitude, then calculate each vertex from
the body envelope and reference landmarks. Vary front/rear radius, opening
latitude, crown profile, and local deformation weights explicitly. Keep the
outer and inner rings paired so thickness and the opening rim remain closed
and inspectable.

### Articulated lame

1. Draw one plate profile around the relevant limb or shoulder cross-section.
2. Give it independent thickness and a clear upper/lower boundary.
3. Place the next plate farther along the articulation axis.
4. Overlap by a declared amount and direction.
5. Vary width or curvature when required by the changing body envelope.
6. Test the aperture from front, side, underside, and X-ray views.

Duplicating one full-size shoulder shell four times with only vertical offsets
does not create articulated armor.

### Belt or strap

Use a closed mesh band, a curve with controlled bevel, or connected front,
side, and back segments. Keep buckles, loops, rivets, and free strap tails
separate until the wrap is correct.

### Designed faceted shell

Author a small number of large planes around the intended form. Do not rely on
random vertex reduction. Preserve:

- a readable front plane;
- side wrap instead of a ninety-degree box corner;
- controlled transitions at sternum, ribs, shoulder, waist, knee, and calf;
- stable plane orientation across mirrored sides;
- a small bevel or split-normal strategy only when it supports the chosen
  plane language.

## Visual hierarchy

For any armor set, choose a small hierarchy:

1. primary silhouette: helmet, shoulder span, torso taper, or leg profile;
2. secondary plate rhythm: pauldrons, faulds, greaves, or helmet bands;
3. tertiary hardware: buckles, rivets, straps, seams, and edge trims.

Do not enlarge every feature. Grounded work normally keeps exaggeration near
zero. A stylized dominant shoulder silhouette still loses impact when every
buckle, edge, and knee wing is also oversized.

Use placeholder material blocks during modeling:

- main metal;
- contrasting edge or trim;
- leather;
- cloth or mail underlayer;
- optional accent.

Keep them quiet enough that geometry errors remain visible.

## Stage gates

### Blockout gate

- The body cage, armor envelope, and full-set silhouette agree.
- Arm, neck, waist, hip, knee, ankle, and foot openings remain usable.
- No primary component reads as an accidental box or inflated body copy.
- Exaggerations match the style contract.

### Construction gate

- Every plate has thickness, overlap, attachment, and a protected region.
- Shoulder and lower-body lames advance along the correct articulation axis.
- Belts and straps wrap around their targets.
- Front-only reference information is not presented as verified hidden
  construction.

### Detail gate

- Bevel hierarchy and facet language remain coherent.
- Rivets and seams support construction rather than disguising it.
- Decorative asymmetry is intentional and does not break required bilateral
  fit.
- Geometry and material roles are ready for later baking or surfacing.

### Static-fit gate

Inspect:

- clean front/back/side/three-quarter renders;
- a front silhouette overlay;
- side and three-quarter X-ray views;
- close views through every opening;
- a gameplay-distance view;
- wireframe and evaluated topology.

Report `generic-static-envelope`, `known-body-neutral`, or
`known-body-pose-swept`; never collapse them into “fits.”

## Common failures

- **Minecraft torso:** rounded edges on a rectangular shell without chest,
  rib, side, back, or waist form.
- **Shoulder stack:** coincident large plates blocking the arm aperture.
- **Front-only belt:** buckle and leather plane with no perimeter wrap.
- **Detail camouflage:** rivets and scratches added while the silhouette or
  fit remains wrong.
- **Uniform decimation:** random facets that ignore anatomy and design planes.
- **Inflated body:** offsetting a body mesh uniformly without designing armor
  planes, openings, closures, and overlaps.
- **Shaded box:** smooth shading or subdivision applied to a section loft whose
  silhouette and wireframe still preserve rectangular corners or a planar end
  cap. Rebuild from anatomy-following radial topology.
- **Static-fit overclaim:** neutral clearance presented as animation-safe.
