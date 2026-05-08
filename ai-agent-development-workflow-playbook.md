# AI Agent Development Workflow Playbook

Author and curator: Matyas Gosztonyi  
License: MIT. See `LICENSE` in this repository.  
SPDX-License-Identifier: MIT  
Status: Public reusable playbook and adaptation guide.  

This playbook was authored and curated by Matyas Gosztonyi with AI-assisted
drafting and revision. The guidance is intended to be copied, adapted, and
specialized for project-specific agent instructions, skills, workflow docs, and
human/AI collaboration practices.

## Purpose

This guide describes a reusable development workflow for AI coding agents and
human developers working in the same repository. It is project-neutral by
design. An agent should be able to read this file and create its own
project-specific `AGENTS.md`, skill files, status documents, command guides,
architecture documents, feature plans, feature documentation, ownership records,
and handoff processes that follow this workflow.

The workflow is built around one central idea: the repository should contain
enough living context that a future agent or developer can recover the current
state, avoid stepping on another person's work, make a safe decision, implement
a scoped change, verify it, and update the record without relying on chat
history.

## Core Model

Use a layered documentation and instruction system:

1. **Standing instructions** define the rules that should always apply.
2. **Repo-local agent skills** summarize project framing and workflow triggers.
3. **Current-status documentation** records the global milestone, latest
   verified result, risks, ownership notes, and next intended move.
4. **Command documentation** records every implemented executable workflow.
5. **Architecture documentation** records durable system boundaries and
   direction.
6. **Feature and module plan files** record evolving implementation plans for
   active or complex work areas.
7. **Feature documentation** records deep technical designs for specific areas.
8. **Signed progress logs** record who changed what, when, why, and what
   remains.
9. **Logs and generated artifacts** preserve evidence from validation runs.
10. **Final handoffs** summarize what changed, what was verified, and what risk
    remains.

Each layer has a different job. Do not collapse all context into one long file.
The workflow works because agents can quickly read the right level of detail
for the task at hand.

## Repository Instruction Files

### Root Agent Instructions

Create a root-level instruction file, usually `AGENTS.md`, that defines the
project's standing rules. This file is the most important durable instruction
source inside the repo.

It should include:

- project scope and non-goals
- directories the agent may edit freely
- directories that are vendored, generated, external, protected, or owned by
  another team
- preferred implementation languages and toolchains
- architecture rules and dependency boundaries
- safety rules for any high-risk behavior
- multi-developer and multi-agent coordination rules
- documentation update rules
- testing expectations
- code style preferences
- decision biases for ambiguous tradeoffs

Keep `AGENTS.md` specific enough to guide implementation, but do not make it a
running progress log. Progress belongs in status files, feature plans, and
signed update logs.

### Repo-Local Skill

Create a compact skill file for the project, for example:

```text
.codex/skills/<project-slug>/SKILL.md
```

The skill should be shorter than `AGENTS.md`. It exists so an AI agent can load
project framing only when the task matches the project domain.

The skill should include:

- when to use the skill
- the most important architecture rules
- the current implementation direction
- protected directories
- documentation files that must stay synchronized
- coordination rules for multiple people or agents
- the safest next-development priorities
- current known constraints future agents must not forget

The skill should not become a duplicate of every project document. It should be
a high-signal index and reminder.

### Runtime System Instructions

An AI agent may also receive runtime or platform-level instructions outside the
repository. The agent must obey those higher-priority instructions, but should
not copy hidden or private instructions verbatim into repository files. When a
workflow rule is useful and allowed to preserve, translate it into a
project-neutral practice.

Example:

- private runtime rule: use safe file editing tools
- repository-level expression: prefer reviewable, scoped patches and avoid
  destructive commands unless explicitly requested

## Living Documentation Set

Every project using this workflow should maintain at least these files:

```text
AGENTS.md
README.md
docs/
  current-status.md
  command-guide.md
  architecture-baseline.md
```

Larger, longer-running, or higher-risk projects should add:

```text
docs/
  active-work.md
  collaboration-log.md
  safety-plan.md
  deployment-plan.md
  <feature-or-module>-plan.md
  <feature-or-module>-development-plan.md
  feature-<area>-architecture.md
  troubleshooting.md
  decision-log.md
configs/
modules/
apps/
tools/
tests/
logs/
exports/
```

Generated `logs/` and `exports/` are often ignored by version control, but the
important findings from them must be summarized in tracked documentation.

## Multi-Developer And Multi-Agent Coordination

When more than one human, agent, branch, terminal session, or background worker
may touch the same repository, the docs must answer three questions:

1. Who is working on what?
2. What state did they leave behind?
3. What can another agent safely continue without guessing?

Use actor stamps, active ownership records, append-only progress notes, and
explicit handoffs.

### Actor Stamps

Every durable progress update should include an actor stamp. This applies to
updates in `docs/current-status.md`, feature/module plan files, active work
files, collaboration logs, safety plans, and important command-validation
notes.

Use a simple format:

```markdown
### Update: <short title>

- Actor: <human name, agent name, or both>
- Role: <human developer | AI agent | reviewer | operator | worker agent>
- Timestamp: <YYYY-MM-DD HH:MM TZ>
- Branch/session: <branch, ticket, PR, terminal, or chat/session id if known>
- Scope: <module, feature, command, doc, or subsystem>
- Status: <planned | in progress | blocked | validated | completed | handed off>
- Files/areas touched: <paths or areas>
- Summary: <what changed or what was learned>
- Verification: <commands, tests, logs, or not run>
- Next intended move: <what should happen next>
```

The stamp does not need to be ceremonial. It exists so another agent can see
provenance quickly.

### Active Ownership

Every feature or module plan with active work should include an ownership
section near the top:

```markdown
## Active Ownership

| Area | Owner | Started | Last Updated | Status | Expected Files | Handoff |
| --- | --- | --- | --- | --- | --- | --- |
| <area> | <actor> | <timestamp> | <timestamp> | in progress | <paths> | <note> |
```

Use ownership for coordination, not gatekeeping. It should prevent accidental
overlap, but it should not permanently block progress.

Status values should be explicit:

- `planned`
- `in progress`
- `blocked`
- `ready for review`
- `validated`
- `completed`
- `paused`
- `handed off`
- `stale`

### Stale Ownership

Ownership claims should expire or be clarified. Otherwise old "in progress"
notes become misleading.

Each project should define a stale-work policy in `AGENTS.md`. A generic rule:

- If an ownership record has no update for 24 hours, another agent may inspect
  but should avoid writing the same files without checking branch state.
- If it has no update for 72 hours and no external issue tracker says
  otherwise, mark it `stale` and add a signed note before taking over.
- For high-risk, production, hardware, legal, medical, billing, credentials, or
  safety work, do not take over silently. Add a signed note and seek explicit
  human confirmation unless the task is an emergency fix.

Example stale takeover note:

```markdown
### Update: Taking Over Stale Work

- Actor: <agent/user>
- Timestamp: <YYYY-MM-DD HH:MM TZ>
- Scope: <area>
- Previous owner: <actor>
- Reason: ownership entry stale since <timestamp>
- Files inspected: <paths>
- Takeover plan: <bounded next step>
- Safety note: <risk assessment>
```

### Append-Only Progress Logs

Important progress should be append-only. Agents may update checklists and
status fields, but meaningful discoveries, validations, failed attempts, and
handoffs should be added as dated notes rather than silently overwritten.

Use append-only notes for:

- validated commands
- failed live tests
- environment changes
- safety decisions
- deployment changes
- API discoveries
- ownership transfers
- blocked states
- handoffs between people or agents

This makes the repository resilient to context loss and honest about how the
current plan emerged.

### Active Work File

For busy repositories, add:

```text
docs/active-work.md
```

This file is a lightweight index of active ownership across the whole repo. It
should point to feature/module plan files rather than duplicating them.

Template:

```markdown
# Active Work

This file indexes active work so humans and agents can avoid collisions. Update
it when starting, pausing, handing off, or completing work that touches shared
areas.

| Area | Owner | Status | Branch/Session | Plan File | Expected Files | Last Updated |
| --- | --- | --- | --- | --- | --- | --- |
| <area> | <actor> | in progress | <branch/session> | <doc path> | <paths> | <timestamp> |

## Coordination Notes

- <signed note>
```

Use `docs/active-work.md` when there are multiple simultaneous work streams.
For small projects, ownership sections inside feature plans may be enough.

### Collaboration Log

For repositories with frequent handoffs, background agents, multiple branches,
or several human collaborators, add:

```text
docs/collaboration-log.md
```

This file is an append-only coordination record. It should capture meaningful
handoffs, ownership transfers, blocked states, environment changes, major failed
attempts, and cross-cutting decisions that affect more than one feature plan.

Use `docs/collaboration-log.md` for events that are broader than one
feature/module plan. Keep local implementation details in the relevant plan
file, then link to that plan from the collaboration log.

Each entry should use the same actor stamp format as other durable progress
updates.

### Conflict Hygiene

Before editing, every agent should check:

```bash
git status --short
```

Then inspect:

- `docs/current-status.md`
- `docs/active-work.md`, if present
- relevant feature/module plan files
- recent signed progress updates
- current branch or issue tracker, if available

Rules:

- Assume uncommitted changes may belong to another human or agent.
- Do not revert changes you did not make unless explicitly requested.
- If unrelated files are dirty, ignore them.
- If a file you need is dirty, read it carefully and work with the current
  content.
- If another active owner lists the same files, do not edit them unless the
  task is explicitly a handoff, review, merge, or emergency fix.
- If a conflict is likely, add a signed note and ask for coordination.

### Branch And File Ownership

Prefer separate branches or disjoint write scopes when multiple developers or
agents work in parallel.

For parallel work:

- define file ownership before implementation
- keep generated files out of shared commits unless needed
- avoid broad formatting changes
- avoid cross-cutting refactors during parallel feature work
- communicate expected touched files in the active ownership block
- update the handoff note when the expected file set changes

For AI sub-agents, assign disjoint write scopes. A worker should know that other
people or agents may be changing the repo and should not revert their edits.

### Handoff Notes

Whenever pausing work, switching tasks, finishing a phase, or handing a feature
to another agent, add a handoff note.

```markdown
### Handoff: <area>

- Actor: <agent/user>
- Timestamp: <YYYY-MM-DD HH:MM TZ>
- Status: <paused | blocked | ready for review | completed>
- Current branch/session: <branch/session>
- What changed: <summary>
- Verified: <commands or artifacts>
- Not verified: <what remains>
- Files touched: <paths>
- Open risks: <risks>
- Next step: <specific next action>
- Safe takeover notes: <what another agent should inspect first>
```

Handoffs are especially important before context compaction, task switching,
long pauses, or when multiple agents are active.

## Current Status Document

`docs/current-status.md` is the global recovery document. A future agent should
read it first when resuming work.

It should answer:

- What phase is the project in?
- What is the immediate goal?
- What active work streams exist?
- Who is currently working on what?
- What was the latest verified result?
- What command, test, or workflow is currently the best known path?
- What risks are known right now?
- What clues, failed attempts, or reverse-engineering notes matter?
- What should the next agent do next?
- What should the next agent avoid doing?

Recommended structure:

````markdown
# Current Status

This document is the short-running milestone log for the workspace. Future
agents should check this file first for the current working state, latest
validated result, active ownership, and next intended move.

## Current Phase

State the active phase in one or two paragraphs. Include the milestone name,
what is currently true, and any important constraint that affects the next move.

## Active Work Summary

| Area | Owner | Status | Plan File | Last Updated |
| --- | --- | --- | --- | --- |
| <area> | <actor> | <status> | <path> | <timestamp> |

## Immediate Goal

1. List the current concrete goal.
2. List the next concrete subgoal.
3. List any blocked or deferred item.

## Latest Verified Result

Describe the most recent validation. Include exact commands, dates when useful,
paths to artifacts, observable output, and the interpretation.

- Actor:
- Timestamp:
- Command or workflow:
- Environment:
- Output:
- Artifacts:
- Interpretation:
- Remaining uncertainty:

## Current Best Workflow

Provide the best known command sequence or procedure. Prefer copy-pasteable
commands and note any placeholders the operator must choose.

```bash
<commands>
```

## Current Risks

List active risks, especially safety, data loss, deployment, dependency,
ownership, coordination, or unknown-state risks.

## Current Clues

Record relevant observations that are not yet formalized into architecture or
code.

## Next Intended Move

Give the next agent a concrete starting point.

1. <Specific next action.>
2. <Fallback if it fails.>

## Signed Progress Updates

### Update: <short title>

- Actor:
- Timestamp:
- Scope:
- Status:
- Summary:
- Verification:
- Next intended move:
````

Update this file whenever:

- the active milestone changes
- active ownership changes
- a live validation succeeds or fails in a meaningful way
- a prior assumption is corrected
- the next intended move changes
- a risk becomes known
- an important artifact is produced

Do not use `current-status.md` as a full changelog. It should remain a concise
operational state document.

## Command Guide

`docs/command-guide.md` is the executable reference. Every implemented CLI,
launch file, service entry point, test workflow, safety guard, and validated
operator procedure should be recorded here.

Each command section should include:

- module or feature owner
- implementation path
- safety level
- required environment
- syntax
- important flags
- validated example
- expected output
- failure modes or caveats
- related docs

Use explicit safety levels. A generic version:

| Level | Meaning |
| --- | --- |
| Read-only | Queries state, inspects files, exports data, or runs analysis without changing external state |
| Local write | Writes local files only |
| Guarded write | Changes external state and requires explicit flags, target checks, or approvals |
| High-risk | Can affect hardware, money, credentials, production systems, user data, safety, or irreversible state |

Command guide entries should prefer copy-pasteable commands. Use placeholders
only where a value must be selected by the operator:

```bash
<tool> <command> --target <target-id> --out <output-dir>
```

Whenever a command changes, update the command guide in the same task.

## Architecture Baseline

`docs/architecture-baseline.md` records the system shape. It should be broad
enough to guide future work, but not so speculative that it becomes fiction.

It should include:

- purpose
- high-level goals
- confirmed assumptions
- non-goals
- system layers
- repository shape
- runtime modes
- safety or risk model
- data and persistence model
- interface strategy
- recommended milestones
- open questions
- current recommendation

Keep architecture documents explicit about boundaries:

- first-party code versus upstream or vendor code
- reusable libraries versus applications
- core logic versus framework adapters
- local runtime versus optional network services
- safety policy versus behavior implementation
- command contracts versus natural-language interfaces

Update architecture documents when the shape of the system changes, not for
every small implementation detail.

## Feature Documents

Create focused technical documents when a subsystem becomes too detailed for the
baseline architecture file or when a plan has matured into a stable design.

Examples:

```text
docs/feature-routing-architecture.md
docs/feature-authentication-architecture.md
docs/feature-observability-plan.md
docs/deployment-plan.md
docs/safety-plan.md
```

A feature document should include:

- purpose
- scope
- data model
- module boundaries
- command or API surface
- persistence format
- safety and failure behavior
- test plan
- current implementation status
- future work

Feature documents are especially useful when the code is still evolving and
future agents need to preserve intent.

For many work areas, a feature/module plan file should come first. Promote the
stable parts of that plan into a feature architecture document once the
implementation direction is clearer.

## Feature And Module Plan Files

Create a feature or module plan file at the start of a meaningful new module,
subsystem, integration path, safety effort, deployment effort, or complex
feature. This file is the local implementation guide for that work area. It
starts as a general plan, then becomes more specific as agents learn, validate
assumptions, hit failure modes, and make design decisions.

Use names such as:

```text
docs/<feature>-plan.md
docs/<feature>-development-plan.md
docs/<module>-implementation-plan.md
docs/<area>-safety-plan.md
docs/<area>-deployment-plan.md
```

The plan file has a different job from the other docs:

- `docs/current-status.md` is the global recovery snapshot for the whole
  workspace.
- `docs/architecture-baseline.md` records durable system shape and boundaries.
- `docs/command-guide.md` records executable workflows.
- feature architecture docs record mature technical design.
- feature/module plan files record the evolving local path for one work stream.

A feature or module plan should include:

- purpose and scope
- active ownership
- starting point or current known state
- goals and non-goals
- assumptions and constraints
- current findings or interface discoveries
- proposed implementation phases
- task checklist or next-session checklist
- validation plan and success criteria
- failure modes and rollback or recovery steps
- safety considerations, if applicable
- signed change log or dated findings
- links to code, command docs, architecture docs, logs, and artifacts
- open questions and next intended move for this work area

Update the plan file whenever:

- a module or feature moves from idea to implementation
- ownership changes
- the implementation path changes
- a new finding changes the next step
- a validation run confirms or disproves an assumption
- a safety constraint, rollback path, or failure mode becomes known
- the task is paused and needs to be resumable later
- the plan has become stale compared with the code

These files are deliberately allowed to be more operational than architecture
docs. They can contain checklists, staged commands, rejected approaches, current
clues, ownership notes, and near-term implementation notes. Once a detail
becomes stable and general, promote it into architecture docs or the command
guide as appropriate.

## Presentation Or Stakeholder Layer

Some projects need a presentation-friendly documentation layer separate from
developer docs. This may be an Obsidian vault, a slide deck folder, a website,
or a report directory.

Keep this layer synchronized when:

- project direction changes
- deployment strategy changes
- architecture boundaries change
- milestones are completed
- stakeholder-facing status changes

Do not make stakeholder documents the only source of truth. Developer docs
remain the authoritative operational layer.

## Task Lifecycle

Use the same lifecycle for most tasks:

1. **Intake**
   - Restate the goal only if useful.
   - Identify whether the request is a question, review, code change, docs
     change, deployment task, or high-risk operation.
   - Read the relevant instructions before acting.

2. **Recovery**
   - Read `AGENTS.md`.
   - Read the repo-local skill if one applies.
   - Read `docs/current-status.md`.
   - Read `docs/active-work.md` if present.
   - Read relevant architecture or command docs.
   - Read the feature/module plan file when the task belongs to an active work
     area.
   - Inspect the working tree before editing.

3. **Classification**
   - Decide the safety level.
   - Decide whether the task touches protected code, generated artifacts,
     external services, hardware, production systems, credentials, or another
     actor's active area.
   - Decide what documentation must be updated if the work succeeds.
   - Decide whether the task needs a new feature/module plan file.

4. **Coordination**
   - Check active ownership.
   - If the same files or subsystem are already owned, coordinate, take an
     explicit handoff, or choose a disjoint scope.
   - Add or update ownership when starting non-trivial work.
   - Add a signed note when taking over stale work.

5. **Scope**
   - Prefer the smallest implementation that satisfies the request and fits the
     architecture.
   - Preserve existing conventions.
   - Avoid unrelated refactors.
   - Avoid editing upstream or generated code unless explicitly approved.

6. **Plan**
   - For non-trivial work, create a short checklist.
   - For a new module or complex feature, create or update the durable plan
     file before implementation details drift beyond what is written down.
   - Keep exactly one item actively in progress.
   - Update the checklist as items complete.
   - If the next step is blocked by a user decision, ask one concise question.

