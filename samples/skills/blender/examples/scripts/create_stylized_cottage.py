"""Create a staged clean-stylized medieval-fantasy cottage fixture."""

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector


ASSEMBLY_NAME = "OUT_StylizedCottageAssembly"
STYLE_PROFILE = "clean-stylized-medieval-fantasy"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
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


def create_empty(name, collection, parent=None):
    obj = bpy.data.objects.new(name, None)
    collection.objects.link(obj)
    obj.parent = parent
    return obj


def material(name, base_color, metallic=0.0, roughness=0.65):
    assigned = bpy.data.materials.new(name)
    assigned.diffuse_color = (*base_color, 1.0)
    assigned.use_nodes = True
    principled = assigned.node_tree.nodes.get("Principled BSDF")
    principled.inputs["Base Color"].default_value = (*base_color, 1.0)
    principled.inputs["Metallic"].default_value = metallic
    principled.inputs["Roughness"].default_value = roughness
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


def create_mesh_object(
    name,
    vertices,
    faces,
    collection,
    parent,
    assigned_material,
    bevel_width=0.0,
    smooth=False,
):
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.validate(verbose=True)
    recalculate_normals(mesh)
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.parent = parent
    obj["artifact_role"] = "OUTPUT"
    obj["style_profile"] = STYLE_PROFILE
    if assigned_material is not None:
        obj.data.materials.append(assigned_material)
    for polygon in mesh.polygons:
        polygon.use_smooth = smooth
    if bevel_width > 0.0:
        bevel = obj.modifiers.new("ConstructionBevel", "BEVEL")
        bevel.width = bevel_width
        bevel.segments = 2
        bevel.limit_method = "ANGLE"
        bevel.angle_limit = math.radians(25.0)
    return obj


