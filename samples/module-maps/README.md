# Module Map Registry

This is a project-neutral sample for `docs/module-maps/README.md`. Replace the
placeholder rows with the target repository's real branches, modules, paths,
and baselines.

Read this registry after the repository instructions. Load only the smallest
applicable map before inspecting authoritative source. Related-map links are
routing options, not a request to preload the entire catalog.

## Branch Coverage

| Branch or integration target | Status | Verified baseline | Notes |
| --- | --- | --- | --- |
| `<default-branch>` | `partial` | `<commit-or-date>` | Adopted maps are listed below; remaining modules are explicit. |
| `<feature-branch>` | `needs-reconciliation` | `<common-baseline>` | Recheck destination instructions and reconcile after integration. |

Allowed branch statuses: `unmapped`, `partial`, `mapped`,
`needs-reconciliation`, `retired`.

## Module Coverage

| Module | Scope | Map | Status | Verified baseline | Related maps |
| --- | --- | --- | --- | --- | --- |
| Orders example | `src/orders/` | [example-module.md](example-module.md) | `mapped` | `<commit-or-date>` | Load related maps only if the task crosses declared boundaries. |
| Unmapped area | `src/legacy/` | — | `unmapped` | — | Inspect source directly and create a map only if recurring work justifies it. |

Allowed module statuses: `unmapped`, `draft`, `mapped`, `needs-review`,
`retired`.

## Loading Rule

1. Select the row whose scope contains the task.
2. Load that map before broad source discovery.
3. Open its named sources of truth.
4. Expand to another map only when a crossed boundary or source evidence
   requires it.
5. Record files discovered outside the map so the map can be corrected.

## Maintenance Rule

Update this registry and affected maps in the same change when mapped nodes,
relationships, boundaries, coverage, or verification baselines change.

During a merge, rebase, or cherry-pick, inspect the destination branch's
instructions and map set before integration. Reconcile maps against the final
source; never resolve derived map conflicts by blindly choosing one side.
