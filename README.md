# AI Coding Agent Development Playbook

A practical toolkit for AI coding-agent workflows: a reusable development
playbook, sample skills, sample agent instructions, and adaptation guides for
making repositories easier for humans and agents to understand, coordinate,
resume, and safely maintain.

## Contents

- `ai-agent-development-workflow-playbook.md` - the reusable workflow playbook.
- `guides/` - guides for adapting the playbook and sharing skills across
  coding agents.
- `samples/agent-instructions/` - root and module-level `AGENTS.md` samples.
- `samples/skills/` - sample skills split by domain, including general coding,
  documentation, Unity, Obsidian, and robotics categories.

## How To Use This With An Agent

Attach `ai-agent-development-workflow-playbook.md` or point your agent at this
whole repository, then use a prompt like this:

```text
Please read the attached AI Coding Agent Development Workflow Playbook and this
sample repository. Then adapt the workflow to my project.

First inspect my repository. Identify the project type, language/toolchain,
frameworks, build/test commands, protected/generated/vendor folders, existing
docs, and any collaboration risks.

Then propose and implement a project-specific agent workflow:
- create or update AGENTS.md as the canonical standing-rules file
- create docs/current-status.md, docs/command-guide.md, and
  docs/architecture-baseline.md, or map those roles to existing project docs
- create docs/active-work.md, or an equivalent ownership tracker, if multiple
  people or agents may work at once
- recommend project skills only for recurring tasks
- if useful, add one canonical skill and thin wrappers for Codex, Claude, and
  GitHub Copilot, following guides/sharing-skills-across-coding-agents.md

Treat the playbook as a set of roles and patterns, not a rigid folder template.
Rename, combine, or skip pieces when my project already has an equivalent place
for that information. Explain any adaptation you make.

If this is a Unity project, use the Unity samples only as patterns. Do not copy
any sample unless the project actually uses that architecture. Keep changes
scoped, preserve existing conventions, and tell me what you changed and what
still needs review.
```

For a first pass, ask the agent to draft the docs and skill recommendations
before making sweeping changes. Once the structure looks right, have it create
or update the files directly.

## License

MIT. See [LICENSE](LICENSE). The playbook, guides, and samples are intended to
be copied and adapted for project-specific agent workflows.