def add_box(
    name,
    location,
    dimensions,
    collection,
    parent,
    assigned_material,
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
    obj["artifact_role"] = "OUTPUT"
    obj["style_profile"] = STYLE_PROFILE
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.select_set(False)
    if bevel_width > 0.0:
        bevel = obj.modifiers.new("ConstructionBevel", "BEVEL")
        bevel.width = bevel_width
        bevel.segments = 2
        bevel.limit_method = "ANGLE"
        bevel.angle_limit = math.radians(25.0)
    return obj


def create_tapered_box(
    name,
    location,
    bottom_size,
    top_size,
    top_shift,
    height,
    collection,
    parent,
    assigned_material,
    bevel_width=0.0,
):
    bottom_z = location[2] - height * 0.5
    top_z = location[2] + height * 0.5
    bottom_x, bottom_y = bottom_size
    top_x, top_y = top_size
    shift_x, shift_y = top_shift
    vertices = [
        (-bottom_x * 0.5, -bottom_y * 0.5, bottom_z),
        (bottom_x * 0.5, -bottom_y * 0.5, bottom_z),
        (bottom_x * 0.5, bottom_y * 0.5, bottom_z),
        (-bottom_x * 0.5, bottom_y * 0.5, bottom_z),
        (shift_x - top_x * 0.5, shift_y - top_y * 0.5, top_z),
        (shift_x + top_x * 0.5, shift_y - top_y * 0.5, top_z),
        (shift_x + top_x * 0.5, shift_y + top_y * 0.5, top_z),
        (shift_x - top_x * 0.5, shift_y + top_y * 0.5, top_z),
    ]
    vertices = [
        (x + location[0], y + location[1], z) for x, y, z in vertices
    ]
    faces = [
        (0, 3, 2, 1),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return create_mesh_object(
        name,
        vertices,
        faces,
        collection,
        parent,
        assigned_material,
        bevel_width=bevel_width,
    )


def create_gable_prism(
    name,
    center_y,
    depth,
    half_width,
    base_z,
    ridge_x,
    ridge_z,
    collection,
    parent,
    assigned_material,
):
    front_y = center_y - depth * 0.5
    back_y = center_y + depth * 0.5
    vertices = [
        (-half_width, front_y, base_z),
        (half_width, front_y, base_z),
        (ridge_x, front_y, ridge_z),
        (-half_width, back_y, base_z),
        (half_width, back_y, base_z),
        (ridge_x, back_y, ridge_z),
    ]
    faces = [
        (0, 2, 1),
        (3, 4, 5),
        (0, 1, 4, 3),
        (1, 2, 5, 4),
        (2, 0, 3, 5),
    ]
    return create_mesh_object(
        name,
        vertices,
        faces,
        collection,
        parent,
        assigned_material,
        bevel_width=0.035,
    )


def create_extruded_xz_profile(
    name,
    polygon,
    center_y,
    depth,
    collection,
    parent,
    assigned_material,
    bevel_width=0.0,
):
    front_y = center_y - depth * 0.5
    back_y = center_y + depth * 0.5
    vertices = [(x, front_y, z) for x, z in polygon]
    vertices.extend((x, back_y, z) for x, z in polygon)
    count = len(polygon)
    faces = [tuple(range(count - 1, -1, -1))]
    faces.append(tuple(range(count, count * 2)))
    for index in range(count):
        following = (index + 1) % count
        faces.append((index, following, following + count, index + count))
    return create_mesh_object(
        name,
        vertices,
        faces,
        collection,
        parent,
        assigned_material,
        bevel_width=bevel_width,
    )


def add_beam_between(
    name,
    start,
    end,
    width,
    depth,
    collection,
    parent,
    assigned_material,
    bevel_width=0.025,
):
    start = Vector(start)
    end = Vector(end)
    direction = end - start
    length = direction.length
    if length <= 1e-6:
        raise ValueError(f"{name}: beam endpoints are coincident.")
    midpoint = (start + end) * 0.5
    rotation = direction.to_track_quat("Z", "Y").to_euler()
    return add_box(
        name,
        midpoint,
        (width, depth, length),
        collection,
        parent,
        assigned_material,
        rotation=rotation,
        bevel_width=bevel_width,
    )


def add_cylinder(
    name,
    location,
    radius,
    depth,
    rotation,
    collection,
    parent,
    assigned_material,
    vertices=16,
    smooth=False,
    bevel_width=0.0,
):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    move_to_collection(obj, collection)
    obj.parent = parent
    obj.data.materials.append(assigned_material)
    obj["artifact_role"] = "OUTPUT"
    obj["style_profile"] = STYLE_PROFILE
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.select_set(False)
    for polygon in obj.data.polygons:
        polygon.use_smooth = smooth
    if bevel_width > 0.0:
        bevel = obj.modifiers.new("ConstructionBevel", "BEVEL")
        bevel.width = bevel_width
        bevel.segments = 2
    return obj


def add_torus(
    name,
    location,
    major_radius,
    minor_radius,
    rotation,
    collection,
    parent,
    assigned_material,
):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_radius,
        minor_radius=minor_radius,
        major_segments=20,
        minor_segments=8,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    move_to_collection(obj, collection)
    obj.parent = parent
    obj.data.materials.append(assigned_material)
    obj["artifact_role"] = "OUTPUT"
    obj["style_profile"] = STYLE_PROFILE
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.select_set(False)
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    return obj


# The longitudinal resolution needs enough samples for the coherent bow to
# read as hand-shaped curvature instead of a sawtooth. Keep the slope direction
# sparse and graphic, but sample the long direction more finely.
ROOF_Y_ROWS = tuple(-2.78 + (5.56 / 10.0) * index for index in range(11))


def roof_point(sign, u, y, lift=0.0):
    row_factor = abs(y) / 2.78
    sag = -0.105 * row_factor**1.45
    coherent_wave = 0.030 * math.sin(y * 1.35 + sign * 0.35)
    x = sign * (
        0.08
        + 3.36 * u
        + 0.075 * math.sin(y / 2.78 * math.pi) * u
    )
    z = 5.30 + sag + coherent_wave - 2.62 * u - 0.08 * u**3 + lift
    return Vector((x, y, z))


def create_thick_grid(
    name,
    rows,
    columns,
    outer_points,
    inner_points,
    collection,
    parent,
    assigned_material,
):
    vertices = [tuple(point) for point in outer_points]
    vertices.extend(tuple(point) for point in inner_points)
    inner_offset = len(outer_points)
    faces = []

    def index(row, column):
        return row * columns + column

    for row in range(rows - 1):
        for column in range(columns - 1):
            a = index(row, column)
            b = index(row + 1, column)
            c = index(row + 1, column + 1)
            d = index(row, column + 1)
            faces.append((a, b, c, d))
            faces.append(
                (
                    a + inner_offset,
                    d + inner_offset,
                    c + inner_offset,
                    b + inner_offset,
                )
            )

    for column in range(columns - 1):
        front_a = index(0, column)
        front_b = index(0, column + 1)
        rear_a = index(rows - 1, column)
        rear_b = index(rows - 1, column + 1)
        faces.append(
            (
                front_a,
                front_b,
                front_b + inner_offset,
                front_a + inner_offset,
            )
        )
        faces.append(
            (
                rear_b,
                rear_a,
                rear_a + inner_offset,
                rear_b + inner_offset,
            )
        )

    for row in range(rows - 1):
        left_a = index(row, 0)
        left_b = index(row + 1, 0)
        right_a = index(row, columns - 1)
        right_b = index(row + 1, columns - 1)
        faces.append(
            (
                left_b,
                left_a,
                left_a + inner_offset,
                left_b + inner_offset,
            )
        )
        faces.append(
            (
                right_a,
                right_b,
                right_b + inner_offset,
                right_a + inner_offset,
            )
        )

    return create_mesh_object(
        name,
        vertices,
        faces,
        collection,
        parent,
        assigned_material,
    )


def create_roof_side(
    sign,
    collection,
    parent,
    assigned_material,
):
    u_values = (0.0, 0.36, 0.70, 1.0)
    outer = []
    inner = []
    for y in ROOF_Y_ROWS:
        for u in u_values:
            point = roof_point(sign, u, y)
            outer.append(point)
            inner.append(point + Vector((0.0, 0.0, -0.18)))
    side = "R" if sign > 0 else "L"
    roof = create_thick_grid(
        f"OUT_RoofPlane_{side}",
        len(ROOF_Y_ROWS),
        len(u_values),
        outer,
        inner,
        collection,
        parent,
        assigned_material,
    )
    roof["construction_role"] = "oversized primary roof mass"
    roof["variation_method"] = "coherent ridge sag and eave bow"
    return roof


def create_roof_course(
    sign,
    course_index,
    center_u,
    width_u,
    collection,
    parent,
    assigned_material,
):
    u_values = (
        max(center_u - width_u * 0.5, 0.0),
        min(center_u + width_u * 0.5, 1.0),
    )
    outer = []
    inner = []
    for y in ROOF_Y_ROWS:
        for u in u_values:
            # Keep both course surfaces proud of the primary roof plane.
            # The first pass sank the inner surface through the roof, which
            # produced jagged z-fighting seams in otherwise clean silhouettes.
            point = roof_point(sign, u, y, lift=0.075)
            outer.append(point)
            inner.append(point + Vector((0.0, 0.0, -0.050)))
    side = "R" if sign > 0 else "L"
    course = create_thick_grid(
        f"OUT_RoofCourse_{side}_{course_index:02d}",
        len(ROOF_Y_ROWS),
        len(u_values),
        outer,
        inner,
        collection,
        parent,
        assigned_material,
    )
    surface_cell_count = (len(ROOF_Y_ROWS) - 1) * (len(u_values) - 1)
    for polygon_index in range(0, surface_cell_count * 2, 2):
        # Only the exposed top quads share smooth normals. The lower and side
        # faces remain flat so the raised course retains a crisp stepped edge.
        course.data.polygons[polygon_index].use_smooth = True
    course["construction_role"] = "silhouette-readable stylized roof course"
    return course


def create_arch_door(
    collection,
    parent,
    door_material,
    timber_material,
    metal_material,
):
    center_x = 0.92
    bottom_z = 0.24
    shoulder_z = 1.62
    radius = 0.72
    polygon = [
        (center_x - radius, bottom_z),
        (center_x + radius, bottom_z),
        (center_x + radius, shoulder_z),
    ]
    for index in range(1, 9):
        angle = math.pi * index / 8.0
        polygon.append(
            (
                center_x + radius * math.cos(angle),
                shoulder_z + radius * math.sin(angle),
            )
        )
    door = create_extruded_xz_profile(
        "OUT_ArchedDoor",
        polygon,
        -2.34,
        0.16,
        collection,
        parent,
        door_material,
        bevel_width=0.035,
    )
    door["opening_status"] = "recessed exterior-shell representation"
    door["playable_interior"] = False

    objects = [door]
    for side, x in (("L", center_x - radius - 0.10), ("R", center_x + radius + 0.10)):
        objects.append(
            add_box(
                f"OUT_DoorFrame_{side}",
                (x, -2.46, (bottom_z + shoulder_z) * 0.5),
                (0.20, 0.25, shoulder_z - bottom_z + 0.12),
                collection,
                parent,
                timber_material,
                bevel_width=0.035,
            )
        )

    arch_radius = radius + 0.10
    arch_points = [
        Vector(
            (
                center_x + arch_radius * math.cos(math.pi * index / 8.0),
                -2.46,
                shoulder_z + arch_radius * math.sin(math.pi * index / 8.0),
            )
        )
        for index in range(9)
    ]
    for index in range(8):
        objects.append(
            add_beam_between(
                f"OUT_DoorArchSegment_{index + 1:02d}",
                arch_points[index],
                arch_points[index + 1],
                0.20,
                0.25,
                collection,
                parent,
                timber_material,
                bevel_width=0.028,
            )
        )

    for index, offset in enumerate((-0.43, -0.14, 0.14, 0.43), start=1):
        objects.append(
            add_box(
                f"OUT_DoorPlank_{index:02d}",
                (center_x + offset, -2.435, 1.02),
                (0.055, 0.055, 1.58),
                collection,
                parent,
                timber_material,
                bevel_width=0.012,
            )
        )

    for index, z in enumerate((0.76, 1.32), start=1):
        objects.append(
            add_box(
                f"OUT_DoorHinge_{index:02d}",
                (center_x - 0.43, -2.485, z),
                (0.62, 0.08, 0.11),
                collection,
                parent,
                metal_material,
                bevel_width=0.018,
            )
        )
    objects.append(
        add_cylinder(
            "OUT_DoorHandle",
            (center_x + 0.43, -2.51, 1.05),
            0.075,
            0.10,
            (math.pi * 0.5, 0.0, 0.0),
            collection,
            parent,
            metal_material,
            vertices=12,
            smooth=True,
        )
    )
    return objects


def create_front_window(
    collection,
    parent,
    pane_material,
    timber_material,
):
    center_x = -1.45
    center_z = 1.48
    width = 1.25
    height = 1.05
    objects = [
        add_box(
            "OUT_WindowPane_Front",
            (center_x, -2.36, center_z),
            (width, 0.11, height),
            collection,
            parent,
            pane_material,
            bevel_width=0.025,
        )
    ]
    for side, x in (
        ("L", center_x - width * 0.5 - 0.10),
        ("R", center_x + width * 0.5 + 0.10),
    ):
        objects.append(
            add_box(
                f"OUT_WindowFrame_Front_{side}",
                (x, -2.44, center_z),
                (0.18, 0.22, height + 0.28),
                collection,
                parent,
                timber_material,
                bevel_width=0.03,
            )
        )
    for edge, z in (
        ("Bottom", center_z - height * 0.5 - 0.10),
        ("Top", center_z + height * 0.5 + 0.10),
    ):
        objects.append(
            add_box(
                f"OUT_WindowFrame_Front_{edge}",
                (center_x, -2.44, z),
                (width + 0.38, 0.22, 0.18),
                collection,
                parent,
                timber_material,
                bevel_width=0.03,
            )
        )
    objects.append(
        add_box(
            "OUT_WindowMullion_Front_V",
            (center_x, -2.49, center_z),
            (0.12, 0.11, height),
            collection,
            parent,
            timber_material,
            bevel_width=0.02,
        )
    )
    objects.append(
        add_box(
            "OUT_WindowMullion_Front_H",
            (center_x, -2.49, center_z),
            (width, 0.11, 0.12),
            collection,
            parent,
            timber_material,
            bevel_width=0.02,
        )
    )
    return objects


def create_side_window(
    collection,
    parent,
    pane_material,
    timber_material,
):
    center_y = 0.18
    center_z = 1.50
    width = 1.25
    height = 1.00
    objects = [
        add_box(
            "OUT_WindowPane_Side",
            (2.94, center_y, center_z),
            (0.11, width, height),
            collection,
            parent,
            pane_material,
            bevel_width=0.025,
        )
    ]
    for side, y in (
        ("Front", center_y - width * 0.5 - 0.10),
        ("Rear", center_y + width * 0.5 + 0.10),
    ):
        objects.append(
            add_box(
                f"OUT_WindowFrame_Side_{side}",
                (3.02, y, center_z),
                (0.22, 0.18, height + 0.28),
                collection,
                parent,
                timber_material,
                bevel_width=0.03,
            )
        )
    for edge, z in (
        ("Bottom", center_z - height * 0.5 - 0.10),
        ("Top", center_z + height * 0.5 + 0.10),
    ):
        objects.append(
            add_box(
                f"OUT_WindowFrame_Side_{edge}",
                (3.02, center_y, z),
                (0.22, width + 0.38, 0.18),
                collection,
                parent,
                timber_material,
                bevel_width=0.03,
            )
        )
    objects.append(
        add_box(
            "OUT_WindowMullion_Side_V",
            (3.07, center_y, center_z),
            (0.11, 0.12, height),
            collection,
            parent,
            timber_material,
            bevel_width=0.02,
        )
    )
    objects.append(
        add_box(
            "OUT_WindowMullion_Side_H",
            (3.07, center_y, center_z),
            (0.11, width, 0.12),
            collection,
            parent,
            timber_material,
            bevel_width=0.02,
        )
    )
    return objects


def create_rear_window(
    collection,
    parent,
    pane_material,
    timber_material,
):
    center_x = 1.40
    center_z = 1.48
    width = 0.92
    height = 0.82
    objects = [
        add_box(
            "OUT_WindowPane_Rear",
            (center_x, 2.36, center_z),
            (width, 0.11, height),
            collection,
            parent,
            pane_material,
            bevel_width=0.025,
        )
    ]
    for side, x in (
        ("L", center_x - width * 0.5 - 0.09),
        ("R", center_x + width * 0.5 + 0.09),
    ):
        objects.append(
            add_box(
                f"OUT_WindowFrame_Rear_{side}",
                (x, 2.44, center_z),
                (0.17, 0.22, height + 0.25),
                collection,
                parent,
                timber_material,
                bevel_width=0.03,
            )
        )
    for edge, z in (
        ("Bottom", center_z - height * 0.5 - 0.09),
        ("Top", center_z + height * 0.5 + 0.09),
    ):
        objects.append(
            add_box(
                f"OUT_WindowFrame_Rear_{edge}",
                (center_x, 2.44, z),
                (width + 0.34, 0.22, 0.17),
                collection,
                parent,
                timber_material,
                bevel_width=0.03,
            )
        )
    objects.append(
        add_box(
            "OUT_WindowMullion_Rear_V",
            (center_x, 2.49, center_z),
            (0.10, 0.11, height),
            collection,
            parent,
            timber_material,
            bevel_width=0.02,
        )
    )
    objects.append(
        add_box(
            "OUT_WindowMullion_Rear_H",
            (center_x, 2.49, center_z),
            (width, 0.11, 0.10),
            collection,
            parent,
            timber_material,
            bevel_width=0.02,
        )
    )
    return objects


def create_gable_window(
    collection,
    parent,
    pane_material,
    timber_material,
):
    center = (-0.68, -2.49, 3.65)
    pane = add_cylinder(
        "OUT_GableWindowPane",
        center,
        0.38,
        0.12,
        (math.pi * 0.5, 0.0, 0.0),
        collection,
        parent,
        pane_material,
        vertices=20,
        smooth=True,
    )
    frame = add_torus(
        "OUT_GableWindowFrame",
        (center[0], center[1] - 0.07, center[2]),
        0.42,
        0.095,
        (math.pi * 0.5, 0.0, 0.0),
        collection,
        parent,
        timber_material,
    )
    cross_v = add_box(
        "OUT_GableWindowMullion_V",
        (center[0], center[1] - 0.14, center[2]),
        (0.10, 0.08, 0.72),
        collection,
        parent,
        timber_material,
        bevel_width=0.015,
    )
    cross_h = add_box(
        "OUT_GableWindowMullion_H",
        (center[0], center[1] - 0.14, center[2]),
        (0.72, 0.08, 0.10),
        collection,
        parent,
        timber_material,
        bevel_width=0.015,
    )
    return [pane, frame, cross_v, cross_h]


def create_human_proxy(collection, assigned_material):
    cage = create_empty("FIT_HumanScale", collection)
    cage["artifact_role"] = "SCALE_REFERENCE"
    cage["height_m"] = 1.80
    body = add_cylinder(
        "FIT_HumanBody",
        (-4.25, -2.60, 0.92),
        0.26,
        1.36,
        (0.0, 0.0, 0.0),
        collection,
        cage,
        assigned_material,
        vertices=16,
        smooth=True,
    )
    body["artifact_role"] = "SCALE_REFERENCE"
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=20,
        ring_count=10,
        radius=0.28,
        location=(-4.25, -2.60, 1.58),
    )
    head = bpy.context.object
    head.name = "FIT_HumanHead"
    move_to_collection(head, collection)
    head.parent = cage
    head.data.materials.append(assigned_material)
    head["artifact_role"] = "SCALE_REFERENCE"
    for polygon in head.data.polygons:
        polygon.use_smooth = True
    return cage


def create_cottage(collections, materials):
    output = collections["ASSEMBLIES"]
    modules = collections["MODULES"]
    zoo = collections["ASSET_ZOO"]
    assembly = create_empty(ASSEMBLY_NAME, output)
    assembly["artifact_role"] = "OUTPUT_ASSEMBLY"
    assembly["artifact_scope"] = "hero building exterior shell"
    assembly["style_contract"] = STYLE_PROFILE
    assembly["interior_status"] = "not modeled"
    assembly["collision_status"] = "not requested"
    assembly["lod_status"] = "not requested"
    assembly["historical_confidence"] = "medieval-fantasy, not verified"

    module_notes = create_empty("MOD_CottageGrammar", modules)
    module_notes["artifact_role"] = "MODULE_DEFINITION"
    module_notes["logical_footprint_m"] = [5.8, 4.6]
    module_notes["grid_increment_m"] = 0.25
    module_notes["pivot_convention"] = "ground center"
    module_notes["kit_status"] = "hero submodules only; not a village kit"

    create_human_proxy(zoo, materials["scale"])
    objects = []

    objects.append(
        create_tapered_box(
            "OUT_FoundationPlinth",
            (0.0, 0.0, 0.26),
            (6.20, 5.00),
            (5.95, 4.78),
            (-0.06, 0.02),
            0.52,
            output,
            assembly,
            materials["stone"],
            bevel_width=0.09,
        )
    )
    objects.append(
        create_tapered_box(
            "OUT_WallMass",
            (0.0, 0.0, 1.55),
            (5.82, 4.62),
            (5.56, 4.44),
            (0.12, 0.02),
            2.58,
            output,
            assembly,
            materials["plaster"],
            bevel_width=0.10,
        )
    )
    objects.extend(
        [
            create_gable_prism(
                "OUT_Gable_Front",
                -2.31,
                0.24,
                2.78,
                2.55,
                0.05,
                5.08,
                output,
                assembly,
                materials["plaster"],
            ),
            create_gable_prism(
                "OUT_Gable_Rear",
                2.31,
                0.24,
                2.78,
                2.55,
                0.05,
                5.08,
                output,
                assembly,
                materials["plaster_dark"],
            ),
        ]
    )

    for sign in (-1, 1):
        objects.append(
            create_roof_side(
                sign,
                output,
                assembly,
                materials["roof"],
            )
        )
        for index, center_u in enumerate((0.22, 0.45, 0.68, 0.89), start=1):
            course_material = (
                materials["roof_dark"] if index % 2 == 0 else materials["roof"]
            )
            objects.append(
                create_roof_course(
                    sign,
                    index,
                    center_u,
                    0.24,
                    output,
                    assembly,
                    course_material,
                )
            )

    for index, y in enumerate((-2.40, -1.60, -0.80, 0.0, 0.80, 1.60, 2.40), start=1):
        lift = 0.035 * math.sin(index * 1.7)
        objects.append(
            add_cylinder(
                f"OUT_RidgeCap_{index:02d}",
                (0.02 * math.sin(index), y, 5.34 + lift),
                0.20,
                0.88,
                (math.pi * 0.5, 0.0, 0.0),
                output,
                assembly,
                materials["roof_dark"],
                vertices=12,
                smooth=False,
                bevel_width=0.015,
            )
        )

    for sign in (-1, 1):
        side = "R" if sign > 0 else "L"
        eave_points = [roof_point(sign, 1.0, y) for y in ROOF_Y_ROWS]
        for index in range(len(eave_points) - 1):
            objects.append(
                add_beam_between(
                    f"OUT_EaveTrim_{side}_{index + 1:02d}",
                    eave_points[index] + Vector((0.0, 0.0, -0.08)),
                    eave_points[index + 1] + Vector((0.0, 0.0, -0.08)),
                    0.18,
                    0.18,
                    output,
                    assembly,
                    materials["timber"],
                    bevel_width=0.025,
                )
            )
        for face, y in (("Front", -2.82), ("Rear", 2.82)):
            objects.append(
                add_beam_between(
                    f"OUT_RoofRafter_{face}_{side}",
                    roof_point(sign, 0.02, y) + Vector((0.0, 0.0, 0.02)),
                    roof_point(sign, 1.0, y) + Vector((0.0, 0.0, 0.02)),
                    0.18,
                    0.22,
                    output,
                    assembly,
                    materials["timber"],
                    bevel_width=0.025,
                )
            )

    corner_specs = (
        ("FL", -2.78, -2.26, -1.2),
        ("FR", 2.88, -2.26, 0.8),
        ("RL", -2.78, 2.26, 0.9),
        ("RR", 2.88, 2.26, -1.0),
    )
    for label, x, y, angle in corner_specs:
        objects.append(
            add_box(
                f"OUT_CornerPost_{label}",
                (x, y, 1.55),
                (0.28, 0.28, 2.75),
                output,
                assembly,
                materials["timber"],
                rotation=(0.0, 0.0, math.radians(angle)),
                bevel_width=0.045,
            )
        )

    for face, y in (("Front", -2.38), ("Rear", 2.38)):
        for level, z in (("Lower", 0.55), ("Upper", 2.47)):
            objects.append(
                add_box(
                    f"OUT_FrameRail_{face}_{level}",
                    (0.05, y, z),
                    (5.75, 0.24, 0.24),
                    output,
                    assembly,
                    materials["timber"],
                    bevel_width=0.04,
                )
            )
    for side, x in (("Left", -2.89), ("Right", 2.99)):
        for level, z in (("Lower", 0.55), ("Upper", 2.47)):
            objects.append(
                add_box(
                    f"OUT_FrameRail_{side}_{level}",
                    (x, 0.0, z),
                    (0.24, 4.56, 0.24),
                    output,
                    assembly,
                    materials["timber"],
                    bevel_width=0.04,
                )
            )

    for label, x in (("FrontDivider", -0.30), ("RearDivider", 0.55)):
        y = -2.40 if label == "FrontDivider" else 2.40
        objects.append(
            add_box(
                f"OUT_FramePost_{label}",
                (x, y, 1.52),
                (0.25, 0.25, 2.65),
                output,
                assembly,
                materials["timber"],
                bevel_width=0.04,
            )
        )

    brace_specs = (
        ("Front_L", (-2.62, -2.43, 0.68), (-1.83, -2.43, 2.33)),
        ("Front_M", (-0.42, -2.43, 2.33), (-1.05, -2.43, 0.70)),
        ("Rear_L", (-2.62, 2.43, 0.68), (-1.55, 2.43, 2.33)),
        ("Rear_R", (2.70, 2.43, 0.68), (1.50, 2.43, 2.33)),
        ("Side_R_F", (2.99, -2.10, 0.68), (2.99, -1.05, 2.33)),
        ("Side_R_R", (2.99, 2.10, 0.68), (2.99, 1.05, 2.33)),
        ("Side_L", (-2.89, 1.95, 0.68), (-2.89, 0.72, 2.33)),
    )
    for label, start, end in brace_specs:
        objects.append(
            add_beam_between(
                f"OUT_FrameBrace_{label}",
                start,
                end,
                0.22,
                0.24,
                output,
                assembly,
                materials["timber"],
                bevel_width=0.035,
            )
        )

    for face, y in (("Front", -2.50), ("Rear", 2.50)):
        objects.extend(
            [
                add_beam_between(
                    f"OUT_GableRafter_{face}_L",
                    (-2.72, y, 2.58),
                    (0.04, y, 5.12),
                    0.20,
                    0.24,
                    output,
                    assembly,
                    materials["timber"],
                    bevel_width=0.035,
                ),
                add_beam_between(
                    f"OUT_GableRafter_{face}_R",
                    (2.72, y, 2.58),
                    (0.04, y, 5.12),
                    0.20,
                    0.24,
                    output,
                    assembly,
                    materials["timber"],
                    bevel_width=0.035,
                ),
            ]
        )

    objects.extend(
        create_arch_door(
            output,
            assembly,
            materials["door"],
            materials["timber"],
            materials["metal"],
        )
    )
    objects.extend(
        create_front_window(
            output,
            assembly,
            materials["window"],
            materials["timber"],
        )
    )
    objects.extend(
        create_side_window(
            output,
            assembly,
            materials["window"],
            materials["timber"],
        )
    )
    objects.extend(
        create_rear_window(
            output,
            assembly,
            materials["window"],
            materials["timber"],
        )
    )
    objects.extend(
        create_gable_window(
            output,
            assembly,
            materials["window"],
            materials["timber"],
        )
    )

    objects.extend(
        [
            create_tapered_box(
                "OUT_ChimneyLower",
                (-1.86, 0.82, 4.08),
                (0.82, 0.78),
                (0.70, 0.68),
                (0.08, 0.02),
                1.34,
                output,
                assembly,
                materials["stone"],
                bevel_width=0.07,
            ),
            create_tapered_box(
                "OUT_ChimneyUpper",
                (-1.78, 0.84, 5.06),
                (0.70, 0.68),
                (0.62, 0.61),
                (-0.07, 0.03),
                0.78,
                output,
                assembly,
                materials["stone_dark"],
                bevel_width=0.06,
            ),
            add_box(
                "OUT_ChimneyCap",
                (-1.85, 0.87, 5.52),
                (0.90, 0.84, 0.20),
                output,
                assembly,
                materials["stone_dark"],
                rotation=(0.0, 0.0, math.radians(-2.0)),
                bevel_width=0.06,
            ),
        ]
    )

    objects.extend(
        [
            add_box(
                "OUT_PorchCanopy",
                (0.90, -2.86, 2.55),
                (2.40, 1.16, 0.18),
                output,
                assembly,
                materials["roof_dark"],
                rotation=(math.radians(-11.0), 0.0, 0.0),
                bevel_width=0.055,
            ),
            add_box(
                "OUT_PorchPost_L",
                (0.03, -3.19, 1.28),
                (0.20, 0.20, 2.28),
                output,
                assembly,
                materials["timber"],
                rotation=(0.0, math.radians(-1.5), math.radians(-1.0)),
                bevel_width=0.035,
            ),
            add_box(
                "OUT_PorchPost_R",
                (1.82, -3.19, 1.28),
                (0.20, 0.20, 2.28),
                output,
                assembly,
                materials["timber"],
                rotation=(0.0, math.radians(1.0), math.radians(1.4)),
                bevel_width=0.035,
            ),
            add_box(
                "OUT_DoorStep_Lower",
                (0.92, -2.98, 0.16),
                (1.92, 0.90, 0.28),
                output,
                assembly,
                materials["stone"],
                bevel_width=0.07,
            ),
            add_box(
                "OUT_DoorStep_Upper",
                (0.92, -2.64, 0.30),
                (1.62, 0.62, 0.30),
                output,
                assembly,
                materials["stone_dark"],
                bevel_width=0.065,
            ),
        ]
    )

    for obj in objects:
        obj["building_role"] = obj.name.removeprefix("OUT_")
    return assembly, objects


def add_preview_floor(collection, assigned_material):
    floor = add_box(
        "PREVIEW_Ground",
        (0.0, 0.0, -0.16),
        (14.0, 14.0, 0.20),
        collection,
        None,
        assigned_material,
        bevel_width=0.0,
    )
    floor["artifact_role"] = "PREVIEW"
    return floor


def configure_scene():
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 900
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.world.color = (0.025, 0.030, 0.040)
    scene["asset_style"] = STYLE_PROFILE
    scene["artifact_scope"] = "stylized medieval-fantasy hero cottage exterior"
    scene["historical_confidence"] = "fantasy; no period claim"
    scene["interior_status"] = "not modeled"
    scene["collision_status"] = "not requested"
    scene["lod_status"] = "not requested"


def object_bounds(objects):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    corners = []
    for obj in objects:
        evaluated = obj.evaluated_get(depsgraph)
        corners.extend(
            evaluated.matrix_world @ Vector(corner)
            for corner in evaluated.bound_box
        )
    minimum = [min(point[index] for point in corners) for index in range(3)]
    maximum = [max(point[index] for point in corners) for index in range(3)]
    return {
        "minimum": [round(value, 6) for value in minimum],
        "maximum": [round(value, 6) for value in maximum],
        "dimensions": [
            round(maximum[index] - minimum[index], 6) for index in range(3)
        ],
    }


def topology_report(objects):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    base_vertices = 0
    base_triangles = 0
    evaluated_vertices = 0
    evaluated_triangles = 0
    components = []
    for obj in objects:
        mesh = obj.data
        base_component_triangles = sum(
            max(len(polygon.vertices) - 2, 0) for polygon in mesh.polygons
        )
        evaluated = obj.evaluated_get(depsgraph)
        evaluated_mesh = evaluated.to_mesh(
            preserve_all_data_layers=False,
            depsgraph=depsgraph,
        )
        try:
            evaluated_mesh.calc_loop_triangles()
            evaluated_component_triangles = len(evaluated_mesh.loop_triangles)
            component = {
                "name": obj.name,
                "base_vertices": len(mesh.vertices),
                "base_triangles": base_component_triangles,
                "evaluated_vertices": len(evaluated_mesh.vertices),
                "evaluated_triangles": evaluated_component_triangles,
                "material": obj.data.materials[0].name if obj.data.materials else None,
                "modifiers": [
                    {"name": modifier.name, "type": modifier.type}
                    for modifier in obj.modifiers
                ],
            }
        finally:
            evaluated.to_mesh_clear()
        base_vertices += component["base_vertices"]
        base_triangles += component["base_triangles"]
        evaluated_vertices += component["evaluated_vertices"]
        evaluated_triangles += component["evaluated_triangles"]
        components.append(component)
    return {
        "objects": len(objects),
        "base_vertices": base_vertices,
        "base_triangles": base_triangles,
        "evaluated_vertices": evaluated_vertices,
        "evaluated_triangles": evaluated_triangles,
        "components": components,
    }


def write_style_contract(path):
    contract = {
        "schema_version": 1,
        "asset": {
            "name": "Stylized Cottage",
            "stage": "clean-stylized exterior geometry",
            "profile": STYLE_PROFILE,
            "intent_summary": (
                "A compact medieval-fantasy cottage whose oversized roof, "
                "chunky timber rhythm, crooked chimney, and asymmetric facade "
                "read immediately at gameplay distance."
            ),
        },
        "references": [],
        "evidence_labels": {
            "reference_fidelity": "unconstrained original design",
            "construction_realism": "stylized but gravity-readable exterior",
            "surface_realism": "placeholder material blocks",
        },
        "style_axes": {
            "proportion_strategy": (
                "oversized roof and eaves; compact walls; enlarged openings; "
                "chunky structural trim"
            ),
            "construction_plausibility": (
                "readable foundation, wall mass, gables, rafters, beams, "
                "roof courses, chimney, and supported porch; no interior"
            ),
            "shape_language": "rounded chunky masses with coherent bow and lean",
            "visual_hierarchy": "roof first, facade openings second, timber rhythm third",
            "geometry_detail_density": "silhouette and major construction only",
            "material_realism": "broad illustrative placeholder blocks",
            "surface_frequency": "macro color blocks; no micro geometry or texture",
            "wear_narrative": "not authored",
            "presentation_target": "three-quarter gameplay and medium beauty views",
        },
        "visual_hierarchy": {
            "primary_element": "oversized bowed roof and ridge silhouette",
            "secondary_elements": [
                "arched door and supported porch",
                "crooked chimney",
                "chunky timber-frame rhythm",
                "round gable window",
            ],
            "allowed_exaggerations": [
                "roof-to-wall height",
                "eave thickness",
                "beam width",
                "door and window scale",
                "controlled chimney lean",
            ],
            "required_restraints": [
                "one coherent lean system",
                "supported roof and porch",
                "human-readable door",
                "quiet tertiary detail",
            ],
        },
        "ratios_and_landmarks": [
            {
                "name": "door_height_m",
                "target": 2.20,
                "unit": "m",
                "evidence": "stylized",
                "tolerance": 0.10,
            },
            {
                "name": "roof_height_to_wall_height",
                "target": 1.05,
                "unit": "ratio",
                "evidence": "stylized",
                "tolerance": 0.10,
            },
            {
                "name": "roof_overhang_m",
                "target": 0.48,
                "unit": "m",
                "evidence": "stylized",
                "tolerance": 0.10,
            },
        ],
        "surface_targets": {
            "macro": "plaster, timber, roof, stone, door, window, metal blocks",
            "mid_frequency": "deferred",
            "micro": "none at modeling stage",
            "base_color": "warm restrained palette with bright window accents",
            "roughness": "placeholder only",
            "normal_or_height": "deferred",
        },
        "review": {
            "fixed_views": [
                "front",
                "right side",
                "rear",
                "top",
                "front three-quarter",
                "rear three-quarter",
                "wireframe",
                "human scale",
                "gameplay distance",
            ],
            "gameplay_distance_m": 18.0,
            "close_review_distance_m": 6.0,
            "human_acceptance_questions": [
                "Does the roof dominate without swallowing the cottage?",
                "Does the asymmetry feel designed rather than random?",
                "Is the result charming and readable enough for further surfacing?",
            ],
            "known_limits": [
                "original design without calibrated image reference",
                "exterior shell only",
                "openings are recessed facade modules, not a playable interior",
                "collision, LOD, UVs, materials, bakes, and export are deferred",
                "medieval-fantasy appearance is not historical verification",
            ],
        },
    }
    path.write_text(json.dumps(contract, indent=2), encoding="utf-8")


def write_notes():
    text = bpy.data.texts.new("StylizedCottage_BenchmarkNotes")
    text.write(
        "Clean-stylized medieval-fantasy cottage benchmark\n"
        "Scope: exterior hero building, no playable interior\n"
        "Primary read: oversized bowed roof\n"
        "Secondary reads: arched door/porch, crooked chimney, timber rhythm\n"
        "Human scale: generic 1.8 m diagnostic in ASSET_ZOO\n"
        "Deferred: procedural surfaces, UVs, bakes, collision, LOD, Unity export\n"
        "Historical status: fantasy, not verified\n"
    )


def main():
    args = parse_args()
    output_path = args.output.resolve()
    report_path = args.report.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    clear_scene()
    configure_scene()
    collections = {
        name: ensure_collection(name)
        for name in (
            "MODULES",
            "VARIANTS",
            "TRIMS",
            "HERO",
            "ASSEMBLIES",
            "ASSET_ZOO",
            "CONTROLS",
            "COLLISION",
            "LOD",
            "PREVIEW",
        )
    }
    materials = {
        "plaster": material("MAT_Blockout_Plaster", (0.72, 0.52, 0.31), 0.0, 0.78),
        "plaster_dark": material(
            "MAT_Blockout_PlasterShade", (0.56, 0.36, 0.22), 0.0, 0.82
        ),
        "timber": material("MAT_Blockout_Timber", (0.16, 0.065, 0.028), 0.0, 0.67),
        "roof": material("MAT_Blockout_Roof", (0.34, 0.075, 0.045), 0.0, 0.76),
        "roof_dark": material(
            "MAT_Blockout_RoofDark", (0.20, 0.038, 0.026), 0.0, 0.80
        ),
        "stone": material("MAT_Blockout_Stone", (0.31, 0.34, 0.38), 0.0, 0.86),
        "stone_dark": material(
            "MAT_Blockout_StoneDark", (0.19, 0.22, 0.26), 0.0, 0.90
        ),
        "door": material("MAT_Blockout_Door", (0.10, 0.20, 0.17), 0.0, 0.68),
        "window": material("MAT_Blockout_Window", (0.20, 0.62, 0.82), 0.0, 0.32),
        "metal": material("MAT_Blockout_Metal", (0.07, 0.085, 0.10), 0.55, 0.44),
        "scale": material("MAT_ScaleReference", (0.10, 0.34, 0.62), 0.0, 0.55),
        "ground": material("MAT_PreviewGround", (0.045, 0.055, 0.062), 0.0, 0.90),
    }

    assembly, objects = create_cottage(collections, materials)
    add_preview_floor(collections["PREVIEW"], materials["ground"])
    write_notes()

    style_path = output_path.parent / "style-contract-v1.json"
    write_style_contract(style_path)
    bpy.ops.wm.save_as_mainfile(filepath=str(output_path), compress=True)

    report = {
        "source_file": str(output_path),
        "source_sha256": sha256(output_path),
        "blender_version": bpy.app.version_string,
        "stage": output_path.stem,
        "asset_parent": assembly.name,
        "artifact_scope": "stylized medieval-fantasy hero cottage exterior",
        "style_contract": str(style_path),
        "style_profile": STYLE_PROFILE,
        "world_units": "meters",
        "logical_footprint_m": [5.8, 4.6],
        "grid_increment_m": 0.25,
        "pivot_convention": "ground center",
        "evaluated_bounds": object_bounds(objects),
        "topology": topology_report(objects),
        "collections": sorted(collections),
        "module_status": "hero submodules only; no reusable village kit approved",
        "human_scale_reference": "FIT_HumanScale / 1.8 m generic diagnostic",
        "material_stage": "placeholder broad color blocks",
        "deferred": [
            "playable interior and circulation",
            "collision",
            "LOD chain",
            "UVs",
            "procedural materials and texture maps",
            "Unity export and round trip",
        ],
        "historical_confidence": "medieval-fantasy; no historical claim",
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"STYLIZED_COTTAGE_BLEND={output_path}")
    print(f"STYLIZED_COTTAGE_REPORT={report_path}")
    print(
        "STYLIZED_COTTAGE_DIMENSIONS_XYZ="
        + json.dumps(report["evaluated_bounds"]["dimensions"])
    )
    print(
        "STYLIZED_COTTAGE_EVALUATED_TRIANGLES="
        + str(report["topology"]["evaluated_triangles"])
    )


if __name__ == "__main__":
    main()
