param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-z0-9][a-z0-9-]*$')]
    [string]$Name,

    [Parameter(Mandatory = $true)]
    [string]$Description
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Utf8 = [System.Text.UTF8Encoding]::new($false)

function Write-SkillFile {
    param([string]$RelativePath, [string]$Content)
    $Path = Join-Path $Root $RelativePath
    $Directory = Split-Path -Parent $Path
    if (-not [System.IO.Directory]::Exists($Directory)) {
        [System.IO.Directory]::CreateDirectory($Directory) > $null
    }
    [System.IO.File]::WriteAllText($Path, $Content, $Utf8)
}

$Title = ($Name -split '-' | ForEach-Object { $_.Substring(0, 1).ToUpperInvariant() + $_.Substring(1) }) -join ' '
$Canonical = @"
---
name: $Name
description: $Description
---

# $Title

Add the reusable workflow here. Keep project-specific names, paths, data, and
credentials out of public examples.
"@

$Wrapper = @"
---
name: $Name
description: $Description
---

# $Title Wrapper

This is a thin wrapper. The canonical skill is:

``../../../.skills/$Name/SKILL.md``

Do not duplicate or edit the workflow here. Update the canonical skill, then
regenerate this wrapper if the trigger description changes.
"@

$Instructions = @"
---
applyTo: "**/*"
---

# $Title Wrapper

Use this instruction file only as a GitHub Copilot wrapper for the canonical
skill at:

``../../.skills/$Name/SKILL.md``

Trigger description: $Description

Do not duplicate or edit the workflow here.
"@

Write-SkillFile ".skills/$Name/SKILL.md" $Canonical
Write-SkillFile ".codex/skills/$Name/SKILL.md" $Wrapper
Write-SkillFile ".claude/skills/$Name/SKILL.md" $Wrapper
Write-SkillFile ".github/instructions/$Name.instructions.md" $Instructions