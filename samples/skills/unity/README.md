# Unity Skills

General Unity skill examples.

These samples demonstrate how to encode repeatable Unity project patterns as
agent skills. They intentionally avoid project-specific game systems, asset
names, team names, or local paths beyond common Unity conventions.

Platform-specific Unity workflows belong here even when they are opinionated:
singleton patterns, ScriptableObject asset maps, Animator Controller editing,
scene setup, prefab wiring, build pipeline checks, and similar recurring Unity
workflows. Move only application-design-specific workflows out of the public
samples, such as a particular game's dialogue schema, encounter format, quest
pipeline, combat model, or progression system.

Current samples:

- `unity-monobehaviour-singleton/`
- `unity-scriptableobject-singleton/`
- `unity-scriptableobject-asset-map/`
- `unity-managed-update-dispatch/`
