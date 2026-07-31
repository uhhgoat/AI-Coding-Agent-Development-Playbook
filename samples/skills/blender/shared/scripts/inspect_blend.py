"""Emit a read-only structural report for the currently opened Blender file."""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import bpy


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        help="JSON report path. Prints JSON to stdout when omitted.",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation level.",
    )
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return parser.parse_args(argv)


def rounded(value):
    if isinstance(value, float):
        return round(value, 6)
    if hasattr(value, "__iter__") and not isinstance(value, (str, bytes)):
        return [rounded(item) for item in value]
    if not isinstance(value, (str, bytes)):
        try:
            return [rounded(value[index]) for index in range(len(value))]
        except (KeyError, TypeError):
            pass
    return value


def json_default(value):
    if hasattr(value, "name"):
        return value.name
    if hasattr(value, "__iter__"):
        return [rounded(item) for item in value]
    try:
        return [rounded(value[index]) for index in range(len(value))]
    except (KeyError, TypeError):
        pass
    return str(value)


def id_name(value):
    return value.name if value is not None and hasattr(value, "name") else None


def safe_attr(owner, attribute):
    if not hasattr(owner, attribute):
        return None
    try:
        return rounded(getattr(owner, attribute))
    except (AttributeError, TypeError, ValueError):
        return None


def modifier_report(modifier):
    attributes_by_type = {
        "ARMATURE": (
            "object",
            "use_deform_preserve_volume",
            "use_vertex_groups",
            "use_bone_envelopes",
        ),
        "ARRAY": (
            "count",
            "fit_type",
            "relative_offset_displace",
            "constant_offset_displace",
            "use_relative_offset",
            "use_constant_offset",
            "use_object_offset",
            "offset_object",
            "use_merge_vertices",
            "merge_threshold",
        ),
        "BEVEL": (
            "width",
            "segments",
            "limit_method",
            "angle_limit",
            "affect",
            "harden_normals",
            "miter_outer",
        ),
        "BOOLEAN": (
            "operation",
            "solver",
            "operand_type",
            "object",
            "collection",
            "double_threshold",
        ),
        "CAST": (
            "cast_type",
            "factor",
            "radius",
            "size",
            "use_radius_as_size",
            "use_x",
            "use_y",
            "use_z",
            "vertex_group",
            "object",
        ),
        "CURVE": ("object", "deform_axis"),
        "DATA_TRANSFER": (
            "object",
            "use_vert_data",
            "data_types_verts",
            "vert_mapping",
            "layers_vgroup_select_src",
            "layers_vgroup_select_dst",
            "mix_mode",
            "mix_factor",
            "vertex_group",
        ),
        "DECIMATE": (
            "decimate_type",
            "ratio",
            "iterations",
            "angle_limit",
            "use_collapse_triangulate",
        ),
        "DISPLACE": (
            "strength",
            "mid_level",
            "direction",
            "texture_coords",
            "texture",
            "texture_coords_object",
            "uv_layer",
        ),
        "MIRROR": (
            "use_axis",
            "use_bisect_axis",
            "use_bisect_flip_axis",
            "use_clip",
            "use_mirror_merge",
            "merge_threshold",
            "mirror_object",
        ),
        "NODES": ("node_group",),
        "REMESH": (
            "mode",
            "octree_depth",
            "scale",
            "sharpness",
            "threshold",
            "voxel_size",
        ),
        "SCREW": (
            "angle",
            "screw_offset",
            "iterations",
            "steps",
            "render_steps",
            "axis",
            "object",
            "use_merge_vertices",
            "merge_threshold",
        ),
        "SHRINKWRAP": (
            "target",
            "auxiliary_target",
            "wrap_method",
            "wrap_mode",
            "offset",
            "project_limit",
            "use_project_x",
            "use_project_y",
            "use_project_z",
        ),
        "SIMPLE_DEFORM": (
            "deform_method",
            "deform_axis",
            "angle",
            "factor",
            "origin",
            "limits",
            "lock_x",
            "lock_y",
            "lock_z",
        ),
        "SOLIDIFY": (
            "thickness",
            "offset",
            "use_even_offset",
            "use_quality_normals",
            "use_rim",
            "solidify_mode",
        ),
        "SUBSURF": (
            "subdivision_type",
            "levels",
            "render_levels",
            "quality",
            "show_only_control_edges",
            "use_creases",
        ),
        "TRIANGULATE": (
            "quad_method",
            "ngon_method",
            "min_vertices",
            "keep_custom_normals",
        ),
        "WELD": ("merge_threshold", "mode", "loose_edges"),
        "WEIGHTED_NORMAL": (
            "mode",
            "weight",
            "keep_sharp",
            "thresh",
            "use_face_influence",
        ),
    }
    result = {
        "name": modifier.name,
        "type": modifier.type,
        "show_viewport": modifier.show_viewport,
        "show_render": modifier.show_render,
    }
    for attribute in attributes_by_type.get(modifier.type, ()):
        value = safe_attr(modifier, attribute)
        if hasattr(getattr(modifier, attribute, None), "name"):
            value = id_name(getattr(modifier, attribute))
        if value is not None:
            result[attribute] = value
    return result


