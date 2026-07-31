"""Render the saved active scene and camera without saving the Blender file."""

import argparse
import math
import re
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resolution", type=int, default=1024)
    parser.add_argument(
        "--engine",
        choices=("saved", "eevee", "workbench"),
        default="saved",
    )
    parser.add_argument(
        "--auto-frame",
        action="store_true",
        help="Fit a camera around the included renderable objects.",
    )
    parser.add_argument(
        "--projection",
        choices=("orthographic", "perspective"),
        default="orthographic",
        help="Projection used by the auto-framed camera.",
    )
    parser.add_argument(
        "--lens",
        type=float,
        default=50.0,
        help="Perspective camera focal length in millimeters.",
    )
    parser.add_argument(
        "--match",
        help="Regular expression matched against object names.",
    )
    parser.add_argument(
        "--parent",
        help="Include only objects whose direct parent has this name.",
    )
    parser.add_argument(
        "--view",
        default="1,-1,0.65",
        help="Comma-separated world-space camera direction used with --auto-frame.",
    )
    parser.add_argument(
        "--xray-alpha",
        type=float,
        help="Optional Workbench X-Ray alpha from 0 to 1 for fit/intersection diagnostics.",
    )
    parser.add_argument(
        "--no-cavity",
        action="store_true",
        help="Disable Workbench cavity shading for flat silhouette overlays.",
    )
    parser.add_argument(
        "--no-shadows",
        action="store_true",
        help="Disable Workbench shadows for flat diagnostic overlays.",
    )
    parser.add_argument(
        "--wireframe",
        action="store_true",
        help="Show Workbench wireframe edges over the shaded result.",
    )
    parser.add_argument(
        "--studio-light",
        help="Optional installed Workbench studio-light name such as rim.sl.",
    )
    parser.add_argument(
        "--frame-scale",
        type=float,
        default=1.0,
        help="Multiply auto-framed orthographic scale for intended-distance views.",
    )
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return parser.parse_args(argv)


def select_render_objects(scene, args):
    name_pattern = re.compile(args.match) if args.match else None
    selected = []
    for obj in scene.objects:
        is_renderable = obj.type in {"MESH", "CURVE", "SURFACE", "META", "FONT"}
        matches_name = name_pattern is None or name_pattern.search(obj.name)
        matches_parent = args.parent is None or (
            obj.parent is not None and obj.parent.name == args.parent
        )
        include = is_renderable and matches_name and matches_parent
        if is_renderable:
            obj.hide_render = not include
        if include:
            selected.append(obj)
    if not selected:
        raise RuntimeError("No renderable objects matched the preview filters.")
    return selected


def evaluated_world_corners(objects):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    corners = []
    for obj in objects:
        evaluated = obj.evaluated_get(depsgraph)
        corners.extend(evaluated.matrix_world @ Vector(corner) for corner in evaluated.bound_box)
    return corners


def add_wire_overlay(scene, objects):
    corners = evaluated_world_corners(objects)
    minimum = Vector(min(corner[index] for corner in corners) for index in range(3))
    maximum = Vector(max(corner[index] for corner in corners) for index in range(3))
    diagonal = (maximum - minimum).length
    thickness = max(diagonal * 0.00065, 0.00005)

    material = bpy.data.materials.new("AgentWireOverlay")
    material.diffuse_color = (0.012, 0.016, 0.022, 1.0)

    overlays = []
    for source in objects:
        if source.type != "MESH":
            continue

        overlay = source.copy()
        overlay.data = source.data.copy()
        overlay.name = f"AgentWire_{source.name}"
        overlay.modifiers.clear()
        overlay.data.materials.clear()
        overlay.data.materials.append(material)
        overlay.hide_render = False

        wire = overlay.modifiers.new("AgentWireframe", "WIREFRAME")
        wire.thickness = thickness
        wire.use_even_offset = True
        wire.use_replace = True

        scene.collection.objects.link(overlay)
        overlays.append(overlay)

    return overlays


