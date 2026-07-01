---
name: unity-ml-agents-training-operations
description: Configure, run, resume, or diagnose Unity ML-Agents training workflows while keeping scenes, behavior names, YAML configs, run artifacts, checkpoints, and generated data under control. Use when a Unity task touches ML-Agents training operations or training configuration.
---

# Unity ML-Agents Training Operations

Use this skill when a Unity project trains agents with Unity ML-Agents. Keep
training operations reproducible and separate from game-specific design rules.

## Inspect First

- `Packages/manifest.json` for ML-Agents package version.
- Python environment, trainer version, and documented setup commands.
- Training configuration YAML files.
- Scenes, prefabs, `Behavior Parameters`, observations, rewards, and trainer
  behavior names.
- Existing run output, checkpoint, model export, and ignored artifact folders.

## Workflow

1. Separate code changes from training runs.
   - Inspect scene and config changes before launching training.
   - Keep generated artifacts, logs, TensorBoard output, checkpoints, and exported
     models out of Git unless the project explicitly tracks selected artifacts.
   - Use synthetic or public-safe run names in shared examples.

2. Verify behavior naming.
   - Match `Behavior Parameters` behavior names to trainer YAML keys.
   - Check observation and action space changes against the trainer config.
   - Confirm inference model references are intentional before replacing models.

3. Start with a smoke run.
   - Prefer a short local run or no-graphics run before long training.
   - Record command, scene, config path, run ID, seed when set, and output path.
   - Stop early if observations, rewards, action spaces, or environment resets are
     obviously broken.

4. Guard expensive or external runs.
   - Treat remote GPU jobs, cloud storage, paid compute, shared training machines,
     and long unattended runs as high-risk operations requiring explicit target
     and approval.
   - Do not upload private scenes, recordings, datasets, or checkpoints to a
     shared service without approval.

5. Resume or compare runs carefully.
   - Confirm whether the task is resume, force overwrite, fine-tune, evaluate, or
     export for inference.
   - Preserve older checkpoints until the user confirms they can be deleted.
   - Compare metrics using the project's established evaluator or TensorBoard
     logs instead of relying on a single visual impression.

## Verification

- Unity opens the relevant scene or prefab without missing script references.
- Trainer config parses and contains the intended behavior key.
- A short run starts, steps the environment, writes output to the expected
  artifact directory, and can be stopped cleanly.
- Exported model references are updated only when intended.
- Generated artifacts are ignored or deliberately tracked.

## Reporting

State package and trainer versions when known, scenes/configs touched, command
run, run ID and output path, smoke-run result, artifact handling, and any checks
skipped because Unity, Python, GPU, or provider access was unavailable.