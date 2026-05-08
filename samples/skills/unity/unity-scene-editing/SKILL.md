---
name: unity-scene-editing
description: Edit Unity scene assets and scene-adjacent setup safely, including `.unity` files, build settings scene lists, cameras, tagged objects, prefab instances, spawn points, and runtime scene dependencies. Use when an agent must modify or review authored scene state without unnecessary YAML churn or broken runtime loading.
---

# Unity Scene Editing

Use this skill when a task touches authored Unity scene state or scene-adjacent
runtime setup.

## Inspect First

- Scene assets under `Assets/Scenes/` or the project's scene folder.
- `ProjectSettings/EditorBuildSettings.asset` for scenes loaded by build or
  runtime flows.
- Scene name constants, scene maps, addressable scene entries, or router assets used by code.
- Runtime loading code that chooses `LoadSceneMode.Single` or `LoadSceneMode.Additive`.
- Prefabs or spawner scripts that own repeated scene setup.

## Workflow

1. Read the code path that consumes the scene before editing scene YAML. Runtime
   requirements usually live in loaders, spawners, bootstraps, UI controllers, or
   gameplay state code.
2. Prefer Unity Editor edits for scene objects, component references, tags,
   layers, lighting, cameras, spawn points, and prefab instances.
3. Use manual YAML edits only for narrow, reviewable repairs. Identify the exact
   object/component block by `m_Name`, script GUID, fileID, or prefab instance
   linkage before editing.
4. Preserve `.meta` GUIDs, scene paths, and build settings entries. If a scene
   is renamed or moved, update every scene route that references it.
5. Keep reusable setup in prefabs when possible. Large scenes become safer when
   repeated actors, spawn markers, cameras, and UI roots are prefab-backed.
6. For additive loading, remember that bootstrap managers may persist while
   runtime scenes load and unload. Do not assume a scene is the only loaded scene
   unless the runtime says so.
7. Verify expected tagged objects and scene-local dependencies explicitly:
   `MainCamera`, `EventSystem`, UI document roots, spawn groups, lighting
   volumes, and manager placeholders.
8. After editing, inspect `git diff --stat` and the relevant YAML blocks. Large
   unrelated transform, lighting, import, or prefab-override churn usually means
   the edit should be revisited.

## Common Scene Patterns

- A startup scene may own persistent bootstrap objects while runtime scenes
  contain presentation and spawn points.
- Runtime scene routers often map stable keys to scene names. Update the map and
  constants together with scene file changes.
- Cameras may be scene-local, persistent, or auto-created. Check tags and
  bootstrap behavior before moving or deleting a camera.
- Spawner components should resolve scene-authored spawn groups without hardcoded
  instance IDs.

## Pitfalls

- Treating Unity recovery scenes as canonical scenes.
- Hand-editing serialized fileIDs without checking prefab or component references.
- Renaming a scene file without updating build settings and runtime routing.
- Accidentally committing broad YAML churn from opening/saving unrelated scenes.
- Assuming missing-reference warnings are harmless after script moves or namespace changes.

## Verification

- Open the scene in Unity and let import finish.
- Check Console for missing script, missing reference, or import warnings.
- Confirm the scene appears in build settings when runtime code loads it by name.
- Enter the relevant play-mode flow and confirm load/unload, camera, UI, and spawn behavior.
- Review the diff for only intended scene, prefab, and project-settings changes.
