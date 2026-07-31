# Shared Blender Automation Contract

Use these rules for every Blender skill in this project.

## Preserve the source

- Treat an existing `.blend` file as immutable unless the user explicitly names it as the output.
- Save generated work to a new file or a disposable fixture directory.
- Record the source path, file size, modification time, and SHA-256 before mutation.
- Confirm the source fingerprint is unchanged after read-only inspection or work on a copy.
- Never overwrite an imported, AI-generated, or third-party source asset
  during experimentation.

## Isolate write-capable Blender work

- When the repository uses concurrent worktrees or long-running branches,
  perform write-capable Blender work in a dedicated task branch/worktree
  separate from unrelated code work.
- Reuse an existing task-specific worktree when it remains valid. Otherwise,
  create one before authoring `.blend` stages, scripts, contracts, reports, or
  previews.
- Keep Blender artifacts and associated skill updates inside the selected
  repository workspace. Read-only source discovery may inspect other
  checkouts, but must not mutate them.
- Record repository-relative artifact paths and the branch in the final
  handoff. Mention an absolute worktree path only in a private/local handoff;
  never commit it to a reusable manifest or public example.

## Freeze visual intent

When appearance, style, or reference matching is part of acceptance, create a
versioned `style-contract.json` through `blender-define-asset-style` before
proportion-sensitive modeling or material authoring.

- Record reference fidelity, proportion strategy, construction plausibility,
  shape language, visual hierarchy, material realism, detail frequency, wear,
  and presentation independently.
- Keep the contract beside operation and material manifests.
- Preserve the contract with its matching stage. A changed contract is a new
  design decision, not silent correction.
- Treat subjective style approval as human-review evidence. Structural scripts
  may measure declared ratios and artifact presence, but cannot pass appeal or
  realism by themselves.

## Work in explicit stages

Use these artifact roles:

1. `SOURCE`: imported or hand-authored input that remains recoverable.
2. `CONTROLS`: cutters, curves, cages, drivers, Geometry Nodes controllers, or other construction inputs.
3. `OUTPUT`: evaluated modeling result intended for review.
4. `PREVIEW`: cameras, lights, turntables, and diagnostic helpers.
5. `EXPORT`: finalized duplicate prepared for interchange.

Keep stage collections separate when practical. Name important objects by role rather than Blender defaults.

## Classify evidence

- `pipeline-valid`: authored through the proposed workflow and suitable as evidence for that workflow.
- `reference-only`: useful for dimensions, modifiers, rigging, weights, shape keys, mesh splits, fitting, or export behavior, but not evidence of how its base mesh or textures were authored.
- `unknown`: origin or construction history cannot be established.

AI-generated or third-party character and apparel topology, UVs, texture
images, and material graphs are `reference-only` unless provenance establishes
otherwise. Their Blender-side modifiers, rigs, weights, shape keys,
transforms, fitting adjustments, and mesh splits may be pipeline evidence when
directly observed.

## Run safely

- Prefer Blender background mode for deterministic inspection, generation, validation, baking, and export.
- Include `--factory-startup`, `--disable-autoexec`, and `--python-exit-code 1` when inspecting untrusted or downloaded files.
- Prefer Blender RNA data APIs and `bmesh` over UI operators.
- Use `bpy.ops` only when its context requirements are understood and explicitly established.
- Make scripts idempotent where practical: rerunning should update or replace their own named outputs, not duplicate arbitrary objects.
- Use deterministic seeds, fixed camera views, explicit units, and explicit color management for comparison artifacts.

## Record provenance

For any write-capable workflow, capture:

- source and output file paths;
- Blender version;
- script or skill version when available;
- input parameters and random seeds;
- important object, collection, material, armature, and image names;
- warnings, failures, and intentionally skipped checks;
- generated preview, report, manifest, bake, and export paths.

## Stop instead of guessing

Stop and report when:

- the output target would overwrite a source unintentionally;
- Blender version compatibility is unknown and a save could make the file unusable in the expected version;
- a rigged edit would discard bones, vertex groups, shape keys, or armature relationships without authorization;
- an operation requires applying destructive modifiers but no recoverable pre-finalization copy exists;
- bake target, UV set, color space, normal convention, or cage strategy is ambiguous;
- export axis, scale, object selection, or Unity import expectations are not defined;
- validation finds a failure that affects the requested downstream operation.