7. **Implement**
   - Read before editing.
   - Make reviewable patches.
   - Keep changes close to the relevant module.
   - Add comments around non-obvious state transitions, safety checks, protocol
     boundaries, or hardware assumptions.

8. **Verify**
   - Run the narrowest meaningful test first.
   - Expand verification when the blast radius is larger.
   - Capture important command output in the final response and in docs when it
     becomes part of the project record.

9. **Document**
   - Update `current-status.md` for milestone state and latest validation.
   - Update `active-work.md` or ownership blocks when ownership changes.
   - Update `collaboration-log.md` for cross-feature handoffs or ownership
     transfers when the project uses that file.
   - Update `command-guide.md` for executable workflows.
   - Update feature/module plan files for evolving implementation steps,
     findings, checklists, validation results, and next-session guidance.
   - Update architecture or feature docs for boundary changes.
   - Update repo-local skills or `AGENTS.md` when standing instructions change.

10. **Handoff**
   - State what changed.
   - State what was verified.
   - State what was not verified.
   - State remaining risks or next useful steps.
   - State whether ownership is completed, paused, blocked, or handed off.

## Task Tracking

This workflow treats documentation as the durable task tracker. Chat checklists
are useful during one turn, but tracked files must survive context loss.

Use these tracking layers:

- **Current turn checklist**: short, temporary, visible to the user while the
  agent works.
- **Active work doc**: current ownership across work streams.
- **Current status doc**: persistent global state, next intended move, latest
  verified result, and ownership summary.
- **Feature/module plan files**: persistent local implementation guides for
  active or resumable work streams.
- **Command guide**: persistent executable knowledge.
- **Architecture docs**: persistent design decisions and boundaries.
- **Feature docs**: persistent subsystem details.
- **Issue tracker**, if available: external planning, assignment, release
  coordination, and human workflow.

Avoid scattering todos in random source comments. If a todo matters to future
work, put it in the relevant plan or status doc with context, actor, timestamp,
and next action.

Recommended todo format:

````markdown
## Next Intended Move

1. Validate <specific workflow> using <specific command or test>.
2. If that passes, update <specific module or doc>.
3. If it fails, inspect <specific log, service, module, or artifact>.

## Open Questions

- Should <decision> prefer <option A> or <option B>?
- What external constraint determines <uncertain item>?
````

## Code Architecture Rules

Use an architecture that preserves boundaries:

- Put reusable first-party logic in `modules/`.
- Put deployable applications in `apps/`.
- Put developer tools, CLIs, scripts, and diagnostics in `tools/`.
- Put runtime configuration in `configs/`.
- Put tests in `tests/` or colocated test directories.
- Put architecture, command, safety, status, and plan docs in `docs/`.
- Put generated validation output in `logs/` or `exports/`.
- Treat vendored, generated, and upstream code as read-only by default.

Recommended repository shape:

```text
AGENTS.md
README.md
docs/
  active-work.md
  collaboration-log.md
  current-status.md
  command-guide.md
  architecture-baseline.md
  <feature-or-module>-plan.md
  safety-plan.md
configs/
modules/
  platform/
  core/
  safety/
  capabilities/
  interface/
  mission/
  hub/
apps/
tools/
tests/
logs/
exports/
```

Use dependency direction deliberately:

- `platform/` wraps vendor SDKs, OS APIs, framework APIs, cloud APIs, or device
  protocols.
- `core/` owns shared state, configuration, logging, events, schemas, and
  lifecycle primitives.
- `safety/` owns command gates, validation, fault handling, recovery, and
  approvals.
- `capabilities/` owns reusable abilities.
- `interface/` owns CLIs, UI adapters, voice or chat intent mapping, and public
  APIs.
- `mission/` owns tasks, routines, workflows, scheduling, or plans.
- `hub/` owns coordination across multiple runtimes, devices, users, or
  services.
- `apps/` compose modules into deployable entry points.

Do not let applications become the only place logic exists. Build the library
first, then expose it through an app, CLI, service, daemon, UI, or automation.

## Vendor And Upstream Boundaries

Every project should identify protected areas. Examples:

```text
vendor/
third_party/
external/
generated/
build/
dist/
```

Rules:

- Do not edit protected directories unless explicitly approved.
- Prefer thin adapters around upstream interfaces.
- Keep vendor-specific types localized to adapter modules.
- If a bug appears to be in upstream code, prove it with a wrapper-level test or
  minimal reproduction before proposing upstream edits.
- If upstream edits are unavoidable, document why wrappers were insufficient.

This boundary keeps the first-party system maintainable and makes upgrades
possible.

## Interfaces And Commands

Every major feature should expose:

- a reusable library API
- a CLI or diagnostic command
- logs understandable without opening source code
- documented syntax and examples
- tests or validation steps

Command design rules:

- Default to read-only behavior.
- Require explicit target selection for external systems.
- Use explicit flags for writes, destructive changes, or high-risk actions.
- Provide dry-run or validation mode where practical.
- Validate inputs before opening external connections when possible.
- Print clear errors with the failed assumption.
- Log enough context to diagnose without reading source.
- Keep natural-language interfaces behind explicit intent objects and command
  contracts.

Example guarded command shape:

```bash
<tool> apply-policy --target <target-id> --config <file> --allow-write
```

Example dry-run shape:

```bash
<tool> apply-policy --target <target-id> --config <file> --dry-run
```

## Safety And Risk Management

Treat a task as high-risk if it can affect:

- physical systems
- production services
- user data
- credentials or secrets
- money or billing
- legal, medical, or safety outcomes
- irreversible files or external state
- deployment availability

High-risk features need layered safeguards:

- explicit enable, arm, or approval conditions
- command validation
- rate limiting or bounded execution
- state monitoring
- fault detection
- emergency stop or rollback path
- operator-visible reporting
- logs and audit trail
- conservative defaults
- staged validation before live operation

For physical systems, movement, actuation, production, or real-world side
effects:

1. read-only observation
2. dry-run or simulation
3. local guarded writes
4. low-energy or bounded live tests
5. broader operation

Never allow raw language-model output to directly control a high-risk action.
Natural language should resolve into explicit internal commands, and those
commands must pass the normal validation and approval gates.

## Testing Strategy

Scale testing to risk and blast radius.

Recommended layers:

- **Unit tests** for pure logic, parsing, validation, policies, schemas, and
  command guards.
