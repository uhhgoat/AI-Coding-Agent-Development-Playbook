---
name: obsidian-bases
description: Create, edit, or review Obsidian Bases files and related note metadata while preserving the workspace's current Bases schema, filters, formulas, views, and public-safe sample data. Use when a task touches `.base` files or Bases-backed note collections.
---

# Obsidian Bases

Use this skill when a task edits Obsidian Bases configuration or the note
metadata consumed by a Base. Bases syntax and plugin behavior can evolve, so
prefer the workspace's existing files and the installed Obsidian version over
memory.

## Inspect First

- Existing `.base` files and their schema shape.
- Notes included by the Base and the frontmatter keys it expects.
- Existing filters, formulas, properties, sort order, view definitions, and
  display names.
- Plugin version notes or vault documentation when present.

## Workflow

1. Preserve the current schema.
   - Parse the file with the format used in the vault.
   - Keep unknown keys and ordering when possible.
   - Do not rename properties or views unless the task explicitly requires it.

2. Update filters and formulas cautiously.
   - Check the expected value type for each property: text, list, number, date,
     checkbox, file reference, tag, or computed expression.
   - Quote strings and escape characters according to the current Bases syntax.
   - Prefer incremental changes over replacing a whole Base definition.

3. Keep notes and Bases aligned.
   - When adding a property to a Base, confirm the related notes either already
     contain it or have a clear default behavior.
   - When changing note frontmatter, preserve YAML validity and existing vault
     conventions.
   - Avoid creating duplicate property names that differ only by case, spacing,
     or punctuation.

4. Sanitize shared examples.
   - Replace private note titles, personal taxonomies, project names, contact
     details, source URLs, and folder paths with neutral examples.
   - Do not publish a Base that reveals a private vault structure.

## Verification

- The `.base` file parses in the format used by the vault.
- Referenced properties exist or have documented fallback behavior.
- Filters and formulas produce the intended note set in Obsidian.
- Related note frontmatter remains valid YAML.
- Public examples contain synthetic note names and metadata.