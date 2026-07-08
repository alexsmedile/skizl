# doctor — Diagnose skill installation

Checks the health of installed skills and reports issues.

## Usage

```
/skizl doctor              # check all skills in .claude/skills/ and skills/
/skizl doctor <name>       # check a specific skill
```

## Checks performed

| Check | What it catches |
|-------|----------------|
| Broken symlinks | Symlink exists in `.claude/skills/` but target is missing |
| Missing SKILL.md | Skill folder exists but has no `SKILL.md` |
| Direct directories | Real dirs in `.claude/skills/` that should be in `skills/` and symlinked |
| Orphaned agents links | `.agents/skills/<name>` missing when `.claude/skills/<name>` exists |
| Empty skill | `SKILL.md` exists but has no frontmatter or description |
| Name mismatch | `name:` in frontmatter differs from folder name |
| Long description | Frontmatter `description:` alone is over Codex's 1024-character limit, or close enough to shorten |

## Script

```bash
PROJECT=$(pwd)
CLAUDE_SKILLS="$PROJECT/.claude/skills"
AGENTS_SKILLS="$PROJECT/.agents/skills"
SOURCE="$PROJECT/skills"
DESCRIPTION_LIMIT=1024
DESCRIPTION_TARGET=900

issues=0
warnings=0

check_description() {
  skill_file="$1"
  label="$2"

  [ -f "$skill_file" ] || return

  # Codex enforces the limit on description alone, not description + when_to_use.
  desc=$(awk '
    /^description:[[:space:]]*[>|]?[[:space:]]*$/ { capture=1; next }
    /^description:[[:space:]]*/ {
      sub(/^description:[[:space:]]*/, "")
      print
      exit
    }
    capture && /^[^[:space:]]/ { exit }
    capture {
      sub(/^[[:space:]]+/, "")
      print
    }
  ' "$skill_file" | tr '\n' ' ' | sed 's/[[:space:]][[:space:]]*/ /g; s/^ //; s/ $//')

  if [ -z "$desc" ]; then
    echo "  [EMPTY]   $label has no description"
    issues=$((issues + 1))
    return
  fi

  len=${#desc}
  if [ "$len" -gt "$DESCRIPTION_LIMIT" ]; then
    echo "  [TOO_LONG] $label description is ${len} chars (Codex limit: ${DESCRIPTION_LIMIT})"
    issues=$((issues + 1))
  elif [ "$len" -gt "$DESCRIPTION_TARGET" ]; then
    echo "  [WARN]    $label description is ${len} chars (target: <=${DESCRIPTION_TARGET}, limit: ${DESCRIPTION_LIMIT})"
    warnings=$((warnings + 1))
  fi
}

echo "=== skizl doctor ==="
echo ""

# Check .claude/skills/
if [ -d "$CLAUDE_SKILLS" ]; then
  for entry in "$CLAUDE_SKILLS"/*/; do
    [ -e "$entry" ] || [ -L "$entry" ] || continue
    name=$(basename "$entry")
    link="$CLAUDE_SKILLS/$name"

    # Broken symlink
    if [ -L "$link" ] && [ ! -e "$link" ]; then
      echo "  [BROKEN]  .claude/skills/$name → $(readlink $link) (target missing)"
      issues=$((issues + 1))
      continue
    fi

    # Direct directory (not symlinked)
    if [ ! -L "$link" ] && [ -d "$link" ]; then
      echo "  [DIRECT]  .claude/skills/$name is a real directory — consider: /skizl sym migrate"
      issues=$((issues + 1))
    fi

    # Missing SKILL.md
    if [ ! -f "$link/SKILL.md" ]; then
      echo "  [NO_SKILL] .claude/skills/$name has no SKILL.md"
      issues=$((issues + 1))
    else
      check_description "$link/SKILL.md" ".claude/skills/$name"
    fi

    # Orphaned .agents/skills link
    if [ ! -e "$AGENTS_SKILLS/$name" ] && [ ! -L "$AGENTS_SKILLS/$name" ]; then
      echo "  [NO_AGENT] .agents/skills/$name missing — run: /skizl sym init"
      issues=$((issues + 1))
    fi
  done
else
  echo "  .claude/skills/ not found"
fi

# Check skills/ source
if [ -d "$SOURCE" ]; then
  for s in "$SOURCE"/*/; do
    name=$(basename "$s")

    # Missing SKILL.md
    if [ ! -f "$s/SKILL.md" ]; then
      echo "  [NO_SKILL] skills/$name has no SKILL.md"
      issues=$((issues + 1))
    else
      check_description "$s/SKILL.md" "skills/$name"
    fi

    # Not linked
    if [ ! -e "$CLAUDE_SKILLS/$name" ] && [ ! -L "$CLAUDE_SKILLS/$name" ]; then
      echo "  [UNLINKED] skills/$name not linked — run: /skizl sym init"
      issues=$((issues + 1))
    fi
  done
fi

echo ""
if [ $issues -eq 0 ]; then
  if [ $warnings -eq 0 ]; then
    echo "✓ All good. No issues found."
  else
    echo "✓ No blocking issues found. $warnings warning(s)."
  fi
else
  echo "✗ $issues issue(s) found."
fi
```

## Fix suggestions

After listing issues, suggest the appropriate fix command for each:

| Issue | Suggested fix |
|-------|--------------|
| Broken symlink | `rm .claude/skills/<name>` then `/skizl sym init` |
| Direct directory | `/skizl sym migrate` |
| Missing SKILL.md | Create minimal `SKILL.md` scaffold |
| No agents link | `/skizl sym init` |
| Unlinked in skills/ | `/skizl sym init` |
| Empty description | Add a concise `description:` to frontmatter |
| Long description | Rewrite under 900 chars; 1024 is the Codex hard limit |
