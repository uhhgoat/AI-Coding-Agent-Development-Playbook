---
name: skill-authoring
description: Create or update reusable agent skills, including canonical SKILL.md files, references, scripts, and thin wrappers for multiple coding-agent surfaces. Use when a recurring workflow should become durable project knowledge instead of remaining in chat history.
---

# Skill Authoring

Use this skill when turning a repeated workflow into a reusable agent skill.
Prefer concise, actionable instructions over transcripts, private examples, or
large policy dumps.

## Workflow

1. Confirm that a skill is warranted.
   - The workflow should be recurring, teachable, and stable enough to reuse.
   - One-off debugging notes, private project decisions, and volatile facts belong
     in project docs instead.
   - If the workflow is tool-specific, explain why a wrapper or command guide is
     insufficient.

2. Choose the canonical location.
   - Prefer one canonical `SKILL.md` under the project's chosen skills directory.
   - Use a kebab-case name with a short, specific trigger.
   - Put tool-specific wrappers under tool-specific directories only when the
     project uses those tools.

3. Write the skill body.
   - Add frontmatter with `name` and a trigger-oriented `description`.
   - Start with when to use the skill.
   - Include the smallest useful workflow, inspection checklist, guardrails,
     validation, and reporting expectations.
   - Put lengthy examples, schemas, or scripts in referenced files instead of the
     main `SKILL.md` when they would distract from the workflow.

4. Sanitize before sharing.
   - Remove personal names, company names, local machine paths, internal domains,
     credentials, customer data, private issue text, and unreleased project
     details.
   - Replace examples with neutral names such as `example-app`, `sample-service`,
     or `test-database`.
   - Make sure screenshots, fixtures, and sample outputs are synthetic or public.

5. Add wrappers and indexes.
   - Keep wrappers thin: metadata, trigger description, canonical-path pointer,
     and a warning not to duplicate the workflow.
   - Update the category README or skill catalog.
   - If a wrapper generator exists, use it and inspect the generated files.

6. Validate the skill.
   - Read the final files as an agent would discover them.
   - Check that relative links resolve.
   - Run markdown or schema checks when the repository provides them.
   - Inspect `git diff --check` and confirm only intended files changed.

## Reporting

State the skill name, canonical path, wrappers added, source material used, what
was sanitized, and any validation that was skipped.