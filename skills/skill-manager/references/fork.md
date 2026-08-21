# fork — Clone a skill as a personal variant

Use this when: cloning a local or remote skill as a personal variant.

Copies a skill into `skills/<new-name>/` and symlinks it, ready for local customization.
The source can be a local path or a GitHub repo URL.

## Usage

```
/skizl fork <source> [--name <new-name>]
```

**Examples:**
```
/skizl fork ~/.claude/skills/grill-me --name my-grill
/skizl fork https://github.com/<username>/skilz
/skizl fork https://github.com/user/repo --name my-variant
/skizl fork skills/cs --name cs-v2
```

## Source types

| Source | How it's handled |
|--------|-----------------|
| Local path | Copied with `cp -r` |
| GitHub repo URL (`https://github.com/...`) | Cloned with `git clone --depth 1`, then `.git/` removed |
| GitHub shorthand (`user/repo`) | Expanded to `https://github.com/user/repo` |

## Steps

### 1 — Resolve source and name

```bash
SOURCE="$1"
NEW_NAME="${2:-}"   # from --name flag, or derived below

# If no --name given, derive from source
if [ -z "$NEW_NAME" ]; then
  # local path: use folder name
  # GitHub URL: use repo name (last segment, strip .git)
  NEW_NAME=$(basename "$SOURCE" .git)
fi

DEST="$(pwd)/skills/$NEW_NAME"
```

### 2 — Check destination doesn't exist

```bash
if [ -e "$DEST" ]; then
  echo "ERROR: skills/$NEW_NAME already exists. Choose a different name with --name."
  exit 1
fi
```

### 3 — Copy or clone

**Local source:**
```bash
cp -r "$SOURCE" "$DEST"
echo "Copied $SOURCE → skills/$NEW_NAME"
```

**GitHub URL:**
```bash
git clone --depth 1 "$SOURCE" "$DEST"
rm -rf "$DEST/.git"
echo "Cloned $SOURCE → skills/$NEW_NAME (git history stripped)"
```

### 4 — Update frontmatter name

If the forked skill has `name:` in frontmatter, update it to match the new folder name so Claude loads it under the right name:

```bash
SKILL_FILE="$DEST/SKILL.md"
if [ -f "$SKILL_FILE" ]; then
  sed -i '' "s/^name: .*/name: $NEW_NAME/" "$SKILL_FILE"
  echo "Updated name: $NEW_NAME in SKILL.md"
fi
```

### 5 — Symlink

```bash
mkdir -p "$(pwd)/.claude/skills" "$(pwd)/.agents/skills"
ln -s "../../skills/$NEW_NAME" "$(pwd)/.claude/skills/$NEW_NAME"
ln -s "../../skills/$NEW_NAME" "$(pwd)/.agents/skills/$NEW_NAME"
echo "Linked → .claude/skills/$NEW_NAME"
echo "Linked → .agents/skills/$NEW_NAME"
```

### 6 — Report

```
✓ Forked as: skills/$NEW_NAME
  Source: <original source>
  Linked: .claude/skills/$NEW_NAME → ../../skills/$NEW_NAME
  Edit:   skills/$NEW_NAME/SKILL.md
```

## Notes

- The fork is a clean copy — no connection to the original after cloning
- To track upstream changes later, use `/skizl diff skills/<name> <original-source>`
- If the source is a bundle repo (multiple skills inside `skills/`), fork picks the whole repo — user can then run `/skizl unpack` to extract individual skills
