# list — Show installed skills

Displays all skills across the three standard locations with their symlink state.

## Usage

```
skizl list
skizl list --global       # only ~/.claude/skills/
skizl list --project      # only .claude/skills/ in cwd
```

## What it shows

For each skill found, report:
- **Name**
- **Location** — `global` (`~/.claude/skills/`), `project` (`.claude/skills/`), or `source` (`skills/`)
- **State** — one of:
  - `linked` — symlink exists and resolves correctly
  - `source` — real directory in `skills/`, not yet symlinked
  - `broken` — symlink exists but target is missing
  - `direct` — real directory sitting directly in `.claude/skills/` (not yet migrated)

## Script

```bash
PROJECT=$(pwd)
GLOBAL="$HOME/.claude/skills"
PROJECT_CLAUDE="$PROJECT/.claude/skills"
SOURCE="$PROJECT/skills"

echo "=== Global (~/.claude/skills/) ==="
if [ -d "$GLOBAL" ]; then
  for s in "$GLOBAL"/*/; do
    name=$(basename "$s")
    if [ -L "$GLOBAL/$name" ]; then
      target=$(readlink "$GLOBAL/$name")
      if [ -e "$GLOBAL/$name" ]; then
        echo "  ✓ $name  [linked → $target]"
      else
        echo "  ✗ $name  [broken → $target]"
      fi
    else
      echo "  • $name  [direct]"
    fi
  done
else
  echo "  (not found)"
fi

echo ""
echo "=== Project (.claude/skills/) ==="
if [ -d "$PROJECT_CLAUDE" ]; then
  for s in "$PROJECT_CLAUDE"/*/; do
    [ -e "$s" ] || [ -L "$s" ] || continue
    name=$(basename "$s")
    if [ -L "$PROJECT_CLAUDE/$name" ]; then
      target=$(readlink "$PROJECT_CLAUDE/$name")
      if [ -e "$PROJECT_CLAUDE/$name" ]; then
        echo "  ✓ $name  [linked → $target]"
      else
        echo "  ✗ $name  [broken → $target]"
      fi
    else
      echo "  • $name  [direct]"
    fi
  done
else
  echo "  (not found)"
fi

echo ""
echo "=== Source (skills/) ==="
if [ -d "$SOURCE" ]; then
  for s in "$SOURCE"/*/; do
    name=$(basename "$s")
    linked=""
    [ -L "$PROJECT_CLAUDE/$name" ] && linked=" → linked in .claude/skills/"
    [ -L "$GLOBAL/$name" ] && linked="$linked → linked in global"
    echo "  • $name$linked"
  done
else
  echo "  (not found)"
fi
```

## Output example

```
=== Global (~/.claude/skills/) ===
  ✓ scrapekit  [linked → /path/to/skills_db/scrapekit]
  ✓ grill-me   [linked → /path/to/skills_db/grill-me]

=== Project (.claude/skills/) ===
  ✓ skill-manager  [linked → ../../skills/skill-manager]
  ✗ old-skill      [broken → ../../skills/old-skill]

=== Source (skills/) ===
  • skill-manager  → linked in .claude/skills/
  • draft-skill
```
