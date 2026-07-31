"""Create staged grounded stone wall-tower modeling fixtures."""

import argparse
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import bmesh
import bpy


SCRIPT_VERSION = "0.1.0"
STYLE_PROFILE = "grounded-realism-low-poly"
ASSEMBLY_NAME = "OUT_StoneTowerAssembly"
OUTER_RADIUS = 3.60
INNER_RADIUS = 2.80
WALL_TOP = 9.25
PARAPET_TOP = 10.00
MERLON_TOP = 11.10
SEGMENTS = 48
DOOR_WIDTH = 1.40
DOOR_SPRING_HEIGHT = 1.52
DOOR_RADIUS = DOOR_WIDTH * 0.5
GROUND_THRESHOLD = 0.05
UPPER_THRESHOLD = 5.25


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--style-contract", type=Path, required=True)
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return parser.parse_args(argv)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (
        bpy.data.meshes,
        bpy.data.curves,
        bpy.data.materials,
        bpy.data.cameras,
        bpy.data.lights,
    ):
        for datablock in list(datablocks):
            if datablock.users == 0:
                datablocks.remove(datablock)


def ensure_collection(name):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    return collection


def move_to_collection(obj, collection):
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)


def create_empty(name, collection, role, parent=None):
    obj = bpy.data.objects.new(name, None)
    collection.objects.link(obj)
    obj.parent = parent
    obj["artifact_role"] = role
    obj["style_profile"] = STYLE_PROFILE
    return obj


def material(name, base_color, roughness, metallic=0.0):
    assigned = bpy.data.materials.new(name)
    assigned.diffuse_color = (*base_color, 1.0)
    assigned.use_nodes = True
    principled = assigned.node_tree.nodes.get("Principled BSDF")
    principled.inputs["Base Color"].default_value = (*base_color, 1.0)
    principled.inputs["Roughness"].default_value = roughness
    principled.inputs["Metallic"].default_value = metallic
    assigned["artifact_stage"] = "modeling_placeholder"
    assigned["style_profile"] = STYLE_PROFILE
    return assigned


def recalculate_normals(mesh):
    editable = bmesh.new()
    editable.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(editable, faces=editable.faces)
    editable.to_mesh(mesh)
    editable.free()
    mesh.update()


def add_bevel(obj, width, segments=2, angle=25.0):
    if width <= 0.0:
        return None
    modifier = obj.modifiers.new("ConstructionBevel", "BEVEL")
    modifier.width = width
    modifier.segments = segments
    modifier.limit_method = "ANGLE"
    modifier.angle_limit = math.radians(angle)
    return modifier


def create_mesh_object(
    name,
    vertices,
    faces,
    collection,
    parent,
    assigned_material,
    role="OUTPUT",
    bevel_width=0.0,
):
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.validate(verbose=True)
    recalculate_normals(mesh)
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.parent = parent
    obj["artifact_role"] = role
    obj["style_profile"] = STYLE_PROFILE
    if assigned_material is not None:
        mesh.materials.append(assigned_material)
    add_bevel(obj, bevel_width)
    return obj


def add_box(
    name,
    location,
    dimensions,
    collection,
    parent,
    assigned_material,
    role="OUTPUT",
    rotation=(0.0, 0.0, 0.0),
    bevel_width=0.0,
):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    move_to_collection(obj, collection)
    obj.parent = parent
    obj.data.materials.append(assigned_material)
    obj["artifact_role"] = role
    obj["style_profile"] = STYLE_PROFILE
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.select_set(False)
    add_bevel(obj, bevel_width)
    return obj


