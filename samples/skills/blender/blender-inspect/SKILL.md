---
name: blender-inspect
description: Inspect Blender `.blend` files without modifying them and produce structural reports, dependency checks, and deterministic previews. Use when identifying objects, collections, modifiers, base versus evaluated topology, materials, images, rigs, shape keys, source versions, or risks in local and third-party Blender files.
---

# Blender Inspect

Inspect through Blender itself. Do not parse the binary file format directly
and do not save the opened source.

## Workflow

1. Read [the shared Blender contract](../blender-validate-asset/references/shared-contract.md)
   and [report interpretation](references/report-interpretation.md).
2. Record the source path, byte length, modification time, and SHA-256.
3. Create an output directory under ignored `Temp/blender-audit/<task>/`.
4. Set `$blenderSkillRoot` to the copied `samples/skills/blender` directory,
   then run the structural inspector:

```powershell
& $blenderPath --factory-startup --disable-autoexec --background $sourceBlend `
  --python-exit-code 1 `
  --python "$blenderSkillRoot/shared/scripts/inspect_blend.py" `
  -- --output $reportPath
```

5. Confirm `BLEND_INSPECT_REPORT=<path>` and read the JSON.
6. Render a Workbench preview by default:

```powershell
& $blenderPath --factory-startup --disable-autoexec --background $sourceBlend `
  --python-exit-code 1 `
  --python "$blenderSkillRoot/shared/scripts/render_blend_preview.py" `
  -- --output $previewPath --engine workbench --auto-frame
```

7. Add filtered views with `--match`, `--parent`, or `--view` when the whole
   scene obscures the requested evidence.
8. Use Eevee only when material/packed-image inspection justifies its memory
   cost.
9. Recheck the source byte length, modification time, and hash.
10. Report structural facts separately from visual judgments and classify
    imported evidence as `pipeline-valid`, `reference-only`, or `unknown`.

## Required Output

- Absolute source path and original Blender save version.
- Report and preview paths.
- Base, object-summed, unique-data, and evaluated geometry counts.
- Modifier order/settings and missing dependency targets.
- Rig, vertex-group, shape-key, material, image, and linked-library findings.
- Risk flags and explicit limits on what statistics or previews prove.
- Confirmation that the source was unchanged.

## Guardrails

- Keep `--disable-autoexec` explicit for every third-party file.
- Keep `--python-exit-code 1`; Blender can otherwise print a traceback and
  still return success.
- Never add save, apply, export, or in-place repair steps to this skill.
- Treat AI-generated or third-party topology, UVs, material graphs, and
  textures as reference-only unless their authoring provenance explicitly
  permits a stronger claim. Blender-side modifiers, rigs, weights, shape
  keys, splits, transforms, and fitting remain valid inspection evidence.
