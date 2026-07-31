"""Rebuild stage-02 barrel as a minimal continuous runtime mesh."""

import argparse
import copy
import json
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import create_grounded_lowpoly_barrel as base


SCRIPT_VERSION = "0.1.0"
OUTPUT_STAGE_NAME = "stage-03-optimized-runtime-barrel.blend"
RADIAL_SEGMENTS = 20
BODY_PROFILE = base.PROFILE
OPTIMIZED_HOOPS = (
    (-0.405, 0.030),
    (-0.255, 0.024),
    (-0.085, 0.023),
    (0.085, 0.023),
    (0.255, 0.024),
    (0.405, 0.030),
)
HOOP_RADIAL_THICKNESS = 0.006
HOOP_BODY_CLEARANCE = 0.002
HEAD_RADIUS = 0.263
HEAD_INSET_Z = 0.455


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--style-contract", type=Path, required=True)
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return parser.parse_args(argv)


def remove_output_meshes(assembly):
    removed = []
    for obj in list(bpy.context.scene.objects):
        if obj.type != "MESH" or obj.parent != assembly:
            continue
        removed.append(
            {
                "name": obj.name,
                "base_vertices": len(obj.data.vertices),
                "base_triangles": sum(
                    max(len(polygon.vertices) - 2, 0)
                    for polygon in obj.data.polygons
                ),
                "modifiers": [modifier.type for modifier in obj.modifiers],
            }
        )
        mesh = obj.data
        bpy.data.objects.remove(obj, do_unlink=True)
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    return removed


def create_runtime_body(collection, assembly, wood_material, end_material):
    vertices = []
    faces = []
    face_materials = []
    smooth_faces = []
    for z, radius in BODY_PROFILE:
        for index in range(RADIAL_SEGMENTS):
            angle = math.tau * index / RADIAL_SEGMENTS
            vertices.append(
                (radius * math.cos(angle), radius * math.sin(angle), z)
            )

    ring_count = len(BODY_PROFILE)
    for ring in range(ring_count - 1):
        current_start = ring * RADIAL_SEGMENTS
        next_start = (ring + 1) * RADIAL_SEGMENTS
        for index in range(RADIAL_SEGMENTS):
            following = (index + 1) % RADIAL_SEGMENTS
            faces.append(
                (
                    current_start + index,
                    next_start + index,
                    next_start + following,
                    current_start + following,
                )
            )
            face_materials.append(0)
            smooth_faces.append(True)

    bottom_inset_start = len(vertices)
    for index in range(RADIAL_SEGMENTS):
        angle = math.tau * index / RADIAL_SEGMENTS
        vertices.append(
            (
                HEAD_RADIUS * math.cos(angle),
                HEAD_RADIUS * math.sin(angle),
                -HEAD_INSET_Z,
            )
        )
    top_inset_start = len(vertices)
    for index in range(RADIAL_SEGMENTS):
        angle = math.tau * index / RADIAL_SEGMENTS
        vertices.append(
            (
                HEAD_RADIUS * math.cos(angle),
                HEAD_RADIUS * math.sin(angle),
                HEAD_INSET_Z,
            )
        )

    bottom_outer_start = 0
    top_outer_start = (ring_count - 1) * RADIAL_SEGMENTS
    for index in range(RADIAL_SEGMENTS):
        following = (index + 1) % RADIAL_SEGMENTS
        faces.append(
            (
                bottom_outer_start + index,
                bottom_outer_start + following,
                bottom_inset_start + following,
                bottom_inset_start + index,
            )
        )
        face_materials.append(0)
        smooth_faces.append(False)
        faces.append(
            (
                top_outer_start + index,
                top_inset_start + index,
                top_inset_start + following,
                top_outer_start + following,
            )
        )
        face_materials.append(0)
        smooth_faces.append(False)

    faces.append(
        tuple(
            bottom_inset_start + index
            for index in range(RADIAL_SEGMENTS - 1, -1, -1)
        )
    )
    face_materials.append(1)
    smooth_faces.append(False)
    faces.append(
        tuple(top_inset_start + index for index in range(RADIAL_SEGMENTS))
    )
    face_materials.append(1)
    smooth_faces.append(False)

    body = base.create_mesh_object(
        "OUT_RuntimeBody",
        vertices,
        faces,
        collection,
        assembly,
        (wood_material, end_material),
        face_materials=face_materials,
        smooth_faces=smooth_faces,
        bevel_width=0.0,
    )
    body["construction"] = (
        "one continuous twenty-sided cylinder with seven loop-profile rings "
        "and top/bottom cap faces inset toward the center"
    )
    body["radial_segments"] = RADIAL_SEGMENTS
    body["profile_rings"] = len(BODY_PROFILE)
    body["head_radius_m"] = HEAD_RADIUS
    body["head_inset_depth_m"] = round(base.HALF_HEIGHT - HEAD_INSET_Z, 6)
    body["runtime_representation"] = (
        "plank and head-board separation deferred to UV/material/normal maps"
    )
    body["shading_contract"] = (
        "outer profile faces smooth; cap and inset-transition faces flat; "
        "no bevel/subdivision/weighted-normal modifiers"
    )
    body["building_role"] = "RuntimeBody"
    return body