def create_annular_shell(
    name,
    outer_radius,
    inner_radius,
    bottom,
    top,
    segments,
    collection,
    parent,
    assigned_material,
    bevel_width=0.0,
):
    vertices = []
    for z in (bottom, top):
        for radius in (outer_radius, inner_radius):
            for index in range(segments):
                angle = math.tau * index / segments
                vertices.append(
                    (radius * math.cos(angle), radius * math.sin(angle), z)
                )
    outer_bottom = 0
    inner_bottom = segments
    outer_top = segments * 2
    inner_top = segments * 3
    faces = []
    for index in range(segments):
        nxt = (index + 1) % segments
        faces.extend(
            (
                (
                    outer_bottom + index,
                    outer_bottom + nxt,
                    outer_top + nxt,
                    outer_top + index,
                ),
                (
                    inner_bottom + index,
                    inner_top + index,
                    inner_top + nxt,
                    inner_bottom + nxt,
                ),
                (
                    outer_bottom + index,
                    inner_bottom + index,
                    inner_bottom + nxt,
                    outer_bottom + nxt,
                ),
                (
                    outer_top + index,
                    outer_top + nxt,
                    inner_top + nxt,
                    inner_top + index,
                ),
            )
        )
    obj = create_mesh_object(
        name,
        vertices,
        faces,
        collection,
        parent,
        assigned_material,
        bevel_width=bevel_width,
    )
    for polygon in obj.data.polygons:
        polygon.use_smooth = abs(polygon.normal.z) < 0.5
    return obj


def create_cylinder(
    name,
    radius,
    depth,
    z,
    segments,
    collection,
    parent,
    assigned_material,
    bevel_width=0.0,
):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=segments,
        radius=radius,
        depth=depth,
        location=(0.0, 0.0, z),
    )
    obj = bpy.context.object
    obj.name = name
    move_to_collection(obj, collection)
    obj.parent = parent
    obj.data.materials.append(assigned_material)
    obj["artifact_role"] = "OUTPUT"
    obj["style_profile"] = STYLE_PROFILE
    add_bevel(obj, bevel_width)
    return obj


def arch_profile(width, threshold, spring_height, samples=10, inset=0.0):
    half = width * 0.5 - inset
    spring = threshold + spring_height - inset
    points = [
        (-half, threshold + inset),
        (half, threshold + inset),
        (half, spring),
    ]
    for index in range(1, samples + 1):
        angle = math.pi * index / samples
        points.append(
            (
                half * math.cos(angle),
                spring + half * math.sin(angle),
            )
        )
    return points


def create_extruded_xz_profile(
    name,
    polygon,
    center_y,
    depth,
    collection,
    parent,
    assigned_material,
    role="OUTPUT",
    bevel_width=0.0,
):
    front_y = center_y - depth * 0.5
    back_y = center_y + depth * 0.5
    vertices = [(x, front_y, z) for x, z in polygon]
    vertices.extend((x, back_y, z) for x, z in polygon)
    count = len(polygon)
    faces = [tuple(range(count - 1, -1, -1)), tuple(range(count, count * 2))]
    for index in range(count):
        nxt = (index + 1) % count
        faces.append((index, nxt, count + nxt, count + index))
    return create_mesh_object(
        name,
        vertices,
        faces,
        collection,
        parent,
        assigned_material,
        role=role,
        bevel_width=bevel_width,
    )


def create_extruded_yz_profile(
    name,
    polygon,
    center_x,
    width,
    collection,
    parent,
    assigned_material,
    bevel_width=0.0,
):
    left_x = center_x - width * 0.5
    right_x = center_x + width * 0.5
    vertices = [(left_x, y, z) for y, z in polygon]
    vertices.extend((right_x, y, z) for y, z in polygon)
    count = len(polygon)
    faces = [tuple(range(count - 1, -1, -1)), tuple(range(count, count * 2))]
    for index in range(count):
        nxt = (index + 1) % count
        faces.append((index, nxt, count + nxt, count + index))
    return create_mesh_object(
        name,
        vertices,
        faces,
        collection,
        parent,
        assigned_material,
        bevel_width=bevel_width,
    )


def add_boolean(target, cutter, name):
    modifier = target.modifiers.new(name, "BOOLEAN")
    modifier.operation = "DIFFERENCE"
    modifier.solver = "EXACT"
    modifier.object = cutter
    return modifier


def create_door_opening(
    name,
    center_y,
    threshold,
    depth,
    controls,
    control_parent,
):
    cutter = create_extruded_xz_profile(
        name,
        arch_profile(DOOR_WIDTH, threshold, DOOR_SPRING_HEIGHT, samples=13),
        center_y,
        depth,
        controls,
        control_parent,
        None,
        role="CONTROL",
    )
    cutter.display_type = "WIRE"
    cutter.hide_render = True
    cutter["control_purpose"] = "true arched wall opening"
    return cutter


