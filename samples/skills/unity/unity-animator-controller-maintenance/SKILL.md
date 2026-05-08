---
name: unity-animator-controller-maintenance
description: Maintain Unity AnimatorController assets, state-name contracts, parameter/trigger schemas, generated or repaired controller graphs, and runtime animation crossfade maps. Use when an agent edits Animator states, transitions, blend trees, controller repair tools, or gameplay code that depends on stable Animator state names.
---

# Unity Animator Controller Maintenance

Use this skill when a Unity project has runtime or presentation code that
depends on a stable `AnimatorController` state graph.

## Inspect First

- The design or implementation document that defines required animation states
  and parameters.
- The target `.controller` asset and its `.meta` file.
- Runtime code that calls `Animator.Play`, `Animator.CrossFade`, `SetTrigger`,
  `SetBool`, `SetFloat`, or `Animator.HasState`.
- Editor scripts, menu items, generators, or repair utilities that modify the
  controller through Unity APIs.
- Prefabs and override controllers that reference the target controller.

## Workflow

1. Treat state names and parameter names as a contract when runtime code
   references them. Update the design table, controller graph, and runtime
   crossfade/trigger map together.
2. Prefer editing or regenerating `AnimatorController` structure through Unity
   editor APIs. Manual YAML edits to `.controller` files are fragile and should
   be narrow repairs only.
3. Preserve the target controller `.meta` GUID. Replacing the asset can break
   prefab, override controller, and scene references.
4. Preserve the root controller/state-machine identity during normal repairs. If
   a graph must be recreated, make that an explicit recovery path and close
   Animator windows first.
5. Reuse or reset existing blend tree and state subassets by stable name when
   possible instead of deleting and recreating every graph object.
6. Keep transitions presentation-focused. Runtime authority, gameplay rules,
   action timing, and state validation should stay in code or data models unless
   the local architecture intentionally places them in animation state.
7. Avoid shell edits to `.controller` or `.meta` files while Unity is open.
   Unity's asset database and Animator window can keep stale references after
   external serialized changes.
8. After structural changes, force validation through Unity: import, open the
   Animator window, inspect state count/default state, and run play-mode code
   paths that use `Animator.HasState` or crossfades.

## Common Recovery Patterns

- If the Animator window shows an empty or non-editable graph but code can load
  the controller, close Animator windows, run the project repair utility if one
  exists, reopen the controller, then validate state count and default state.
- If Unity reports asset database timestamp or import-cache errors after
  external edits, close Unity, clear only the relevant Unity cache files
  according to the project's command guide, reopen, and let import finish.
- If a generated controller drifts, update the generator or repair utility
  first. Treat the generated `.controller` asset as output unless a one-off
  serialized repair is explicitly safer.

## Guardrails

- Do not rename runtime-facing states casually; use clips, blend trees, override
  controllers, or animation data for visual variation.
- Do not remove legacy/fallback states until all runtime code and prefabs no
  longer reference them.
- Do not copy a temporary controller YAML file over the target controller while
  Unity or the Animator window is open.
- Do not churn generated controller YAML only to satisfy whitespace or formatting
  preferences.
- Document newly discovered Animator failure modes in the skill or the project's
  command/architecture docs.

## Verification

- Unity imports the controller without Console errors.
- Animator window shows the expected layer, default state, state count, and
  transitions.
- Runtime code can find every required state and parameter.
- Prefabs still reference the intended controller or override controller.
- Play mode exercises at least one default/idle path and one triggered
  transition path affected by the change.
- The diff is limited to intended generator, controller, prefab, or documentation
  changes.
