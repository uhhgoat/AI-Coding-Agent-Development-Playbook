"""Emit report-only structural validation for hard-surface Blender assets."""

import argparse
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

import bpy
from mathutils import Vector
from mathutils.kdtree import KDTree


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--parent", required=True)
    parser.add_argument(
        "--mirror-pair",
        action="append",
        default=[],
        help="Comma-separated left,right object names expected to mirror across parent-local X.",
    )
    parser.add_argument(
        "--mirror-tolerance",
        type=float,
        default=1e-5,
        help="Maximum parent-local distance allowed by mirror-pair checks.",
    )
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return parser.parse_args(argv)


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def topology_metrics(mesh):
    edge_face_counts = Counter()
    used_vertices = set()
    degenerate_faces = 0
    for polygon in mesh.polygons:
        used_vertices.update(polygon.vertices)
        edge_face_counts.update(polygon.edge_keys)
        if len(polygon.vertices) < 3 or not math.isfinite(polygon.area):
            degenerate_faces += 1
        elif polygon.area <= 1e-12:
            degenerate_faces += 1

    mesh_edge_keys = {edge.key for edge in mesh.edges}
    non_manifold_edges = sum(
        1 for edge_key in mesh_edge_keys if edge_face_counts[edge_key] != 2
    )
    loose_edges = sum(1 for edge_key in mesh_edge_keys if edge_face_counts[edge_key] == 0)
    loose_vertices = len(mesh.vertices) - len(used_vertices)
    return {
        "vertices": len(mesh.vertices),
        "edges": len(mesh.edges),
        "polygons": len(mesh.polygons),
        "triangles": sum(max(len(polygon.vertices) - 2, 0) for polygon in mesh.polygons),
        "non_manifold_edges": non_manifold_edges,
        "loose_edges": loose_edges,
        "loose_vertices": loose_vertices,
        "degenerate_faces": degenerate_faces,
    }


def evaluated_metrics(obj, depsgraph):
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh(preserve_all_data_layers=False, depsgraph=depsgraph)
    try:
        return topology_metrics(mesh)
    finally:
        evaluated.to_mesh_clear()


def evaluated_world_bounds(obj, depsgraph):
    evaluated = obj.evaluated_get(depsgraph)
    corners = [evaluated.matrix_world @ Vector(corner) for corner in evaluated.bound_box]
    minimum = [min(corner[index] for corner in corners) for index in range(3)]
    maximum = [max(corner[index] for corner in corners) for index in range(3)]
    return {
        "minimum": [round(value, 6) for value in minimum],
        "maximum": [round(value, 6) for value in maximum],
        "dimensions": [
            round(maximum[index] - minimum[index], 6) for index in range(3)
        ],
    }


def modifier_dependencies(obj):
    dependencies = []
    for modifier in obj.modifiers:
        dependency = {
            "name": modifier.name,
            "type": modifier.type,
            "show_viewport": modifier.show_viewport,
            "show_render": modifier.show_render,
            "valid": True,
        }
        if modifier.type == "ARRAY":
            dependency["count"] = modifier.count
            dependency["offset_object"] = (
                modifier.offset_object.name if modifier.offset_object else None
            )
            if modifier.use_object_offset and modifier.offset_object is None:
                dependency["valid"] = False
        elif modifier.type == "BOOLEAN":
            dependency["operand"] = modifier.object.name if modifier.object else None
            if modifier.object is None:
                dependency["valid"] = False
        elif modifier.type == "CURVE":
            dependency["curve_object"] = (
                modifier.object.name if modifier.object else None
            )
            if modifier.object is None:
                dependency["valid"] = False
        dependencies.append(dependency)
    return dependencies


def mesh_coordinates(obj, depsgraph, mirror_x, evaluated):
    evaluated_obj = obj.evaluated_get(depsgraph) if evaluated else obj
    mesh = (
        evaluated_obj.to_mesh(
            preserve_all_data_layers=False,
            depsgraph=depsgraph,
        )
        if evaluated
        else obj.data
    )
    try:
        matrix = evaluated_obj.matrix_local
        coordinates = []
        for vertex in mesh.vertices:
            point = matrix @ vertex.co
            x = -point.x if mirror_x else point.x
            coordinates.append(Vector((x, point.y, point.z)))
        return coordinates, topology_metrics(mesh)
    finally:
        if evaluated:
            evaluated_obj.to_mesh_clear()


def coordinate_sets_match(left, right, tolerance):
    if len(left) != len(right):
        return False, None

    def maximum_nearest_distance(source, target):
        tree = KDTree(len(target))
        for index, point in enumerate(target):
            tree.insert(point, index)
        tree.balance()
        return max((tree.find(point)[2] for point in source), default=0.0)

    maximum_distance = max(
        maximum_nearest_distance(left, right),
        maximum_nearest_distance(right, left),
    )
    return maximum_distance <= tolerance, maximum_distance