def create_door_leaf(
    name,
    center_y,
    threshold,
    outputs,
    assembly,
    wood,
):
    return create_extruded_xz_profile(
        name,
        arch_profile(
            DOOR_WIDTH - 0.14,
            threshold + 0.03,
            DOOR_SPRING_HEIGHT - 0.08,
            samples=12,
        ),
        center_y,
        0.10,
        outputs,
        assembly,
        wood,
        bevel_width=0.025,
    )


def create_arch_surround(
    prefix,
    center_y,
    threshold,
    outputs,
    assembly,
    dressed_stone,
):
    spring = threshold + DOOR_SPRING_HEIGHT
    inner_radius = DOOR_RADIUS + 0.04
    outer_radius = inner_radius + 0.27
    depth = 0.24
    count = 9
    created = []
    for index in range(count):
        start = math.pi * index / count + 0.012
        end = math.pi * (index + 1) / count - 0.012
        polygon = (
            (
                inner_radius * math.cos(start),
                spring + inner_radius * math.sin(start),
            ),
            (
                outer_radius * math.cos(start),
                spring + outer_radius * math.sin(start),
            ),
            (
                outer_radius * math.cos(end),
                spring + outer_radius * math.sin(end),
            ),
            (
                inner_radius * math.cos(end),
                spring + inner_radius * math.sin(end),
            ),
        )
        created.append(
            create_extruded_xz_profile(
                f"{prefix}_ArchStone_{index + 1:02d}",
                polygon,
                center_y,
                depth,
                outputs,
                assembly,
                dressed_stone,
                bevel_width=0.018,
            )
        )
    courses = 4
    course_height = DOOR_SPRING_HEIGHT / courses
    for side, sign in (("L", -1.0), ("R", 1.0)):
        center_x = sign * (inner_radius + 0.135)
        for index in range(courses):
            z = threshold + (index + 0.5) * course_height
            created.append(
                add_box(
                    f"{prefix}_Jamb_{side}_{index + 1:02d}",
                    (center_x, center_y, z),
                    (0.27, depth, course_height - 0.025),
                    outputs,
                    assembly,
                    dressed_stone,
                    bevel_width=0.018,
                )
            )
    return created


def create_door_hardware(
    prefix,
    center_y,
    threshold,
    outward_sign,
    outputs,
    assembly,
    iron,
):
    hardware_y = center_y + outward_sign * 0.065
    for index, z_offset in enumerate((0.58, 1.18), start=1):
        add_box(
            f"{prefix}_IronStrap_{index:02d}",
            (0.0, hardware_y, threshold + z_offset),
            (1.03, 0.045, 0.105),
            outputs,
            assembly,
            iron,
            bevel_width=0.015,
        )
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=12,
        ring_count=6,
        radius=0.075,
        location=(0.34, hardware_y + outward_sign * 0.04, threshold + 0.91),
    )
    handle = bpy.context.object
    handle.name = f"{prefix}_IronHandle"
    move_to_collection(handle, outputs)
    handle.parent = assembly
    handle.data.materials.append(iron)
    handle["artifact_role"] = "OUTPUT"
    handle["style_profile"] = STYLE_PROFILE


def create_merlons(modules, outputs, module_parent, assembly, stone):
    source = add_box(
        "MODULE_MerlonSource",
        (0.0, 0.0, 0.55),
        (0.92, 0.62, 1.10),
        modules,
        module_parent,
        stone,
        role="MODULE",
        bevel_width=0.035,
    )
    bpy.context.view_layer.objects.active = source
    source.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    source.select_set(False)
    source.hide_render = True
    source["module_dimensions_m"] = [0.92, 0.62, 1.10]
    source["pivot_convention"] = "bottom center"
    radius = 3.36
    count = 16
    placed = []
    for index in range(count):
        angle = math.tau * index / count
        obj = source.copy()
        obj.data = source.data
        obj.name = f"OUT_Merlon_{index + 1:02d}"
        outputs.objects.link(obj)
        obj.parent = assembly
        obj.hide_render = False
        obj.location = (
            radius * math.cos(angle),
            radius * math.sin(angle),
            PARAPET_TOP,
        )
        obj.rotation_euler[2] = angle - math.pi * 0.5
        obj["artifact_role"] = "OUTPUT"
        obj["module_source"] = source.name
        placed.append(obj)
    return source, placed


