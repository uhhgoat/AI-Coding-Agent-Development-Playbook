"""Build a reusable, project-neutral Blender procedural material library.

Run with Blender, not the system Python:

    blender --background --factory-startup --python build_material_library.py \
      -- --output general-procedural-material-library-v1.blend \
         --manifest material-library-manifest.json \
         --preview material-library-preview.png

The graphs are original implementations of common procedural-shading
principles. They do not copy a tutorial graph or require external images.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

import bpy
from mathutils import Vector


LIBRARY_VERSION = "1.0.0"
MINIMUM_BLENDER = (4, 3, 0)
GROUP_PREFIX = "GP_Surface_"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--preview", type=Path, required=True)
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return parser.parse_args(argv)


def clear_file() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for collection in (
        bpy.data.materials,
        bpy.data.node_groups,
        bpy.data.curves,
        bpy.data.cameras,
        bpy.data.lights,
    ):
        for datablock in list(collection):
            collection.remove(datablock)


def add_socket(
    group: bpy.types.NodeTree,
    name: str,
    in_out: str,
    socket_type: str,
    default: Any = None,
    minimum: float | None = None,
    maximum: float | None = None,
) -> Any:
    socket = group.interface.new_socket(
        name=name,
        in_out=in_out,
        socket_type=socket_type,
    )
    if default is not None and hasattr(socket, "default_value"):
        socket.default_value = default
    if minimum is not None and hasattr(socket, "min_value"):
        socket.min_value = minimum
    if maximum is not None and hasattr(socket, "max_value"):
        socket.max_value = maximum
    return socket


def new_surface_group(
    name: str,
    material_family: str,
    coordinate_contract: str,
    extra_inputs: list[tuple[str, str, Any, float | None, float | None]],
) -> tuple[bpy.types.NodeTree, bpy.types.Node, bpy.types.Node]:
    group = bpy.data.node_groups.new(name, "ShaderNodeTree")
    group.use_fake_user = True
    group["library_version"] = LIBRARY_VERSION
    group["material_family"] = material_family
    group["coordinate_contract"] = coordinate_contract
    group["physical_scale_unit"] = "meters"
    group["provenance"] = "independently-authored-general-purpose"
    group["tutorial_graph_copied"] = False

    add_socket(group, "Vector", "INPUT", "NodeSocketVector")
    add_socket(group, "Scale (1/m)", "INPUT", "NodeSocketFloat", 1.0, 0.01, 1000.0)
    add_socket(group, "Macro Amount", "INPUT", "NodeSocketFloat", 1.0, 0.0, 1.0)
    add_socket(group, "Mid Amount", "INPUT", "NodeSocketFloat", 1.0, 0.0, 1.0)
    add_socket(group, "Micro Amount", "INPUT", "NodeSocketFloat", 1.0, 0.0, 1.0)
    add_socket(group, "Normal Strength", "INPUT", "NodeSocketFloat", 0.25, 0.0, 2.0)
    add_socket(group, "Wear Mask", "INPUT", "NodeSocketFloat", 0.0, 0.0, 1.0)
    add_socket(group, "Wear Amount", "INPUT", "NodeSocketFloat", 0.0, 0.0, 1.0)
    for socket_name, socket_type, default, minimum, maximum in extra_inputs:
        add_socket(
            group,
            socket_name,
            "INPUT",
            socket_type,
            default,
            minimum,
            maximum,
        )

    add_socket(group, "Base Color", "OUTPUT", "NodeSocketColor")
    add_socket(group, "Roughness", "OUTPUT", "NodeSocketFloat")
    add_socket(group, "Metallic", "OUTPUT", "NodeSocketFloat")
    add_socket(group, "Normal", "OUTPUT", "NodeSocketVector")
    add_socket(group, "Height", "OUTPUT", "NodeSocketFloat")
    add_socket(group, "Wear", "OUTPUT", "NodeSocketFloat")

    group_input = group.nodes.new("NodeGroupInput")
    group_input.name = "INPUTS_MaterialContract"
    group_input.label = "Material contract (meters)"
    group_input.location = (-1400, 0)

    group_output = group.nodes.new("NodeGroupOutput")
    group_output.name = "OUTPUTS_SurfaceChannels"
    group_output.label = "Bakeable surface channels"
    group_output.location = (1400, 0)

    for frame_name, label, x in (
        ("FRAME_Coordinates", "1. Coordinates and physical scale", -1160),
        ("FRAME_Macro", "2. Macro identity", -800),
        ("FRAME_Mid", "3. Characteristic mid structure", -380),
        ("FRAME_Micro", "4. Micro response", 60),
        ("FRAME_Wear", "5. Authored contact/use mask", 440),
        ("FRAME_Outputs", "6. PBR channel assembly", 900),
    ):
        frame = group.nodes.new("NodeFrame")
        frame.name = frame_name
        frame.label = label
        frame.location = (x, 0)

    return group, group_input, group_output


def add_node(
    group: bpy.types.NodeTree,
    node_type: str,
    name: str,
    label: str,
    location: tuple[float, float],
    frame: str | None = None,
) -> bpy.types.Node:
    node = group.nodes.new(node_type)
    node.name = name
    node.label = label
    node.location = location
    if frame:
        node.parent = group.nodes[frame]
    return node


def math_node(
    group: bpy.types.NodeTree,
    operation: str,
    name: str,
    label: str,
    location: tuple[float, float],
    frame: str,
    value: float | None = None,
) -> bpy.types.Node:
    node = add_node(
        group,
        "ShaderNodeMath",
        name,
        label,
        location,
        frame,
    )
    node.operation = operation
    if value is not None:
        node.inputs[1].default_value = value
    return node


def map_range(
    group: bpy.types.NodeTree,
    name: str,
    label: str,
    location: tuple[float, float],
    frame: str,
    from_min: float,
    from_max: float,
    to_min: float = 0.0,
    to_max: float = 1.0,
) -> bpy.types.Node:
    node = add_node(
        group,
        "ShaderNodeMapRange",
        name,
        label,
        location,
        frame,
    )
    node.clamp = True
    node.inputs["From Min"].default_value = from_min
    node.inputs["From Max"].default_value = from_max
    node.inputs["To Min"].default_value = to_min
    node.inputs["To Max"].default_value = to_max
    return node


def mix_rgb(
    group: bpy.types.NodeTree,
    name: str,
    label: str,
    location: tuple[float, float],
    frame: str,
    blend_type: str = "MIX",
) -> bpy.types.Node:
    node = add_node(
        group,
        "ShaderNodeMixRGB",
        name,
        label,
        location,
        frame,
    )
    node.blend_type = blend_type
    node.inputs["Fac"].default_value = 1.0
    return node


def scaled_vector(
    group: bpy.types.NodeTree,
    group_input: bpy.types.Node,
) -> bpy.types.NodeSocket:
    scale = add_node(
        group,
        "ShaderNodeVectorMath",
        "COORD_MeterScale",
        "Object/material space × Scale (1/m)",
        (-1120, 0),
        "FRAME_Coordinates",
    )
    scale.operation = "SCALE"
    group.links.new(group_input.outputs["Vector"], scale.inputs["Vector"])
    group.links.new(group_input.outputs["Scale (1/m)"], scale.inputs["Scale"])
    return scale.outputs["Vector"]


def multiplied_amount(
    group: bpy.types.NodeTree,
    source: bpy.types.NodeSocket,
    amount: bpy.types.NodeSocket,
    name: str,
    label: str,
    location: tuple[float, float],
    frame: str,
) -> bpy.types.NodeSocket:
    multiply = math_node(
        group,
        "MULTIPLY",
        name,
        label,
        location,
        frame,
    )
    group.links.new(source, multiply.inputs[0])
    group.links.new(amount, multiply.inputs[1])
    return multiply.outputs[0]


def assemble_wear(
    group: bpy.types.NodeTree,
    group_input: bpy.types.Node,
) -> bpy.types.NodeSocket:
    wear = math_node(
        group,
        "MULTIPLY",
        "MASK_AuthoredWear",
        "Wear Mask × Wear Amount",
        (470, -260),
        "FRAME_Wear",
    )
    wear.use_clamp = True
    group.links.new(group_input.outputs["Wear Mask"], wear.inputs[0])
    group.links.new(group_input.outputs["Wear Amount"], wear.inputs[1])
    return wear.outputs[0]


def assemble_outputs(
    group: bpy.types.NodeTree,
    group_input: bpy.types.Node,
    group_output: bpy.types.Node,
    color: bpy.types.NodeSocket,
    roughness: bpy.types.NodeSocket,
    metallic: bpy.types.NodeSocket | float,
    height: bpy.types.NodeSocket,
    wear: bpy.types.NodeSocket,
    bump_distance_meters: float,
) -> None:
    bump = add_node(
        group,
        "ShaderNodeBump",
        "NORMAL_SurfaceResponse",
        f"Shallow response ({bump_distance_meters:g} m)",
        (930, -140),
        "FRAME_Outputs",
    )
    bump.inputs["Distance"].default_value = bump_distance_meters
    group.links.new(group_input.outputs["Normal Strength"], bump.inputs["Strength"])
    group.links.new(height, bump.inputs["Height"])

    group.links.new(color, group_output.inputs["Base Color"])
    group.links.new(roughness, group_output.inputs["Roughness"])
    if isinstance(metallic, float):
        group_output.inputs["Metallic"].default_value = metallic
    else:
        group.links.new(metallic, group_output.inputs["Metallic"])
    group.links.new(bump.outputs["Normal"], group_output.inputs["Normal"])
    group.links.new(height, group_output.inputs["Height"])
    group.links.new(wear, group_output.inputs["Wear"])


def build_wood_group() -> bpy.types.NodeTree:
    group, inputs, outputs = new_surface_group(
        f"{GROUP_PREFIX}WoodGrain_v1",
        "wood",
        "Object/material space; local Z follows the grain and XY crosses the virtual log.",
        [
            ("Earlywood Color", "NodeSocketColor", (0.12, 0.035, 0.008, 1.0), None, None),
            ("Latewood Color", "NodeSocketColor", (0.42, 0.17, 0.045, 1.0), None, None),
            ("Roughness Min", "NodeSocketFloat", 0.22, 0.0, 1.0),
            ("Roughness Max", "NodeSocketFloat", 0.48, 0.0, 1.0),
            ("Ring Frequency", "NodeSocketFloat", 14.0, 2.0, 80.0),
            ("Fiber Frequency", "NodeSocketFloat", 38.0, 4.0, 200.0),
            ("Finish Amount", "NodeSocketFloat", 0.5, 0.0, 1.0),
        ],
    )
    vector = scaled_vector(group, inputs)

    separate = add_node(
        group,
        "ShaderNodeSeparateXYZ",
        "COORD_LogAxes",
        "XY radial / Z longitudinal",
        (-1000, 110),
        "FRAME_Coordinates",
    )
    group.links.new(vector, separate.inputs["Vector"])

    drift_noise = add_node(
        group,
        "ShaderNodeTexNoise",
        "FORM_HeartlineDrift",
        "Slow log-heart drift",
        (-760, -230),
        "FRAME_Macro",
    )
    drift_noise.noise_dimensions = "3D"
    drift_noise.inputs["Scale"].default_value = 0.75
    drift_noise.inputs["Detail"].default_value = 2.0
    drift_noise.inputs["Roughness"].default_value = 0.55
    group.links.new(vector, drift_noise.inputs["Vector"])

    drift_center = math_node(
        group,
        "SUBTRACT",
        "FORM_CenteredDrift",
        "Center drift around zero",
        (-580, -230),
        "FRAME_Macro",
        0.5,
    )
    group.links.new(drift_noise.outputs["Fac"], drift_center.inputs[0])

    drift_amount = multiplied_amount(
        group,
        drift_center.outputs[0],
        inputs.outputs["Macro Amount"],
        "FORM_DriftAmount",
        "Macro-controlled heart drift",
        (-390, -230),
        "FRAME_Macro",
    )

    x_drift = math_node(
        group,
        "ADD",
        "FORM_DriftedX",
        "Drifted elliptical X",
        (-720, 120),
        "FRAME_Macro",
    )
    group.links.new(separate.outputs["X"], x_drift.inputs[0])
    group.links.new(drift_amount, x_drift.inputs[1])

    x_ellipse = math_node(
        group,
        "MULTIPLY",
        "FORM_EllipticalX",
        "Elliptical log section",
        (-540, 120),
        "FRAME_Macro",
        1.35,
    )
    group.links.new(x_drift.outputs[0], x_ellipse.inputs[0])

    combine = add_node(
        group,
        "ShaderNodeCombineXYZ",
        "FORM_LogCrossSection",
        "Virtual log cross-section",
        (-360, 100),
        "FRAME_Macro",
    )
    group.links.new(x_ellipse.outputs[0], combine.inputs["X"])
    group.links.new(separate.outputs["Y"], combine.inputs["Y"])

    radius = add_node(
        group,
        "ShaderNodeVectorMath",
        "FORM_RadialDistance",
        "Distance from virtual heart",
        (-170, 100),
        "FRAME_Macro",
    )
    radius.operation = "LENGTH"
    group.links.new(combine.outputs["Vector"], radius.inputs["Vector"])

    ring_scale = math_node(
        group,
        "MULTIPLY",
        "FORM_RingFrequency",
        "Radial growth frequency",
        (10, 105),
        "FRAME_Macro",
    )
    group.links.new(radius.outputs["Value"], ring_scale.inputs[0])
    group.links.new(inputs.outputs["Ring Frequency"], ring_scale.inputs[1])

    ring_sine = math_node(
        group,
        "SINE",
        "FORM_GrowthOscillation",
        "Growth-ring oscillation",
        (190, 105),
        "FRAME_Macro",
    )
    group.links.new(ring_scale.outputs[0], ring_sine.inputs[0])

    ring_abs = math_node(
        group,
        "ABSOLUTE",
        "FORM_GrowthBands",
        "Asymmetric growth bands",
        (350, 105),
        "FRAME_Macro",
    )
    group.links.new(ring_sine.outputs[0], ring_abs.inputs[0])

    rings = map_range(
        group,
        "MASK_GrowthRings",
        "Recognizable annual-ring mask",
        (520, 105),
        "FRAME_Macro",
        0.12,
        0.92,
    )
    group.links.new(ring_abs.outputs[0], rings.inputs["Value"])

    anisotropic = add_node(
        group,
        "ShaderNodeVectorMath",
        "DETAIL_LongitudinalCoordinates",
        "High XY / low Z for longitudinal vessels",
        (-330, 20),
        "FRAME_Mid",
    )
    anisotropic.operation = "MULTIPLY"
    anisotropic.inputs[1].default_value = (38.0, 38.0, 0.65)
    group.links.new(vector, anisotropic.inputs[0])

    fibers = add_node(
        group,
        "ShaderNodeTexNoise",
        "DETAIL_LongitudinalVessels",
        "Continuous grain-following vessels",
        (-130, 20),
        "FRAME_Mid",
    )
    fibers.noise_dimensions = "3D"
    fibers.inputs["Scale"].default_value = 1.0
    fibers.inputs["Detail"].default_value = 2.7
    fibers.inputs["Roughness"].default_value = 0.62
    group.links.new(anisotropic.outputs["Vector"], fibers.inputs["Vector"])

    fiber_contrast = map_range(
        group,
        "MASK_Vessels",
        "Restrained vessel mask",
        (70, 20),
        "FRAME_Mid",
        0.28,
        0.73,
    )
    group.links.new(fibers.outputs["Fac"], fiber_contrast.inputs["Value"])

    fiber_amount = multiplied_amount(
        group,
        fiber_contrast.outputs["Result"],
        inputs.outputs["Mid Amount"],
        "MASK_VesselAmount",
        "Mid-frequency vessel amount",
        (250, 20),
        "FRAME_Mid",
    )

    grain = mix_rgb(
        group,
        "MASK_WoodIdentity",
        "Growth rings plus weaker vessels",
        (430, 10),
        "FRAME_Mid",
        "MULTIPLY",
    )
    grain.inputs["Fac"].default_value = 0.35
    group.links.new(rings.outputs["Result"], grain.inputs[1])
    group.links.new(fiber_amount, grain.inputs[2])

    color = mix_rgb(
        group,
        "COLOR_WoodSpecies",
        "Earlywood / latewood",
        (750, 150),
        "FRAME_Outputs",
    )
    group.links.new(grain.outputs["Color"], color.inputs["Fac"])
    group.links.new(inputs.outputs["Earlywood Color"], color.inputs[1])
    group.links.new(inputs.outputs["Latewood Color"], color.inputs[2])

    finish_rough = math_node(
        group,
        "MULTIPLY",
        "ROUGHNESS_FinishReduction",
        "Finish narrows roughness",
        (700, -40),
        "FRAME_Outputs",
        -0.14,
    )
    group.links.new(inputs.outputs["Finish Amount"], finish_rough.inputs[0])

    rough_map = map_range(
        group,
        "ROUGHNESS_Grain",
        "Grain-aware finish",
        (880, 40),
        "FRAME_Outputs",
        0.0,
        1.0,
    )
    group.links.new(grain.outputs["Color"], rough_map.inputs["Value"])
    group.links.new(inputs.outputs["Roughness Min"], rough_map.inputs["To Min"])
    group.links.new(inputs.outputs["Roughness Max"], rough_map.inputs["To Max"])

    roughness = math_node(
        group,
        "ADD",
        "ROUGHNESS_FinishedWood",
        "Polished/oiled finish response",
        (1060, 10),
        "FRAME_Outputs",
    )
    roughness.use_clamp = True
    group.links.new(rough_map.outputs["Result"], roughness.inputs[0])
    group.links.new(finish_rough.outputs[0], roughness.inputs[1])

    micro = add_node(
        group,
        "ShaderNodeTexNoise",
        "MICRO_WoodPores",
        "Subtle pore response",
        (70, -50),
        "FRAME_Micro",
    )
    micro.noise_dimensions = "3D"
    micro.inputs["Scale"].default_value = 140.0
    micro.inputs["Detail"].default_value = 2.0
    micro.inputs["Roughness"].default_value = 0.7
    group.links.new(vector, micro.inputs["Vector"])

    micro_amount = multiplied_amount(
        group,
        micro.outputs["Fac"],
        inputs.outputs["Micro Amount"],
        "MICRO_PoreAmount",
        "Micro pore amount",
        (260, -55),
        "FRAME_Micro",
    )

    ring_height = multiplied_amount(
        group,
        rings.outputs["Result"],
        inputs.outputs["Macro Amount"],
        "HEIGHT_RingAmount",
        "Growth-ring height",
        (590, -130),
        "FRAME_Outputs",
    )
    height_mix = mix_rgb(
        group,
        "HEIGHT_WoodSurface",
        "Rings with weak pores",
        (760, -150),
        "FRAME_Outputs",
        "ADD",
    )
    height_mix.inputs["Fac"].default_value = 0.16
    group.links.new(ring_height, height_mix.inputs[1])
    group.links.new(micro_amount, height_mix.inputs[2])

    wear = assemble_wear(group, inputs)
    assemble_outputs(
        group,
        inputs,
        outputs,
        color.outputs["Color"],
        roughness.outputs[0],
        0.0,
        height_mix.outputs["Color"],
        wear,
        0.00022,
    )
    return group


def build_forged_metal_group() -> bpy.types.NodeTree:
    group, inputs, outputs = new_surface_group(
        f"{GROUP_PREFIX}ForgedMetal_v1",
        "metal",
        "Object/material space in meters; align axes only when scratches need a direction.",
        [
            ("Dark Metal", "NodeSocketColor", (0.035, 0.045, 0.055, 1.0), None, None),
            ("Light Metal", "NodeSocketColor", (0.22, 0.25, 0.28, 1.0), None, None),
            ("Roughness Min", "NodeSocketFloat", 0.42, 0.0, 1.0),
            ("Roughness Max", "NodeSocketFloat", 0.72, 0.0, 1.0),
            ("Hammer Frequency", "NodeSocketFloat", 26.0, 2.0, 120.0),
            ("Pit Frequency", "NodeSocketFloat", 150.0, 10.0, 600.0),
        ],
    )
    vector = scaled_vector(group, inputs)

    macro = add_node(
        group,
        "ShaderNodeTexNoise",
        "FORM_ForgeScale",
        "Broad manufacturing variation",
        (-760, 180),
        "FRAME_Macro",
    )
    macro.noise_dimensions = "3D"
    macro.inputs["Scale"].default_value = 4.2
    macro.inputs["Detail"].default_value = 3.2
    macro.inputs["Roughness"].default_value = 0.62
    group.links.new(vector, macro.inputs["Vector"])

    macro_amount = multiplied_amount(
        group,
        macro.outputs["Fac"],
        inputs.outputs["Macro Amount"],
        "FORM_ForgeAmount",
        "Macro forge amount",
        (-560, 180),
        "FRAME_Macro",
    )

    hammer = add_node(
        group,
        "ShaderNodeTexVoronoi",
        "DETAIL_HammerCells",
        "Irregular shallow hammer marks",
        (-310, 100),
        "FRAME_Mid",
    )
    hammer.voronoi_dimensions = "3D"
    hammer.feature = "F1"
    hammer.distance = "EUCLIDEAN"
    group.links.new(vector, hammer.inputs["Vector"])
    group.links.new(inputs.outputs["Hammer Frequency"], hammer.inputs["Scale"])

    hammer_profile = map_range(
        group,
        "MASK_HammerMarks",
        "Soft, nonuniform hammer impressions",
        (-110, 100),
        "FRAME_Mid",
        0.06,
        0.46,
        1.0,
        0.0,
    )
    group.links.new(hammer.outputs["Distance"], hammer_profile.inputs["Value"])

    hammer_amount = multiplied_amount(
        group,
        hammer_profile.outputs["Result"],
        inputs.outputs["Mid Amount"],
        "DETAIL_HammerAmount",
        "Mid-frequency hammer amount",
        (80, 100),
        "FRAME_Mid",
    )

    pits = add_node(
        group,
        "ShaderNodeTexNoise",
        "MICRO_Pitting",
        "Sparse fine pitting",
        (70, -80),
        "FRAME_Micro",
    )
    pits.noise_dimensions = "3D"
    pits.inputs["Detail"].default_value = 2.2
    pits.inputs["Roughness"].default_value = 0.72
    group.links.new(vector, pits.inputs["Vector"])
    group.links.new(inputs.outputs["Pit Frequency"], pits.inputs["Scale"])

    pit_mask = map_range(
        group,
        "MASK_SparsePits",
        "Thresholded pit mask",
        (250, -80),
        "FRAME_Micro",
        0.73,
        0.89,
    )
    group.links.new(pits.outputs["Fac"], pit_mask.inputs["Value"])

    pit_amount = multiplied_amount(
        group,
        pit_mask.outputs["Result"],
        inputs.outputs["Micro Amount"],
        "MICRO_PitAmount",
        "Micro pit amount",
        (430, -80),
        "FRAME_Micro",
    )

    color = mix_rgb(
        group,
        "COLOR_ForgeVariation",
        "Restrained iron value variation",
        (700, 170),
        "FRAME_Outputs",
    )
    group.links.new(macro_amount, color.inputs["Fac"])
    group.links.new(inputs.outputs["Dark Metal"], color.inputs[1])
    group.links.new(inputs.outputs["Light Metal"], color.inputs[2])

    roughness = map_range(
        group,
        "ROUGHNESS_Manufacturing",
        "Forge and hammer roughness",
        (700, 10),
        "FRAME_Outputs",
        0.0,
        1.0,
    )
    group.links.new(macro_amount, roughness.inputs["Value"])
    group.links.new(inputs.outputs["Roughness Min"], roughness.inputs["To Min"])
    group.links.new(inputs.outputs["Roughness Max"], roughness.inputs["To Max"])

    height = mix_rgb(
        group,
        "HEIGHT_ForgedSurface",
        "Hammer marks plus sparse pits",
        (690, -140),
        "FRAME_Outputs",
        "SUBTRACT",
    )
    height.inputs["Fac"].default_value = 0.35
    group.links.new(hammer_amount, height.inputs[1])
    group.links.new(pit_amount, height.inputs[2])

    wear = assemble_wear(group, inputs)
    polished_color = mix_rgb(
        group,
        "COLOR_ContactPolish",
        "Authored contact polish",
        (940, 170),
        "FRAME_Outputs",
    )
    polished_color.inputs[2].default_value = (0.34, 0.38, 0.42, 1.0)
    group.links.new(wear, polished_color.inputs["Fac"])
    group.links.new(color.outputs["Color"], polished_color.inputs[1])

    polished_roughness = mix_rgb(
        group,
        "ROUGHNESS_ContactPolish",
        "Lower roughness only where use supports it",
        (940, 20),
        "FRAME_Outputs",
    )
    polished_roughness.inputs[2].default_value = (0.22, 0.22, 0.22, 1.0)
    group.links.new(wear, polished_roughness.inputs["Fac"])
    group.links.new(roughness.outputs["Result"], polished_roughness.inputs[1])

    assemble_outputs(
        group,
        inputs,
        outputs,
        polished_color.outputs["Color"],
        polished_roughness.outputs["Color"],
        1.0,
        height.outputs["Color"],
        wear,
        0.0003,
    )
    return group


def build_polished_metal_group() -> bpy.types.NodeTree:
    group, inputs, outputs = new_surface_group(
        f"{GROUP_PREFIX}PolishedMetal_v1",
        "metal",
        "Object/material space in meters; local Z follows brushing or grinding direction.",
        [
            ("Metal Dark", "NodeSocketColor", (0.18, 0.21, 0.24, 1.0), None, None),
            ("Metal Light", "NodeSocketColor", (0.58, 0.65, 0.72, 1.0), None, None),
            ("Roughness Min", "NodeSocketFloat", 0.12, 0.0, 1.0),
            ("Roughness Max", "NodeSocketFloat", 0.3, 0.0, 1.0),
            ("Brush Frequency", "NodeSocketFloat", 220.0, 10.0, 1000.0),
            ("Scratch Amount", "NodeSocketFloat", 0.25, 0.0, 1.0),
        ],
    )
    vector = scaled_vector(group, inputs)

    macro = add_node(
        group,
        "ShaderNodeTexNoise",
        "FORM_SteelVariation",
        "Very weak alloy/manufacturing variation",
        (-760, 170),
        "FRAME_Macro",
    )
    macro.noise_dimensions = "3D"
    macro.inputs["Scale"].default_value = 5.0
    macro.inputs["Detail"].default_value = 2.0
    macro.inputs["Roughness"].default_value = 0.55
    group.links.new(vector, macro.inputs["Vector"])

    macro_amount = multiplied_amount(
        group,
        macro.outputs["Fac"],
        inputs.outputs["Macro Amount"],
        "FORM_SteelAmount",
        "Macro steel amount",
        (-560, 170),
        "FRAME_Macro",
    )

    anisotropic = add_node(
        group,
        "ShaderNodeVectorMath",
        "DETAIL_BrushCoordinates",
        "Fine across-brush / long along local Z",
        (-330, 90),
        "FRAME_Mid",
    )
    anisotropic.operation = "MULTIPLY"
    anisotropic.inputs[1].default_value = (1.0, 1.0, 0.025)
    group.links.new(vector, anisotropic.inputs[0])

    brush = add_node(
        group,
        "ShaderNodeTexNoise",
        "DETAIL_DirectionalBrush",
        "Directional finishing marks",
        (-130, 90),
        "FRAME_Mid",
    )
    brush.noise_dimensions = "3D"
    brush.inputs["Detail"].default_value = 1.5
    brush.inputs["Roughness"].default_value = 0.58
    group.links.new(anisotropic.outputs["Vector"], brush.inputs["Vector"])
    group.links.new(inputs.outputs["Brush Frequency"], brush.inputs["Scale"])

    scratches = map_range(
        group,
        "MASK_SegmentedScratches",
        "Sparse directional scratches",
        (70, 90),
        "FRAME_Mid",
        0.68,
        0.88,
    )
    group.links.new(brush.outputs["Fac"], scratches.inputs["Value"])

    scratch_amount = math_node(
        group,
        "MULTIPLY",
        "DETAIL_ScratchControl",
        "Scratch amount × Mid Amount",
        (250, 90),
        "FRAME_Mid",
    )
    group.links.new(inputs.outputs["Scratch Amount"], scratch_amount.inputs[0])
    group.links.new(inputs.outputs["Mid Amount"], scratch_amount.inputs[1])

    controlled_scratches = multiplied_amount(
        group,
        scratches.outputs["Result"],
        scratch_amount.outputs[0],
        "DETAIL_VisibleScratches",
        "Controlled scratch mask",
        (430, 90),
        "FRAME_Mid",
    )

    micro = add_node(
        group,
        "ShaderNodeTexNoise",
        "MICRO_SteelRoughness",
        "Fine roughness breakup",
        (80, -90),
        "FRAME_Micro",
    )
    micro.noise_dimensions = "3D"
    micro.inputs["Scale"].default_value = 420.0
    micro.inputs["Detail"].default_value = 2.0
    micro.inputs["Roughness"].default_value = 0.7
    group.links.new(vector, micro.inputs["Vector"])

    micro_amount = multiplied_amount(
        group,
        micro.outputs["Fac"],
        inputs.outputs["Micro Amount"],
        "MICRO_SteelAmount",
        "Micro roughness amount",
        (270, -90),
        "FRAME_Micro",
    )

    color = mix_rgb(
        group,
        "COLOR_PolishedSteel",
        "Restrained polished-steel range",
        (700, 170),
        "FRAME_Outputs",
    )
    group.links.new(macro_amount, color.inputs["Fac"])
    group.links.new(inputs.outputs["Metal Dark"], color.inputs[1])
    group.links.new(inputs.outputs["Metal Light"], color.inputs[2])

    rough_mask = mix_rgb(
        group,
        "ROUGHNESS_FinishMask",
        "Directional marks plus micro breakup",
        (650, 20),
        "FRAME_Outputs",
        "ADD",
    )
    rough_mask.inputs["Fac"].default_value = 0.35
    group.links.new(controlled_scratches, rough_mask.inputs[1])
    group.links.new(micro_amount, rough_mask.inputs[2])

    roughness = map_range(
        group,
        "ROUGHNESS_PolishedSteel",
        "Polished finish range",
        (850, 20),
        "FRAME_Outputs",
        0.0,
        1.0,
    )
    group.links.new(rough_mask.outputs["Color"], roughness.inputs["Value"])
    group.links.new(inputs.outputs["Roughness Min"], roughness.inputs["To Min"])
    group.links.new(inputs.outputs["Roughness Max"], roughness.inputs["To Max"])

    wear = assemble_wear(group, inputs)
    assemble_outputs(
        group,
        inputs,
        outputs,
        color.outputs["Color"],
        roughness.outputs["Result"],
        1.0,
        controlled_scratches,
        wear,
        0.000035,
    )
    return group


def build_leather_group() -> bpy.types.NodeTree:
    group, inputs, outputs = new_surface_group(
        f"{GROUP_PREFIX}Leather_v1",
        "leather",
        "UV or object/material space in meters; use UVs for straps, stitches, and directional stretch.",
        [
            ("Leather Dark", "NodeSocketColor", (0.035, 0.012, 0.006, 1.0), None, None),
            ("Leather Light", "NodeSocketColor", (0.20, 0.065, 0.025, 1.0), None, None),
            ("Roughness Min", "NodeSocketFloat", 0.34, 0.0, 1.0),
            ("Roughness Max", "NodeSocketFloat", 0.68, 0.0, 1.0),
            ("Cell Frequency", "NodeSocketFloat", 90.0, 8.0, 500.0),
            ("Pore Frequency", "NodeSocketFloat", 300.0, 20.0, 1200.0),
        ],
    )
    vector = scaled_vector(group, inputs)

    macro = add_node(
        group,
        "ShaderNodeTexNoise",
        "FORM_LeatherCompression",
        "Broad compression and tone",
        (-760, 160),
        "FRAME_Macro",
    )
    macro.noise_dimensions = "3D"
    macro.inputs["Scale"].default_value = 3.5
    macro.inputs["Detail"].default_value = 3.0
    macro.inputs["Roughness"].default_value = 0.65
    group.links.new(vector, macro.inputs["Vector"])

    macro_amount = multiplied_amount(
        group,
        macro.outputs["Fac"],
        inputs.outputs["Macro Amount"],
        "FORM_LeatherAmount",
        "Macro compression amount",
        (-560, 160),
        "FRAME_Macro",
    )

    cells = add_node(
        group,
        "ShaderNodeTexVoronoi",
        "DETAIL_LeatherCells",
        "Irregular hide grain",
        (-310, 70),
        "FRAME_Mid",
    )
    cells.voronoi_dimensions = "3D"
    cells.feature = "DISTANCE_TO_EDGE"
    cells.distance = "EUCLIDEAN"
    group.links.new(vector, cells.inputs["Vector"])
    group.links.new(inputs.outputs["Cell Frequency"], cells.inputs["Scale"])

    cell_mask = map_range(
        group,
        "MASK_LeatherGrain",
        "Soft cell-edge grain",
        (-110, 70),
        "FRAME_Mid",
        0.0,
        0.12,
        1.0,
        0.0,
    )
    group.links.new(cells.outputs["Distance"], cell_mask.inputs["Value"])

    cell_amount = multiplied_amount(
        group,
        cell_mask.outputs["Result"],
        inputs.outputs["Mid Amount"],
        "DETAIL_LeatherGrainAmount",
        "Mid-frequency grain amount",
        (80, 70),
        "FRAME_Mid",
    )

    pores = add_node(
        group,
        "ShaderNodeTexNoise",
        "MICRO_LeatherPores",
        "Fine hide pores",
        (70, -80),
        "FRAME_Micro",
    )
    pores.noise_dimensions = "3D"
    pores.inputs["Detail"].default_value = 2.0
    pores.inputs["Roughness"].default_value = 0.72
    group.links.new(vector, pores.inputs["Vector"])
    group.links.new(inputs.outputs["Pore Frequency"], pores.inputs["Scale"])

    pore_mask = map_range(
        group,
        "MASK_LeatherPores",
        "Sparse pore mask",
        (250, -80),
        "FRAME_Micro",
        0.66,
        0.86,
    )
    group.links.new(pores.outputs["Fac"], pore_mask.inputs["Value"])

    pore_amount = multiplied_amount(
        group,
        pore_mask.outputs["Result"],
        inputs.outputs["Micro Amount"],
        "MICRO_LeatherPoreAmount",
        "Micro pore amount",
        (430, -80),
        "FRAME_Micro",
    )

    color = mix_rgb(
        group,
        "COLOR_LeatherTone",
        "Natural hide tone variation",
        (700, 170),
        "FRAME_Outputs",
    )
    group.links.new(macro_amount, color.inputs["Fac"])
    group.links.new(inputs.outputs["Leather Dark"], color.inputs[1])
    group.links.new(inputs.outputs["Leather Light"], color.inputs[2])

    rough_mask = mix_rgb(
        group,
        "ROUGHNESS_LeatherStructure",
        "Grain plus pores",
        (660, 20),
        "FRAME_Outputs",
        "ADD",
    )
    rough_mask.inputs["Fac"].default_value = 0.4
    group.links.new(cell_amount, rough_mask.inputs[1])
    group.links.new(pore_amount, rough_mask.inputs[2])

    roughness = map_range(
        group,
        "ROUGHNESS_Leather",
        "Leather finish range",
        (850, 20),
        "FRAME_Outputs",
        0.0,
        1.0,
    )
    group.links.new(rough_mask.outputs["Color"], roughness.inputs["Value"])
    group.links.new(inputs.outputs["Roughness Min"], roughness.inputs["To Min"])
    group.links.new(inputs.outputs["Roughness Max"], roughness.inputs["To Max"])

    height = mix_rgb(
        group,
        "HEIGHT_LeatherSurface",
        "Hide cells plus fine pores",
        (690, -140),
        "FRAME_Outputs",
        "SUBTRACT",
    )
    height.inputs["Fac"].default_value = 0.22
    group.links.new(cell_amount, height.inputs[1])
    group.links.new(pore_amount, height.inputs[2])

    wear = assemble_wear(group, inputs)
    worn_color = mix_rgb(
        group,
        "COLOR_HandledLeather",
        "Selective grip and edge polish",
        (1040, 170),
        "FRAME_Outputs",
    )
    worn_color.inputs[2].default_value = (0.30, 0.12, 0.05, 1.0)
    group.links.new(wear, worn_color.inputs["Fac"])
    group.links.new(color.outputs["Color"], worn_color.inputs[1])

    worn_roughness = mix_rgb(
        group,
        "ROUGHNESS_HandledLeather",
        "Use-polished leather",
        (1030, 20),
        "FRAME_Outputs",
    )
    worn_roughness.inputs[2].default_value = (0.25, 0.25, 0.25, 1.0)
    group.links.new(wear, worn_roughness.inputs["Fac"])
    group.links.new(roughness.outputs["Result"], worn_roughness.inputs[1])

    assemble_outputs(
        group,
        inputs,
        outputs,
        worn_color.outputs["Color"],
        worn_roughness.outputs["Color"],
        0.0,
        height.outputs["Color"],
        wear,
        0.00012,
    )
    return group


def build_cloth_group() -> bpy.types.NodeTree:
    group, inputs, outputs = new_surface_group(
        f"{GROUP_PREFIX}WovenCloth_v1",
        "cloth",
        "UV or material space; local X and Y follow warp and weft.",
        [
            ("Cloth Dark", "NodeSocketColor", (0.025, 0.035, 0.05, 1.0), None, None),
            ("Cloth Light", "NodeSocketColor", (0.10, 0.16, 0.24, 1.0), None, None),
            ("Roughness Min", "NodeSocketFloat", 0.68, 0.0, 1.0),
            ("Roughness Max", "NodeSocketFloat", 0.9, 0.0, 1.0),
            ("Thread Frequency", "NodeSocketFloat", 180.0, 10.0, 1000.0),
        ],
    )
    vector = scaled_vector(group, inputs)

    macro = add_node(
        group,
        "ShaderNodeTexNoise",
        "FORM_ClothDye",
        "Broad dye and fiber-bundle variation",
        (-760, 160),
        "FRAME_Macro",
    )
    macro.noise_dimensions = "3D"
    macro.inputs["Scale"].default_value = 5.0
    macro.inputs["Detail"].default_value = 2.5
    macro.inputs["Roughness"].default_value = 0.6
    group.links.new(vector, macro.inputs["Vector"])

    macro_amount = multiplied_amount(
        group,
        macro.outputs["Fac"],
        inputs.outputs["Macro Amount"],
        "FORM_ClothDyeAmount",
        "Macro dye amount",
        (-560, 160),
        "FRAME_Macro",
    )

    warp = add_node(
        group,
        "ShaderNodeTexWave",
        "DETAIL_WarpThreads",
        "Warp threads",
        (-310, 105),
        "FRAME_Mid",
    )
    warp.wave_type = "BANDS"
    warp.bands_direction = "X"
    warp.inputs["Distortion"].default_value = 0.6
    warp.inputs["Detail"].default_value = 2.0
    group.links.new(vector, warp.inputs["Vector"])
    group.links.new(inputs.outputs["Thread Frequency"], warp.inputs["Scale"])

    weft = add_node(
        group,
        "ShaderNodeTexWave",
        "DETAIL_WeftThreads",
        "Weft threads",
        (-310, -25),
        "FRAME_Mid",
    )
    weft.wave_type = "BANDS"
    weft.bands_direction = "Y"
    weft.inputs["Distortion"].default_value = 0.6
    weft.inputs["Detail"].default_value = 2.0
    group.links.new(vector, weft.inputs["Vector"])
    group.links.new(inputs.outputs["Thread Frequency"], weft.inputs["Scale"])

    weave = mix_rgb(
        group,
        "DETAIL_OverUnderWeave",
        "Warp/weft crossing response",
        (-80, 60),
        "FRAME_Mid",
        "MULTIPLY",
    )
    weave.inputs["Fac"].default_value = 1.0
    group.links.new(warp.outputs["Color"], weave.inputs[1])
    group.links.new(weft.outputs["Color"], weave.inputs[2])

    weave_amount = multiplied_amount(
        group,
        weave.outputs["Color"],
        inputs.outputs["Mid Amount"],
        "DETAIL_WeaveAmount",
        "Mid-frequency weave amount",
        (140, 60),
        "FRAME_Mid",
    )

    micro = add_node(
        group,
        "ShaderNodeTexNoise",
        "MICRO_FiberBreakup",
        "Fine fiber roughness",
        (80, -80),
        "FRAME_Micro",
    )
    micro.noise_dimensions = "3D"
    micro.inputs["Scale"].default_value = 520.0
    micro.inputs["Detail"].default_value = 2.0
    micro.inputs["Roughness"].default_value = 0.75
    group.links.new(vector, micro.inputs["Vector"])

    micro_amount = multiplied_amount(
        group,
        micro.outputs["Fac"],
        inputs.outputs["Micro Amount"],
        "MICRO_ClothAmount",
        "Micro fiber amount",
        (270, -80),
        "FRAME_Micro",
    )

    color = mix_rgb(
        group,
        "COLOR_ClothDye",
        "Dye variation",
        (700, 170),
        "FRAME_Outputs",
    )
    group.links.new(macro_amount, color.inputs["Fac"])
    group.links.new(inputs.outputs["Cloth Dark"], color.inputs[1])
    group.links.new(inputs.outputs["Cloth Light"], color.inputs[2])

    rough_mask = mix_rgb(
        group,
        "ROUGHNESS_ClothStructure",
        "Weave plus fiber breakup",
        (670, 20),
        "FRAME_Outputs",
        "ADD",
    )
    rough_mask.inputs["Fac"].default_value = 0.35
    group.links.new(weave_amount, rough_mask.inputs[1])
    group.links.new(micro_amount, rough_mask.inputs[2])

    roughness = map_range(
        group,
        "ROUGHNESS_Cloth",
        "Dry woven response",
        (870, 20),
        "FRAME_Outputs",
        0.0,
        1.0,
    )
    group.links.new(rough_mask.outputs["Color"], roughness.inputs["Value"])
    group.links.new(inputs.outputs["Roughness Min"], roughness.inputs["To Min"])
    group.links.new(inputs.outputs["Roughness Max"], roughness.inputs["To Max"])

    height = mix_rgb(
        group,
        "HEIGHT_WovenCloth",
        "Thread crossings with restrained fibers",
        (700, -140),
        "FRAME_Outputs",
        "ADD",
    )
    height.inputs["Fac"].default_value = 0.12
    group.links.new(weave_amount, height.inputs[1])
    group.links.new(micro_amount, height.inputs[2])

    wear = assemble_wear(group, inputs)
    assemble_outputs(
        group,
        inputs,
        outputs,
        color.outputs["Color"],
        roughness.outputs["Result"],
        0.0,
        height.outputs["Color"],
        wear,
        0.00005,
    )
    return group


def build_masonry_group() -> bpy.types.NodeTree:
    group, inputs, outputs = new_surface_group(
        f"{GROUP_PREFIX}Masonry_v1",
        "masonry",
        "UV or object/material space in meters; preserve scale across modular pieces.",
        [
            ("Stone Dark", "NodeSocketColor", (0.12, 0.105, 0.085, 1.0), None, None),
            ("Stone Light", "NodeSocketColor", (0.42, 0.37, 0.29, 1.0), None, None),
            ("Mortar Color", "NodeSocketColor", (0.12, 0.11, 0.09, 1.0), None, None),
            ("Stone Roughness", "NodeSocketFloat", 0.68, 0.0, 1.0),
            ("Mortar Roughness", "NodeSocketFloat", 0.9, 0.0, 1.0),
            ("Block Width (m)", "NodeSocketFloat", 0.28, 0.05, 2.0),
            ("Block Height (m)", "NodeSocketFloat", 0.12, 0.03, 1.0),
            ("Mortar Size (m)", "NodeSocketFloat", 0.009, 0.001, 0.05),
        ],
    )
    vector = scaled_vector(group, inputs)

    layout = add_node(
        group,
        "ShaderNodeTexBrick",
        "FORM_BlockBond",
        "Running-bond masonry layout",
        (-740, 120),
        "FRAME_Macro",
    )
    layout.offset = 0.5
    layout.offset_frequency = 2
    layout.squash = 1.0
    layout.squash_frequency = 2
    group.links.new(vector, layout.inputs["Vector"])
    group.links.new(inputs.outputs["Stone Dark"], layout.inputs["Color1"])
    group.links.new(inputs.outputs["Stone Light"], layout.inputs["Color2"])
    group.links.new(inputs.outputs["Mortar Color"], layout.inputs["Mortar"])
    group.links.new(inputs.outputs["Block Width (m)"], layout.inputs["Brick Width"])
    group.links.new(inputs.outputs["Block Height (m)"], layout.inputs["Row Height"])
    group.links.new(inputs.outputs["Mortar Size (m)"], layout.inputs["Mortar Size"])

    mask_layout = add_node(
        group,
        "ShaderNodeTexBrick",
        "MASK_BlockVsMortar",
        "Reusable identity mask",
        (-740, -80),
        "FRAME_Macro",
    )
    mask_layout.offset = 0.5
    mask_layout.offset_frequency = 2
    mask_layout.inputs["Color1"].default_value = (1.0, 1.0, 1.0, 1.0)
    mask_layout.inputs["Color2"].default_value = (1.0, 1.0, 1.0, 1.0)
    mask_layout.inputs["Mortar"].default_value = (0.0, 0.0, 0.0, 1.0)
    group.links.new(vector, mask_layout.inputs["Vector"])
    group.links.new(inputs.outputs["Block Width (m)"], mask_layout.inputs["Brick Width"])
    group.links.new(inputs.outputs["Block Height (m)"], mask_layout.inputs["Row Height"])
    group.links.new(inputs.outputs["Mortar Size (m)"], mask_layout.inputs["Mortar Size"])

    identity = add_node(
        group,
        "ShaderNodeRGBToBW",
        "MASK_StoneIdentity",
        "Stone=1, mortar=0",
        (-520, -80),
        "FRAME_Macro",
    )
    group.links.new(mask_layout.outputs["Color"], identity.inputs["Color"])

    stone_noise = add_node(
        group,
        "ShaderNodeTexNoise",
        "DETAIL_StoneGrain",
        "Stone-specific mid-frequency grain",
        (-290, 90),
        "FRAME_Mid",
    )
    stone_noise.noise_dimensions = "3D"
    stone_noise.inputs["Scale"].default_value = 22.0
    stone_noise.inputs["Detail"].default_value = 4.0
    stone_noise.inputs["Roughness"].default_value = 0.66
    group.links.new(vector, stone_noise.inputs["Vector"])

    stone_amount = multiplied_amount(
        group,
        stone_noise.outputs["Fac"],
        inputs.outputs["Mid Amount"],
        "DETAIL_StoneGrainAmount",
        "Mid-frequency stone amount",
        (-90, 90),
        "FRAME_Mid",
    )

    pores = add_node(
        group,
        "ShaderNodeTexNoise",
        "MICRO_StonePores",
        "Fine mineral pores",
        (80, -80),
        "FRAME_Micro",
    )
    pores.noise_dimensions = "3D"
    pores.inputs["Scale"].default_value = 180.0
    pores.inputs["Detail"].default_value = 2.4
    pores.inputs["Roughness"].default_value = 0.72
    group.links.new(vector, pores.inputs["Vector"])

    pore_amount = multiplied_amount(
        group,
        pores.outputs["Fac"],
        inputs.outputs["Micro Amount"],
        "MICRO_StonePoreAmount",
        "Micro pore amount",
        (270, -80),
        "FRAME_Micro",
    )

    stone_tint = mix_rgb(
        group,
        "COLOR_StoneGrain",
        "Subtle stone value variation",
        (620, 180),
        "FRAME_Outputs",
        "MULTIPLY",
    )
    stone_tint.inputs["Fac"].default_value = 0.18
    group.links.new(layout.outputs["Color"], stone_tint.inputs[1])
    group.links.new(stone_amount, stone_tint.inputs[2])

    roughness = mix_rgb(
        group,
        "ROUGHNESS_StoneMortar",
        "Separate stone and mortar response",
        (760, 20),
        "FRAME_Outputs",
    )
    group.links.new(identity.outputs["Val"], roughness.inputs["Fac"])
    group.links.new(inputs.outputs["Mortar Roughness"], roughness.inputs[1])
    group.links.new(inputs.outputs["Stone Roughness"], roughness.inputs[2])

    height = mix_rgb(
        group,
        "HEIGHT_Masonry",
        "Recessed mortar plus stone pores",
        (710, -140),
        "FRAME_Outputs",
        "ADD",
    )
    height.inputs["Fac"].default_value = 0.2
    group.links.new(identity.outputs["Val"], height.inputs[1])
    group.links.new(pore_amount, height.inputs[2])

    wear = assemble_wear(group, inputs)
    assemble_outputs(
        group,
        inputs,
        outputs,
        stone_tint.outputs["Color"],
        roughness.outputs["Color"],
        0.0,
        height.outputs["Color"],
        wear,
        0.0015,
    )
    return group


def build_plaster_group() -> bpy.types.NodeTree:
    group, inputs, outputs = new_surface_group(
        f"{GROUP_PREFIX}Plaster_v1",
        "plaster",
        "Object/material space in meters; use authored masks for missing plaster or damp.",
        [
            ("Plaster Dark", "NodeSocketColor", (0.28, 0.23, 0.17, 1.0), None, None),
            ("Plaster Light", "NodeSocketColor", (0.72, 0.62, 0.46, 1.0), None, None),
            ("Roughness Min", "NodeSocketFloat", 0.66, 0.0, 1.0),
            ("Roughness Max", "NodeSocketFloat", 0.9, 0.0, 1.0),
            ("Trowel Frequency", "NodeSocketFloat", 7.0, 1.0, 80.0),
            ("Pore Frequency", "NodeSocketFloat", 180.0, 10.0, 800.0),
        ],
    )
    vector = scaled_vector(group, inputs)

    macro = add_node(
        group,
        "ShaderNodeTexNoise",
        "FORM_PlasterDrift",
        "Broad warm/cool plaster drift",
        (-760, 170),
        "FRAME_Macro",
    )
    macro.noise_dimensions = "3D"
    macro.inputs["Detail"].default_value = 3.5
    macro.inputs["Roughness"].default_value = 0.65
    group.links.new(vector, macro.inputs["Vector"])
    group.links.new(inputs.outputs["Trowel Frequency"], macro.inputs["Scale"])

    macro_amount = multiplied_amount(
        group,
        macro.outputs["Fac"],
        inputs.outputs["Macro Amount"],
        "FORM_PlasterAmount",
        "Macro plaster amount",
        (-560, 170),
        "FRAME_Macro",
    )

    trowel = add_node(
        group,
        "ShaderNodeTexNoise",
        "DETAIL_TrowelVariation",
        "Soft trowel and aggregate response",
        (-310, 70),
        "FRAME_Mid",
    )
    trowel.noise_dimensions = "3D"
    trowel.inputs["Scale"].default_value = 28.0
    trowel.inputs["Detail"].default_value = 2.0
    trowel.inputs["Roughness"].default_value = 0.6
    group.links.new(vector, trowel.inputs["Vector"])

    trowel_amount = multiplied_amount(
        group,
        trowel.outputs["Fac"],
        inputs.outputs["Mid Amount"],
        "DETAIL_TrowelAmount",
        "Mid-frequency trowel amount",
        (-100, 70),
        "FRAME_Mid",
    )

    pores = add_node(
        group,
        "ShaderNodeTexNoise",
        "MICRO_PlasterPores",
        "Fine plaster pores",
        (80, -80),
        "FRAME_Micro",
    )
    pores.noise_dimensions = "3D"
    pores.inputs["Detail"].default_value = 2.2
    pores.inputs["Roughness"].default_value = 0.75
    group.links.new(vector, pores.inputs["Vector"])
    group.links.new(inputs.outputs["Pore Frequency"], pores.inputs["Scale"])

    pore_amount = multiplied_amount(
        group,
        pores.outputs["Fac"],
        inputs.outputs["Micro Amount"],
        "MICRO_PlasterPoreAmount",
        "Micro pore amount",
        (270, -80),
        "FRAME_Micro",
    )

    color = mix_rgb(
        group,
        "COLOR_Plaster",
        "Broad plaster color drift",
        (700, 170),
        "FRAME_Outputs",
    )
    group.links.new(macro_amount, color.inputs["Fac"])
    group.links.new(inputs.outputs["Plaster Dark"], color.inputs[1])
    group.links.new(inputs.outputs["Plaster Light"], color.inputs[2])

    roughness = map_range(
        group,
        "ROUGHNESS_Plaster",
        "Trowel and pore roughness",
        (800, 20),
        "FRAME_Outputs",
        0.0,
        1.0,
    )
    group.links.new(trowel_amount, roughness.inputs["Value"])
    group.links.new(inputs.outputs["Roughness Min"], roughness.inputs["To Min"])
    group.links.new(inputs.outputs["Roughness Max"], roughness.inputs["To Max"])

    height = mix_rgb(
        group,
        "HEIGHT_Plaster",
        "Trowel variation plus pores",
        (700, -140),
        "FRAME_Outputs",
        "ADD",
    )
    height.inputs["Fac"].default_value = 0.18
    group.links.new(trowel_amount, height.inputs[1])
    group.links.new(pore_amount, height.inputs[2])

    wear = assemble_wear(group, inputs)
    assemble_outputs(
        group,
        inputs,
        outputs,
        color.outputs["Color"],
        roughness.outputs["Result"],
        0.0,
        height.outputs["Color"],
        wear,
        0.00035,
    )
    return group


def set_group_input(group_node: bpy.types.Node, name: str, value: Any) -> None:
    socket = group_node.inputs.get(name)
    if socket is None:
        raise RuntimeError(f"{group_node.node_tree.name}: missing input {name}")
    socket.default_value = value


def create_material(
    name: str,
    group: bpy.types.NodeTree,
    style_profile: str,
    preset: dict[str, Any],
) -> bpy.types.Material:
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    material.use_fake_user = True
    material["library_version"] = LIBRARY_VERSION
    material["style_profile"] = style_profile
    material["source_group"] = group.name
    material["coordinate_strategy"] = "object-local-or-explicit-material-space"
    material["engine_path"] = "bake approved PBR channels or recreate in target shader"
    nodes = material.node_tree.nodes
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.name = "OUTPUT_Material"
    output.location = (520, 0)

    shader = nodes.new("ShaderNodeBsdfPrincipled")
    shader.name = "SHADER_Principled"
    shader.label = "Single explicit Principled output"
    shader.location = (220, 0)

    group_node = nodes.new("ShaderNodeGroup")
    group_node.name = "SURFACE_ReusableGroup"
    group_node.label = group.name
    group_node.node_tree = group
    group_node.location = (-120, 0)

    coordinates = nodes.new("ShaderNodeTexCoord")
    coordinates.name = "COORD_ObjectOrMaterialSpace"
    coordinates.label = "Replace with UV/mapped vector when placement requires it"
    coordinates.location = (-430, 0)

    coordinate_output = coordinates.outputs["Object"]
    if group["material_family"] in {"cloth", "masonry"}:
        mapping = nodes.new("ShaderNodeMapping")
        mapping.name = "COORD_PreviewPlaneAlignment"
        mapping.label = "Preview only: local X/Z onto material X/Y"
        mapping.location = (-280, -170)
        mapping.vector_type = "POINT"
        mapping.inputs["Rotation"].default_value[0] = math.radians(90.0)
        material.node_tree.links.new(coordinate_output, mapping.inputs["Vector"])
        coordinate_output = mapping.outputs["Vector"]
    material.node_tree.links.new(coordinate_output, group_node.inputs["Vector"])
    material.node_tree.links.new(
        group_node.outputs["Base Color"],
        shader.inputs["Base Color"],
    )
    material.node_tree.links.new(
        group_node.outputs["Roughness"],
        shader.inputs["Roughness"],
    )
    material.node_tree.links.new(
        group_node.outputs["Metallic"],
        shader.inputs["Metallic"],
    )
    material.node_tree.links.new(
        group_node.outputs["Normal"],
        shader.inputs["Normal"],
    )
    material.node_tree.links.new(shader.outputs["BSDF"], output.inputs["Surface"])

    for input_name, value in preset.items():
        set_group_input(group_node, input_name, value)

    if group["material_family"] == "cloth":
        sheen = shader.inputs.get("Sheen Weight")
        if sheen:
            sheen.default_value = 0.18 if style_profile == "grounded-realism" else 0.08
    if group["material_family"] == "wood":
        coat = shader.inputs.get("Coat Weight")
        if coat:
            coat.default_value = 0.18 if preset.get("Finish Amount", 0.0) > 0.5 else 0.04
        coat_roughness = shader.inputs.get("Coat Roughness")
        if coat_roughness:
            coat_roughness.default_value = 0.18

    if hasattr(material, "asset_mark"):
        material.asset_mark()
        material.asset_data.description = (
            f"{style_profile} preset using {group.name}; "
            "procedural Blender source intended for controlled baking."
        )
    return material


def style_presets(groups: dict[str, bpy.types.NodeTree]) -> list[bpy.types.Material]:
    grounded = {
        "Scale (1/m)": 1.0,
        "Macro Amount": 0.72,
        "Mid Amount": 0.72,
        "Micro Amount": 0.42,
        "Normal Strength": 0.24,
        "Wear Amount": 0.0,
    }
    clean = {
        "Scale (1/m)": 1.0,
        "Macro Amount": 0.45,
        "Mid Amount": 0.24,
        "Micro Amount": 0.04,
        "Normal Strength": 0.08,
        "Wear Amount": 0.0,
    }

    definitions = [
        (
            "GP_Grounded_PolishedAsh",
            "wood",
            "grounded-realism",
            {
                **grounded,
                "Earlywood Color": (0.31, 0.15, 0.052, 1.0),
                "Latewood Color": (0.095, 0.032, 0.011, 1.0),
                "Roughness Min": 0.25,
                "Roughness Max": 0.44,
                "Finish Amount": 0.62,
            },
        ),
        (
            "GP_Grounded_ForgedIron",
            "forged",
            "grounded-realism",
            {
                **grounded,
                "Mid Amount": 0.62,
                "Micro Amount": 0.34,
                "Normal Strength": 0.28,
                "Dark Metal": (0.025, 0.032, 0.042, 1.0),
                "Light Metal": (0.18, 0.21, 0.24, 1.0),
                "Roughness Min": 0.45,
                "Roughness Max": 0.7,
            },
        ),
        (
            "GP_Grounded_PolishedSteel",
            "polished",
            "grounded-realism",
            {
                **grounded,
                "Macro Amount": 0.28,
                "Mid Amount": 0.42,
                "Micro Amount": 0.18,
                "Normal Strength": 0.12,
                "Metal Dark": (0.34, 0.38, 0.43, 1.0),
                "Metal Light": (0.66, 0.72, 0.78, 1.0),
                "Roughness Min": 0.13,
                "Roughness Max": 0.28,
                "Scratch Amount": 0.22,
            },
        ),
        (
            "GP_Grounded_OiledLeather",
            "leather",
            "grounded-realism",
            {
                **grounded,
                "Macro Amount": 0.58,
                "Mid Amount": 0.7,
                "Micro Amount": 0.38,
                "Normal Strength": 0.2,
                "Leather Dark": (0.025, 0.008, 0.003, 1.0),
                "Leather Light": (0.22, 0.065, 0.018, 1.0),
                "Roughness Min": 0.34,
                "Roughness Max": 0.61,
            },
        ),
        (
            "GP_Grounded_WovenWool",
            "cloth",
            "grounded-realism",
            {
                **grounded,
                "Macro Amount": 0.42,
                "Mid Amount": 0.66,
                "Micro Amount": 0.3,
                "Normal Strength": 0.14,
                "Cloth Dark": (0.026, 0.038, 0.06, 1.0),
                "Cloth Light": (0.12, 0.19, 0.30, 1.0),
                "Thread Frequency": 90.0,
            },
        ),
        (
            "GP_Grounded_LimestoneMasonry",
            "masonry",
            "grounded-realism",
            {
                **grounded,
                "Macro Amount": 0.45,
                "Mid Amount": 0.72,
                "Micro Amount": 0.42,
                "Normal Strength": 0.26,
                "Stone Dark": (0.16, 0.135, 0.095, 1.0),
                "Stone Light": (0.48, 0.42, 0.31, 1.0),
                "Mortar Color": (0.095, 0.085, 0.07, 1.0),
            },
        ),
        (
            "GP_Grounded_LimePlaster",
            "plaster",
            "grounded-realism",
            {
                **grounded,
                "Macro Amount": 0.5,
                "Mid Amount": 0.5,
                "Micro Amount": 0.26,
                "Normal Strength": 0.16,
            },
        ),
        (
            "GP_CleanStylized_Wood",
            "wood",
            "clean-stylized",
            {
                **clean,
                "Earlywood Color": (0.09, 0.025, 0.006, 1.0),
                "Latewood Color": (0.42, 0.12, 0.025, 1.0),
                "Roughness Min": 0.3,
                "Roughness Max": 0.44,
                "Finish Amount": 0.46,
            },
        ),
        (
            "GP_CleanStylized_Metal",
            "forged",
            "clean-stylized",
            {
                **clean,
                "Dark Metal": (0.055, 0.07, 0.09, 1.0),
                "Light Metal": (0.33, 0.39, 0.46, 1.0),
                "Roughness Min": 0.32,
                "Roughness Max": 0.48,
            },
        ),
        (
            "GP_CleanStylized_Leather",
            "leather",
            "clean-stylized",
            {
                **clean,
                "Leather Dark": (0.055, 0.012, 0.004, 1.0),
                "Leather Light": (0.30, 0.075, 0.02, 1.0),
                "Roughness Min": 0.42,
                "Roughness Max": 0.54,
            },
        ),
        (
            "GP_CleanStylized_Stone",
            "masonry",
            "clean-stylized",
            {
                **clean,
                "Stone Dark": (0.12, 0.11, 0.10, 1.0),
                "Stone Light": (0.42, 0.39, 0.34, 1.0),
                "Mortar Color": (0.07, 0.065, 0.06, 1.0),
                "Stone Roughness": 0.62,
                "Mortar Roughness": 0.78,
            },
        ),
    ]
    return [
        create_material(name, groups[group_key], profile, preset)
        for name, group_key, profile, preset in definitions
    ]


def look_at(obj: bpy.types.Object, target: Vector) -> None:
    direction = target - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def create_preview_scene(materials: list[bpy.types.Material]) -> None:
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.image_settings.color_mode = "RGBA"
    scene.view_settings.look = "AgX - Medium High Contrast"

    world = bpy.data.worlds.new("World_NeutralStudio")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (
        0.075,
        0.09,
        0.12,
        1.0,
    )
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.5
    scene.world = world

    collection = bpy.data.collections.new("MaterialLibrary_Preview")
    scene.collection.children.link(collection)

    for index, material in enumerate(materials[:7]):
        row = index // 4
        column = index % 4
        x = (column - 1.5) * 1.65
        z = 1.35 - row * 2.0
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0.0, z))
        swatch = bpy.context.object
        swatch.name = f"Swatch_{material.name}"
        swatch.dimensions = (1.25, 0.72, 1.25)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        swatch.data.materials.append(material)
        bevel = swatch.modifiers.new("Preview_RoundedEdges", "BEVEL")
        bevel.width = 0.14
        bevel.segments = 6
        bpy.ops.object.shade_smooth()
        for source_collection in list(swatch.users_collection):
            source_collection.objects.unlink(swatch)
        collection.objects.link(swatch)

    bpy.ops.mesh.primitive_plane_add(size=30.0, location=(0.0, 0.9, -1.5))
    floor = bpy.context.object
    floor.name = "Preview_Ground"
    for source_collection in list(floor.users_collection):
        source_collection.objects.unlink(floor)
    collection.objects.link(floor)

    floor_material = bpy.data.materials.new("Preview_NeutralFloor")
    floor_material.diffuse_color = (0.028, 0.034, 0.045, 1.0)
    floor_material.use_nodes = True
    floor_shader = floor_material.node_tree.nodes.get("Principled BSDF")
    floor_shader.inputs["Base Color"].default_value = (0.028, 0.034, 0.045, 1.0)
    floor_shader.inputs["Roughness"].default_value = 0.72
    floor.data.materials.append(floor_material)

    camera_data = bpy.data.cameras.new("Camera_MaterialLibrary")
    camera = bpy.data.objects.new("Camera_MaterialLibrary", camera_data)
    scene.collection.objects.link(camera)
    camera.location = (0.0, -9.8, 4.0)
    camera_data.lens = 58.0
    look_at(camera, Vector((0.0, 0.0, 0.15)))
    scene.camera = camera

    def area_light(
        name: str,
        location: tuple[float, float, float],
        energy: float,
        size: float,
        color: tuple[float, float, float],
    ) -> None:
        data = bpy.data.lights.new(name, "AREA")
        data.energy = energy
        data.shape = "DISK"
        data.size = size
        data.color = color
        obj = bpy.data.objects.new(name, data)
        scene.collection.objects.link(obj)
        obj.location = location
        look_at(obj, Vector((0.0, 0.0, 0.0)))

    area_light("Light_Key", (-4.0, -4.2, 6.5), 1150.0, 4.0, (1.0, 0.77, 0.58))
    area_light("Light_Fill", (4.8, -1.0, 3.0), 850.0, 3.5, (0.48, 0.68, 1.0))
    area_light("Light_Rim", (0.0, 3.5, 5.0), 1250.0, 3.0, (0.72, 0.82, 1.0))


def manifest_for(
    output: Path,
    preview: Path,
    groups: dict[str, bpy.types.NodeTree],
    materials: list[bpy.types.Material],
) -> dict[str, Any]:
    group_records = []
    for group in sorted(groups.values(), key=lambda item: item.name):
        sockets = []
        for item in group.interface.items_tree:
            if item.item_type != "SOCKET":
                continue
            record = {
                "name": item.name,
                "direction": item.in_out,
                "socket_type": item.socket_type,
            }
            if hasattr(item, "default_value"):
                value = item.default_value
                try:
                    record["default"] = list(value)
                except TypeError:
                    record["default"] = value
            sockets.append(record)
        group_records.append(
            {
                "name": group.name,
                "family": group["material_family"],
                "coordinate_contract": group["coordinate_contract"],
                "physical_scale_unit": group["physical_scale_unit"],
                "provenance": group["provenance"],
                "nodes": len(group.nodes),
                "links": len(group.links),
                "sockets": sockets,
            }
        )

    return {
        "schema_version": 1,
        "library_version": LIBRARY_VERSION,
        "blender_version": bpy.app.version_string,
        "minimum_blender": ".".join(str(value) for value in MINIMUM_BLENDER),
        "scope": "general-purpose procedural material source graphs",
        "license_note": (
            "Original graph implementation. Verify the destination repository's "
            "license before redistribution."
        ),
        "provenance": {
            "construction": "independently authored from general procedural-shading principles",
            "external_images": [],
            "copied_tutorial_graphs": [],
        },
        "style_profiles": {
            "grounded-realism": (
                "Realistic scale and material identity with restrained multi-frequency "
                "detail; performance-aware rather than hyperreal."
            ),
            "clean-stylized": (
                "Broad color/value blocks, reduced micro response, and sparse normals; "
                "select only when clean stylization is explicitly requested."
            ),
        },
        "output_blend": output.name,
        "preview": preview.name,
        "groups": group_records,
        "materials": [
            {
                "name": material.name,
                "style_profile": material["style_profile"],
                "source_group": material["source_group"],
                "engine_path": material["engine_path"],
            }
            for material in sorted(materials, key=lambda item: item.name)
        ],
        "usage": [
            "Append or link a preset material, or append a GP_Surface_* node group.",
            "Supply object/material coordinates in meters; align documented material axes.",
            "Replace Wear Mask with painted, geometric, or baked causal masks.",
            "Tune macro, mid, micro, and normal controls at intended viewing distance.",
            "Bake approved channels before game-engine export; Blender nodes do not transfer through FBX.",
        ],
    }


def main() -> None:
    if bpy.app.version < MINIMUM_BLENDER:
        raise RuntimeError(
            f"Blender {MINIMUM_BLENDER} or newer is required; found {bpy.app.version_string}"
        )
    args = parse_args()
    output = args.output.resolve()
    manifest = args.manifest.resolve()
    preview = args.preview.resolve()
    for path in (output, manifest, preview):
        path.parent.mkdir(parents=True, exist_ok=True)

    clear_file()
    groups = {
        "wood": build_wood_group(),
        "forged": build_forged_metal_group(),
        "polished": build_polished_metal_group(),
        "leather": build_leather_group(),
        "cloth": build_cloth_group(),
        "masonry": build_masonry_group(),
        "plaster": build_plaster_group(),
    }
    for group in groups.values():
        if hasattr(group, "asset_mark"):
            group.asset_mark()
            group.asset_data.description = (
                f"{group['material_family']} procedural surface signals; "
                f"{group['coordinate_contract']}"
            )

    materials = style_presets(groups)
    create_preview_scene(materials)
    bpy.context.scene.render.filepath = str(preview)
    bpy.ops.wm.save_as_mainfile(filepath=str(output), compress=True)
    bpy.ops.render.render(write_still=True)

    payload = manifest_for(output, preview, groups, materials)
    manifest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"MATERIAL_LIBRARY_BLEND={output}")
    print(f"MATERIAL_LIBRARY_MANIFEST={manifest}")
    print(f"MATERIAL_LIBRARY_PREVIEW={preview}")
    print(f"MATERIAL_LIBRARY_GROUPS={len(groups)}")
    print(f"MATERIAL_LIBRARY_PRESETS={len(materials)}")


if __name__ == "__main__":
    main()
