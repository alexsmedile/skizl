# diff — Compare skill versions

Compares two versions of a skill's `SKILL.md` side by side.

## Usage

```
/skizl diff <skill-path>                        # diff local vs global installed
/skizl diff <skill-path-a> <skill-path-b>       # diff two explicit paths
/skizl diff <skill-name>                        # resolve by name then diff
```

## Resolution order

When a single name/path is given:
1. Check `skills/<name>/SKILL.md` in cwd
2. Check `.claude/skills/<name>/SKILL.md`
3. Check `~/.claude/skills/<name>/SKILL.md`

The first match is the **local** version. The global (`~/.claude/skills/`) is the **remote** version.

## Script

```bash
# Resolve paths
LOCAL="$1/SKILL.md"
GLOBAL="$HOME/.claude/skills/$(basename $1)/SKILL.md"

if [ ! -f "$LOCAL" ]; then
  echo "ERROR: $LOCAL not found"
  exit 1
fi

if [ -n "$2" ]; then
  GLOBAL="$2/SKILL.md"
fi

if [ ! -f "$GLOBAL" ]; then
  echo "No comparison target found at $GLOBAL — showing local only"
  cat -n "$LOCAL"
  exit 0
fi

echo "=== diff: $LOCAL  vs  $GLOBAL ==="
diff --color=always -u "$GLOBAL" "$LOCAL" || true
```

## What to report

After running diff:
- If **identical**: "No differences — both versions match."
- If **local is ahead**: show added/changed lines, note the local is newer. Then ask: **"Local is ahead — snapshot current version? (yes / skip)"** — if yes, load `references/snapshot.md` and follow its steps to snapshot the skill.
- If **global is ahead**: warn the user their local copy may be outdated
- If **both differ**: show full diff and ask if they want to sync

## Version check

If both files have a `version:` field in frontmatter, extract and compare:

```bash
local_ver=$(grep '^version:' "$LOCAL" | head -1 | awk '{print $2}')
global_ver=$(grep '^version:' "$GLOBAL" | head -1 | awk '{print $2}')
echo "Local:  $local_ver"
echo "Global: $global_ver"
```
