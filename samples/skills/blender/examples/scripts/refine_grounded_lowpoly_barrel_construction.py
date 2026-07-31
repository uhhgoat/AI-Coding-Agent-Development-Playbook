"""Distribute barrel hoop joints after stage-01 visual review."""

import argparse
import copy
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import create_grounded_lowpoly_barrel as base


SCRIPT_VERSION = "0.1.0"
OUTPUT_STAGE_NAME = "stage-02-grounded-lowpoly-barrel-construction.blend"
TARGET_ANGLES_DEGREES = (-105.0, 25.0, -165.0, 80.0, -45.0, 145.0)
SOURCE_OFFSET_DEGREES = (-5.0, 3.0, -2.0, 4.0, -4.0, 2.0)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return parser.parse_args(argv)


def rotate_object_around_z(obj, delta):
    rotation = Matrix.Rotation(delta, 4, "Z")
    obj.location = rotation @ Vector(obj.location)
    obj.rotation_euler.z += delta


def distribute_hoop_joints():
    records = []
    for index, (source_offset, target_angle) in enumerate(
        zip(SOURCE_OFFSET_DEGREES, TARGET_ANGLES_DEGREES),
        start=1,
    ):
        source_angle = -90.0 + source_offset
        delta = math.radians(target_angle - source_angle)
        names = (
            f"OUT_HoopLap_{index:02d}",
            f"OUT_HoopRivet_{index:02d}_1",
            f"OUT_HoopRivet_{index:02d}_2",
        )
        for name in names:
            obj = bpy.data.objects.get(name)
            if obj is None:
                raise RuntimeError(f"Expected stage-01 object not found: {name}")
            rotate_object_around_z(obj, delta)
            obj["joint_angle_degrees"] = target_angle
        records.append(
            {
                "hoop": index,
                "source_angle_degrees": source_angle,
                "target_angle_degrees": target_angle,
                "objects": names,
            }
        )
    return records


def main():
    args = parse_args()
    output_dir = args.output_dir.resolve()
    source_manifest_path = args.source_manifest.resolve()
    source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    source_path = Path(bpy.data.filepath).resolve()
    if source_path.name != "stage-01-grounded-lowpoly-barrel-construction.blend":
        raise RuntimeError("Refinement must open the stage-01 barrel construction")
    expected_hash = source_manifest["stages"]["stage_01"]["sha256"]
    actual_hash = base.file_sha256(source_path)
    if actual_hash != expected_hash:
        raise RuntimeError(f"Stage-01 hash mismatch: {actual_hash} != {expected_hash}")

    assembly = bpy.data.objects.get(base.ASSEMBLY_NAME)
    if assembly is None:
        raise RuntimeError(f"Assembly not found: {base.ASSEMBLY_NAME}")
    geometry_before = base.mesh_summary(base.output_meshes(assembly))
    joint_records = distribute_hoop_joints()
    geometry_after = base.mesh_summary(base.output_meshes(assembly))
    if (
        geometry_before["base_vertices"] != geometry_after["base_vertices"]
        or geometry_before["base_triangles"] != geometry_after["base_triangles"]
        or geometry_before["evaluated_triangles"]
        != geometry_after["evaluated_triangles"]
    ):
        raise RuntimeError("Joint distribution unexpectedly changed topology")

    bpy.context.scene["construction_iteration"] = (
        "distributed hoop lap joints after fixed-view visual review"
    )
    output_path = output_dir / OUTPUT_STAGE_NAME
    if output_path.resolve() == source_path:
        raise RuntimeError("Stage-02 output must not overwrite stage 01")
    bpy.ops.wm.save_as_mainfile(filepath=str(output_path))

    manifest = copy.deepcopy(source_manifest)
    manifest["schema_version"] = 2
    manifest["refinement_script_version"] = SCRIPT_VERSION
    manifest["source_construction_stage"] = {
        "path": str(source_path),
        "sha256": actual_hash,
        "size_bytes": source_path.stat().st_size,
    }
    manifest["stages"]["stage_02"] = {
        "path": str(output_path),
        "sha256": base.file_sha256(output_path),
        "size_bytes": output_path.stat().st_size,
        "summary": geometry_after,
        "purpose": "final pre-texture construction with distributed hoop joints",
    }
    manifest["hoop_joint_distribution"] = joint_records
    manifest["iteration_log"].append(
        {
            "stage": "stage-01",
            "severity": "medium",
            "contract_axis": "visual hierarchy and construction plausibility",
            "observation": "six hoop lap plates formed a near-vertical front column and competed with the stave rhythm",
            "evidence_view": "stage-01-front.png and stage-01-wireframe.png",
            "intended_fix": "distribute the lap joints around the circumference while preserving hoop fit and topology",
            "result": "fixed in stage-02",
            "residual": "exact historical hoop-making pattern is not claimed",
        }
    )
    manifest["preview"]["required"] = [
        filename.replace("stage-01", "stage-02")
        for filename in manifest["preview"]["required"]
    ]
    manifest["validation"]["path"] = str(
        (
            output_dir
            / "validation"
            / "stage-02-structural.json"
        ).resolve()
    )
    manifest["validation"]["status"] = "pending"
    manifest_path = output_dir / "operation-manifest-v2.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"BARREL_STAGE_02={output_path}")
    print(f"BARREL_STAGE_02_SHA256={manifest['stages']['stage_02']['sha256']}")
    print(f"BARREL_MANIFEST_V2={manifest_path}")


if __name__ == "__main__":
    main()