def mirror_pair_report(pair, depsgraph, tolerance=1e-5):
    names = [name.strip() for name in pair.split(",", 1)]
    if len(names) != 2 or not all(names):
        return {
            "pair": pair,
            "status": "fail",
            "reason": "Expected --mirror-pair LeftObject,RightObject.",
        }

    left = bpy.data.objects.get(names[0])
    right = bpy.data.objects.get(names[1])
    if left is None or right is None:
        return {
            "left": names[0],
            "right": names[1],
            "status": "fail",
            "reason": "One or both objects were not found.",
        }
    if left.type != "MESH" or right.type != "MESH":
        return {
            "left": left.name,
            "right": right.name,
            "status": "fail",
            "reason": "Mirror-pair objects must both be meshes.",
        }

    left_base, left_base_topology = mesh_coordinates(
        left, depsgraph, True, False
    )
    right_base, right_base_topology = mesh_coordinates(
        right, depsgraph, False, False
    )
    left_evaluated, left_evaluated_topology = mesh_coordinates(
        left, depsgraph, True, True
    )
    right_evaluated, right_evaluated_topology = mesh_coordinates(
        right, depsgraph, False, True
    )
    base_coordinates_match, base_maximum_distance = coordinate_sets_match(
        left_base, right_base, tolerance
    )
    evaluated_coordinates_match, evaluated_maximum_distance = coordinate_sets_match(
        left_evaluated, right_evaluated, tolerance
    )
    same_parent = left.parent == right.parent
    base_match = (
        base_coordinates_match and left_base_topology == right_base_topology
    )
    evaluated_match = (
        evaluated_coordinates_match
        and left_evaluated_topology == right_evaluated_topology
    )
    return {
        "left": left.name,
        "right": right.name,
        "axis": "parent-local X",
        "tolerance": tolerance,
        "same_parent": same_parent,
        "base_geometry_match": base_match,
        "base_maximum_nearest_distance": base_maximum_distance,
        "evaluated_geometry_match": evaluated_match,
        "evaluated_maximum_nearest_distance": evaluated_maximum_distance,
        "status": "pass" if same_parent and base_match and evaluated_match else "fail",
    }


def add_check(checks, name, status, evidence):
    checks.append({"name": name, "status": status, "evidence": evidence})