def animation_report(obj):
    animation_data = obj.animation_data
    if animation_data is None:
        return None
    return {
        "action": id_name(animation_data.action),
        "nla_tracks": [
            {
                "name": track.name,
                "strips": [
                    {
                        "name": strip.name,
                        "action": id_name(strip.action),
                        "frame_start": rounded(strip.frame_start),
                        "frame_end": rounded(strip.frame_end),
                    }
                    for strip in track.strips
                ],
            }
            for track in animation_data.nla_tracks
        ],
    }


def mesh_report(mesh):
    mesh.calc_loop_triangles()
    return {
        "vertices": len(mesh.vertices),
        "edges": len(mesh.edges),
        "polygons": len(mesh.polygons),
        "triangles": len(mesh.loop_triangles),
        "loops": len(mesh.loops),
        "uv_layers": [layer.name for layer in mesh.uv_layers],
        "color_attributes": [attribute.name for attribute in mesh.color_attributes],
        "shape_keys": (
            [key.name for key in mesh.shape_keys.key_blocks]
            if mesh.shape_keys is not None
            else []
        ),
        "materials": [id_name(material) for material in mesh.materials],
        "users": mesh.users,
    }


def armature_report(armature):
    return {
        "bones": len(armature.bones),
        "bone_names": [bone.name for bone in armature.bones],
        "users": armature.users,
    }


def evaluated_mesh_report(obj, depsgraph):
    if obj.type != "MESH" or not obj.modifiers:
        return None
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh(preserve_all_data_layers=False, depsgraph=depsgraph)
    try:
        mesh.calc_loop_triangles()
        return {
            "vertices": len(mesh.vertices),
            "edges": len(mesh.edges),
            "polygons": len(mesh.polygons),
            "triangles": len(mesh.loop_triangles),
        }
    finally:
        evaluated.to_mesh_clear()


def object_report(obj, depsgraph):
    collections = sorted(collection.name for collection in obj.users_collection)
    result = {
        "name": obj.name,
        "type": obj.type,
        "data": id_name(obj.data),
        "collections": collections,
        "parent": id_name(obj.parent),
        "parent_type": obj.parent_type,
        "location": rounded(obj.location),
        "rotation_mode": obj.rotation_mode,
        "rotation_euler": rounded(obj.rotation_euler),
        "scale": rounded(obj.scale),
        "dimensions": rounded(obj.dimensions),
        "negative_world_determinant": obj.matrix_world.determinant() < 0.0,
        "hide_viewport": obj.hide_viewport,
        "hide_render": obj.hide_render,
        "display_type": obj.display_type,
        "instance_type": obj.instance_type,
        "instance_collection": id_name(obj.instance_collection),
        "vertex_groups": [group.name for group in obj.vertex_groups],
        "modifiers": [modifier_report(modifier) for modifier in obj.modifiers],
        "constraints": [
            {"name": constraint.name, "type": constraint.type}
            for constraint in obj.constraints
        ],
        "animation": animation_report(obj),
        "custom_property_keys": sorted(
            key for key in obj.keys() if key != "_RNA_UI"
        ),
    }
    if obj.type == "MESH" and obj.data is not None:
        result["mesh"] = mesh_report(obj.data)
        evaluated_mesh = evaluated_mesh_report(obj, depsgraph)
        if evaluated_mesh is not None:
            result["evaluated_mesh"] = evaluated_mesh
    elif obj.type == "ARMATURE" and obj.data is not None:
        result["armature"] = armature_report(obj.data)
        result["pose_constraint_count"] = sum(
            len(pose_bone.constraints) for pose_bone in obj.pose.bones
        )
    return result


def material_report(material):
    node_types = Counter()
    image_nodes = []
    principled_inputs = {}
    if material.use_nodes and material.node_tree is not None:
        for node in material.node_tree.nodes:
            node_types[node.bl_idname] += 1
            if node.bl_idname == "ShaderNodeTexImage":
                image_nodes.append(id_name(node.image))
            elif node.bl_idname == "ShaderNodeBsdfPrincipled":
                for input_name in (
                    "Base Color",
                    "Metallic",
                    "Roughness",
                    "IOR",
                    "Alpha",
                    "Normal",
                ):
                    socket = node.inputs.get(input_name)
                    if socket is not None and not socket.is_linked:
                        principled_inputs[input_name] = rounded(socket.default_value)
    return {
        "name": material.name,
        "users": material.users,
        "use_nodes": material.use_nodes,
        "node_types": dict(sorted(node_types.items())),
        "image_nodes": image_nodes,
        "principled_unlinked_inputs": principled_inputs,
        "surface_render_method": safe_attr(material, "surface_render_method"),
        "use_backface_culling": safe_attr(material, "use_backface_culling"),
    }


def image_report(image):
    return {
        "name": image.name,
        "source": image.source,
        "filepath": bpy.path.abspath(image.filepath) if image.filepath else "",
        "size": list(image.size),
        "packed": image.packed_file is not None,
        "colorspace": image.colorspace_settings.name,
        "users": image.users,
    }


