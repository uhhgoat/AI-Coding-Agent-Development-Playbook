"""Create staged grounded low-poly wooden-barrel geometry."""

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector


SCRIPT_VERSION = "0.1.0"
ASSEMBLY_NAME = "OUT_GroundedBarrelAssembly"
STYLE_PROFILE = "grounded-realism-low-poly"
STAVE_COUNT = 24
HALF_HEIGHT = 0.48
PROFILE = (
    (-0.48, 0.285),
    (-0.425, 0.297),
    (-0.285, 0.323),
    (0.0, 0.337),
    (0.285, 0.323),
    (0.425, 0.297),
    (0.48, 0.285),
)
HOOP_SPECS = (
    (-0.405, 0.052),
    (-0.255, 0.044),
    (-0.085, 0.042),
    (0.085, 0.042),
    (0.255, 0.044),
    (0.405, 0.052),
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--style-contract", type=Path, required=True)
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return parser.parse_args(argv)


def file_sha256(path):
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


def create_material(name, color, metallic=0.0, roughness=0.62):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    material.diffuse_color = (*color, 1.0)
    principled = material.node_tree.nodes.get("Principled BSDF")
    principled.inputs["Base Color"].default_value = (*color, 1.0)
    principled.inputs["Metallic"].default_value = metallic
    principled.inputs["Roughness"].default_value = roughness
    material["artifact_stage"] = "modeling_placeholder"
    material["style_profile"] = STYLE_PROFILE
    return material


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
    materials,
    face_materials=None,
    bevel_width=0.0,
    bevel_segments=1,
    smooth_faces=None,
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
    for material in materials:
        mesh.materials.append(material)
    if face_materials is not None:
        for polygon, material_index in zip(mesh.polygons, face_materials):
            polygon.material_index = material_index
    if smooth_faces is not None:
        for polygon, should_smooth in zip(mesh.polygons, smooth_faces):
            polygon.use_smooth = should_smooth
    if bevel_width > 0.0:
        bevel = obj.modifiers.new("ConstructionBevel", "BEVEL")
        bevel.width = bevel_width
        bevel.segments = bevel_segments
        bevel.limit_method = "ANGLE"
        bevel.angle_limit = math.radians(20.0)
    return obj


def add_box(
    name,
    location,
    dimensions,
    rotation,
    collection,
    parent,
    material,
    bevel_width=0.0,
):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    move_to_collection(obj, collection)
    obj.parent = parent
    obj.data.materials.append(material)
    obj["artifact_role"] = "OUTPUT"
    obj["style_profile"] = STYLE_PROFILE
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.select_set(False)
    if bevel_width > 0.0:
        bevel = obj.modifiers.new("ConstructionBevel", "BEVEL")
        bevel.width = bevel_width
        bevel.segments = 1
        bevel.limit_method = "ANGLE"
        bevel.angle_limit = math.radians(20.0)
    return obj


def add_cylinder(
    name,
    location,
    radius,
    depth,
    direction,
    collection,
    parent,
    material,
    vertices=10,
    bevel_width=0.0,
):
    direction = Vector(direction).normalized()
    rotation = direction.to_track_quat("Z", "Y").to_euler()
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
    obj.data.materials.append(material)
    obj["artifact_role"] = "OUTPUT"
    obj["style_profile"] = STYLE_PROFILE
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.select_set(False)
    if bevel_width > 0.0:
        bevel = obj.modifiers.new("ConstructionBevel", "BEVEL")
        bevel.width = bevel_width
        bevel.segments = 1
        bevel.limit_method = "ANGLE"
        bevel.angle_limit = math.radians(20.0)
    return obj


def radius_at(z):
    if z <= PROFILE[0][0]:
        return PROFILE[0][1]
    if z >= PROFILE[-1][0]:
        return PROFILE[-1][1]
    for (z0, r0), (z1, r1) in zip(PROFILE, PROFILE[1:]):
        if z0 <= z <= z1:
            factor = (z - z0) / (z1 - z0)
            eased = factor * factor * (3.0 - 2.0 * factor)
            return r0 + (r1 - r0) * eased
    raise RuntimeError(f"Could not evaluate barrel radius at z={z}")


def append_closed_shell_segment(
    vertices,
    faces,
    face_materials,
    smooth_faces,
    angle_start,
    angle_end,
    material_index,
):
    start = len(vertices)
    radial_thickness = 0.033
    for z, outer_radius in PROFILE:
        inner_radius = outer_radius - radial_thickness
        for radius in (outer_radius, inner_radius):
            vertices.append(
                (
                    radius * math.cos(angle_start),
                    radius * math.sin(angle_start),
                    z,
                )
            )
            vertices.append(
                (
                    radius * math.cos(angle_end),
                    radius * math.sin(angle_end),
                    z,
                )
            )
    ring_count = len(PROFILE)
    for level in range(ring_count - 1):
        current = start + level * 4
        following = current + 4
        faces.append((current, following, following + 1, current + 1))
        face_materials.append(material_index)
        smooth_faces.append(True)
        faces.append((current + 2, current + 3, following + 3, following + 2))
        face_materials.append(material_index)
        smooth_faces.append(False)
        faces.append((current, current + 2, following + 2, following))
        face_materials.append(material_index)
        smooth_faces.append(False)
        faces.append(
            (current + 1, following + 1, following + 3, current + 3)
        )
        face_materials.append(material_index)
        smooth_faces.append(False)
    bottom = start
    top = start + (ring_count - 1) * 4
    faces.append((bottom, bottom + 1, bottom + 3, bottom + 2))
    face_materials.append(material_index)
    smooth_faces.append(False)
    faces.append((top, top + 2, top + 3, top + 1))
    face_materials.append(material_index)
    smooth_faces.append(False)


def create_staves(collection, parent, materials):
    vertices = []
    faces = []
    face_materials = []
    smooth_faces = []
    pitch = math.tau / STAVE_COUNT
    seam_angle = 0.012
    for index in range(STAVE_COUNT):
        center = -math.pi * 0.5 + index * pitch
        angle_start = center - pitch * 0.5 + seam_angle * 0.5
        angle_end = center + pitch * 0.5 - seam_angle * 0.5
        material_index = 1 if index in {3, 8, 14, 20} else 0
        append_closed_shell_segment(
            vertices,
            faces,
            face_materials,
            smooth_faces,
            angle_start,
            angle_end,
            material_index,
        )
    obj = create_mesh_object(
        "OUT_Staves",
        vertices,
        faces,
        collection,
        parent,
        materials,
        face_materials=face_materials,
        bevel_width=0.0025,
        bevel_segments=1,
        smooth_faces=smooth_faces,
    )
    obj["construction"] = (
        "twenty-four individually closed bowed stave volumes around a hollow body"
    )
    obj["stave_count"] = STAVE_COUNT
    obj["radial_thickness_m"] = 0.033
    obj["geometry_material_boundary"] = (
        "stave silhouette, seams, thickness, and bilge curvature are geometry"
    )
    return obj


def append_annular_band(vertices, faces, center_z, height, segment_count=24):
    start = len(vertices)
    z_low = center_z - height * 0.5
    z_high = center_z + height * 0.5
    inner_low = radius_at(z_low) + 0.004
    inner_high = radius_at(z_high) + 0.004
    outer_low = inner_low + 0.014
    outer_high = inner_high + 0.014
    for index in range(segment_count):
        angle = math.tau * index / segment_count
        cosine = math.cos(angle)
        sine = math.sin(angle)
        vertices.extend(
            (
                (inner_low * cosine, inner_low * sine, z_low),
                (outer_low * cosine, outer_low * sine, z_low),
                (inner_high * cosine, inner_high * sine, z_high),
                (outer_high * cosine, outer_high * sine, z_high),
            )
        )
    for index in range(segment_count):
        following = (index + 1) % segment_count
        current = start + index * 4
        next_vertex = start + following * 4
        faces.extend(
            (
                (current + 1, next_vertex + 1, next_vertex + 3, current + 3),
                (current, current + 2, next_vertex + 2, next_vertex),
                (current + 2, current + 3, next_vertex + 3, next_vertex + 2),
                (current, next_vertex, next_vertex + 1, current + 1),
            )
        )
    return outer_low, outer_high


def create_hoops(collection, parent, material):
    vertices = []
    faces = []
    radii = []
    for center_z, height in HOOP_SPECS:
        radii.append(
            append_annular_band(vertices, faces, center_z, height)
        )
    obj = create_mesh_object(
        "OUT_IronHoops",
        vertices,
        faces,
        collection,
        parent,
        (material,),
        bevel_width=0.0018,
        bevel_segments=1,
    )
    obj["construction"] = (
        "six closed low-poly bands conforming to the stave profile"
    )
    obj["hoop_count"] = len(HOOP_SPECS)
    obj["radial_thickness_m"] = 0.014
    return obj, radii


def clip_polygon_x(polygon, boundary, keep_greater):
    if not polygon:
        return []
    result = []
    previous = polygon[-1]
    previous_inside = previous[0] >= boundary if keep_greater else previous[0] <= boundary
    for current in polygon:
        current_inside = current[0] >= boundary if keep_greater else current[0] <= boundary
        if current_inside != previous_inside:
            delta_x = current[0] - previous[0]
            factor = 0.0 if abs(delta_x) < 1e-9 else (boundary - previous[0]) / delta_x
            result.append(
                (
                    boundary,
                    previous[1] + (current[1] - previous[1]) * factor,
                )
            )
        if current_inside:
            result.append(current)
        previous = current
        previous_inside = current_inside
    return result


def append_extruded_head_board(
    vertices,
    faces,
    face_materials,
    polygon,
    z_low,
    z_high,
    material_index,
):
    start = len(vertices)
    count = len(polygon)
    vertices.extend((x, y, z_low) for x, y in polygon)
    vertices.extend((x, y, z_high) for x, y in polygon)
    faces.append(tuple(start + index for index in range(count - 1, -1, -1)))
    face_materials.append(material_index)
    faces.append(tuple(start + count + index for index in range(count)))
    face_materials.append(material_index)
    for index in range(count):
        following = (index + 1) % count
        faces.append(
            (
                start + index,
                start + following,
                start + count + following,
                start + count + index,
            )
        )
        face_materials.append(material_index)


def create_head_boards(name, z_low, z_high, collection, parent, materials):
    radius = 0.263
    circle = [
        (
            radius * math.cos(math.tau * index / 32),
            radius * math.sin(math.tau * index / 32),
        )
        for index in range(32)
    ]
    board_count = 7
    step = radius * 2.0 / board_count
    gap = 0.0022
    vertices = []
    faces = []
    face_materials = []
    created = 0
    for index in range(board_count):
        lower = -radius + index * step + (gap * 0.5 if index > 0 else 0.0)
        upper = -radius + (index + 1) * step - (
            gap * 0.5 if index < board_count - 1 else 0.0
        )
        polygon = clip_polygon_x(circle, lower, keep_greater=True)
        polygon = clip_polygon_x(polygon, upper, keep_greater=False)
        if len(polygon) < 3:
            continue
        append_extruded_head_board(
            vertices,
            faces,
            face_materials,
            polygon,
            z_low,
            z_high,
            1 if index in {1, 5} else 0,
        )
        created += 1
    obj = create_mesh_object(
        name,
        vertices,
        faces,
        collection,
        parent,
        materials,
        face_materials=face_materials,
        bevel_width=0.0012,
        bevel_segments=1,
    )
    obj["construction"] = (
        "seven straight coopered head boards clipped to a circular head"
    )
    obj["board_count"] = created
    obj["head_radius_m"] = radius
    return obj


def create_hoop_laps_and_rivets(collection, parent, iron_material, radii):
    objects = []
    angle_offsets = (-5.0, 3.0, -2.0, 4.0, -4.0, 2.0)
    for index, ((center_z, height), (outer_low, outer_high), offset) in enumerate(
        zip(HOOP_SPECS, radii, angle_offsets),
        start=1,
    ):
        angle = -math.pi * 0.5 + math.radians(offset)
        radial = Vector((math.cos(angle), math.sin(angle), 0.0))
        tangent_angle = angle + math.pi * 0.5
        outer_radius = max(outer_low, outer_high)
        lap_depth = 0.008
        lap = add_box(
            f"OUT_HoopLap_{index:02d}",
            radial * (outer_radius + lap_depth * 0.5) + Vector((0.0, 0.0, center_z)),
            (0.070, lap_depth, height * 0.78),
            (0.0, 0.0, tangent_angle),
            collection,
            parent,
            iron_material,
            bevel_width=0.0015,
        )
        lap["construction"] = "overlapping hoop joint"
        objects.append(lap)
        tangent = Vector((-math.sin(angle), math.cos(angle), 0.0))
        for rivet_index, tangent_offset in enumerate((-0.021, 0.021), start=1):
            location = (
                radial * (outer_radius + lap_depth + 0.0035)
                + tangent * tangent_offset
                + Vector((0.0, 0.0, center_z))
            )
            rivet = add_cylinder(
                f"OUT_HoopRivet_{index:02d}_{rivet_index}",
                location,
                0.0065,
                0.006,
                radial,
                collection,
                parent,
                iron_material,
                vertices=8,
                bevel_width=0.0012,
            )
            rivet["construction"] = "low-poly peened hoop rivet"
            objects.append(rivet)
    return objects


def create_bung(collection, parent, wood_material, dark_material):
    angle = -math.pi * 0.5
    z = 0.035
    radial = Vector((math.cos(angle), math.sin(angle), 0.0))
    radius = radius_at(z)
    seat = add_cylinder(
        "OUT_BungSeat",
        radial * (radius + 0.001) + Vector((0.0, 0.0, z)),
        0.033,
        0.008,
        radial,
        collection,
        parent,
        dark_material,
        vertices=10,
        bevel_width=0.001,
    )
    seat["construction"] = "recessed dark bung-hole seat"
    plug = add_cylinder(
        "OUT_BungPlug",
        radial * (radius + 0.009) + Vector((0.0, 0.0, z)),
        0.027,
        0.017,
        radial,
        collection,
        parent,
        wood_material,
        vertices=10,
        bevel_width=0.0018,
    )
    plug["construction"] = "inserted tapered-plug approximation"
    return [seat, plug]


def create_lathed_blockout(collection, parent, wood_material, iron_material):
    vertices = []
    faces = []
    segments = 24
    for z, radius in PROFILE:
        for index in range(segments):
            angle = math.tau * index / segments
            vertices.append((radius * math.cos(angle), radius * math.sin(angle), z))
    ring_count = len(PROFILE)
    for level in range(ring_count - 1):
        for index in range(segments):
            following = (index + 1) % segments
            current = level * segments + index
            next_ring = current + segments
            faces.append((current, next_ring, next_ring - index + following, level * segments + following))
    faces.append(tuple(range(segments - 1, -1, -1)))
    top_start = (ring_count - 1) * segments
    faces.append(tuple(top_start + index for index in range(segments)))
    body = create_mesh_object(
        "OUT_BlockoutEnvelope",
        vertices,
        faces,
        collection,
        parent,
        (wood_material,),
        bevel_width=0.0,
        smooth_faces=[True] * len(faces),
    )
    body["construction"] = "continuous envelope only; not accepted stave topology"
    vertices = []
    faces = []
    for center_z, height in HOOP_SPECS:
        append_annular_band(vertices, faces, center_z, height)
    hoops = create_mesh_object(
        "OUT_BlockoutHoopZones",
        vertices,
        faces,
        collection,
        parent,
        (iron_material,),
        bevel_width=0.0,
    )
    hoops["construction"] = "blockout hoop placement only"
    return [body, hoops]


def delete_objects(objects):
    for obj in objects:
        mesh = obj.data if obj.type == "MESH" else None
        bpy.data.objects.remove(obj, do_unlink=True)
        if mesh is not None and mesh.users == 0:
            bpy.data.meshes.remove(mesh)


def create_profile_control(collection):
    curve_data = bpy.data.curves.new("CTRL_BarrelProfile_Curve", "CURVE")
    curve_data.dimensions = "3D"
    curve_data.resolution_u = 1
    spline = curve_data.splines.new("POLY")
    spline.points.add(len(PROFILE) - 1)
    for point, (z, radius) in zip(spline.points, PROFILE):
        point.co = (radius, 0.0, z, 1.0)
    control = bpy.data.objects.new("CTRL_BarrelProfile", curve_data)
    collection.objects.link(control)
    control.hide_render = True
    control["artifact_role"] = "CONTROL"
    control["profile_z_radius_m"] = json.dumps(PROFILE)
    return control


def add_preview_floor(collection, material):
    return add_box(
        "PREVIEW_Ground",
        (0.0, 0.0, -0.505),
        (3.5, 3.5, 0.03),
        (0.0, 0.0, 0.0),
        collection,
        None,
        material,
        bevel_width=0.0,
    )


def add_area_light(collection, name, location, target, energy, size, color):
    light_data = bpy.data.lights.new(name, "AREA")
    light_data.energy = energy
    light_data.shape = "DISK"
    light_data.size = size
    light_data.color = color
    light = bpy.data.objects.new(name, light_data)
    collection.objects.link(light)
    light.location = Vector(location)
    light.rotation_euler = (
        Vector(target) - light.location
    ).to_track_quat("-Z", "Y").to_euler()
    light["artifact_role"] = "PREVIEW"
    return light


def configure_scene(preview_collection, floor_material):
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 800
    scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.image_settings.color_mode = "RGBA"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.world.color = (0.018, 0.022, 0.028)
    if scene.world and scene.world.use_nodes:
        background = scene.world.node_tree.nodes.get("Background")
        background.inputs["Color"].default_value = (0.018, 0.022, 0.028, 1.0)
        background.inputs["Strength"].default_value = 0.25
    add_preview_floor(preview_collection, floor_material)
    target = (0.0, 0.0, 0.02)
    add_area_light(
        preview_collection,
        "PREVIEW_Key",
        (2.2, -3.0, 2.7),
        target,
        650.0,
        2.0,
        (1.0, 0.78, 0.58),
    )
    add_area_light(
        preview_collection,
        "PREVIEW_Fill",
        (-2.0, -1.2, 1.3),
        target,
        300.0,
        2.2,
        (0.52, 0.68, 1.0),
    )
    add_area_light(
        preview_collection,
        "PREVIEW_Rim",
        (1.2, 2.5, 2.2),
        target,
        720.0,
        1.8,
        (0.70, 0.82, 1.0),
    )
    scene["asset_style"] = STYLE_PROFILE
    scene["artifact_scope"] = "grounded low-poly wooden barrel modeling source"
    scene["surface_status"] = "placeholder materials only"
    scene["uv_status"] = "not authored"
    scene["collision_status"] = "not requested"
    scene["lod_status"] = "LOD0 modeling candidate; no LOD chain authored"


def output_meshes(assembly):
    return sorted(
        (
            obj
            for obj in bpy.context.scene.objects
            if obj.type == "MESH" and obj.parent == assembly
        ),
        key=lambda obj: obj.name,
    )


def mesh_summary(objects):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    base_vertices = sum(len(obj.data.vertices) for obj in objects)
    base_triangles = sum(
        sum(max(len(polygon.vertices) - 2, 0) for polygon in obj.data.polygons)
        for obj in objects
    )
    evaluated_vertices = 0
    evaluated_triangles = 0
    corners = []
    for obj in objects:
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh(preserve_all_data_layers=False, depsgraph=depsgraph)
        try:
            evaluated_vertices += len(mesh.vertices)
            evaluated_triangles += sum(
                max(len(polygon.vertices) - 2, 0)
                for polygon in mesh.polygons
            )
            corners.extend(
                evaluated.matrix_world @ Vector(corner)
                for corner in evaluated.bound_box
            )
        finally:
            evaluated.to_mesh_clear()
    minimum = [min(corner[index] for corner in corners) for index in range(3)]
    maximum = [max(corner[index] for corner in corners) for index in range(3)]
    return {
        "objects": len(objects),
        "base_vertices": base_vertices,
        "base_triangles": base_triangles,
        "evaluated_vertices": evaluated_vertices,
        "evaluated_triangles": evaluated_triangles,
        "bounds": {
            "minimum": [round(value, 6) for value in minimum],
            "maximum": [round(value, 6) for value in maximum],
            "dimensions": [
                round(maximum[index] - minimum[index], 6)
                for index in range(3)
            ],
        },
    }


def save_stage(path):
    bpy.ops.wm.save_as_mainfile(filepath=str(path))
    return {
        "path": str(path),
        "sha256": file_sha256(path),
        "size_bytes": path.stat().st_size,
    }


def main():
    args = parse_args()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    style_contract_path = args.style_contract.resolve()
    if not style_contract_path.exists():
        raise RuntimeError(f"Style contract not found: {style_contract_path}")
    style_contract = json.loads(style_contract_path.read_text(encoding="utf-8"))
    if style_contract["asset"]["profile"] != STYLE_PROFILE:
        raise RuntimeError("Style-contract profile does not match barrel generator")

    clear_scene()
    collections = {
        name: ensure_collection(name)
        for name in ("SOURCE", "CONTROLS", "OUTPUT", "PREVIEW")
    }
    assembly = create_empty(ASSEMBLY_NAME, collections["OUTPUT"])
    assembly["artifact_role"] = "OUTPUT_ASSEMBLY"
    assembly["style_profile"] = STYLE_PROFILE
    assembly["construction"] = "coopered wooden barrel with fitted iron hoops"
    assembly["origin_convention"] = "ground-centered, upright local Z"
    assembly["height_m"] = 0.96
    assembly["maximum_diameter_m"] = 0.674
    assembly["stave_count"] = STAVE_COUNT
    assembly["hoop_count"] = len(HOOP_SPECS)
    source = create_empty("SOURCE_BarrelDesign", collections["SOURCE"])
    source["artifact_role"] = "SOURCE"
    source["evidence_class"] = "pipeline-valid original construction"
    source["reference_status"] = "no external mesh or tutorial project used"
    create_profile_control(collections["CONTROLS"])

    materials = {
        "wood": create_material("MAT_Blockout_BarrelWood", (0.29, 0.105, 0.028), roughness=0.62),
        "wood_alt": create_material("MAT_Blockout_BarrelWoodAlt", (0.235, 0.070, 0.018), roughness=0.64),
        "head": create_material("MAT_Blockout_HeadWood", (0.34, 0.145, 0.045), roughness=0.66),
        "head_alt": create_material("MAT_Blockout_HeadWoodAlt", (0.285, 0.105, 0.030), roughness=0.68),
        "iron": create_material("MAT_Blockout_HoopIron", (0.075, 0.085, 0.095), metallic=0.82, roughness=0.36),
        "dark": create_material("MAT_Blockout_Recess", (0.025, 0.014, 0.008), roughness=0.78),
        "floor": create_material("MAT_PREVIEW_Floor", (0.045, 0.052, 0.060), roughness=0.83),
    }
    configure_scene(collections["PREVIEW"], materials["floor"])

    blockout_objects = create_lathed_blockout(
        collections["OUTPUT"],
        assembly,
        materials["wood"],
        materials["iron"],
    )
    blockout_summary = mesh_summary(output_meshes(assembly))
    stage_00_path = output_dir / "stage-00-grounded-lowpoly-barrel-blockout.blend"
    stage_00 = save_stage(stage_00_path)

    delete_objects(blockout_objects)
    constructed = [
        create_staves(
            collections["OUTPUT"],
            assembly,
            (materials["wood"], materials["wood_alt"]),
        ),
        create_head_boards(
            "OUT_HeadBoards_Top",
            0.442,
            0.461,
            collections["OUTPUT"],
            assembly,
            (materials["head"], materials["head_alt"]),
        ),
        create_head_boards(
            "OUT_HeadBoards_Bottom",
            -0.461,
            -0.442,
            collections["OUTPUT"],
            assembly,
            (materials["head"], materials["head_alt"]),
        ),
    ]
    hoops, radii = create_hoops(
        collections["OUTPUT"],
        assembly,
        materials["iron"],
    )
    constructed.append(hoops)
    constructed.extend(
        create_hoop_laps_and_rivets(
            collections["OUTPUT"],
            assembly,
            materials["iron"],
            radii,
        )
    )
    constructed.extend(
        create_bung(
            collections["OUTPUT"],
            assembly,
            materials["head"],
            materials["dark"],
        )
    )
    for obj in constructed:
        obj["building_role"] = obj.name.removeprefix("OUT_")
    construction_summary = mesh_summary(output_meshes(assembly))
    budget = style_contract["budget"]
    if construction_summary["base_triangles"] > budget["base_triangle_target_max"]:
        raise RuntimeError("Base triangle budget exceeded")
    if construction_summary["evaluated_triangles"] > budget["evaluated_triangle_target_max"]:
        raise RuntimeError("Evaluated triangle budget exceeded")

    stage_01_path = output_dir / "stage-01-grounded-lowpoly-barrel-construction.blend"
    stage_01 = save_stage(stage_01_path)
    manifest = {
        "schema_version": 1,
        "script_version": SCRIPT_VERSION,
        "blender_version": bpy.app.version_string,
        "style_contract": {
            "path": str(style_contract_path),
            "sha256": file_sha256(style_contract_path),
        },
        "source_evidence": {
            "classification": "pipeline-valid",
            "description": "original project-owned scripted coopered-barrel construction",
            "external_reference": None,
        },
        "stages": {
            "stage_00": {
                **stage_00,
                "summary": blockout_summary,
                "purpose": "macro envelope and hoop placement",
            },
            "stage_01": {
                **stage_01,
                "summary": construction_summary,
                "purpose": "staves, board-built heads, conforming hoops, lap joints, rivets, and bung",
            },
        },
        "construction_parameters": {
            "profile_z_radius_m": PROFILE,
            "stave_count": STAVE_COUNT,
            "hoop_specs_z_height_m": HOOP_SPECS,
            "head_radius_m": 0.263,
            "head_board_count": 7,
            "stave_thickness_m": 0.033,
            "hoop_radial_thickness_m": 0.014,
        },
        "geometry_material_boundary": {
            "geometry": [
                "overall bilge-to-head silhouette",
                "stave seams and thickness",
                "head-board seams and inset",
                "hoop profile, lap joints, and rivets",
                "bung seat and plug",
            ],
            "deferred_surface": [
                "longitudinal and end grain",
                "wood pores and finish",
                "iron forging, oxidation, and scratches",
                "moisture, hoop contact, and rim wear",
            ],
        },
        "preview": {
            "directory": str((output_dir / "renders").resolve()),
            "required": [
                "stage-01-front.png",
                "stage-01-side.png",
                "stage-01-top.png",
                "stage-01-front-three-quarter.png",
                "stage-01-grazing.png",
                "stage-01-wireframe.png",
                "stage-01-gameplay-distance.png",
            ],
        },
        "validation": {
            "path": str(
                (
                    output_dir
                    / "validation"
                    / "stage-01-structural.json"
                ).resolve()
            ),
            "status": "pending",
        },
        "iteration_log": [
            {
                "stage": "stage-00",
                "severity": "high",
                "contract_axis": "construction plausibility",
                "observation": "continuous envelope does not expose stave thickness, head construction, or fitted hardware",
                "evidence_view": "stage-00 is a recoverable proportional blockout",
                "intended_fix": "replace the envelope with closed stave volumes and explicit coopered construction",
                "result": "fixed in stage-01",
                "residual": "visual review pending",
            }
        ],
        "deferred": [
            "UV unwrap",
            "realistic procedural wood/end-grain/iron materials",
            "PBR bake",
            "collision",
            "LOD chain",
            "Unity export and URP validation",
        ],
    }
    manifest_path = output_dir / "operation-manifest-v1.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"BARREL_STAGE_00={stage_00_path}")
    print(f"BARREL_STAGE_01={stage_01_path}")
    print(f"BARREL_MANIFEST={manifest_path}")
    print(f"BARREL_STAGE_01_SHA256={stage_01['sha256']}")
    print(f"BARREL_STAGE_01_SUMMARY={json.dumps(construction_summary, sort_keys=True)}")


if __name__ == "__main__":
    main()