- **Fixture tests** for file formats, sample payloads, and compatibility data.
- **CLI smoke tests** for user-facing command paths.
- **Dry-run tests** for orchestration without external side effects.
- **Integration tests** for service boundaries and adapters.
- **Simulation tests** for physical, timing, or workflow behavior when
  available.
- **Guarded live validation** for hardware, production-like, or external
  systems.

For every validation run that matters, record:

- actor
- timestamp
- exact command
- environment assumptions
- target or fixture
- observed output
- artifact paths
- interpretation
- remaining uncertainty

If tests cannot be run, state why in the final handoff and, if important, in
the relevant status or plan document.

## Documentation Update Matrix

Use this matrix to decide what to update:

| Change | Required documentation |
| --- | --- |
| New CLI, flag, launch command, script, or workflow | `docs/command-guide.md` |
| New module, complex feature, staged integration, deployment effort, or safety effort | create or update a feature/module plan file |
| New active owner, paused task, blocked task, or handoff | feature/module plan ownership block and `docs/active-work.md` if present |
| Cross-feature ownership transfer, background-agent handoff, or coordination decision | `docs/collaboration-log.md` if present |
| New module boundary, runtime layer, dependency direction, or deployment shape | `docs/architecture-baseline.md` or feature architecture doc |
| New safety behavior, high-risk command, approval gate, recovery path, or hazard | safety plan and command guide |
| New validated milestone, failed live test, changed next step, or important clue | `docs/current-status.md` |
| New persistent project rule or protected boundary | `AGENTS.md` |
| New durable agent workflow reminder | repo-local skill |
| Stakeholder-facing milestone or direction change | presentation/report layer |
| New generated artifact | summarize in docs and store under `logs/` or `exports/` |

Documentation should be updated in the same change as the code whenever
possible. A feature is not really done if the next agent cannot find who owns
it, how to run it, or how to continue it.

## Agent Operating Practices

Agents following this workflow should:

- read instructions before editing
- inspect the repository shape before making assumptions
- check active ownership before touching shared areas
- prefer fast search tools
- read relevant files in parallel when possible
- keep edits scoped
- preserve user or teammate changes
- avoid destructive commands unless explicitly requested
- avoid broad refactors during narrow fixes
- implement the requested change rather than stopping at a proposal when the
  request clearly asks for action
- ask only when a missing decision is genuinely blocking or risky
- provide short progress updates during long work
- verify before final handoff
- sign durable progress updates
- report failures clearly

For code review tasks, lead with findings. Prioritize bugs, regressions, risks,
coordination issues, and missing tests. Summaries come after findings.

For implementation tasks, carry the work through code, verification, docs, and
handoff when feasible.

## Working Tree Discipline

Before editing:

```bash
git status --short
```

Rules:

- Assume uncommitted changes may belong to the user or another agent.
- Do not revert changes you did not make unless explicitly requested.
- If unrelated files are dirty, ignore them.
- If a file you need is dirty, read it carefully and work with the current
  content.
- Check active ownership before touching shared areas.
- Avoid commands that discard work.
- Keep patches small enough to review.

When editing files:

- Use structured or patch-based edits.
- Avoid generated metadata churn.
- Avoid reformatting unrelated code.
- Keep comments meaningful.
- Prefer explicit state machines and readable names over clever abstractions.

## Environment And Tooling

Document environment boundaries. Examples:

- language versions
- build tools
- shell activation scripts
- service dependencies
- hardware interfaces
- cloud credentials
- local-only versus internet-connected modes
- incompatible environment combinations

If two environments cannot be mixed in one shell, say that explicitly in
`AGENTS.md` and `command-guide.md`.

Command docs should include setup blocks:

```bash
cd <repo-root>
export <PROJECT_TOOL>=./build/tools/<tool>
export <PROJECT_TARGET>=<target>
```

Prefer named helper scripts for complex environment activation. Document the
helper script and use it consistently.

## Logs And Artifacts

Use `logs/` for runtime logs and `exports/` for generated or downloaded
artifacts. If another convention fits the project better, document it.

Rules:

- Keep generated outputs out of source directories.
- Ignore bulky generated artifacts in version control unless they are small,
  stable fixtures.
- Promote important generated files into `tests/fixtures/` only when they are
  needed for repeatable tests.
- Summarize important artifact paths and results in tracked docs.

A future agent should not need to inspect every log to know what happened. The
tracked docs should explain which logs matter and why.

## Recovery After Context Loss

When an agent enters a repo with little or no chat history, it should run this
recovery sequence:

1. Read `AGENTS.md`.
2. Read the relevant repo-local skill.
3. Read `docs/current-status.md`.
4. Read `docs/active-work.md` if present.
5. Read `docs/command-guide.md` for the affected area.
6. Read `docs/architecture-baseline.md` or feature docs for boundary context.
7. Read the feature/module plan file if one exists for the affected area.
8. Inspect `git status --short`.
9. Inspect recent logs or exports only if `current-status.md`, `active-work.md`,
   the collaboration log, or the relevant plan file points to them.
10. Continue from the relevant `Next Intended Move`.

This sequence is the reason the documentation set exists.

## Review Workflow

When asked to review code:

1. Inspect the diff or target files.
2. Identify behavioral regressions, safety risks, data-loss risks, security
   issues, coordination risks, and missing tests.
3. Report findings first, ordered by severity.
4. Reference exact files and lines.
5. Include open questions or assumptions.
6. Summarize only after findings.
7. If no issues are found, say that clearly and mention residual risk or test
   gaps.

Do not turn a review into a rewrite unless the user asks for fixes.

## Implementation Workflow

When asked to implement:

1. Read relevant instructions and docs.
2. Locate existing patterns.
3. Check active ownership and dirty worktree state.
4. Create or update the feature/module plan file when the work is new, complex,
   staged, safety-sensitive, or likely to be paused and resumed later.
5. Add or update ownership for the area.
6. Choose the smallest architecture-consistent design.
7. Implement the reusable module first when practical.
8. Add CLI, app, service, or UI exposure second.
9. Add focused tests.
10. Run verification.
11. Update docs and signed progress logs.
12. Mark ownership completed, paused, blocked, or handed off.
13. Handoff with changed files, verification, and remaining risk.

If the implementation touches a high-risk surface, add safety gates before
adding convenience flows.

## Natural Language And AI Features

For projects that include chat, voice, or language models:

- Treat model output as advisory.
- Convert user language into explicit intent objects.
- Validate intents against schemas and policy.
- Require confirmation for high-risk actions.
- Log the resolved command, not just the natural-language request.
- Keep core operation functional without online AI services where practical.
- Keep model-serving code behind replaceable interfaces.

This prevents prompts from becoming hidden control code.

## Deployment Workflow

Deployment guidance should separate:

- local development
- single-instance runtime
- optional connected services
- fleet or multi-instance coordination
- production deployment
- rollback and recovery

Do not start with custom operating systems, appliance images, or elaborate
deployment packaging unless the project truly requires it. Prefer a standard,
well-understood runtime first, then package it later.

Deployment docs should include:

- target platform
- install steps
- configuration
- secrets handling
- service startup
- health checks
- log paths
- backup and restore
- rollback
- known limitations
- active owner or release coordinator

## Status Update Style

During long tasks, agents should keep users informed with short, concrete
updates:

- what is being inspected
- what was learned
- what edit is about to happen
- what verification is running
- what remains

Avoid noisy narration. The purpose is to help the user trust the process and
interrupt if priorities change.

## Final Handoff Style

A good final handoff is concise and useful:

- what changed
- where it changed
- what was verified
- what failed or was not run
- what remains risky or next
- whether active ownership is completed, paused, blocked, or handed off when
  relevant

Example:

```text
Implemented the new parser in <path> and exposed it through <tool>. Updated the
command guide with the new syntax and added fixture coverage for malformed
input.

Verified with:
- <test command>
- <smoke command>

Not run: <reason>.
```

Do not bury failures. If verification was incomplete, say so.

## Templates

### `AGENTS.md` Template

````markdown
# Project Instructions

## Scope

- Describe what this workspace contains.
- Identify first-party code areas.
- Identify upstream, generated, external, or protected areas.
- State when protected areas may be edited.

## Collaboration And Ownership

- Durable progress updates must include an actor stamp.
- Active work must be recorded in feature/module plan files.
- Use `docs/active-work.md` when multiple active work streams exist.
- Do not edit files owned by another active work stream without handoff,
  coordination, review scope, or explicit approval.
- Stale ownership may be taken over only after adding a signed note and
  following the project's stale-work policy.

## Platform And Context

- Target operating systems or runtime platforms.
- Primary languages and toolchains.
- Important environment boundaries.
- Optional versus required external services.

## Core Engineering Rules

- Preferred architecture style.
- Dependency and module boundaries.
- Library-first or API-first expectations.
- Offline or local-first requirements.
- Maintainability preferences.

## Repository Direction

- `modules/` for reusable libraries.
- `apps/` for composed applications.
- `tools/` for CLIs, diagnostics, and developer utilities.
- `docs/` for operational, plan, safety, command, and architecture docs.
- `configs/` for runtime configuration.
- `tests/` for test coverage.
- `logs/` and `exports/` for generated artifacts.

## Project Skill

- Keep `.codex/skills/<project-slug>/SKILL.md` aligned with major workflow,
  architecture, and status changes.
- Keep `docs/current-status.md` updated for active phase, latest validation,
  risks, ownership summary, and next intended move.
- Keep `docs/command-guide.md` updated for executable workflows.
- Keep feature/module plan files updated while implementation details are being
  discovered.
- Keep architecture and stakeholder docs synchronized when direction changes.

## Safety-Critical Or High-Risk Development

- Define what counts as high-risk.
- Require explicit gates for high-risk actions.
- Require validation, logging, and recovery paths.
- Prefer fail-safe behavior.
- Do not merge or run high-risk features without a documented test plan.

## Interfaces And Tooling

- Every major feature should expose a library API.
- Every major feature should expose a CLI or diagnostic path.
- Commands should have safe defaults and explicit write flags.
- Natural-language interfaces must resolve to explicit commands.

## Architecture Preferences

- Define core layers and dependency direction.
- Keep adapters around vendor or framework APIs.
- Keep reusable capabilities separate from app-specific orchestration.
- Keep optional services replaceable.

## Code Style And Documentation

- Preferred language standard.
- Comment expectations.
- Naming and readability preferences.
- Formatting or linting expectations.

## Testing Expectations

- Unit tests for logic.
- Fixture tests for formats.
- Integration tests for boundaries.
- Dry-run or simulation for high-risk behavior.
- Guarded live validation where applicable.

## Decision Bias

- Maintainability over speed for shared modules.
- Wrapper layers over upstream edits.
- Local/offline robustness over convenience for core behavior.
- Explicit state and contracts over hidden prompt behavior.
````

### Repo-Local Skill Template

```markdown
---
name: <project-slug>
description: Use when working on <project domain>, architecture, reusable
modules, command workflows, docs, collaboration state, or status tracking for
this repository.
---

# <Project Name> Skill

Use this skill when changing architecture, scaffolding modules, adding command
workflows, updating safety-sensitive behavior, coordinating active work, or
preserving project status.

## Core Working Rules

- Keep first-party code outside protected upstream directories.
- Prefer reusable modules over app-specific logic.
- Keep runtime, interfaces, and optional services modular.
- Check active ownership before touching shared files or active work streams.
- Do not revert human or agent changes unless explicitly requested.
- Update `docs/current-status.md` when phase, validation, risks, ownership, or
  next move changes.
- Update `docs/active-work.md` when active ownership changes and the project
  uses that file.
- Update `docs/command-guide.md` when commands or workflows change.
- Create or update feature/module plan files for staged implementation work.
- Add signed progress updates for meaningful discoveries, validations, blocked
  states, ownership transfers, and handoffs.
- Update architecture docs when boundaries or deployment direction change.
- Update stakeholder docs when presentation-facing status changes.

## Current Architecture Direction

- Summarize the major layers.
- Summarize current implementation order.
- Summarize important environment boundaries.
- Summarize known constraints future agents must not forget.

## Scaffolding Priorities

- Build narrow interfaces first.
- Add app or service composition after reusable boundaries are clear.
- Keep logs and docs sufficient for future recovery.
- Keep ownership notes sufficient for future safe takeover.

## When Adding New Work

- Classify the work by layer.
- Check active ownership and dirty worktree state.
- Place reusable logic in modules.
- Place orchestration in apps, profiles, workflows, or services.
- Create or update the relevant feature/module plan when the work is complex or
  resumable.
- Update docs as part of the same change.
```

### `docs/current-status.md` Template

````markdown
# Current Status