def append_runtime_hoop(vertices, faces, center_z, height):
    start = len(vertices)
    z_low = center_z - height * 0.5
    z_high = center_z + height * 0.5
    inner_low = base.radius_at(z_low) + HOOP_BODY_CLEARANCE
    inner_high = base.radius_at(z_high) + HOOP_BODY_CLEARANCE
    outer_low = inner_low + HOOP_RADIAL_THICKNESS
    outer_high = inner_high + HOOP_RADIAL_THICKNESS
    for index in range(RADIAL_SEGMENTS):
        angle = math.tau * index / RADIAL_SEGMENTS
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
    for index in range(RADIAL_SEGMENTS):
        following = (index + 1) % RADIAL_SEGMENTS
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


def create_runtime_hoops(collection, assembly, iron_material):
    vertices = []
    faces = []
    for center_z, height in OPTIMIZED_HOOPS:
        append_runtime_hoop(vertices, faces, center_z, height)
    hoops = base.create_mesh_object(
        "OUT_RuntimeHoops",
        vertices,
        faces,
        collection,
        assembly,
        (iron_material,),
        bevel_width=0.0,
    )
    hoops["construction"] = (
        "six thin closed hoop strips consolidated into one runtime mesh"
    )
    hoops["hoop_count"] = len(OPTIMIZED_HOOPS)
    hoops["radial_thickness_m"] = HOOP_RADIAL_THICKNESS
    hoops["height_range_m"] = [
        min(height for _, height in OPTIMIZED_HOOPS),
        max(height for _, height in OPTIMIZED_HOOPS),
    ]
    hoops["runtime_representation"] = (
        "lap joints, rivets, scratches, rounding, and oxidation deferred to maps"
    )
    hoops["building_role"] = "RuntimeHoops"
    return hoops


def create_runtime_bung(collection, assembly, material):
    angle = -math.pi * 0.5
    z = 0.035
    radial = (math.cos(angle), math.sin(angle), 0.0)
    radius = base.radius_at(z)
    bung = base.add_cylinder(
        "OUT_RuntimeBung",
        (
            radial[0] * (radius + 0.006),
            radial[1] * (radius + 0.006),
            z,
        ),
        0.024,
        0.012,
        radial,
        collection,
        assembly,
        material,
        vertices=8,
        bevel_width=0.0,
    )
    bung["construction"] = "single low-sided silhouette bung"
    bung["runtime_representation"] = (
        "seat, insertion shadow, and end grain deferred to maps"
    )
    bung["building_role"] = "RuntimeBung"
    return bung


