"""Emit report-only validation for procedural Blender material stages."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--parent", required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return parser.parse_args(argv)


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def add_check(checks, name, status, evidence):
    checks.append({"name": name, "status": status, "evidence": evidence})


def geometry_signature(objects):
    records = []
    for obj in objects:
        records.append(
            {
                "name": obj.name,
                "parent": obj.parent.name if obj.parent else None,
                "matrix_world": [
                    round(value, 9)
                    for row in obj.matrix_world
                    for value in row
                ],
                "vertices": [
                    [round(component, 9) for component in vertex.co]
                    for vertex in obj.data.vertices
                ],
                "edges": [list(edge.vertices) for edge in obj.data.edges],
                "polygons": [list(polygon.vertices) for polygon in obj.data.polygons],
                "modifiers": [
                    {
                        "name": modifier.name,
                        "type": modifier.type,
                        "show_render": modifier.show_render,
                        "width": getattr(modifier, "width", None),
                        "segments": getattr(modifier, "segments", None),
                        "limit_method": getattr(modifier, "limit_method", None),
                    }
                    for modifier in obj.modifiers
                ],
            }
        )
    encoded = json.dumps(
        records,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()


def recursive_image_nodes(node_tree, visited=None):
    visited = visited or set()
    if node_tree is None or node_tree.as_pointer() in visited:
        return []
    visited.add(node_tree.as_pointer())
    result = []
    for node in node_tree.nodes:
        if node.bl_idname == "ShaderNodeTexImage":
            result.append(
                {
                    "node_tree": node_tree.name,
                    "node": node.name,
                    "image": node.image.name if node.image else None,
                }
            )
        elif node.bl_idname == "ShaderNodeGroup":
            result.extend(recursive_image_nodes(node.node_tree, visited))
    return result


def material_report(material):
    report = {
        "name": material.name,
        "users": material.users,
        "use_nodes": material.use_nodes,
        "coordinate_strategy": material.get("coordinate_strategy"),
        "physical_scale_unit": material.get("physical_scale_unit"),
        "procedural_group": material.get("procedural_group"),
        "unity_path": material.get("unity_path"),
        "node_count": 0,
        "group_nodes": [],
        "object_coordinate_links": 0,
        "surface_output_links": 0,
        "principled_to_surface": 0,
        "image_nodes": [],
    }
    if not material.use_nodes or material.node_tree is None:
        return report

    node_tree = material.node_tree
    report["node_count"] = len(node_tree.nodes)
    report["group_nodes"] = [
        node.node_tree.name
        for node in node_tree.nodes
        if node.bl_idname == "ShaderNodeGroup" and node.node_tree is not None
    ]
    report["object_coordinate_links"] = sum(
        1
        for link in node_tree.links
        if link.from_node.bl_idname == "ShaderNodeTexCoord"
        and link.from_socket.name == "Object"
        and link.to_node.bl_idname == "ShaderNodeGroup"
        and link.to_socket.name == "Vector"
    )
    report["surface_output_links"] = sum(
        1
        for link in node_tree.links
        if link.to_node.bl_idname == "ShaderNodeOutputMaterial"
        and link.to_socket.name == "Surface"
    )
    report["principled_to_surface"] = sum(
        1
        for link in node_tree.links
        if link.from_node.bl_idname == "ShaderNodeBsdfPrincipled"
        and link.to_node.bl_idname == "ShaderNodeOutputMaterial"
        and link.to_socket.name == "Surface"
    )
    report["image_nodes"] = recursive_image_nodes(node_tree)
    return report


def group_report(group):
    sockets = []
    for item in group.interface.items_tree:
        if getattr(item, "item_type", None) != "SOCKET":
            continue
        sockets.append(
            {
                "name": item.name,
                "in_out": item.in_out,
                "socket_type": item.socket_type,
            }
        )
    return {
        "name": group.name,
        "coordinate_strategy": group.get("coordinate_strategy"),
        "physical_scale_unit": group.get("physical_scale_unit"),
        "provenance": group.get("provenance"),
        "nodes": len(group.nodes),
        "links": len(group.links),
        "sockets": sockets,
        "image_nodes": recursive_image_nodes(group),
    }


def main():
    args = parse_args()
    blend_path = Path(bpy.data.filepath).resolve()
    manifest_path = args.manifest.resolve()
    if not blend_path.exists():
        raise RuntimeError("Validation requires a saved .blend file.")
    if not manifest_path.exists():
        raise RuntimeError(f"Material manifest not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    parent = bpy.data.objects.get(args.parent)
    if parent is None:
        raise RuntimeError(f"Parent object not found: {args.parent}")
    output_objects = sorted(
        (
            obj
            for obj in bpy.context.scene.objects
            if obj.type == "MESH" and obj.parent == parent
        ),
        key=lambda obj: obj.name,
    )
    if not output_objects:
        raise RuntimeError(f"No mesh objects are parented to {args.parent}.")

    expected_materials = [record["name"] for record in manifest["materials"]]
    expected_groups = [record["name"] for record in manifest["node_groups"]]
    expected_material_records = {
        record["name"]: record for record in manifest["materials"]
    }
    expected_group_records = {
        record["name"]: record for record in manifest["node_groups"]
    }
    assigned_materials = sorted(
        {
            material.name
            for obj in output_objects
            for material in obj.data.materials
            if material is not None
        }
    )
    material_reports = [
        material_report(bpy.data.materials[name])
        for name in expected_materials
        if bpy.data.materials.get(name) is not None
    ]
    group_reports = [
        group_report(bpy.data.node_groups[name])
        for name in expected_groups
        if bpy.data.node_groups.get(name) is not None
    ]

    checks = []
    missing_materials = sorted(set(expected_materials) - set(assigned_materials))
    unexpected_materials = sorted(set(assigned_materials) - set(expected_materials))
    add_check(
        checks,
        "material-assignments",
        "pass" if not missing_materials and not unexpected_materials else "fail",
        {
            "expected": expected_materials,
            "assigned": assigned_materials,
            "missing": missing_materials,
            "unexpected": unexpected_materials,
        },
    )

    empty_slots = [
        {"object": obj.name, "slot": index}
        for obj in output_objects
        for index, material in enumerate(obj.data.materials)
        if material is None
    ]
    invalid_polygon_indices = [
        {
            "object": obj.name,
            "polygon": polygon.index,
            "material_index": polygon.material_index,
            "slots": len(obj.data.materials),
        }
        for obj in output_objects
        for polygon in obj.data.polygons
        if polygon.material_index >= len(obj.data.materials)
    ]
    add_check(
        checks,
        "material-slots",
        "pass" if not empty_slots and not invalid_polygon_indices else "fail",
        {
            "empty_slots": empty_slots,
            "invalid_polygon_indices": invalid_polygon_indices,
        },
    )

    invalid_graphs = [
        report["name"]
        for report in material_reports
        if not report["use_nodes"]
        or report["surface_output_links"] != 1
        or report["principled_to_surface"] != 1
        or report["object_coordinate_links"] != 1
        or len(report["group_nodes"]) != 1
    ]
    add_check(
        checks,
        "material-output-paths",
        "pass" if not invalid_graphs and len(material_reports) == len(expected_materials) else "fail",
        {
            "invalid_materials": invalid_graphs,
            "reports_found": len(material_reports),
            "reports_expected": len(expected_materials),
        },
    )

    undocumented_materials = [
        report["name"]
        for report in material_reports
        if report["coordinate_strategy"]
        != expected_material_records[report["name"]].get(
            "coordinate_strategy",
            report["coordinate_strategy"],
        )
        or report["physical_scale_unit"] != "meters"
        or not report["unity_path"]
    ]
    add_check(
        checks,
        "coordinate-scale-unity-contract",
        "pass" if not undocumented_materials else "fail",
        {"invalid_materials": undocumented_materials},
    )

    missing_groups = sorted(
        set(expected_groups) - {report["name"] for report in group_reports}
    )
    invalid_groups = [
        report["name"]
        for report in group_reports
        if report["coordinate_strategy"]
        != expected_group_records[report["name"]].get(
            "coordinate_strategy",
            report["coordinate_strategy"],
        )
        or report["physical_scale_unit"] != "meters"
        or not any(
            "(m)" in socket["name"] or "(1/m)" in socket["name"]
            for socket in report["sockets"]
            if socket["in_out"] == "INPUT"
        )
        or not any(socket["name"] == "Base Color" for socket in report["sockets"])
        or not any(socket["name"] == "Roughness" for socket in report["sockets"])
        or not any(socket["name"] == "Metallic" for socket in report["sockets"])
        or not any(socket["name"] == "Normal" for socket in report["sockets"])
    ]
    add_check(
        checks,
        "procedural-node-groups",
        "pass" if not missing_groups and not invalid_groups else "fail",
        {
            "expected": expected_groups,
            "missing": missing_groups,
            "invalid": invalid_groups,
        },
    )

    image_nodes = [
        image_node
        for report in material_reports
        for image_node in report["image_nodes"]
    ]
    external_images = [
        {
            "name": image.name,
            "source": image.source,
            "filepath": image.filepath,
            "packed": image.packed_file is not None,
        }
        for image in bpy.data.images
        if image.source == "FILE"
    ]
    allowed_packed_names = {
        record["name"]
        for record in manifest.get("allowed_packed_images", [])
        if record.get("packed")
    }
    invalid_external_images = [
        record
        for record in external_images
        if not record["packed"] or record["name"] not in allowed_packed_names
    ]
    add_check(
        checks,
        "image-dependencies",
        "pass" if not image_nodes and not invalid_external_images else "fail",
        {
            "image_nodes": image_nodes,
            "external_images": external_images,
            "allowed_packed_images": sorted(allowed_packed_names),
            "invalid_external_images": invalid_external_images,
        },
    )

    geometry_contract = manifest.get("geometry_invariance")
    if geometry_contract:
        current_geometry_hash = geometry_signature(output_objects)
        source_geometry_hash = geometry_contract.get("source", {}).get("sha256")
        output_geometry_hash = geometry_contract.get("output", {}).get("sha256")
        geometry_unchanged = (
            current_geometry_hash
            and current_geometry_hash == source_geometry_hash
            and current_geometry_hash == output_geometry_hash
        )
        add_check(
            checks,
            "geometry-invariance",
            "pass" if geometry_unchanged else "fail",
            {
                "current_sha256": current_geometry_hash,
                "source_sha256": source_geometry_hash,
                "output_sha256": output_geometry_hash,
            },
        )

    source_copy_record = manifest.get("source_copy") or manifest.get(
        "preserved_source_copy"
    )
    if source_copy_record is None:
        raise RuntimeError("Manifest is missing source_copy lineage metadata.")
    source_copy = Path(source_copy_record["path"])
    source_copy_valid = (
        source_copy.exists()
        and file_sha256(source_copy) == source_copy_record["sha256"]
        and source_copy_record["sha256"] == manifest["source"]["sha256"]
    )
    output_hash_matches = file_sha256(blend_path) == manifest["output"]["sha256"]
    add_check(
        checks,
        "stage-lineage",
        "pass" if source_copy_valid and output_hash_matches else "fail",
        {
            "source_copy": str(source_copy),
            "source_copy_valid": source_copy_valid,
            "output_hash_matches": output_hash_matches,
        },
    )

    preview_record = manifest.get("preview", {})
    preview_paths = [
        Path(path)
        for path in preview_record.get("in_context", [])
    ]
    if preview_record.get("two_scale_swatches"):
        preview_paths.append(Path(preview_record["two_scale_swatches"]))
    missing_previews = [
        str(path) for path in preview_paths if not path.exists() or path.stat().st_size == 0
    ]
    add_check(
        checks,
        "preview-evidence",
        "pass" if preview_paths and not missing_previews else "fail",
        {
            "previews": [str(path) for path in preview_paths],
            "missing_or_empty": missing_previews,
        },
    )

    add_check(
        checks,
        "unity-transfer",
        "warn",
        "Blender procedural nodes do not transfer through FBX; approved channels require baking or a tested URP Shader Graph recreation.",
    )
    add_check(
        checks,
        "visual-material-quality",
        "not-evaluated",
        "Requires human review of neutral, grazing, perspective, and two-scale swatch previews.",
    )

    structural_checks = [
        check
        for check in checks
        if check["name"] not in {"unity-transfer", "visual-material-quality"}
    ]
    status = (
        "fail"
        if any(check["status"] == "fail" for check in structural_checks)
        else "warn"
        if any(check["status"] == "warn" for check in structural_checks)
        else "pass"
    )

    report = {
        "source_file": str(blend_path),
        "source_sha256": file_sha256(blend_path),
        "blender_version": bpy.app.version_string,
        "manifest": str(manifest_path),
        "asset_parent": args.parent,
        "structural_status": status,
        "checks": checks,
        "summary": {
            "output_objects": len(output_objects),
            "expected_materials": len(expected_materials),
            "procedural_groups": len(group_reports),
            "external_images": len(invalid_external_images),
            "allowed_packed_images": len(allowed_packed_names),
            "preview_files": len(preview_paths),
        },
        "materials": material_reports,
        "node_groups": group_reports,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"PROCEDURAL_MATERIAL_VALIDATION={args.output.resolve()}")
    print(f"PROCEDURAL_MATERIAL_STRUCTURAL_STATUS={status}")


if __name__ == "__main__":
    main()
