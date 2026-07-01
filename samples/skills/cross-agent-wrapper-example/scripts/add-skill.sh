#!/usr/bin/env sh
set -eu

name="${1:-}"
description="${2:-}"

if [ -z "$name" ] || [ -z "$description" ]; then
  echo "usage: ./add-skill.sh <kebab-case-name> <description>" >&2
  exit 2
fi

case "$name" in
  *[!a-z0-9-]*|''|-*)
    echo "skill name must be kebab-case lowercase letters, numbers, and dashes" >&2
    exit 2
    ;;
esac

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
title=$(printf '%s' "$name" | awk -F- '{ for (i=1; i<=NF; i++) { $i=toupper(substr($i,1,1)) substr($i,2) } print }')

mkdir -p \
  "$root/.skills/$name" \
  "$root/.codex/skills/$name" \
  "$root/.claude/skills/$name" \
  "$root/.github/instructions"

cat > "$root/.skills/$name/SKILL.md" <<EOF
---
name: $name
description: $description
---

# $title

Add the reusable workflow here. Keep project-specific names, paths, data, and
credentials out of public examples.
EOF

cat > "$root/.codex/skills/$name/SKILL.md" <<EOF
---
name: $name
description: $description
---

# $title Wrapper

This is a thin wrapper. The canonical skill is:

\`../../../.skills/$name/SKILL.md\`

Do not duplicate or edit the workflow here.
EOF

cp "$root/.codex/skills/$name/SKILL.md" "$root/.claude/skills/$name/SKILL.md"

cat > "$root/.github/instructions/$name.instructions.md" <<EOF
---
applyTo: "**/*"
---

# $title Wrapper

Use this instruction file only as a GitHub Copilot wrapper for the canonical
skill at:

\`../../.skills/$name/SKILL.md\`

Trigger description: $description

Do not duplicate or edit the workflow here.
EOF