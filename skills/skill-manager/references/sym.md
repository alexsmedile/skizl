# sym — Symlink skill installation

Ensures skills in `skills/` are registered into `.claude/skills/` and `.agents/skills/` as portable relative symlinks.

## Convention

```
<project-root>/
├── skills/
│   └── <name>/SKILL.md          ← source of truth
├── .claude/
│   └── skills/
│       └── <name> → ../../skills/<name>   ← relative symlink (portable)
└── .agents/
    └── skills/
        └── <name> → ../../skills/<name>   ← relative symlink (portable)
```

Skills live once in `skills/` and are symlinked into both locations. Relative paths survive the project being moved, renamed, or cloned.

---

## Commands

| Sub-command | Shorthand | What it does |
|-------------|-----------|--------------|
| `sym init` | `sym in` | Link all skills from `skills/` into `.claude/skills/` and `.agents/skills/` |
| `sym migrate` | `sym out` | Move real dirs from `.claude/skills/` into `skills/` and re-link |
| `sym status` | — | Show what's linked, what's missing |

### `/skizl sym init` / `/skizl sym in`

Links all skills from `skills/` into `.claude/skills/` and `.agents/skills/` that aren't already symlinked.

```bash
PROJECT=$(pwd)
mkdir -p "$PROJECT/.claude/skills" "$PROJECT/.agents/skills"

linked=0
for s in "$PROJECT/skills"/*/; do
  [ -d "$s" ] || continue
  name=$(basename "$s")
  claude_link="$PROJECT/.claude/skills/$name"
  agents_link="$PROJECT/.agents/skills/$name"

  if [ ! -e "$claude_link" ] && [ ! -L "$claude_link" ]; then
    ln -s "../../skills/$name" "$claude_link"
    echo "linked .claude/skills/$name"
    linked=$((linked + 1))
  else
    echo "skipped .claude/skills/$name (already exists)"
  fi

  if [ ! -e "$agents_link" ] && [ ! -L "$agents_link" ]; then
    ln -s "../../skills/$name" "$agents_link"
    echo "linked .agents/skills/$name"
  else
    echo "skipped .agents/skills/$name (already exists)"
  fi
done

echo ""
echo "Done. $linked skill(s) linked."
ls -la "$PROJECT/.claude/skills/"
```

---

### `/skizl sym migrate` / `/skizl sym out`

Moves any **real directories** from `.claude/skills/` into `skills/` and creates relative symlinks in both `.claude/skills/` and `.agents/skills/`. Leaves existing symlinks untouched.

```bash
PROJECT=$(pwd)
mkdir -p "$PROJECT/skills" "$PROJECT/.claude/skills" "$PROJECT/.agents/skills"

migrated=0
for s in "$PROJECT/.claude/skills"/*/; do
  name=$(basename "$s")
  src="$PROJECT/.claude/skills/$name"

  # Skip if already a symlink
  [ -L "$src" ] && echo "skipped $name (already a symlink)" && continue
  # Skip if not a directory
  [ -d "$src" ] || continue

  dest="$PROJECT/skills/$name"

  # Warn if destination already exists
  if [ -e "$dest" ]; then
    echo "WARNING: skills/$name already exists — skipping $name"
    continue
  fi

  mv "$src" "$dest"
  ln -s "../../skills/$name" "$PROJECT/.claude/skills/$name"
  ln -s "../../skills/$name" "$PROJECT/.agents/skills/$name"
  echo "migrated $name → skills/$name"
  migrated=$((migrated + 1))
done

echo ""
echo "Done. $migrated skill(s) migrated."
ls -la "$PROJECT/.claude/skills/"
```

---

### `/skizl sym status`

Shows the current state of all skills — what's in `skills/`, what's linked, what's missing.

```bash
PROJECT=$(pwd)
echo "=== skills/ ==="
ls "$PROJECT/skills/" 2>/dev/null || echo "(empty)"

echo ""
echo "=== .claude/skills/ ==="
ls -la "$PROJECT/.claude/skills/" 2>/dev/null || echo "(empty)"

echo ""
echo "=== .agents/skills/ ==="
ls -la "$PROJECT/.agents/skills/" 2>/dev/null || echo "(empty)"

echo ""
echo "=== Unlinked in skills/ (not yet in .claude/skills/) ==="
for s in "$PROJECT/skills"/*/; do
  name=$(basename "$s")
  [ -e "$PROJECT/.claude/skills/$name" ] || echo "  missing: $name"
done
```

---

## Notes

- Always use **relative symlinks** (`../../skills/<name>`) — never absolute paths
- `init` is safe to re-run: skips skills that are already linked
- `migrate` only moves real directories — existing symlinks are untouched
- After `migrate`, verify with `ls -la .claude/skills/` that all entries are symlinks (`->`)
- If a skill lives outside the project entirely (e.g. `~/.claude/skills/`), use an absolute path as the symlink target since relative paths can't reach across unrelated directories
