# Primitive And Base-Shape Decomposition

Choose topology from the object's underlying masses before choosing modifiers
or decorative features. The purpose is not to use primitives literally; it is
to begin with loop flow and continuity that already agree with the target.

## Decomposition record

Before blockout, record one row per base mass:

| Field | Decision |
|---|---|
| Semantic mass | The continuous volume or surface this part owns |
| Topological class | Ring, revolved shell, closed volume, open patch, profile extrusion, beam, repeated module, or other declared class |
| Base primitive | Torus, cylinder, sphere/egg, cone, cube, plane, curve, or authored profile |
| Local axis and origin | Axis of revolution/deformation and functional pivot |
| Modification | Ring scaling, loop reshaping, extrusion, taper, bend, Boolean, Solidify, or another bounded operation |
| Boundary | Where it joins, overlaps, clears, or remains separate from another mass |
| Continuity contract | Closed/welded, intentionally open, or intentionally segmented |
| Evidence | Views and numeric checks that can prove the decision |

Use the fewest masses that explain the construction, not the fewest Blender
objects. One continuous mass may contain several semantic regions, while an
assembly with genuinely separate manufacture or motion may need several base
shapes.

## Match the primitive to the form

- Use a torus or cylinder-derived annulus for a continuous circlet, hoop,
  collar, barrel body, pipe, rim, or other ring-based form.
- Use a cylinder, cone, or revolved profile when loop stations should control
  radial breadth along one axis.
- Use a sphere or egg-like ring topology for an anatomy-following cranial or
  rounded shell.
- Use a planar profile extrusion for a blade, plate, bracket, or other form
  whose decisive information is a two-dimensional outline plus thickness.
- Use a station loft for a hull, fuselage, vehicle body, or other long volume
  whose cross-section, centerline height, and breadth change together. Author
  sparse transverse rings at decisive stations, keep vertex correspondence
  across rings, and control sheer/rocker, taper, bilge, and upper-side tuck as
  separate profile decisions. Review the loft from end-on and low grazing
  views; a convincing side silhouette can still conceal a box-like or
  canoe-like section.
- Use a cube or beam only when broad planar faces and rectangular section are
  genuinely part of the design.
- Use curves for paths, cords, trim, and rails when path continuity is more
  important than hand-authored vertex correspondence.

Do not start from a cube merely because it is convenient when the target's
identity is revolved, annular, or organic. Bevels and smooth shading cannot
replace missing topological curvature.

## Continuous forms versus repetition

Reserve Array, radial duplication, and Geometry Nodes repetition for parts
that are actually repeated: teeth, rivets, shingles, merlons, ribs, separate
ornaments, or modular segments.

Do not use repetition to impersonate one continuous manufactured surface. A
ring assembled from repeated vertical plates can leave a first/last gap,
overlap, tangent mismatch, normal discontinuity, or thickness change even
when the front view looks acceptable. Build the ring from closed annular
topology, then add true repeated features onto it.

When segmented construction is intentional:

- retain the source element and radial control;
- define the exact angular step and count;
- test the first/last boundary independently;
- state whether neighboring parts overlap, touch, weld, or leave a designed
  gap;
- inspect the complete 360-degree result from front, rear, both sides, top,
  and grazing light.

## Multi-mass assemblies

Split a complex asset when different regions need incompatible topology,
manufacture, movement, materials, or iteration cadence. Typical examples are
a continuous crown band plus rolled rims and separate ornaments; a weapon
blade plus guard, grip, and pommel; or an armor shell plus articulated lames
and straps.

For every split, define who owns the visible silhouette and how the parts
meet. Avoid coincident faces, unexplained floating pieces, hidden gaps, and a
decorative part that falsely appears to carry structural continuity.

For a sailing rig or another structure carrying suspended membranes, split
the load-bearing scaffold from the cloth before adding surface detail. Model
each mast as a continuous tapered pole or a declared set of overlapping mast
stages, each yard/boom as an axis-correct spar, and collars/platforms/bands as
separate manufactured attachments. Review this bare scaffold as its own
blockout. A sail is then a bounded thin shell attached to declared support
edges, not an infinitely thin plane and not a material effect. Give it enough
grid resolution for controlled camber, lower-edge sag, and restrained ripple;
use cloth simulation only when animation or physical settling is actually in
scope. Geometry owns the silhouette and billow, while the material owns weave,
panel seams, staining, and other sub-silhouette response.

For stepped floors, decks, platforms, or terraces, treat every elevation
change as an attachment boundary in its own right. A raised slab plus two side
walls is still open at its step face. Add a transverse bulkhead/riser, columns,
or another declared support condition across that boundary unless the design
is intentionally cantilevered or open. Seat the support into both adjacent
levels and inspect it from the direction a viewer would approach the step.
Declare which wall face owns the visible deck boundary. Put the wall thickness
under or behind the supported level so it does not project past the deck lip,
then bridge the exposed wall-to-side-support and wall-to-deck edges with
plausible posts, beams, trim, or another explicit joint. Doors and windows do
not repair a floating or mismatched boundary; add them only after the wall
plane and its perimeter fit are correct.

## Blockout gate

Do not advance from blockout until:

- each major mass reads from all principal views;
- every continuous form is closed or explicitly open;
- the first/last seam of every circular or repeated construction is inspected;
- attachments have plausible overlap or clearance;
- primitive choice and loop flow can support the intended later curvature;
- no modifier or material is being relied upon to disguise a wrong base
  topology.

For a station-lofted form, the gate also requires explicit end conditions.
Declare whether each end converges to a stem/point, closes with a transom or
cap, or remains intentionally open. Do not let a repeated station stand in for
a physically different terminal construction.
