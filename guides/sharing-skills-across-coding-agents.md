# Sharing Skills Across Coding Agents

This guide shows the pattern for keeping one canonical skill body available to
multiple coding agents.

## Core Idea

Keep the real instructions in one canonical file, then create thin wrappers for
each tool.

Example layout:

```text
.skills/
  <skill-name>/
    SKILL.md
.codex/
  skills/
    <skill-name>/
      SKILL.md
      agents/
        openai.yaml
.claude/
  skills/
    <skill-name>/
      SKILL.md
.github/
  instructions/
    <skill-name>.instructions.md
```

The wrappers should contain only:

- tool-specific frontmatter or metadata
- a short description
- a link to the canonical skill
- a warning not to duplicate or edit skill content in the wrapper

## Why This Helps

- Every agent receives the same durable recipe.
- Skill edits happen once.
- Tool-specific discovery mechanisms still work.
- Teams can change tools without losing project knowledge.
- Projects can skip wrappers for tools they do not use.

## Wrapper Checklist

- The canonical skill name and directory match.
- Each wrapper points at the canonical path.
- Each wrapper repeats only the short trigger description.
- If a trigger description changes, all wrappers are regenerated or updated.
- Tool-specific fields, such as `applyTo` globs or display metadata, stay in
  the wrapper.
