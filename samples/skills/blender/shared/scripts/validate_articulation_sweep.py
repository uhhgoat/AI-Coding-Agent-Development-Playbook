"""Report triangle overlap and sampled clearance across a shared-axis sweep."""

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--moving", action="append", default=[], required=True)
    parser.add_argument("--static", action="append", default=[], required=True)
    parser.add_argument("--fit", action="append", default=[])
    parser.add_argument(
        "--angles",
        default="0,-10,-20,-30,-40,-50,-60,-65",
        help="Comma-separated rotation angles in degrees.",
    )
    parser.add_argument(
        "--axis",
        choices=("X", "Y", "Z"),
        default="X",
    )
    parser.add_argument(
        "--allowed-contact-angle",
        type=float,
        default=0.0,
        help="Angle at which contact is recorded but does not fail the sweep.",
    )
    parser.add_argument(
        "--origin-tolerance",
        type=float,
        default=1e-6,
    )
    parser.add_argument(
        "--allow-static-overlap",
        action="store_true",
        help="Allow declared attachment/contact overlap with static geometry.",
    )
    parser.add_argument(
        "--allow-fit-overlap",
        action="store_true",
        help="Allow overlap with fit geometry; normally leave disabled.",
    )
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return parser.parse_args(argv)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def resolve_meshes(names, role):
    objects = []
    for name in names:
        obj = bpy.data.objects.get(name)
        if obj is None:
            raise RuntimeError(f"{role} object not found: {name}")
        if obj.type != "MESH":
            raise RuntimeError(f"{role} object is not a mesh: {name}")
        objects.append(obj)
    return objects


def evaluated_geometry(objects, depsgraph, matrix_for_object):
    vertices = []
    triangles = []
    for obj in objects:
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh(
            preserve_all_data_layers=False,
            depsgraph=depsgraph,
        )
        try:
            mesh.calc_loop_triangles()
            matrix = matrix_for_object(obj, evaluated)
            offset = len(vertices)
            vertices.extend(matrix @ vertex.co for vertex in mesh.vertices)
            triangles.extend(
                tuple(offset + index for index in triangle.vertices)
                for triangle in mesh.loop_triangles
            )
        finally:
            evaluated.to_mesh_clear()
    return vertices, triangles


def make_bvh(vertices, triangles):
    return BVHTree.FromPolygons(
        vertices,
        triangles,
        all_triangles=True,
        epsilon=1e-7,
    )


def minimum_vertex_distance(vertices, target_bvh):
    minimum = math.inf
    for vertex in vertices:
        nearest = target_bvh.find_nearest(vertex)
        if nearest is not None:
            minimum = min(minimum, nearest[3])
    return minimum if math.isfinite(minimum) else None


def main():
    args = parse_args()
    if not args.moving or not args.static:
        raise ValueError("At least one --moving and --static object is required.")
    if args.origin_tolerance <= 0.0:
        raise ValueError("--origin-tolerance must be positive.")
    angles = [float(value.strip()) for value in args.angles.split(",")]
    if not angles:
        raise ValueError("--angles must contain at least one angle.")

    source_path = Path(bpy.data.filepath).resolve()
    if not source_path.exists():
        raise RuntimeError("Articulation validation requires a saved .blend file.")

    moving_objects = resolve_meshes(args.moving, "moving")
    static_objects = resolve_meshes(args.static, "static")
    fit_objects = resolve_meshes(args.fit, "fit") if args.fit else []

    origins = [obj.matrix_world.translation.copy() for obj in moving_objects]
    pivot = origins[0]
    origin_deltas = [(origin - pivot).length for origin in origins]
    shared_origin = all(
        delta <= args.origin_tolerance for delta in origin_deltas
    )
    if not shared_origin:
        raise RuntimeError(
            "Moving objects do not share one articulation origin: "
            + ", ".join(
                f"{obj.name}={delta:.8f}"
                for obj, delta in zip(moving_objects, origin_deltas)
            )
        )

    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    static_vertices, static_triangles = evaluated_geometry(
        static_objects,
        depsgraph,
        lambda _obj, evaluated: evaluated.matrix_world,
    )
    static_bvh = make_bvh(static_vertices, static_triangles)

    fit_bvh = None
    if fit_objects:
        fit_vertices, fit_triangles = evaluated_geometry(
            fit_objects,
            depsgraph,
            lambda _obj, evaluated: evaluated.matrix_world,
        )
        fit_bvh = make_bvh(fit_vertices, fit_triangles)

    angle_reports = []
    for angle in angles:
        articulation_matrix = (
            Matrix.Translation(pivot)
            @ Matrix.Rotation(math.radians(angle), 4, args.axis)
        )
        moving_vertices, moving_triangles = evaluated_geometry(
            moving_objects,
            depsgraph,
            lambda _obj, _evaluated: articulation_matrix,
        )
        moving_bvh = make_bvh(moving_vertices, moving_triangles)
        static_overlaps = static_bvh.overlap(moving_bvh)
        fit_overlaps = fit_bvh.overlap(moving_bvh) if fit_bvh else []
        contact_allowed = math.isclose(
            angle,
            args.allowed_contact_angle,
            abs_tol=1e-6,
        )
        static_pass = (
            contact_allowed
            or args.allow_static_overlap
            or not static_overlaps
        )
        fit_pass = (
            contact_allowed
            or args.allow_fit_overlap
            or not fit_overlaps
        )
        status = "pass" if static_pass and fit_pass else "fail"
        angle_reports.append(
            {
                "angle_degrees": angle,
                "status": status,
                "contact_allowed": contact_allowed,
                "static_triangle_overlaps": len(static_overlaps),
                "fit_triangle_overlaps": len(fit_overlaps),
                "static_overlap_allowed": args.allow_static_overlap,
                "fit_overlap_allowed": args.allow_fit_overlap,
                "minimum_static_vertex_distance_m": minimum_vertex_distance(
                    moving_vertices, static_bvh
                ),
                "minimum_fit_vertex_distance_m": (
                    minimum_vertex_distance(moving_vertices, fit_bvh)
                    if fit_bvh
                    else None
                ),
            }
        )

    sweep_status = (
        "pass"
        if all(report["status"] == "pass" for report in angle_reports)
        else "fail"
    )
    report = {
        "source_file": str(source_path),
        "source_sha256": sha256(source_path),
        "blender_version": bpy.app.version_string,
        "status": sweep_status,
        "axis": args.axis,
        "pivot_xyz_m": [round(value, 8) for value in pivot],
        "shared_origin": shared_origin,
        "origin_tolerance_m": args.origin_tolerance,
        "moving_objects": [obj.name for obj in moving_objects],
        "static_objects": [obj.name for obj in static_objects],
        "fit_objects": [obj.name for obj in fit_objects],
        "allowed_contact_angle_degrees": args.allowed_contact_angle,
        "allow_static_overlap": args.allow_static_overlap,
        "allow_fit_overlap": args.allow_fit_overlap,
        "limitations": [
            "Triangle overlap is evaluated for the declared moving and static meshes only.",
            "Vertex-to-surface distance is sampled evidence, not a signed clearance field.",
            "Visor arms are excluded when they intentionally ride against the shell.",
            "The generic fit cage does not prove known-character or pose-swept fit.",
        ],
        "angles": angle_reports,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"ARTICULATION_SWEEP_REPORT={args.output.resolve()}")
    print(f"ARTICULATION_SWEEP_STATUS={sweep_status}")


if __name__ == "__main__":
    main()
