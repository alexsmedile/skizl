# archive — Full skill folder backup

Archives the entire skill folder as a timestamped tarball. Unlike `snapshot` (which saves only `SKILL.md`), `archive` captures every file in the skill directory: `references/`, `scripts/`, `versions/`, `examples/`, etc.

**Always manual** — never auto-triggered. Skizl may *suggest* it when a diff reveals large-scale changes.

---

## Usage

```
/skizl archive <skill-path>                        # archive to _backups/ at the repo root
/skizl archive <skill-path> --dest <directory>     # archive to a specific directory
/skizl archive <skill-path> --tag <label>          # add a human label to the filename
```

**Examples:**
```
/skizl archive skills/my-skill
/skizl archive skills/my-skill --dest _backups/
/skizl archive skills/my-skill --tag before-refactor
```

---

## Behavior

1. Resolve the skill folder path.
2. Determine destination:
   - Default: `_backups/` at the repository root level (create if missing).
   - `--dest <dir>`: use that directory (create if missing).
3. Build filename: `<skill-name>@<timestamp>[--<tag>].tar.gz`
   - Timestamp format: `YYYYMMDD-HHMM` (local time)
   - Example: `my-skill@20260510-1430.tar.gz`
   - With tag: `my-skill@20260510-1430--before-refactor.tar.gz`
4. Run:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || dirname "$(dirname <skill-path>)")
DEST="${dest:-$REPO_ROOT/_backups}"
mkdir -p "$DEST"
STAMP=$(date +%Y%m%d-%H%M)
NAME=$(basename <skill-path>)
TAG=${tag:+--$tag}
OUTFILE="$DEST/${NAME}@${STAMP}${TAG}.tar.gz"
tar -czf "$OUTFILE" -C "$(dirname <skill-path>)" "$NAME"
echo "✓ Archive saved: $OUTFILE"
```

5. Report file size:

```
✓ Archive saved: _backups/my-skill@20260510-1430.tar.gz  (42 KB)
```

---

## Suggest archive on large diffs

When `/skizl diff` shows a large-scale change (many lines added/removed, or structural changes across multiple reference files), offer:

> **This diff is substantial — archive the full skill folder before continuing? (yes / skip)**

If yes: load `references/archive.md` and follow its steps to archive the skill with default destination. If skip: continue with the original diff flow.

**"Large-scale" heuristic** (use judgment):
- More than ~30 lines changed total, or
- Changes span 3+ files in the skill folder, or
- The user signals intent to rewrite/restructure ("refactor", "redo", "start over")

---

## Intent detection

Skizl should understand natural-language requests and route to `archive`:

| User says | Action |
|-----------|--------|
| "archive skills/my-skill" | archive with default dest |
| "backup skills/my-skill before I refactor it" | archive with `--tag before-refactor` |
| "save a full copy of this skill" | archive (not snapshot — full folder) |
| "zip up the skill" | archive |
| "I want to keep a copy before major changes" | archive, ask which skill |

If intent is ambiguous between `snapshot` (SKILL.md only) and `archive` (full folder), ask:

> **Save just SKILL.md (snapshot) or the entire skill folder (archive)?**

---

## What's included

Everything inside `<skill-path>/`:

```
my-skill/
├── SKILL.md
├── references/
├── scripts/
├── versions/        ← snapshots are included in the archive
├── examples/
├── templates/
├── docs/
└── evals/
```

Archives are complete and self-contained — restoring is a simple `tar -xzf`.

---

## _backups/ convention

- Default destination: `_backups/` at the repository root level (i.e., next to `skills/` or `agents/`)
- `_backups/` is gitignored by default (added by `/skizl publish` via `.gitignore`)
- Never delete archives manually without explicit user instruction
- No automatic cleanup — archives accumulate until manually removed