def main():
    args = parse_args()
    if args.mirror_tolerance <= 0.0:
        raise ValueError("--mirror-tolerance must be positive.")
    source_path = Path(bpy.data.filepath).resolve()
    if not source_path.exists():
        raise RuntimeError("Validation requires a saved .blend file.")

    parent = bpy.data.objects.get(args.parent)
    if parent is None:
        raise RuntimeError(f"Parent object not found: {args.parent}")

    objects = sorted(
        (
            obj
            for obj in bpy.context.scene.objects
            if obj.type == "MESH" and obj.parent == parent
        ),
        key=lambda obj: obj.name,
    )
    if not objects:
        raise RuntimeError(f"No mesh objects are parented to {args.parent}.")

    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    object_reports = []
    for obj in objects:
        base = topology_metrics(obj.data)
        evaluated = evaluated_metrics(obj, depsgraph)
        dependencies = modifier_dependencies(obj)
        object_reports.append(
            {
                "name": obj.name,
                "data": obj.data.name,
                "location": [round(value, 6) for value in obj.location],
                "rotation_euler": [round(value, 6) for value in obj.rotation_euler],
                "scale": [round(value, 6) for value in obj.scale],
                "negative_world_determinant": obj.matrix_world.determinant() < 0.0,
                "materials": [material.name for material in obj.data.materials],
                "uv_layers": [layer.name for layer in obj.data.uv_layers],
                "base": base,
                "evaluated": evaluated,
                "world_bounds": evaluated_world_bounds(obj, depsgraph),
                "modifiers": dependencies,
            }
        )

    checks = []
    names = [report["name"] for report in object_reports]
    add_check(
        checks,
        "output-selection",
        "pass" if len(names) == len(set(names)) else "fail",
        {"parent": args.parent, "objects": names},
    )

    unit_settings = bpy.context.scene.unit_settings
    metric_units = unit_settings.system == "METRIC" and math.isclose(
        unit_settings.scale_length, 1.0
    )
    add_check(
        checks,
        "metric-units",
        "pass" if metric_units else "fail",
        {
            "system": unit_settings.system,
            "length_unit": unit_settings.length_unit,
            "scale_length": unit_settings.scale_length,
        },
    )

    negative_objects = [
        report["name"]
        for report in object_reports
        if report["negative_world_determinant"]
    ]
    add_check(
        checks,
        "negative-determinants",
        "pass" if not negative_objects else "fail",
        {"objects": negative_objects},
    )

    non_unit_scale = [
        report["name"]
        for report in object_reports
        if any(not math.isclose(value, 1.0, abs_tol=1e-6) for value in report["scale"])
    ]
    add_check(
        checks,
        "unit-object-scale",
        "pass" if not non_unit_scale else "warn",
        {"objects": non_unit_scale},
    )

    base_topology_issues = {
        report["name"]: {
            key: report["base"][key]
            for key in (
                "non_manifold_edges",
                "loose_edges",
                "loose_vertices",
                "degenerate_faces",
            )
            if report["base"][key]
        }
        for report in object_reports
    }
    base_topology_issues = {
        name: issues for name, issues in base_topology_issues.items() if issues
    }
    add_check(
        checks,
        "base-topology",
        "pass" if not base_topology_issues else "fail",
        base_topology_issues,
    )

    evaluated_topology_issues = {
        report["name"]: {
            key: report["evaluated"][key]
            for key in (
                "non_manifold_edges",
                "loose_edges",
                "loose_vertices",
                "degenerate_faces",
            )
            if report["evaluated"][key]
        }
        for report in object_reports
    }
    evaluated_topology_issues = {
        name: issues
        for name, issues in evaluated_topology_issues.items()
        if issues
    }
    add_check(
        checks,
        "evaluated-topology",
        "pass" if not evaluated_topology_issues else "fail",
        evaluated_topology_issues,
    )

    missing_materials = [
        report["name"] for report in object_reports if not report["materials"]
    ]
    add_check(
        checks,
        "material-assignments",
        "pass" if not missing_materials else "warn",
        {"objects_without_materials": missing_materials},
    )

    invalid_dependencies = [
        {
            "object": report["name"],
            "modifier": modifier["name"],
            "type": modifier["type"],
        }
        for report in object_reports
        for modifier in report["modifiers"]
        if not modifier["valid"]
        or not modifier["show_viewport"]
        or not modifier["show_render"]
    ]
    add_check(
        checks,
        "modifier-dependencies",
        "pass" if not invalid_dependencies else "fail",
        invalid_dependencies,
    )

    arrays = [
        {
            "object": report["name"],
            "modifier": modifier["name"],
            "count": modifier.get("count"),
            "offset_object": modifier.get("offset_object"),
        }
        for report in object_reports
        for modifier in report["modifiers"]
        if modifier["type"] == "ARRAY"
    ]
    add_check(
        checks,
        "retained-arrays",
        "pass" if arrays else "not-evaluated",
        arrays,
    )

    mirror_pairs = [
        mirror_pair_report(pair, depsgraph, args.mirror_tolerance)
        for pair in args.mirror_pair
    ]
    add_check(
        checks,
        "mirror-pairs",
        (
            "pass"
            if mirror_pairs and all(pair["status"] == "pass" for pair in mirror_pairs)
            else "fail"
            if mirror_pairs
            else "not-evaluated"
        ),
        mirror_pairs,
    )

    add_check(
        checks,
        "uv-readiness",
        "not-evaluated",
        "UVs were not requested for this modeling-stage fixture.",
    )
    add_check(
        checks,
        "collision-lod",
        "not-evaluated",
        "Collision and LOD were not requested for this modeling-stage fixture.",
    )
    add_check(
        checks,
        "visual-silhouette-and-shading",
        "not-evaluated",
        "Requires review of deterministic preview images.",
    )

    structural_checks = [
        check
        for check in checks
        if check["name"]
        not in {"uv-readiness", "collision-lod", "visual-silhouette-and-shading"}
    ]
    if any(check["status"] == "fail" for check in structural_checks):
        structural_status = "fail"
    elif any(check["status"] == "warn" for check in structural_checks):
        structural_status = "warn"
    else:
        structural_status = "pass"

    aggregate_minimum = [
        min(report["world_bounds"]["minimum"][index] for report in object_reports)
        for index in range(3)
    ]
    aggregate_maximum = [
        max(report["world_bounds"]["maximum"][index] for report in object_reports)
        for index in range(3)
    ]

    report = {
        "source_file": str(source_path),
        "source_sha256": file_sha256(source_path),
        "blender_version": bpy.app.version_string,
        "asset_parent": args.parent,
        "structural_status": structural_status,
        "checks": checks,
        "summary": {
            "output_objects": len(object_reports),
            "base_vertices": sum(
                report["base"]["vertices"] for report in object_reports
            ),
            "base_triangles": sum(
                report["base"]["triangles"] for report in object_reports
            ),
            "evaluated_vertices": sum(
                report["evaluated"]["vertices"] for report in object_reports
            ),
            "evaluated_triangles": sum(
                report["evaluated"]["triangles"] for report in object_reports
            ),
            "modifier_count": sum(
                len(report["modifiers"]) for report in object_reports
            ),
            "array_count": len(arrays),
            "world_bounds": {
                "minimum": [round(value, 6) for value in aggregate_minimum],
                "maximum": [round(value, 6) for value in aggregate_maximum],
                "dimensions": [
                    round(aggregate_maximum[index] - aggregate_minimum[index], 6)
                    for index in range(3)
                ],
            },
        },
        "objects": object_reports,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"HARD_SURFACE_VALIDATION={args.output.resolve()}")
    print(f"HARD_SURFACE_STRUCTURAL_STATUS={structural_status}")


if __name__ == "__main__":
    main()
