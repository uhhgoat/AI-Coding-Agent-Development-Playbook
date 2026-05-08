---
name: unity-scriptableobject-singleton
description: Create or update Unity ScriptableObject singleton assets loaded from Resources. Use when a project stores editor-authored configuration, maps, or lookup data in one asset accessed through a lazy static getter.
---

# Unity ScriptableObject Singleton

Use this pattern for editor-authored configuration assets, maps, and lookup
tables that have one canonical asset instance in the project.

## Required Structure

1. Define a private static backing field:

```csharp
private static MyConfigAsset _instance;
```

2. Define a lazy singleton property:

```csharp
public static MyConfigAsset Singleton
{
    get
    {
        if (_instance == null)
        {
            _instance = Resources.Load<MyConfigAsset>("MyConfigAsset");
        }

        return _instance;
    }
}
```

3. If the project already uses the non-generic `Resources.Load("Name") as
   MyType` convention, preserve that style unless there is a reason to update
   the local pattern.

4. Make the asset creatable in the editor:

```csharp
[CreateAssetMenu(fileName = "MyConfigAsset", menuName = "Config/My Config Asset")]
public sealed class MyConfigAsset : ScriptableObject
{
}
```

## Resource Contract

- The asset must exist under an `Assets/Resources` folder.
- The `Resources.Load` path must match the asset path relative to `Resources`
  without the file extension.
- Missing assets should produce a clear error or be handled safely by callers.
- Keep lookup behavior null-safe and deterministic.

## Behavior Rules

- Treat ScriptableObject singleton assets as runtime read models by default.
- Avoid heavy runtime mutation unless the project already persists such
  changes deliberately.
- Keep key and value types explicit and stable when the asset acts as a lookup
  map.
- Document any editor scripts, importers, or generators that populate the
  asset.

## Verification

- Confirm the asset exists at the expected `Resources` path.
- Confirm `Singleton` resolves the asset in editor play mode.
- Confirm missing or duplicate mapping entries are handled according to the
  project's conventions.
