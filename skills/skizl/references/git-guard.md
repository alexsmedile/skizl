# git-guard — version drift protection via git hooks

Installs a `pre-commit` git hook that checks all version strings in the repo agree before every commit. Uses `core.hooksPath` so hooks are committed to the repo and apply to anyone who clones it.

## Commands

| Command | What it does |
|---|---|
| `skizl git-guard install` | Writes `scripts/hooks/pre-commit`, configures `core.hooksPath`, saves config |
| `skizl git-guard remove` | Removes the script, unsets `core.hooksPath` |
| `skizl git-guard check` | Runs the version check now without committing |

---

## install

### Step 1 — Detect existing hook

```bash
[ -f scripts/hooks/pre-commit ] && echo "exists" || echo "missing"
git config core.hooksPath 2>/dev/null
```

If already installed, ask: **"git-guard is already installed — reinstall? (yes / no)"**

### Step 2 — Ask about SKILL.md inclusion

Skills can be standalone with their own versioning cadence, independent of the plugin manifests. Ask:

> **Should SKILL.md version fields be included in the version check?**
> 1. Yes — include all `skills/*/SKILL.md` files
> 2. No — skip SKILL.md entirely (skill versions are independent)
> 3. Ask per skill — prompt for each skill found in `skills/`

Save the answer to `scripts/hooks/.git-guard.json`:

```json
{
  "skill_check": "all" | "none" | "ask"
}
```

If `"ask"` was chosen and multiple skills exist, list them and ask which to include. Save the result as:

```json
{
  "skill_check": "selected",
  "skill_paths": ["skills/scrapekit/SKILL.md"]
}
```

### Step 3 — Write the hook script

Create `scripts/hooks/` if missing, then write `scripts/hooks/pre-commit`:

```bash
mkdir -p scripts/hooks
```

Make it executable:

```bash
chmod +x scripts/hooks/pre-commit
```

Script content — see **Hook script** section below.

### Step 4 — Configure git

```bash
git config core.hooksPath scripts/hooks
```

### Step 5 — Report

```
✓ git-guard installed

  Hook:    scripts/hooks/pre-commit
  Config:  scripts/hooks/.git-guard.json
  git:     core.hooksPath = scripts/hooks

  SKILL.md check: <all | none | selected: skills/scrapekit/SKILL.md>

  Anyone who clones this repo needs to run once:
    git config core.hooksPath scripts/hooks
```

---

## remove

```bash
rm -f scripts/hooks/pre-commit scripts/hooks/.git-guard.json
git config --unset core.hooksPath
```

If `scripts/hooks/` is now empty, offer to remove it too.

Report: `✓ git-guard removed — core.hooksPath unset`

---

## check

Run the version check manually (same logic as the hook, but never blocks):

```bash
bash scripts/hooks/pre-commit --check
```

Always exits 0. Prints the full version table regardless of result.

---

## Hook script

The script written to `scripts/hooks/pre-commit`:

