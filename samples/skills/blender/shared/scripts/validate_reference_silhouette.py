"""Validate calibrated 2D-reference landmarks against projected Blender geometry."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector
from mathutils.kdtree import KDTree


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return parser.parse_args(argv)


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def projected_tree(obj, depsgraph):
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh(preserve_all_data_layers=False, depsgraph=depsgraph)
    try:
        tree = KDTree(len(mesh.vertices))
        for index, vertex in enumerate(mesh.vertices):
            world = evaluated.matrix_world @ vertex.co
            tree.insert((world.x, world.z, 0.0), index)
        tree.balance()
        return tree, len(mesh.vertices)
    finally:
        evaluated.to_mesh_clear()


def add_check(checks, name, status, evidence):
    checks.append({"name": name, "status": status, "evidence": evidence})


def main():
    args = parse_args()
    manifest_path = args.manifest.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    blend_path = Path(bpy.data.filepath).resolve()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    checks = []

    reference = manifest["reference"]
    reference_copy = Path(reference["copy_path"])
    reference_copy_valid = (
        reference_copy.exists()
        and file_sha256(reference_copy) == reference["copy_sha256"]
        and reference["copy_sha256"] == reference["source_sha256"]
    )
    add_check(
        checks,
        "reference-copy-lineage",
        "pass" if reference_copy_valid else "fail",
        {
            "path": str(reference_copy),
            "hash_matches": reference_copy_valid,
        },
    )

    reference_obj = bpy.data.objects.get(reference["object"])
    reference_image_valid = (
        reference_obj is not None
        and reference_obj.empty_display_type == "IMAGE"
        and reference_obj.data is not None
        and reference_obj.data.packed_file is not None
        and reference_obj.get("meters_per_pixel")
        == manifest["reference_mapping"]["meters_per_pixel"]
    )
    add_check(
        checks,
        "packed-reference-object",
        "pass" if reference_image_valid else "fail",
        {
            "object": reference["object"],
            "exists": reference_obj is not None,
            "packed": bool(
                reference_obj
                and reference_obj.data
                and reference_obj.data.packed_file is not None
            ),
        },
    )

    tolerance = manifest["reference_match"]["tolerance_m"]
    target_reports = []
    targets_pass = True
    for target in manifest["reference_match"]["targets"]:
        obj = bpy.data.objects.get(target["object"])
        if obj is None:
            targets_pass = False
            target_reports.append(
                {
                    "object": target["object"],
                    "status": "fail",
                    "reason": "missing object",
                }
            )
            continue
        tree, vertex_count = projected_tree(obj, depsgraph)
        distances = []
        for x, z in target["landmarks_xz"]:
            _, _, distance = tree.find((x, z, 0.0))
            distances.append(distance)
        maximum = max(distances) if distances else float("inf")
        status = "pass" if maximum <= tolerance else "fail"
        targets_pass = targets_pass and status == "pass"
        target_reports.append(
            {
                "object": obj.name,
                "status": status,
                "evaluated_vertices": vertex_count,
                "landmarks": len(distances),
                "maximum_nearest_distance_m": maximum,
                "mean_nearest_distance_m": (
                    sum(distances) / len(distances) if distances else None
                ),
                "tolerance_m": tolerance,
            }
        )
    add_check(
        checks,
        "projected-landmark-match",
        "pass" if targets_pass else "fail",
        target_reports,
    )

    preview_paths = [Path(path) for path in manifest["preview"].values()]
    missing_previews = [
        str(path) for path in preview_paths if not path.exists() or path.stat().st_size == 0
    ]
    add_check(
        checks,
        "reference-preview-evidence",
        "pass" if not missing_previews else "fail",
        {
            "previews": [str(path) for path in preview_paths],
            "missing_or_empty": missing_previews,
        },
    )
    add_check(
        checks,
        "hidden-depth-realism",
        "not-evaluated",
        "The side image constrains X/Z silhouette only. Y thickness and hidden eye construction remain documented inferences requiring human review.",
    )
    add_check(
        checks,
        "reference-style",
        "not-evaluated",
        "Structural landmark proximity does not prove perceived realism, historical accuracy, or construction plausibility.",
    )

    structural = [
        check
        for check in checks
        if check["status"] not in {"not-evaluated", "warn"}
    ]
    status = "fail" if any(check["status"] == "fail" for check in structural) else "pass"
    report = {
        "source_file": str(blend_path),
        "source_sha256": file_sha256(blend_path),
        "blender_version": bpy.app.version_string,
        "manifest": str(manifest_path),
        "structural_status": status,
        "checks": checks,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"REFERENCE_SILHOUETTE_VALIDATION={args.output.resolve()}")
    print(f"REFERENCE_SILHOUETTE_STATUS={status}")


if __name__ == "__main__":
    main()