def configure_scene():
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.image_settings.file_format = "PNG"
    scene.render.resolution_x = 800
    scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.world.color = (0.014, 0.018, 0.024)

    camera_data = bpy.data.cameras.new("PREVIEW_Camera")
    camera = bpy.data.objects.new("PREVIEW_Camera", camera_data)
    bpy.context.scene.collection.objects.link(camera)
    camera.location = (13.5, -15.5, 10.5)
    camera.data.lens = 55.0
    scene.camera = camera

    lights = (
        (
            "PREVIEW_Key",
            "AREA",
            (-7.5, -9.0, 15.0),
            1500.0,
            (1.0, 0.84, 0.68),
            7.0,
        ),
        (
            "PREVIEW_Fill",
            "AREA",
            (8.0, -4.0, 9.0),
            900.0,
            (0.58, 0.72, 1.0),
            6.0,
        ),
        (
            "PREVIEW_Rim",
            "AREA",
            (2.0, 9.0, 13.0),
            1250.0,
            (0.72, 0.82, 1.0),
            5.0,
        ),
    )
    for name, light_type, location, energy, color, size in lights:
        data = bpy.data.lights.new(name, light_type)
        data.energy = energy
        data.color = color
        data.shape = "DISK"
        data.size = size
        obj = bpy.data.objects.new(name, data)
        bpy.context.scene.collection.objects.link(obj)
        obj.location = location


def geometry_report(assembly):
    objects = [
        obj
        for obj in bpy.context.scene.objects
        if obj.parent == assembly and obj.type == "MESH"
    ]
    depsgraph = bpy.context.evaluated_depsgraph_get()
    base_vertices = sum(len(obj.data.vertices) for obj in objects)
    base_triangles = sum(
        sum(max(len(face.vertices) - 2, 0) for face in obj.data.polygons)
        for obj in objects
    )
    evaluated_vertices = 0
    evaluated_triangles = 0
    for obj in objects:
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        try:
            evaluated_vertices += len(mesh.vertices)
            evaluated_triangles += sum(
                max(len(face.vertices) - 2, 0) for face in mesh.polygons
            )
        finally:
            evaluated.to_mesh_clear()
    return {
        "objects": len(objects),
        "base_vertices": base_vertices,
        "base_triangles": base_triangles,
        "evaluated_vertices": evaluated_vertices,
        "evaluated_triangles": evaluated_triangles,
        "modifiers": sum(len(obj.modifiers) for obj in objects),
    }