This document is the short-running milestone log for the workspace. Future
agents should check this file first for the current working state, latest
validated result, active ownership, and next intended move.

## Current Phase

<Phase name and summary.>

## Active Work Summary

| Area | Owner | Status | Plan File | Last Updated |
| --- | --- | --- | --- | --- |
| <area> | <actor> | <status> | <path> | <timestamp> |

## Immediate Goal

1. <Concrete goal.>
2. <Concrete goal.>
3. <Blocked or deferred goal.>

## Latest Verified Result

- Actor:
- Timestamp:
- Command or workflow:
- Environment:
- Output:
- Artifacts:
- Interpretation:
- Remaining uncertainty:

## Current Best Workflow

```bash
<commands>
```

## Current Risks

- <Risk and consequence.>

## Current Clues

- <Observation that may matter later.>

## Next Intended Move

1. <Next action.>
2. <Fallback if it fails.>

## Signed Progress Updates

### Update: <short title>

- Actor:
- Timestamp:
- Scope:
- Status:
- Summary:
- Verification:
- Next intended move:
````

### `docs/command-guide.md` Template

````markdown
# Command Guide

This is the operator and developer command reference for implemented tooling.
Keep this guide updated whenever a CLI, launch file, app entry point, command
flag, safety guard, or validated workflow changes.

## Command Safety Levels

| Level | Meaning | Examples |
| --- | --- | --- |
| Read-only | Queries state or exports artifacts | `<tool> status` |
| Local write | Writes local files only | `<tool> generate --out ...` |
| Guarded write | Changes external state and requires explicit approval flags | `<tool> apply --allow-write` |
| High-risk | Can affect safety, production, money, credentials, or irreversible state | `<tool> deploy-prod` |

## Common Setup

```bash
cd <repo-root>
export <PROJECT_TOOL>=./build/tools/<tool>
```

## Build Commands

```bash
<build command>
```

## Module: <Module Name>

Source:

- [Library](../modules/<path>)
- [CLI](../tools/<path>)
- [Architecture](feature-<area>-architecture.md)
- [Plan](<area>-plan.md)

Owner or active work:

- <actor, team, plan file, or active-work entry>

Safety level: <level>

### Read-Only Commands

```bash
<command>
```

Expected result:

- <result>

### Write Commands

All commands in this section require `<explicit flag>`.

```bash
<command>
```

### Validated Workflow

```bash
<commands>
```

Validated result:

- Actor:
- Timestamp:
- Result:
- Artifacts:
- Remaining uncertainty:
````

### `docs/architecture-baseline.md` Template

````markdown
# Architecture Baseline

## Purpose

<Why this system exists and what the baseline captures.>

## High-Level Goals

- <Goal>

## Confirmed Working Assumptions

- <Assumption>

## Non-Goals For The First Phase

- <Non-goal>

## Proposed System Layers

### 1. Vendor Or Platform Boundary Layer

Purpose: isolate external dependencies behind local interfaces.

### 2. Core Runtime Layer

Purpose: host shared lifecycle, state, configuration, logging, and contracts.

### 3. Safety Or Policy Layer

Purpose: centralize permissions, validation, fault handling, and recovery.

### 4. Capability Modules

Purpose: implement reusable abilities as standalone libraries.

### 5. Interface Layer

Purpose: expose commands, APIs, UI, voice, chat, or diagnostics.

### 6. Mission Or Workflow Layer

Purpose: represent repeatable tasks, schedules, plans, and routines.

### 7. Hub Or Coordination Layer

Purpose: coordinate multiple runtimes, users, devices, agents, or services while
preserving local safety and independence.

## Suggested Repository Shape

```text
AGENTS.md
docs/
configs/
modules/
apps/
tools/
tests/
```

## Runtime Modes

- Local/offline
- Optional connected
- Coordinated or fleet/multi-instance

## Safety Baseline

- Command gates.
- State monitoring.
- Fault response.
- Recovery.
- Audit logging.

## Data And Persistence

- Config files.
- State files.
- Schemas.
- Logs.
- Artifacts.

## CLI Direction

- Safe defaults.
- Dry-run support.
- Explicit targets.
- Verbose diagnostics.

## Collaboration Direction

- Ownership records.
- Active-work index, if needed.
- Handoff expectations.
- Stale-work policy.

## Recommended Near-Term Milestones

1. <Milestone>

## Key Open Questions

- <Question>

## Current Recommendation

<Short recommendation.>
````

### Feature Or Module Plan Template

````markdown
# <Feature Or Module> Plan

This document is the local implementation guide for <feature or module>. Future
agents should read it before changing this work area, especially after context
loss or a pause in development.

## Active Ownership

| Area | Owner | Started | Last Updated | Status | Expected Files | Handoff |
| --- | --- | --- | --- | --- | --- | --- |
| <area> | <actor> | <timestamp> | <timestamp> | planned | <paths> | <note> |

## Purpose

<Why this work exists and what problem it solves.>

## Scope

- In scope:
- Out of scope:

## Starting Point

- Current code:
- Current commands:
- Current docs:
- Current constraints:
- Known working baseline:

## Goals

1. <Goal>
2. <Goal>
3. <Goal>

## Non-Goals

- <Non-goal>

## Current Findings

- <Observation, interface finding, failed attempt, dependency note, or
  discovered constraint.>

## Implementation Plan

### Phase 1: <Name>

- [ ] <Task>
- [ ] <Task>

### Phase 2: <Name>

- [ ] <Task>
- [ ] <Task>

## Design Decisions

| Decision | Reason | Actor | Date |
| --- | --- | --- | --- |
| <decision> | <reason> | <actor> | <date> |

## Validation Plan

1. <Read-only or fixture validation.>
2. <Dry-run or local validation.>
3. <Integration or live validation, if applicable.>

## Current Best Commands

```bash
<commands>
```

## Failure Modes And Recovery

- Failure:
  Recovery:

## Success Criteria

- <Criterion>

## Signed Progress Updates

### Update: <short title>

- Actor:
- Role:
- Timestamp:
- Branch/session:
- Scope:
- Status:
- Files/areas touched:
- Summary:
- Verification:
- Next intended move:

## Change Log

If the plan keeps a compact change log in addition to signed progress updates,
each entry must still include an actor and timestamp or link to the relevant
signed update.

- <timestamp> - <actor>: <finding, validation result, or intentional state change.>

## Open Questions

- <Question>

## Next Session Checklist

1. <Next action.>
2. <Fallback if it fails.>
````

