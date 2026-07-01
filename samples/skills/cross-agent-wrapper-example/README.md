# Cross-Agent Wrapper Example

This sample shows one canonical skill exposed through thin wrappers for multiple
coding-agent surfaces.

The canonical instructions live in:

- `.skills/example-review-checklist/SKILL.md`

The wrappers live in:

- `.codex/skills/example-review-checklist/SKILL.md`
- `.claude/skills/example-review-checklist/SKILL.md`
- `.github/instructions/example-review-checklist.instructions.md`

The wrapper files intentionally repeat only the trigger description and a pointer
to the canonical skill. Update the canonical file first, then regenerate or
refresh wrappers when the trigger text changes.

The scripts in `scripts/` are small examples for creating the same wrapper shape
for another skill name. They are not required by the playbook.