def main():
    args = parse_args()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    style_contract_path = args.style_contract.resolve()
    style_contract = json.loads(
        style_contract_path.read_text(encoding="utf-8")
    )
    if style_contract["asset"]["profile"] != STYLE_PROFILE:
        raise RuntimeError("Tower style contract profile does not match")

    clear_scene()
    collections = {
        name: ensure_collection(name)
        for name in (
            "SOURCE",
            "MODULES",
            "CONTROLS",
            "ASSEMBLIES",
            "COLLISION",
            "LOD",
            "PREVIEW",
        )
    }
    source_parent = create_empty(
        "SOURCE_StoneTowerEnvelope", collections["SOURCE"], "SOURCE"
    )
    source_parent["origin"] = "original project-owned procedural construction"
    module_parent = create_empty(
        "MODULE_StoneTowerKit", collections["MODULES"], "MODULE"
    )
    control_parent = create_empty(
        "CTRL_StoneTowerConstruction", collections["CONTROLS"], "CONTROL"
    )
    assembly = create_empty(
        ASSEMBLY_NAME, collections["ASSEMBLIES"], "OUTPUT"
    )
    assembly["profile"] = STYLE_PROFILE
    assembly["units"] = "meters"
    assembly["forward_axis"] = "-Y ground entrance / +Y wall-walk entrance"
    assembly["up_axis"] = "+Z"
    assembly["collision_status"] = "not required for modeling pass"
    assembly["lod_status"] = "not required for modeling pass"

    stone = material("MAT_TowerStone_Placeholder", (0.24, 0.26, 0.29), 0.82)
    dressed = material(
        "MAT_DressedStone_Placeholder", (0.36, 0.37, 0.39), 0.76
    )
    wood = material("MAT_DoorWood_Placeholder", (0.16, 0.055, 0.018), 0.70)
    iron = material(
        "MAT_DoorIron_Placeholder", (0.025, 0.030, 0.036), 0.68, 0.85
    )

    ground_cutter = create_door_opening(
        "CUT_GroundDoorArch",
        -3.20,
        GROUND_THRESHOLD,
        1.55,
        collections["CONTROLS"],
        control_parent,
    )
    upper_cutter = create_door_opening(
        "CUT_UpperDoorArch",
        3.20,
        UPPER_THRESHOLD,
        1.55,
        collections["CONTROLS"],
        control_parent,
    )

    wall = create_annular_shell(
        "OUT_TowerWallShell",
        OUTER_RADIUS,
        INNER_RADIUS,
        0.0,
        WALL_TOP,
        SEGMENTS,
        collections["ASSEMBLIES"],
        assembly,
        stone,
        bevel_width=0.0,
    )
    add_boolean(wall, ground_cutter, "OpenGroundDoor")
    add_boolean(wall, upper_cutter, "OpenUpperDoor")
    # Keep the multi-opening shell unbeveled. Dressed frames own visible edge
    # softness without generating fragile slivers around Boolean reveals.

    parapet = create_annular_shell(
        "OUT_ParapetRing",
        3.68,
        3.03,
        9.18,
        PARAPET_TOP,
        SEGMENTS,
        collections["ASSEMBLIES"],
        assembly,
        stone,
        bevel_width=0.035,
    )
    create_cylinder(
        "OUT_BattlementDeck",
        3.06,
        0.18,
        9.17,
        SEGMENTS,
        collections["ASSEMBLIES"],
        assembly,
        stone,
        bevel_width=0.025,
    )
    create_merlons(
        collections["MODULES"],
        collections["ASSEMBLIES"],
        module_parent,
        assembly,
        stone,
    )
    create_door_leaf(
        "OUT_GroundDoorLeaf",
        -3.43,
        GROUND_THRESHOLD,
        collections["ASSEMBLIES"],
        assembly,
        wood,
    )
    create_door_leaf(
        "OUT_UpperDoorLeaf",
        3.43,
        UPPER_THRESHOLD,
        collections["ASSEMBLIES"],
        assembly,
        wood,
    )
    add_box(
        "OUT_UpperWallWalkLanding",
        (0.0, 3.99, 5.10),
        (2.05, 1.02, 0.25),
        collections["ASSEMBLIES"],
        assembly,
        dressed,
        bevel_width=0.035,
    )

    configure_scene()
    stage_00 = output_dir / "stage-00-stone-tower-blockout.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(stage_00), check_existing=False)
    stage_00_hash = sha256(stage_00)

    plinth = create_annular_shell(
        "OUT_FoundationPlinth",
        3.78,
        2.74,
        -0.22,
        0.30,
        SEGMENTS,
        collections["ASSEMBLIES"],
        assembly,
        dressed,
        bevel_width=0.0,
    )
    add_boolean(plinth, ground_cutter, "OpenGroundThreshold")
    add_bevel(plinth, 0.04)
    create_annular_shell(
        "OUT_MidStringCourse",
        3.69,
        2.79,
        4.42,
        4.62,
        SEGMENTS,
        collections["ASSEMBLIES"],
        assembly,
        dressed,
        bevel_width=0.025,
    )
    create_annular_shell(
        "OUT_ParapetStringCourse",
        3.72,
        3.00,
        9.05,
        9.25,
        SEGMENTS,
        collections["ASSEMBLIES"],
        assembly,
        dressed,
        bevel_width=0.025,
    )
    create_arch_surround(
        "OUT_GroundDoorFrame",
        -3.64,
        GROUND_THRESHOLD,
        collections["ASSEMBLIES"],
        assembly,
        dressed,
    )
    create_arch_surround(
        "OUT_UpperDoorFrame",
        3.64,
        UPPER_THRESHOLD,
        collections["ASSEMBLIES"],
        assembly,
        dressed,
    )
    create_door_hardware(
        "OUT_GroundDoor",
        -3.49,
        GROUND_THRESHOLD,
        -1.0,
        collections["ASSEMBLIES"],
        assembly,
        iron,
    )
    create_door_hardware(
        "OUT_UpperDoor",
        3.49,
        UPPER_THRESHOLD,
        1.0,
        collections["ASSEMBLIES"],
        assembly,
        iron,
    )
    corbel_profile = (
        (3.48, 5.04),
        (4.38, 5.04),
        (3.48, 4.28),
    )
    for side, x in (("L", -0.70), ("R", 0.70)):
        create_extruded_yz_profile(
            f"OUT_UpperLandingCorbel_{side}",
            corbel_profile,
            x,
            0.30,
            collections["ASSEMBLIES"],
            assembly,
            dressed,
            bevel_width=0.025,
        )

    assembly["stage"] = "stage-01-construction"
    geometry = geometry_report(assembly)
    stage_01 = output_dir / "stage-01-stone-tower-construction.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(stage_01), check_existing=False)
    manifest = {
        "asset": "Grounded Stone Wall Tower",
        "schema_version": 1,
        "script_version": SCRIPT_VERSION,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "blender_version": bpy.app.version_string,
        "classification": "pipeline-valid original project-owned fixture",
        "style_contract": {
            "path": str(style_contract_path),
            "sha256": sha256(style_contract_path),
            "profile": STYLE_PROFILE,
        },
        "stages": [
            {
                "name": "stage-00-blockout",
                "path": str(stage_00),
                "sha256": stage_00_hash,
            },
            {
                "name": "stage-01-construction",
                "path": str(stage_01),
                "sha256": sha256(stage_01),
            },
        ],
        "module_contract": {
            "units": "meters",
            "grid_increment_m": 0.05,
            "forward_axis": "-Y",
            "up_axis": "+Z",
            "assembly_pivot": "tower center at ground datum",
            "wall_walk_connection": {
                "side": "+Y rear",
                "threshold_z_m": UPPER_THRESHOLD,
                "landing_width_m": 2.05,
                "landing_outer_reach_m": 0.90,
            },
            "merlon_source": "MODULE_MerlonSource",
            "merlon_instances": 16,
        },
        "dimensions_m": {
            "outer_diameter": OUTER_RADIUS * 2.0,
            "inner_diameter": INNER_RADIUS * 2.0,
            "wall_thickness": OUTER_RADIUS - INNER_RADIUS,
            "wall_top": WALL_TOP,
            "parapet_top": PARAPET_TOP,
            "merlon_top": MERLON_TOP,
            "ground_door_threshold": GROUND_THRESHOLD,
            "upper_door_threshold": UPPER_THRESHOLD,
            "door_clear_width": DOOR_WIDTH,
            "door_clear_height": DOOR_SPRING_HEIGHT + DOOR_RADIUS,
        },
        "geometry": geometry,
        "construction": {
            "wall": "closed annular shell with retained exact Boolean arch cutters",
            "battlements": "continuous parapet plus sixteen linked merlon instances",
            "doors": "closed arched wood leaves behind true shell openings",
            "upper_connection": "stone landing with two structural corbels",
            "deferred": [
                "interior stairs and rooms",
                "curtain walls",
                "stone block relief",
                "UVs and textures",
                "collision and LODs",
            ],
        },
        "preview": {
            "directory": str(output_dir / "renders" / "stage-01"),
            "required": [
                "stage-01-front.png",
                "stage-01-rear.png",
                "stage-01-side.png",
                "stage-01-top.png",
                "stage-01-front-three-quarter.png",
                "stage-01-rear-three-quarter.png",
                "stage-01-wireframe.png",
                "stage-01-gameplay-distance.png",
            ],
        },
        "iteration_log": [
            {
                "stage": "stage-00-blockout",
                "status": "pending fixed-view inspection",
                "focus": "overall round mass, two-door separation, battlement rhythm, wall-walk connection",
            }
        ],
    }
    manifest_path = output_dir / "operation-manifest-v1.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"TOWER_STAGE_00={stage_00}")
    print(f"TOWER_STAGE_00_SHA256={stage_00_hash}")
    print(f"TOWER_STAGE_01={stage_01}")
    print(f"TOWER_STAGE_01_SHA256={manifest['stages'][1]['sha256']}")
    print(f"TOWER_OPERATION_MANIFEST={manifest_path}")
    print(f"TOWER_GEOMETRY={json.dumps(geometry, sort_keys=True)}")


if __name__ == "__main__":
    main()
