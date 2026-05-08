---
name: unity-input-system-settings
description: Maintain Unity Input System action assets and project settings, including `.inputactions` files, action maps, bindings, default input action configuration, active input handling, UI input modules, and serialized `InputActionReference` fields. Use when an agent edits input behavior or project-level Input System setup.
---

# Unity Input System Settings

Use this skill when a Unity project depends on the Input System package and a
task touches actions, bindings, serialized references, UI input modules, or
project settings.

## Inspect First

- `.inputactions` assets under `Assets/`.
- `.inputactions.meta` importer settings, especially wrapper generation and the
  asset GUID.
- Input System settings under `ProjectSettings/`, such as
  `InputSystem.settings.asset` when present.
- `ProjectSettings/EditorBuildSettings.asset` for Input System config objects or
  default action references when the Unity/Input System version stores them
  there.
- `ProjectSettings/ProjectSettings.asset` for the active input handler.
- `Packages/manifest.json` for `com.unity.inputsystem`.
- Prefabs, scene objects, UI modules, or scripts with serialized
  `InputActionReference` fields.

## Workflow

1. Inspect existing action maps, action names, bindings, control schemes, and
   runtime consumers before editing.
2. Prefer Unity's Input Actions editor for action and binding edits. Manual JSON
   edits must preserve valid JSON, unique IDs, composite binding structure,
   binding groups, and expected control types.
3. Preserve existing action IDs when possible. Serialized `InputActionReference`
   fields can break when an action is deleted and recreated instead of edited in
   place.
4. Keep the `.inputactions` asset GUID stable. If the asset is replaced, update
   default-action settings and all serialized references.
5. Confirm project-level default action settings point at the intended asset
   when the project uses a default actions asset.
6. Confirm the active input handler matches the runtime code path: legacy,
   Input System package, or both.
7. If wrapper generation changes, check generated code expectations, namespaces,
   and importer settings in the `.meta` file.
8. After action or binding changes, inspect prefabs and scenes that serialize
   `InputActionReference` fields. Unity may clear or stale links after action
   asset changes.
9. Validate gameplay and UI separately. Gameplay input can work while
   `InputSystemUIInputModule` navigation is broken, and the reverse can also
   happen.

## Editing Guardrails

- Do not add a second input actions asset unless the project explicitly wants
  multiple assets.
- Do not remove binding groups casually; keyboard, mouse, gamepad, XR, and UI
  paths may depend on them.
- Do not bulk-regenerate action and binding IDs to clean formatting.
- Do not mix legacy Input Manager changes with Input System changes unless the
  active input handler and runtime code require both.
- Treat project settings edits as repo-wide changes that affect every scene and
  developer machine.

## Verification

- The `.inputactions` file parses as JSON.
- Unity imports and opens the Input Actions asset without errors.
- Default project input actions still reference the intended asset when the
  project uses them.
- Serialized action references on prefabs, scenes, and UI modules resolve to
  existing actions.
- Changed bindings work in play mode for every device/control scheme touched.
- UI navigation and gameplay input are both checked when project settings changed.
