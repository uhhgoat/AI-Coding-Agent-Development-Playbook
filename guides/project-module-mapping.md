# Project Module Mapping

Use project module maps to reduce repeated repository discovery without treating
generated or hand-maintained documentation as a substitute for source code.
Maps are a project-neutral navigation layer: they identify the smallest useful
source set, explain important relationships, and make gaps visible.

## When To Add Maps

Mapping is useful when a project has several modules, non-obvious runtime flows,
cross-cutting configuration, or repeated agent work that otherwise requires the
same broad searches. A small repository with obvious boundaries may need only an
architecture document and no map layer.

Choose one canonical map location. This guide uses:

```text
docs/module-maps/
  README.md
  <module>.md
```

The registry and maps are version-controlled project documentation. Source,
configuration, schemas, and authored assets remain authoritative.

## Registry And Coverage Status

`docs/module-maps/README.md` is the entry point. It should record both branch
coverage and module coverage so an agent can distinguish a mapped area from an
area that has never been examined.

Recommended branch statuses:

| Status | Meaning |
| --- | --- |
| `unmapped` | The branch has not adopted or been checked against the map set. |
| `partial` | Some relevant modules are mapped, but known coverage is incomplete. |
| `mapped` | Relevant maps were checked against the recorded branch baseline. |
| `needs-reconciliation` | Code, instructions, or maps changed across branches and have not been reconciled. |
| `retired` | The branch is no longer an active integration target. |

Recommended module statuses:

| Status | Meaning |
| --- | --- |
| `unmapped` | No reliable module map exists. |
| `draft` | A map exists, but important paths or relationships remain unverified. |
| `mapped` | The declared scope and relationships were checked against the recorded baseline. |
| `needs-review` | The map may be stale because relevant implementation or integration state changed. |
| `retired` | The module no longer exists or the map is kept only for history. |

Record a commit, tag, or dated revision as the verification baseline. Do not
label a branch or module `mapped` without a traceable baseline.

## Scoped Map Loading

Map loading should save context, not consume it.

1. Read the repository instructions and the map registry.
2. Select the smallest map whose scope contains the requested change.
3. Read that map before broad source discovery.
4. Open the map's sources of truth and the specific files required by the
   affected relationships.
5. Load another map only when the task crosses a declared boundary, source
   evidence reveals an undeclared dependency, or validation requires the other
   side of a contract.
6. Record any map expansion and why it was necessary.

A link to another map is a routing choice, not an instruction to load every
related map. Do not preload the whole map catalog. For a simple isolated edit,
the applicable map plus a few authoritative files should be enough.

Maps guide discovery; they do not authorize blind edits. Verify relevant map
claims against the current source before changing behavior.

## Required Map Shape

Keep each map concise and evidence-oriented:

- **Metadata**: scope, status, verified baseline, owner or maintainer if useful.
- **Purpose and boundaries**: what the module owns and explicitly does not own.
- **Sources of truth**: the files, schemas, configuration, or assets that define
  behavior.
- **Nodes**: important classes, interfaces, services, data types, scripts,
  assets, or configuration entries and their responsibilities.
- **Connections**: directed semantic relationships between nodes.
- **Runtime or data flows**: only the few sequences needed to reason about
  behavior.
- **Change impact and validation**: what normally changes together and how to
  verify it.
- **Known gaps**: missing coverage or uncertain relationships.

Do not turn a map into a full file inventory. Include a node when its role or
connection materially helps an agent choose files, reason about behavior, or
estimate blast radius.

## Relationship Rule

A connection must explain logic, not merely name two related classes. Use a
compact directed form:

```text
<source> -> <target> | <kind> | <concise behavior, ownership, timing, or constraint>
```

Useful relationship kinds include `calls`, `owns`, `reads`, `writes`,
`publishes`, `subscribes`, `constructs`, `configures`, `serializes`,
`implements`, and `validates`.

Prefer statements such as:

```text
OrderService -> OrderRepository | writes | persists an order only after payment authorization succeeds
```

Avoid statements such as:

```text
OrderService -> OrderRepository | related
```

When useful, cite the defining symbol or file beside the connection. Record
direction, timing, ownership, data shape, and failure constraints only to the
degree they affect reasoning.

## Maintenance Rule

Update affected maps in the same change whenever implementation adds, removes,
or changes a mapped node or connection. Examples include new classes,
interfaces, pointers or references, calls, events, ownership, serialization
paths, configuration keys, asset references, lifecycle ordering, or module
boundaries.

When a change exposes a missing relationship:

1. correct the map rather than working around it silently
2. update the module status and verification baseline
3. add a known gap if full verification is not possible
4. update the registry when coverage or map routing changes

Map maintenance belongs in the definition of done, not in a later cleanup
task.

## Branch And Integration Reconciliation

Before merging, rebasing, or cherry-picking into a destination branch:

1. inspect the destination branch's current agent instructions, skill pointers,
   map registry, and applicable maps
2. compare them with the source branch before resolving conflicts
3. integrate the implementation
4. reconcile the combined map set against the integrated source
5. preserve relevant maps that exist on only one side unless the mapped module
   was intentionally removed
6. update branch/module statuses and the verified baseline

Do not resolve map conflicts by accepting `ours` or `theirs` wholesale. Maps are
derived from the integrated result and must be rebuilt or edited to describe
that result. Destination-branch instructions govern the final branch, subject
to any higher-priority instructions. If reconciliation cannot be completed,
mark the affected branch `needs-reconciliation` and modules `needs-review`
instead of claiming mapped coverage.

This check is required even when the code merge is conflict-free. An instruction
or map can become stale through a clean textual merge.

## Validation And Utility Trace

Validate a map change with the narrowest useful checks:

- every listed source path exists or is explicitly marked planned/external
- every cross-map link resolves
- important connections are supported by current source evidence
- module and branch statuses match the recorded baseline
- the diff contains map updates for changed mapped relationships
- no project-specific fact was copied into a project-neutral reusable skill

To measure whether maps are useful, record a lightweight context trace during a
representative task:

- initial maps loaded
- source files opened because the map named them
- additional maps loaded and the boundary that required each one
- source files discovered outside the map
- searches needed to repair or extend the map
- stale or missing relationships found

A useful map reduces broad discovery while still leading the agent to the
authoritative evidence. A map that causes every map to be loaded, hides needed
source files, or repeatedly misses connections should be simplified or
corrected.

See [the sample registry](../samples/module-maps/README.md) and
[sample module map](../samples/module-maps/example-module.md) for copyable
starting points.
