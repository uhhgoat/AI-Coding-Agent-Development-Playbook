---
name: unity-scriptableobject-asset-map
description: Implement or modify Unity ScriptableObject asset maps that resolve stable keys to assets, prefabs, sprites, styles, scenes, or other objects. Use when a project prefers data-driven lookup assets over hardcoded tables.
---

# Unity ScriptableObject Asset Map

Use this pattern for data-driven lookup registries.

## Standard Layout

- A `ScriptableObject` map asset.
- A serialized list of mapping entries.
- A serializable entry type with explicit `key` and `value` fields.
- A public lookup method.
- Optional editor-only or guarded `Add` behavior when population is automated.

Example:

```csharp
[CreateAssetMenu(fileName = "PrefabMap", menuName = "Config/Prefab Map")]
public sealed class PrefabMap : ScriptableObject
{
    [SerializeField] private List<Entry> _entries = new();

    public GameObject Get(string key)
    {
        foreach (Entry entry in _entries)
        {
            if (entry.Key == key)
            {
                return entry.Value;
            }
        }

        return null;
    }

    [Serializable]
    private sealed class Entry
    {
        public string Key;
        public GameObject Value;
    }
}
```

## Implementation Checklist

1. Pick a stable key type: enum, string ID, integer ID, GUID, or structured key.
2. Keep missing-key behavior explicit.
3. Keep mapping entries serializable by Unity.
4. Avoid hardcoded fallback tables unless there is a clear migration reason.
5. Keep asset creation, loading, and registration documented.

## Verification

- Confirm the asset contains every expected key.
- Confirm missing-key behavior is safe at call sites.
- Confirm duplicate keys are rejected, warned about, or intentionally resolved.
