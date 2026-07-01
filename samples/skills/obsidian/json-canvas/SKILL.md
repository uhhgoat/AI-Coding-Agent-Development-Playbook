---
name: json-canvas
description: Create, edit, or validate Obsidian JSON Canvas files while preserving node IDs, positions, edges, groups, file references, and valid JSON. Use when a task touches `.canvas` files or portable JSON Canvas diagrams.
---

# JSON Canvas

Use this skill when editing `.canvas` files that follow the JSON Canvas format.
Treat the canvas as structured data, not as free-form text.

## Inspect First

- Existing `nodes` and `edges` arrays.
- Node IDs, types, positions, sizes, colors, labels, and file references.
- Edge IDs, endpoints, sides, labels, and colors.
- Nearby markdown notes or attachments referenced by file nodes.

## Workflow

1. Parse before editing.
   - Load the file as JSON and preserve valid object structure.
   - Keep unknown fields unless there is a clear reason to remove them.
   - Preserve stable IDs for existing nodes and edges.

2. Add or update nodes deliberately.
   - Use unique IDs for new nodes and edges.
   - Choose the appropriate node type: text, file, link, or group.
   - Place nodes with explicit `x`, `y`, `width`, and `height` values so the
     canvas opens in a readable layout.
   - Keep file paths relative to the vault when that is the existing convention.

3. Maintain edges.
   - Ensure every edge endpoint references an existing node.
   - Preserve side hints when they make the layout readable.
   - Do not leave orphaned edges after deleting or renaming nodes.

4. Keep content public-safe.
   - Do not copy private note titles, internal roadmaps, customer names, local
     folders, or personal knowledge graphs into reusable examples.
   - Use neutral node titles and synthetic relationships for shared samples.

## Verification

- The canvas parses as JSON.
- Every node and edge ID is unique.
- Every edge endpoint references an existing node.
- File nodes point to intended vault-relative paths.
- The layout is readable and does not stack new nodes on top of existing ones.