Use this template for development plans, module implementation plans,
deployment plans, integration plans, and safety-adjacent plans that need more
local detail than the global current-status document.

### Active Work Template

````markdown
# Active Work

This file indexes active work so humans and agents can avoid collisions. Update
it when starting, pausing, handing off, or completing work that touches shared
areas.

| Area | Owner | Status | Branch/Session | Plan File | Expected Files | Last Updated |
| --- | --- | --- | --- | --- | --- | --- |
| <area> | <actor> | in progress | <branch/session> | <doc path> | <paths> | <timestamp> |

## Coordination Notes

### Update: <short title>

- Actor:
- Timestamp:
- Scope:
- Summary:
- Next intended move:
````

### Collaboration Log Template

````markdown
# Collaboration Log

This append-only file records cross-cutting handoffs, ownership transfers,
blocked states, environment changes, and coordination decisions that affect more
than one feature/module plan.

## Entries

### Update: <short title>

- Actor:
- Role:
- Timestamp:
- Branch/session:
- Scope:
- Related plan files:
- Status:
- Files/areas touched:
- Summary:
- Verification:
- Next intended move:
````

### Safety Plan Template

```markdown
# Safety Plan

## Scope

<What high-risk behavior this plan covers.>

## Hazards

| Hazard | Cause | Consequence | Mitigation |
| --- | --- | --- | --- |
| <hazard> | <cause> | <consequence> | <mitigation> |

## Command Gates

- <Gate>

## State Monitoring

- <State source>

## Fault Response

- <Fault>
- <Immediate response>
- <Recovery path>

## Operator Alerts

- <Alert channel>

## Test Plan

1. Read-only validation.
2. Dry-run validation.
3. Simulation or fixture validation.
4. Guarded live validation.

## Stop Conditions

- <Condition that halts testing.>
```

## Instruction Generation Process

When adapting this workflow to a new project, generate project instructions in
this order:

1. **Inventory the repository**
   - Identify first-party directories.
   - Identify protected directories.
   - Identify build tools, languages, and runtime environments.
   - Identify existing docs, tests, logs, and generated artifacts.
   - Identify likely shared files or modules where ownership records will help.

2. **Classify the project risk**
   - Is it purely local software?
   - Does it touch production?
   - Does it control hardware?
   - Does it manage personal data, credentials, billing, safety, or legal
     outcomes?
   - Can multiple humans, branches, terminals, or agents edit it at once?

3. **Write `AGENTS.md`**
   - Encode durable rules.
   - Protect upstream and generated code.
   - Define architecture direction.
   - Define documentation responsibilities.
   - Define coordination, ownership, and stale-work rules.
   - Define safety and test expectations.

4. **Create the repo-local skill**
   - Summarize the most important rules.
   - Include trigger conditions.
   - Point to the living docs.
   - Include the active-work and handoff rules agents must not forget.
   - Keep it short enough to load often.

5. **Create `docs/current-status.md`**
   - Record the active phase.
   - Record the active work summary when concurrent work exists.
   - Record the latest verified result.
   - Record the next intended move.
   - Record current risks.

6. **Create `docs/command-guide.md`**
   - Record build commands first.
   - Add command safety levels.
   - Add setup and environment.
   - Add each implemented command as it appears.

7. **Create `docs/architecture-baseline.md`**
   - Record the desired system layers.
   - Record dependency direction.
   - Record non-goals.
   - Record runtime and coordination modes.
   - Record near-term milestones.

8. **Create active-work or collaboration docs when needed**
   - Create `docs/active-work.md` if concurrent work is likely.
   - Create `docs/collaboration-log.md` if cross-feature handoffs, background
     agents, or frequent ownership transfers are likely.
   - Keep these files as indexes and append-only records, not replacements for
     feature/module plans.

9. **Create the first feature or module plan when work begins**
   - Start a plan file before a complex feature accumulates hidden chat-only
     context.
   - Record active ownership, starting point, goals, staged implementation plan,
     validation plan, failure modes, and next-session checklist.

10. **Add feature docs as designs mature**
   - Create a document when a subsystem outgrows the baseline architecture.
   - Promote stable design from plans into feature architecture docs.

11. **Keep everything synchronized**
   - Docs are part of the definition of done.
   - Every future agent should be able to resume from the files alone.
   - Every future collaborator should be able to tell who owns active work and
     what can be safely continued.

## Definition Of Done

A task is done when:

- the requested behavior or answer is complete
- active ownership was checked before editing
- code changes are scoped and consistent with local patterns
- protected directories were not edited without approval
- relevant tests or validation were run
- failures or skipped tests are documented
- command docs are updated for executable changes
- current status is updated for milestone or validation changes
- feature/module plan files are updated for active implementation work
- ownership is marked completed, paused, blocked, or handed off
- collaboration logs are updated for cross-workstream handoffs when the project
  uses them
- architecture docs are updated for boundary changes
- safety docs are updated for high-risk behavior
- the final handoff states what changed, what was verified, and what remains

## Anti-Patterns

Avoid these:

- hiding durable state in chat history only
- starting a complex module without a feature/module plan file
- leaving active ownership stale or unsigned
- silently overwriting progress notes instead of appending important updates
- editing files owned by another active work stream without coordination
- putting running progress into architecture docs
- putting architecture decisions only in status logs
- editing upstream code before trying adapters
- making an app before the reusable module exists
- exposing only a UI without a diagnostic CLI
- letting natural-language output bypass command validation
- using generated artifacts as the only record of validation
- leaving commands undocumented
- leaving future agents without a concrete next step
- using broad refactors to solve narrow requests
- ignoring dirty worktrees
- treating a passing build as a complete validation for high-risk behavior

## Quick Start For A New Agent

If you are an AI agent entering a repository that follows this playbook:

1. Read `AGENTS.md`.
2. Load the repo-local skill if one applies.
3. Read `docs/current-status.md`.
4. Read `docs/active-work.md` if present.
5. Read `docs/command-guide.md` for the area you will touch.
6. Read the feature/module plan file for the area, if one exists.
7. Read architecture or feature docs for module boundaries.
8. Run `git status --short`.
9. Classify the task and safety level.
10. Check active ownership and dirty worktree state.
11. Implement or answer within the existing architecture.
12. Verify.
13. Update docs with signed progress notes.
14. Handoff clearly.

The goal is not just to complete one task. The goal is to leave the repository
more recoverable and less collision-prone for the next human or agent than it
was when you arrived.
