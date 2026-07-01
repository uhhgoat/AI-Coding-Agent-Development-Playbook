---
name: upstream-contribution-workflow
description: Prepare narrow upstream issues, pull requests, and reviewer responses without turning a dependency into a casual fork. Use when adapting local fixes for an upstream repository or responding to upstream review feedback.
---

# Upstream Contribution Workflow

Use this skill when a local repository depends on an upstream project and a fix
should be proposed upstream instead of carried as an unstructured local patch.

## Workflow

1. Establish the upstream boundary.
   - Identify whether the target is first-party code, a fork, a vendored copy, a
     submodule, or an external dependency.
   - Read contribution guidelines, issue templates, coding standards, and test
     commands before editing.
   - Preserve local integration work unless the user explicitly approves changing
     the dependency pointer or fork state.

2. Reproduce and scope the issue.
   - Capture expected behavior, actual behavior, reproduction steps, environment,
     and affected versions.
   - Reduce the case to the smallest patch that still fixes the bug.
   - Split unrelated UI, backend, persistence, provider, policy, or documentation
     changes into separate issues or PRs when practical.

3. Implement for upstream review.
   - Follow upstream naming, style, build, test, and documentation patterns.
   - Add focused tests for the reported behavior and reviewer-provided examples.
   - Avoid local-only assumptions such as private endpoints, machine paths,
     workspace names, feature flags, or deployment topology.

4. Prepare the public explanation.
   - Link a concrete issue for non-trivial fixes when the project expects one.
   - Write a PR body with problem, reproduction, fix summary, validation, and
     screenshots or clips for UI behavior when useful.
   - Redact private logs, tokens, internal project names, customer data, and
     unpublished roadmap details.

5. Respond to review.
   - Treat reviewer comments as regression-test input.
   - Reproduce the reported case, add or update focused tests, then reply with
     the exact fix and validation that passed.
   - If the fix broadens in scope, update the PR title, summary, and testing notes
     so reviewers can see the wider behavior change.

## Guardrails

- Do not rewrite upstream history or overwrite local submodule work casually.
- Do not push private reproduction artifacts to public branches.
- Do not claim coverage across providers, platforms, or versions that were not
  tested.
- Keep public replies precise: acknowledge the issue, describe the scoped fix,
  and state remaining limitations.

## Reporting

State the upstream target, branch or patch location, issue or PR link when one
exists, validation run, files intentionally excluded, and any remaining review
risk.