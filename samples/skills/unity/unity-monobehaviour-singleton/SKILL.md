---
name: unity-monobehaviour-singleton
description: Create or modify Unity MonoBehaviour singleton classes. Use when a manager or controller needs one globally reachable instance, duplicate-instance protection, optional scene persistence, and clear lifecycle/event cleanup.
---

# Unity MonoBehaviour Singleton

Use this pattern only when the target project already accepts global
manager-style MonoBehaviours. Prefer explicit references or dependency
injection when that is the local convention.

## Required Implementation

1. Define a static singleton property:

```csharp
public static MyManager Singleton { get; private set; }
```

2. Implement the duplicate guard in `Awake`:

```csharp
private void Awake()
{
    if (Singleton != null && Singleton != this)
    {
        Destroy(gameObject);
        return;
    }

    Singleton = this;
}
```

3. If the existing project convention destroys only the duplicate component,
   use `Destroy(this)` instead and preserve that convention consistently.
4. Use `DontDestroyOnLoad(gameObject)` only for services that must survive
   scene changes.
5. Keep one-time wiring in `Awake` or `Start`; avoid hidden side effects in
   static property getters.

## Lifecycle Rules

- Subscribe to events in clear lifecycle entry points.
- Unsubscribe in matching exit points such as `OnDestroy`, state teardown, or
  an equivalent project lifecycle method.
- Keep `Update` and `FixedUpdate` light; avoid expensive object lookups or
  allocations per frame.
- Document whether the singleton is scene-local or persistent.

## Platform-Level Variants

- If the project uses a central update dispatcher, register core runtime
  systems there instead of adding independent `Update` loops.
- UI controllers may remain on normal Unity lifecycle methods when that is the
  local convention.
- When a duplicate GameObject contains other meaningful components, decide
  whether destroying the component or the whole GameObject matches the target
  architecture before editing.

## Verification

- Enter the scene once and confirm `Singleton` is assigned.
- Load or reload the scene and confirm duplicates are handled as intended.
- Confirm event subscriptions are cleaned up when the object is destroyed.
