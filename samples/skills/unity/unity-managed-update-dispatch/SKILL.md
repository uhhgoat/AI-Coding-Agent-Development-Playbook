---
name: unity-managed-update-dispatch
description: Add or modify Unity runtime systems that are updated through an explicit manager dispatch order instead of each system using its own MonoBehaviour Update loop. Use when a project centralizes tick order for gameplay, simulation, or deterministic runtime systems.
---

# Unity Managed Update Dispatch

Use this skill when the project has a central runtime dispatcher for systems
that must update in a deliberate order.

## Core Pattern

- A bootstrap step creates or registers runtime managers.
- Each managed system implements a small interface such as `ManagedStart`,
  `ManagedUpdate`, or `ManagedFixedUpdate`.
- A dispatcher invokes systems in an explicit order.
- UI-only controllers may remain on normal Unity lifecycle methods if that is
  the local convention.

## When Adding A Managed System

1. Find the dispatcher interface and existing manager registration pattern.
2. Implement the required managed lifecycle methods.
3. Register the manager in bootstrap or the dispatcher list.
4. Add calls in the explicit start/update/fixed-update order.
5. Document ordering changes when they affect behavior.

## Guardrails

- Do not update the same core state from both dispatcher methods and a separate
  MonoBehaviour `Update`.
- Keep paused-time behavior explicit.
- Avoid hidden registration through scene searches in hot paths.
- Keep dependencies between managers visible in the dispatch order.

## Verification

- Confirm the managed start method runs once.
- Confirm update and fixed-update cadence match the intended loop.
- Confirm no double dispatch occurs.
- Confirm pause, scene transition, or teardown behavior still works.