def main():
    args = parse_args()
    output_dir = args.output_dir.resolve()
    source_manifest_path = args.source_manifest.resolve()
    style_contract_path = args.style_contract.resolve()
    source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    style_contract = json.loads(style_contract_path.read_text(encoding="utf-8"))
    if style_contract["schema_version"] != 2:
        raise RuntimeError("Expected the revised runtime style contract")

    source_path = Path(bpy.data.filepath).resolve()
    if source_path.name != "stage-02-grounded-lowpoly-barrel-construction.blend":
        raise RuntimeError("Optimization must open the stage-02 barrel")
    expected_hash = source_manifest["stages"]["stage_02"]["sha256"]
    actual_hash = base.file_sha256(source_path)
    if actual_hash != expected_hash:
        raise RuntimeError(f"Stage-02 hash mismatch: {actual_hash} != {expected_hash}")

    assembly = bpy.data.objects.get(base.ASSEMBLY_NAME)
    if assembly is None:
        raise RuntimeError(f"Assembly not found: {base.ASSEMBLY_NAME}")
    output_collection = bpy.data.collections.get("OUTPUT")
    if output_collection is None:
        raise RuntimeError("OUTPUT collection not found")
    source_summary = base.mesh_summary(base.output_meshes(assembly))
    removed = remove_output_meshes(assembly)

    body = create_runtime_body(
        output_collection,
        assembly,
        bpy.data.materials["MAT_Blockout_BarrelWood"],
        bpy.data.materials["MAT_Blockout_HeadWood"],
    )
    hoops = create_runtime_hoops(
        output_collection,
        assembly,
        bpy.data.materials["MAT_Blockout_HoopIron"],
    )
    bung = create_runtime_bung(
        output_collection,
        assembly,
        bpy.data.materials["MAT_Blockout_HeadWood"],
    )
    output_objects = (body, hoops, bung)
    optimized_summary = base.mesh_summary(output_objects)
    budget = style_contract["budget"]
    if optimized_summary["objects"] > budget["output_object_target_max"]:
        raise RuntimeError("Runtime object budget exceeded")
    if optimized_summary["base_triangles"] > budget["base_triangle_target_max"]:
        raise RuntimeError("Runtime base triangle budget exceeded")
    if optimized_summary["evaluated_triangles"] > budget["evaluated_triangle_target_max"]:
        raise RuntimeError("Runtime evaluated triangle budget exceeded")
    modifier_count = sum(len(obj.modifiers) for obj in output_objects)
    if modifier_count != budget["modifier_target"]:
        raise RuntimeError("Runtime modifier target was not met")

    assembly["style_contract"] = style_contract_path.name
    assembly["runtime_geometry"] = (
        "continuous body, combined thin hoops, single silhouette bung"
    )
    assembly["plank_geometry"] = False
    assembly["head_board_geometry"] = False
    assembly["rounded_edge_geometry"] = False
    assembly["modifier_count"] = modifier_count
    bpy.context.scene["asset_style"] = style_contract["asset"]["profile"]
    bpy.context.scene["geometry_stage"] = "optimized-runtime-v1"
    bpy.context.scene["style_contract"] = style_contract_path.name

    output_path = output_dir / OUTPUT_STAGE_NAME
    if output_path.resolve() == source_path:
        raise RuntimeError("Stage-03 output must not overwrite stage 02")
    bpy.ops.wm.save_as_mainfile(filepath=str(output_path))

    manifest = copy.deepcopy(source_manifest)
    manifest["schema_version"] = 3
    manifest["optimization_script_version"] = SCRIPT_VERSION
    manifest["style_contract_v2"] = {
        "path": str(style_contract_path),
        "sha256": base.file_sha256(style_contract_path),
        "supersedes": manifest["style_contract"],
    }
    manifest["source_detailed_stage"] = {
        "path": str(source_path),
        "sha256": actual_hash,
        "size_bytes": source_path.stat().st_size,
        "summary": source_summary,
        "status": "preserved high-detail comparison; superseded for runtime",
    }
    manifest["stages"]["stage_03"] = {
        "path": str(output_path),
        "sha256": base.file_sha256(output_path),
        "size_bytes": output_path.stat().st_size,
        "summary": optimized_summary,
        "purpose": "optimized runtime mesh from explicit human feedback",
    }
    manifest["runtime_optimization"] = {
        "removed_output_objects": removed,
        "added_output_objects": [obj.name for obj in output_objects],
        "body": {
            "radial_segments": RADIAL_SEGMENTS,
            "profile_rings": BODY_PROFILE,
            "top_bottom_inset_depth_m": round(base.HALF_HEIGHT - HEAD_INSET_Z, 6),
            "plank_geometry": False,
            "head_board_geometry": False,
        },
        "hoops": {
            "specs_z_height_m": OPTIMIZED_HOOPS,
            "radial_thickness_m": HOOP_RADIAL_THICKNESS,
            "lap_joint_geometry": False,
            "rivet_geometry": False,
        },
        "modifiers": 0,
        "rounded_edge_geometry": False,
        "reduction": {
            "objects_percent": round(
                100.0
                * (source_summary["objects"] - optimized_summary["objects"])
                / source_summary["objects"],
                2,
            ),
            "base_triangles_percent": round(
                100.0
                * (
                    source_summary["base_triangles"]
                    - optimized_summary["base_triangles"]
                )
                / source_summary["base_triangles"],
                2,
            ),
            "evaluated_triangles_percent": round(
                100.0
                * (
                    source_summary["evaluated_triangles"]
                    - optimized_summary["evaluated_triangles"]
                )
                / source_summary["evaluated_triangles"],
                2,
            ),
        },
        "deferred_to_uv_material_normal": [
            "vertical plank seams and stave-to-stave variation",
            "head-board separation and end grain",
            "hoop lap joints and rivets",
            "rounded-edge highlight response",
            "bung seat and end grain",
        ],
    }
    manifest["iteration_log"].append(
        {
            "stage": "stage-02",
            "severity": "high",
            "contract_axis": "runtime topology and geometry/material boundary",
            "observation": "individual closed staves, separate head boards, thick beveled hoops, lap joints, and rivets were unnecessary for the intended optimized game asset",
            "evidence_view": "human feedback after stage-02 modeling review",
            "intended_fix": "replace detailed coopered construction with one loop-profiled cylinder, inset integral caps, thinner un-beveled hoops, and map-driven plank/hardware detail",
            "result": "implemented in stage-03",
            "residual": "UV and shading work are required to restore realistic construction detail",
        }
    )
    manifest["preview"]["required"] = [
        filename.replace("stage-02", "stage-03")
        for filename in manifest["preview"]["required"]
    ]
    manifest["validation"] = {
        "path": str(
            (
                output_dir
                / "validation"
                / "stage-03-structural.json"
            ).resolve()
        ),
        "status": "pending",
    }
    manifest["visual_review"] = {
        "status": "pending",
        "comparison_source": "stage-02 fixed views",
    }
    manifest_path = output_dir / "operation-manifest-v3.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"BARREL_STAGE_03={output_path}")
    print(f"BARREL_STAGE_03_SHA256={manifest['stages']['stage_03']['sha256']}")
    print(f"BARREL_MANIFEST_V3={manifest_path}")
    print(f"BARREL_STAGE_03_SUMMARY={json.dumps(optimized_summary, sort_keys=True)}")
    print(
        "BARREL_REDUCTION="
        + json.dumps(manifest["runtime_optimization"]["reduction"], sort_keys=True)
    )


if __name__ == "__main__":
    main()
