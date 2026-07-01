---
name: obsidian-markdown
description: Create, edit, or review Obsidian markdown notes while preserving frontmatter, wikilinks, embeds, callouts, tags, tasks, and vault-local conventions. Use for public-safe note templates, documentation vaults, or generalized Obsidian workflows.
---

# Obsidian Markdown

Use this skill when editing Obsidian-flavored markdown. Keep examples public-safe
and avoid copying private note contents into reusable samples.

## Inspect First

- Vault or folder instructions.
- Existing note naming, frontmatter keys, tags, aliases, and link style.
- Templates, snippets, plugins, and lint or formatting rules.
- Attachments folder conventions and whether embedded files are safe to share.

## Workflow

1. Preserve metadata.
   - Keep YAML frontmatter valid.
   - Preserve stable keys such as aliases, tags, created, updated, source, status,
     or publish flags unless the task asks to change them.
   - Do not invent dates, sources, or attribution.

2. Preserve Obsidian links.
   - Keep `[[wikilinks]]`, aliases, heading links, block links, and embeds in the
     style used by the vault.
   - When renaming notes, update backlinks or rely on Obsidian only when the user
     explicitly wants an app-driven rename.
   - Avoid changing markdown links to wikilinks, or the reverse, unless the vault
     convention requires it.

3. Edit note structure.
   - Use headings, lists, callouts, tasks, tables, and code fences consistently
     with nearby notes.
   - Keep tags meaningful and avoid creating duplicate tag variants.
   - Keep query blocks, dataview blocks, and transclusions syntactically intact.

4. Sanitize shared examples.
   - Replace personal journals, private project names, internal meeting notes,
     customer details, emails, local file paths, and sync provider paths with
     neutral sample content.
   - Do not include private attachment names or screenshots unless explicitly
     cleared.

## Verification

- Frontmatter parses as YAML.
- Markdown renders without broken fences, tables, or callouts.
- Links and embeds point to intended vault paths.
- Queries or plugin blocks remain fenced and unchanged unless intentionally
  edited.