def auto_frame(scene, objects, view_text, projection, lens):
    try:
        view = Vector(float(value.strip()) for value in view_text.split(","))
    except (TypeError, ValueError) as error:
        raise ValueError("--view must contain three comma-separated numbers.") from error
    if len(view) != 3 or view.length_squared == 0.0:
        raise ValueError("--view must be a non-zero three-dimensional vector.")
    view.normalize()

    corners = evaluated_world_corners(objects)
    minimum = Vector(min(corner[index] for corner in corners) for index in range(3))
    maximum = Vector(max(corner[index] for corner in corners) for index in range(3))
    center = (minimum + maximum) * 0.5
    diagonal = (maximum - minimum).length

    camera = scene.camera
    if camera is None:
        camera_data = bpy.data.cameras.new("AgentPreviewCamera")
        camera = bpy.data.objects.new("AgentPreviewCamera", camera_data)
        scene.collection.objects.link(camera)
        scene.camera = camera
    camera.hide_render = False
    camera.data.clip_start = max(diagonal * 0.001, 0.001)
    camera.data.clip_end = max(diagonal * 10.0, 100.0)
    if projection == "orthographic":
        camera.data.type = "ORTHO"
        camera.location = center + view * max(diagonal * 2.0, 1.0)
        camera.rotation_euler = (-view).to_track_quat("-Z", "Y").to_euler()

        inverse_camera = camera.matrix_world.inverted()
        camera_corners = [inverse_camera @ corner for corner in corners]
        width = max(corner.x for corner in camera_corners) - min(
            corner.x for corner in camera_corners
        )
        height = max(corner.y for corner in camera_corners) - min(
            corner.y for corner in camera_corners
        )
        camera.data.ortho_scale = max(width, height) * 1.15
    else:
        if lens <= 0.0:
            raise ValueError("--lens must be positive.")
        camera.data.type = "PERSP"
        camera.data.lens = lens
        radius = max(diagonal * 0.5, 0.001)
        half_angle = min(camera.data.angle_x, camera.data.angle_y) * 0.5
        distance = radius * 1.15 / max(math.sin(half_angle), 0.001)
        camera.location = center + view * distance
        camera.rotation_euler = (-view).to_track_quat("-Z", "Y").to_euler()


def main():
    args = parse_args()
    if args.frame_scale <= 0.0:
        raise ValueError("--frame-scale must be positive.")
    scene = bpy.context.scene
    if scene.camera is None and not args.auto_frame:
        raise RuntimeError("The active scene has no camera.")

    scene.render.resolution_x = args.resolution
    scene.render.resolution_y = args.resolution
    scene.render.resolution_percentage = 100
    selected = select_render_objects(scene, args)
    if args.auto_frame:
        auto_frame(scene, selected, args.view, args.projection, args.lens)
        if args.projection == "orthographic":
            scene.camera.data.ortho_scale *= args.frame_scale

    if args.engine == "eevee":
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    elif args.engine == "workbench":
        scene.render.engine = "BLENDER_WORKBENCH"

    args.output.parent.mkdir(parents=True, exist_ok=True)
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(args.output.resolve())
    scene.render.film_transparent = False
    if args.engine == "workbench":
        scene.display.shading.light = "STUDIO"
        scene.display.shading.color_type = "MATERIAL"
        if args.studio_light:
            scene.display.shading.studio_light = args.studio_light
        scene.display.shading.show_shadows = not args.no_shadows
        scene.display.shading.show_cavity = not args.no_cavity
        scene.display.shading.cavity_type = "WORLD"
        if args.wireframe:
            add_wire_overlay(scene, selected)
        if args.xray_alpha is not None:
            if not 0.0 <= args.xray_alpha <= 1.0:
                raise ValueError("--xray-alpha must be between 0 and 1.")
            scene.display.shading.show_xray = True
            scene.display.shading.xray_alpha = args.xray_alpha

    bpy.ops.render.render(write_still=True)
    if not args.output.exists():
        raise RuntimeError(f"Blender did not create the expected render: {args.output}")
    print(f"BLEND_PREVIEW={args.output.resolve()}")


if __name__ == "__main__":
    main()
