# Medieval Weapon Construction in Blender

## Establish a weapon contract

Record:

- weapon family and whether it is historical, historically inspired, or
  fantasy;
- real-world or game-scale total length;
- blade/head, haft, guard, grip, and pommel/poll ratios;
- primary and secondary grip locations;
- intended camera distance and first-person/third-person use;
- object-space symmetry;
- local axes and pivot;
- cross-section type and thickness landmarks;
- edge condition and sharpening band;
- attachment method;
- evaluated polygon budget;
- style exaggerations and material roles.

If an authoritative dimension is unavailable, label the value as a design
assumption. Do not disguise a pleasing ratio as historical evidence.

## Reference reconstruction

For a side image:

1. Determine whether the camera is orthographic or perspective.
2. Establish a single image-to-world scale from one agreed dimension.
3. Mark the centerline, grip bounds, head/blade bounds, tip, heel, beard, poll,
   guard, shoulder, fuller, edge seam, or other decisive landmarks.
4. Sample clean arcs and line segments; ignore compression artifacts, lighting,
   wear, and subpixel irregularity.
5. Trace only the axes the image constrains.
6. Infer cross-sections from construction references or declare them.
7. Validate the aligned silhouette and independent edge-on view.

For a three-quarter reference, first decide which apparent differences are
foreshortening. Author one canonical half for a symmetric head and mirror it.

## Weapon-family patterns

### Sword

Model as an assembly:

- blade profile and distal taper;
- explicit blade cross-sections at several stations;
- center ridge, fuller, hollow, flat, or lenticular section only when intended;
- ricasso or shoulder transition when present;
- tang passing into the grip;
- guard with hand clearance;
- grip core and wrap;
- pommel or cap that closes the construction.

Start with the blade's center plane or half profile, then establish thickness.
Use longitudinal loops or controlled profile stations where the cross-section
changes. A groove may use inset topology, a retained Boolean, or a high-to-low
bake depending on scale and budget.

### Axe

Separate:

- eye or socket;
- cheek/body;
- bit and sharpened edge wedge;
- toe, heel, beard, horn, and poll as applicable;
- haft and any wedge, langet, or reinforcement.

The edge insert should own the visible outer cutting arc when it is a distinct
wedge. Do not leave a full-size cheek behind it that occludes the edge.

Check the haft through the eye from top and bottom. A stylized axe may enlarge
the bit, but the attachment still needs a readable load path unless the style
contract explicitly embraces magical construction.

### Mace and war hammer

Use a longitudinal shaft plus a controlled radial head:

- retain one flange, stud, or striking-face source;
- repeat with Array plus object offset or Geometry Nodes;
- preserve exact radial count and rotation;
- distinguish striking faces, beak, crown, and central core;
- model the socket or tang relation to the shaft.

Avoid high segment counts that erase the intended faceting. Validate rotational
symmetry and the evaluated merge or intersection strategy.

### Polearm

Treat it as a head assembly attached to a long handling shaft:

- blade, hook, spike, hammer, or fork components;
- central socket;
- langets or straps when present;
- shaft taper and grip zones;
- butt cap or shoe when present.

Review the full-length silhouette and a close construction view. A correct
head can still fail when its shaft is too short, thick, thin, or visually
unbalanced.

### Shield

Define:

- plan shape;
- curvature or dish;
- shell thickness;
- rim;
- boss;
- grip, straps, or enarmes;
- arm and hand clearance;
- front decoration as a later material/decal task when appropriate.

Use a curved surface plus Solidify for many shields, but validate the rear
hardware and held orientation. A front-only disc with no grip is not a
constructed shield.

## Style-aware proportion choices

### Toon or heroic

- Enlarge one primary read, such as blade, axe bit, hammer face, or shield
  boss.
- Shorten or thicken the handle only as an explicit design decision.
- Use few decisive profile changes and broad bevels.
- Enlarge secondary hardware sparingly.
- Prefer simple material/value blocks and restrained surface detail.

### Grounded

- Preserve handling length, grip space, physical thickness, taper, and assembly
  ratios.
- Keep bevel widths at plausible scale.
- Use construction detail to explain attachment, not to decorate.
- Reserve asymmetry for wear, hand-built variation, or an asymmetric weapon
  family.

A stylized weapon can remain mechanically plausible. A grounded material does
not make heroic proportions grounded.

## Geometry and material boundary

Keep in geometry:

- silhouette;
- tip, horn, beard, hook, guard, and pommel profiles;
- major cross-section ridges and fullers visible at gameplay distance;
- sockets, eyes, grips, and attachment hardware;
- large wrap thickness and shield curvature.

Prefer material, decal, or bake:

- fine scratches;
- shallow hammer marks;
- maker marks and painted emblems;
- tiny engravings;
- micro wood pores;
- small leather grain;
- sharpening striations.

Use a distinct material role for polished cutting edges when the rough head or
blade body differs. The mesh split is optional; the semantic mask is required.

## Review checklist

- Profile matches the declared reference and scale.
- Opposite side confirms real symmetry or intended asymmetry.
- Edge-on and top views confirm thickness and taper.
- All points remain sharp enough for the style.
- The blade edge reads as a wedge, not a sticker.
- Head-to-haft, blade-to-grip, and hardware ratios match the contract.
- Assembly intersections and load paths are plausible.
- A simple hand/arm proxy has grip and guard clearance.
- Pivot and local axes support intended engine attachment.
- Base and evaluated polygon counts meet the budget.
- Decorative detail has not hidden a high-impact shape error.
