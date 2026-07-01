---
name: windows-workspace-permission-guard
description: Diagnose and repair Windows filesystem ownership or ACL drift in Git workspaces. Use when Codex encounters Permission denied errors while editing, generating, staging, committing, fetching, pulling, or writing files; when files are owned by a sandbox, administrator, service, SID-only, or wrong user account; or when `.git/index`, reflogs, Git objects, generated files, or scaffolded folders are not writable by the intended Windows user.
---

# Windows Workspace Permission Guard

## Overview

Use this skill to keep a Windows workspace writable by the intended human user after tools, sandboxes, generators, editors, or elevated commands create files with the wrong owner or ACL. Repair the smallest safe scope and preserve file contents.

## Diagnose

1. Identify the blocked path.
   - Use the exact path from the error message when available.
   - If the path is stale, find the real file with `rg --files`, `git status --short`, or the editor's current path.

2. Check repository state.
   - Run `git status --short --branch`.
   - Treat modified, added, and untracked files intended for commit as candidates for ownership checks.
   - Include `.git/index` and `.git/logs/HEAD` when Git, IDE staging, commits, fetches, pulls, or ref updates fail.

3. Inspect ownership and write access.
   - Use `Get-Acl -LiteralPath <path>` for owner and ACL.
   - Use `icacls <path>` when inheritance or explicit deny entries matter.
   - Verify write access with a real open/write probe, not just an ACL read.

PowerShell file probe:

```powershell
$fs = [System.IO.File]::Open(
    '<path>',
    [System.IO.FileMode]::Open,
    [System.IO.FileAccess]::ReadWrite,
    [System.IO.FileShare]::ReadWrite
)
$fs.Close()
```

Directory probe:

```powershell
$testPath = Join-Path '<directory>' ('.write-test-' + [guid]::NewGuid().ToString('N'))
[System.IO.File]::WriteAllText($testPath, 'test')
Remove-Item -LiteralPath $testPath -Force
```

## Repair Files Or Folders

- Prefer a single file repair for one bad file.
- Prefer a containing folder repair only when several files in that folder share the same bad owner or ACL.
- Do not run broad recursive ownership changes from the drive root or user profile.
- Resolve paths before destructive or recursive operations and confirm they remain inside the intended workspace.
- Preserve content by moving the bad path aside, recreating the original path under the intended user context, copying content back, verifying ownership/write access, then deleting the backup.
- Use a temporary sibling suffix such as `.permission-backup` or `.acl-backup`, and remove it before handoff.

Common repair options:

- `icacls <path> /setowner <expected-user> /T /C` for a scoped folder when policy allows ownership changes.
- Recreate-copy-back when ownership changes are denied or the sandbox owns the file.
- Regenerate build artifacts when the files are disposable and documented as generated.

## Git Metadata

For `.git/index`:

- Move `.git/index` aside.
- Recreate `.git/index` by copying it back under the intended user context so staged state is preserved.
- Verify a read/write open probe before retrying Git or IDE staging.

For reflogs such as `.git/logs/HEAD` or `.git/logs/refs/heads/<branch>`:

- Repair the exact blocked reflog files.
- Keep `core.logAllRefUpdates=true` unless the repository intentionally disables reflogs.
- Verify both `HEAD` and current branch reflog when branch operations failed.

For `.git/objects/<fanout>/<object>`:

- Repair only the exact object path named by the Git error, or exact objects proven to correspond to current working files.
- Use `git hash-object <file>` to map a working file to a blob object.
- Do not delete pack files or unrelated loose objects.

## Finish

Before handoff:

- Remove temporary backup paths.
- Re-run `git status --short --branch`.
- Verify ownership and write access for touched files, intended commit files, `.git/index`, and `.git/logs/HEAD`.
- State what was repaired, what command or copy-back method was used, and any remaining editor restart or retry needed.