```bash
#!/usr/bin/env bash
# git-guard — version consistency check
# Managed by skizl git-guard. Edit scripts/hooks/.git-guard.json to configure.

set -uo pipefail

CHECK_ONLY=false
[[ "${1:-}" == "--check" ]] && CHECK_ONLY=true

CONFIG="scripts/hooks/.git-guard.json"
VERSIONS=()   # parallel arrays
LABELS=()

collect() {
  local label="$1" version="$2"
  LABELS+=("$label")
  VERSIONS+=("$version")
}

# ── Collect all version strings ───────────────────────────────────────────────

# .claude-plugin/plugin.json
if [ -f .claude-plugin/plugin.json ]; then
  v=$(jq -r '.version // empty' .claude-plugin/plugin.json 2>/dev/null)
  [ -n "$v" ] && collect ".claude-plugin/plugin.json" "$v"
fi

# .claude-plugin/marketplace.json (metadata.version + plugins[0].version)
if [ -f .claude-plugin/marketplace.json ]; then
  v=$(jq -r '.metadata.version // empty' .claude-plugin/marketplace.json 2>/dev/null)
  [ -n "$v" ] && collect ".claude-plugin/marketplace.json (metadata)" "$v"
  v=$(jq -r '.plugins[0].version // empty' .claude-plugin/marketplace.json 2>/dev/null)
  [ -n "$v" ] && collect ".claude-plugin/marketplace.json (plugins[0])" "$v"
fi

# .codex-plugin/plugin.json
if [ -f .codex-plugin/plugin.json ]; then
  v=$(jq -r '.version // empty' .codex-plugin/plugin.json 2>/dev/null)
  [ -n "$v" ] && collect ".codex-plugin/plugin.json" "$v"
fi

# README.md badge
if [ -f README.md ]; then
  v=$(grep -oE 'version-[0-9]+\.[0-9]+\.[0-9]+' README.md | head -1 | sed 's/version-//')
  [ -n "$v" ] && collect "README.md badge" "$v"
fi

# CHANGELOG.md top entry
if [ -f CHANGELOG.md ]; then
  v=$(grep -oE '^\#\# \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
  [ -n "$v" ] && collect "CHANGELOG.md (top entry)" "$v"
fi

# Latest git tag
v=$(git tag --sort=-version:refname 2>/dev/null | grep -E '^v?[0-9]+\.[0-9]+\.[0-9]+$' | head -1 | sed 's/^v//')
[ -n "$v" ] && collect "git tag (latest)" "$v"

# SKILL.md files — controlled by config
SKILL_CHECK=$(jq -r '.skill_check // "none"' "$CONFIG" 2>/dev/null || echo "none")
if [ "$SKILL_CHECK" = "all" ]; then
  for f in skills/*/SKILL.md; do
    [ -f "$f" ] || continue
    v=$(grep -E '^version:' "$f" | head -1 | sed 's/version:[[:space:]]*//')
    [ -n "$v" ] && collect "$f" "$v"
  done
elif [ "$SKILL_CHECK" = "selected" ]; then
  while IFS= read -r f; do
    [ -f "$f" ] || continue
    v=$(grep -E '^version:' "$f" | head -1 | sed 's/version:[[:space:]]*//')
    [ -n "$v" ] && collect "$f" "$v"
  done < <(jq -r '.skill_paths[]? // empty' "$CONFIG" 2>/dev/null)
fi

# ── Find highest version ───────────────────────────────────────────────────────

HIGHEST=""
for v in "${VERSIONS[@]:-}"; do
  if [ -z "$HIGHEST" ]; then
    HIGHEST="$v"
  else
    # compare semver: sort -V, take last
    HIGHEST=$(printf '%s\n%s' "$HIGHEST" "$v" | sort -V | tail -1)
  fi
done

# ── Print table ───────────────────────────────────────────────────────────────

DRIFT=0
echo ""
echo "version check"
echo "─────────────────────────────────────────────────"
printf "  %-42s %s\n" "source of truth (highest found):" "$HIGHEST"
echo ""
for i in "${!LABELS[@]}"; do
  label="${LABELS[$i]}"
  ver="${VERSIONS[$i]}"
  if [ "$ver" = "$HIGHEST" ]; then
    mark="✓"
  else
    mark="✗"
    DRIFT=1
  fi
  printf "  %s  %-40s %s\n" "$mark" "$label" "$ver"
done
echo ""

# ── Block or pass ─────────────────────────────────────────────────────────────

if [ "$DRIFT" -eq 1 ] && [ "$CHECK_ONLY" = false ]; then
  echo "  version mismatch — commit blocked"
  echo "  update the ✗ files to $HIGHEST, then commit again"
  echo ""
  exit 1
fi

[ "$DRIFT" -eq 0 ] && echo "  all versions consistent ✓"
echo ""
exit 0
```

---

## Notes

- `core.hooksPath` requires git ≥ 2.9 (released 2016 — safe to assume)
- Anyone who clones the repo must run `git config core.hooksPath scripts/hooks` once — add this to the repo README under a "Development" section
- The hook never modifies files — it only checks and blocks; fixing is always the developer's job
- Git tag comparison uses `sort -V` (version sort) — available on macOS via `gsort` (coreutils) or native on Linux; on macOS without coreutils the tag check degrades gracefully (skips if `sort -V` fails)
- To bypass in an emergency: `git commit --no-verify` — but this should be rare