def collection_report(collection, parents):
    return {
        "name": collection.name,
        "parents": sorted(parents.get(collection.name, [])),
        "children": sorted(child.name for child in collection.children),
        "objects": sorted(obj.name for obj in collection.objects),
        "hide_viewport": collection.hide_viewport,
        "hide_render": collection.hide_render,
        "instance_offset": rounded(collection.instance_offset),
    }


def action_report(action):
    frame_range = rounded(action.frame_range)
    result = {
        "name": action.name,
        "users": action.users,
        "frame_range": frame_range,
    }
    if hasattr(action, "fcurves"):
        result["fcurves"] = len(action.fcurves)
    if hasattr(action, "layers"):
        result["layers"] = len(action.layers)
    return result


def build_report():
    depsgraph = bpy.context.evaluated_depsgraph_get()
    objects = [
        object_report(obj, depsgraph)
        for obj in sorted(bpy.data.objects, key=lambda x: x.name)
    ]
    modifier_types = Counter(
        modifier["type"]
        for obj in objects
        for modifier in obj["modifiers"]
    )
    object_types = Counter(obj["type"] for obj in objects)
    unique_mesh_vertices = 0
    unique_mesh_triangles = 0
    for mesh in bpy.data.meshes:
        mesh.calc_loop_triangles()
        unique_mesh_vertices += len(mesh.vertices)
        unique_mesh_triangles += len(mesh.loop_triangles)
    parents = defaultdict(set)
    for scene in bpy.data.scenes:
        for child in scene.collection.children:
            parents[child.name].add(f"SCENE:{scene.name}")
    for collection in bpy.data.collections:
        for child in collection.children:
            parents[child.name].add(collection.name)

    return {
        "source_file": bpy.data.filepath,
        "source_blender_version": ".".join(str(part) for part in bpy.data.version),
        "blender_version": bpy.app.version_string,
        "summary": {
            "scenes": len(bpy.data.scenes),
            "collections": len(bpy.data.collections),
            "objects": len(bpy.data.objects),
            "object_types": dict(sorted(object_types.items())),
            "meshes": len(bpy.data.meshes),
            "materials": len(bpy.data.materials),
            "images": len(bpy.data.images),
            "armatures": len(bpy.data.armatures),
            "actions": len(bpy.data.actions),
            "objects_with_modifiers": sum(bool(obj["modifiers"]) for obj in objects),
            "modifier_count": sum(len(obj["modifiers"]) for obj in objects),
            "modifier_types": dict(sorted(modifier_types.items())),
            "negative_determinant_objects": sum(
                obj["negative_world_determinant"] for obj in objects
            ),
            "object_mesh_vertices": sum(
                obj["mesh"]["vertices"] for obj in objects if "mesh" in obj
            ),
            "object_mesh_triangles": sum(
                obj["mesh"]["triangles"] for obj in objects if "mesh" in obj
            ),
            "evaluated_object_mesh_vertices": sum(
                obj.get("evaluated_mesh", obj["mesh"])["vertices"]
                for obj in objects
                if "mesh" in obj
            ),
            "evaluated_object_mesh_triangles": sum(
                obj.get("evaluated_mesh", obj["mesh"])["triangles"]
                for obj in objects
                if "mesh" in obj
            ),
            "unique_mesh_vertices": unique_mesh_vertices,
            "unique_mesh_triangles": unique_mesh_triangles,
        },
        "scenes": [
            {
                "name": scene.name,
                "objects": len(scene.objects),
                "camera": id_name(scene.camera),
                "frame_start": scene.frame_start,
                "frame_end": scene.frame_end,
                "unit_system": scene.unit_settings.system,
                "unit_scale": rounded(scene.unit_settings.scale_length),
                "root_collections": sorted(
                    collection.name for collection in scene.collection.children
                ),
                "custom_property_keys": sorted(
                    key for key in scene.keys() if key != "_RNA_UI"
                ),
            }
            for scene in bpy.data.scenes
        ],
        "collections": [
            collection_report(collection, parents)
            for collection in sorted(bpy.data.collections, key=lambda x: x.name)
        ],
        "objects": objects,
        "materials": [
            material_report(material)
            for material in sorted(bpy.data.materials, key=lambda x: x.name)
        ],
        "images": [
            image_report(image)
            for image in sorted(bpy.data.images, key=lambda x: x.name)
        ],
        "actions": [
            action_report(action)
            for action in sorted(bpy.data.actions, key=lambda x: x.name)
        ],
        "libraries": [
            {
                "name": library.name,
                "filepath": bpy.path.abspath(library.filepath),
            }
            for library in bpy.data.libraries
        ],
    }


def main():
    args = parse_args()
    report = build_report()
    report_text = json.dumps(
        report,
        indent=args.indent,
        sort_keys=False,
        default=json_default,
    )
    if args.output is None:
        print(report_text)
        return
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report_text + "\n", encoding="utf-8")
    print(f"BLEND_INSPECT_REPORT={args.output.resolve()}")


if __name__ == "__main__":
    main()
