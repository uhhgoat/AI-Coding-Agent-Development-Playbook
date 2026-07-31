"""Validate the general-purpose procedural material library in the open blend."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import bpy


EXPECTED_GROUPS = {
    "GP_Surface_WoodGrain_v1",
    "GP_Surface_ForgedMetal_v1",
    "GP_Surface_PolishedMetal_v1",
    "GP_Surface_Leather_v1",
    "GP_Surface_WovenCloth_v1",
    "GP_Surface_Masonry_v1",
    "GP_Surface_Plaster_v1",
}
REQUIRED_INPUTS = {
    "Vector",
    "Scale (1/m)",
    "Macro Amount",
    "Mid Amount",
    "Micro Amount",
    "Normal Strength",
    "Wear Mask",
    "Wear Amount",
}
REQUIRED_OUTPUTS = {
    "Base Color",
    "Roughness",
    "Metallic",
    "Normal",
    "Height",
    "Wear",
}
REQUIRED_FRAMES = {
    "FRAME_Coordinates",
    "FRAME_Macro",
    "FRAME_Mid",
    "FRAME_Micro",
    "FRAME_Wear",
    "FRAME_Outputs",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--preview", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return parser.parse_args(argv)


def sockets(group: bpy.types.NodeTree, direction: str) -> set[str]:
    return {
        item.name
        for item in group.interface.items_tree
        if item.item_type == "SOCKET" and item.in_out == direction
    }


def main() -> None:
    args = parse_args()
    manifest_path = args.manifest.resolve()
    preview_path = args.preview.resolve()
    report_path = args.report.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    groups = {
        group.name: group
        for group in bpy.data.node_groups
        if group.bl_idname == "ShaderNodeTree" and group.name.startswith("GP_Surface_")
    }
    group_reports = []
    for name in sorted(EXPECTED_GROUPS):
        group = groups.get(name)
        if group is None:
            group_reports.append({"name": name, "status": "fail", "missing": True})
            continue
        missing_inputs = sorted(REQUIRED_INPUTS - sockets(group, "INPUT"))
        missing_outputs = sorted(REQUIRED_OUTPUTS - sockets(group, "OUTPUT"))
        missing_frames = sorted(REQUIRED_FRAMES - set(group.nodes.keys()))
        invalid_provenance = (
            group.get("provenance") != "independently-authored-general-purpose"
            or group.get("tutorial_graph_copied") is not False
        )
        group_reports.append(
            {
                "name": name,
                "status": (
                    "pass"
                    if not missing_inputs
                    and not missing_outputs
                    and not missing_frames
                    and not invalid_provenance
                    else "fail"
                ),
                "nodes": len(group.nodes),
                "links": len(group.links),
                "missing_inputs": missing_inputs,
                "missing_outputs": missing_outputs,
                "missing_frames": missing_frames,
                "invalid_provenance": invalid_provenance,
            }
        )

    material_reports = []
    for material in sorted(bpy.data.materials, key=lambda item: item.name):
        if not material.name.startswith("GP_"):
            continue
        nodes = material.node_tree.nodes if material.use_nodes else []
        image_nodes = [node.name for node in nodes if node.type == "TEX_IMAGE"]
        outputs = [node for node in nodes if node.type == "OUTPUT_MATERIAL"]
        principled = [node for node in nodes if node.type == "BSDF_PRINCIPLED"]
        groups_used = [
            node.node_tree.name
            for node in nodes
            if node.type == "GROUP" and node.node_tree is not None
        ]
        valid_profile = material.get("style_profile") in {
            "grounded-realism",
            "clean-stylized",
        }
        valid = (
            len(outputs) == 1
            and len(principled) == 1
            and len(groups_used) == 1
            and groups_used[0] in EXPECTED_GROUPS
            and not image_nodes
            and valid_profile
        )
        material_reports.append(
            {
                "name": material.name,
                "status": "pass" if valid else "fail",
                "style_profile": material.get("style_profile"),
                "groups": groups_used,
                "image_nodes": image_nodes,
            }
        )

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
    manifest_groups = {record["name"] for record in manifest.get("groups", [])}
    manifest_materials = {record["name"] for record in manifest.get("materials", [])}
    actual_materials = {record["name"] for record in material_reports}

    checks = [
        {
            "name": "expected-groups",
            "status": "pass" if set(groups) == EXPECTED_GROUPS else "fail",
            "actual": sorted(groups),
        },
        {
            "name": "group-contracts",
            "status": (
                "pass"
                if all(record["status"] == "pass" for record in group_reports)
                else "fail"
            ),
        },
        {
            "name": "material-contracts",
            "status": (
                "pass"
                if material_reports
                and all(record["status"] == "pass" for record in material_reports)
                else "fail"
            ),
        },
        {
            "name": "manifest-parity",
            "status": (
                "pass"
                if manifest_groups == EXPECTED_GROUPS
                and manifest_materials == actual_materials
                else "fail"
            ),
        },
        {
            "name": "external-image-dependencies",
            "status": "pass" if not external_images else "fail",
            "images": external_images,
        },
        {
            "name": "preview",
            "status": (
                "pass"
                if preview_path.exists() and preview_path.stat().st_size > 0
                else "fail"
            ),
            "path": str(preview_path),
        },
    ]
    status = "pass" if all(check["status"] == "pass" for check in checks) else "fail"
    report = {
        "status": status,
        "blend": bpy.data.filepath,
        "blender_version": bpy.app.version_string,
        "manifest": str(manifest_path),
        "preview": str(preview_path),
        "checks": checks,
        "groups": group_reports,
        "materials": material_reports,
        "notes": [
            "Visual quality still requires human review at intended scale and lighting.",
            "Bake validation is a separate stage.",
        ],
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"MATERIAL_LIBRARY_VALIDATION={report_path}")
    print(f"MATERIAL_LIBRARY_STATUS={status}")
    if status != "pass":
        raise RuntimeError("Material library validation failed.")


if __name__ == "__main__":
    main()
