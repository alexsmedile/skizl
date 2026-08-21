# git-guard — version drift protection via git hooks

Use this when: installing, removing, or checking the pre-commit version consistency hook.

Installs a `pre-commit` git hook that checks all version strings in the repo agree before every commit. Uses `core.hooksPath` so hooks are committed to the repo and apply to anyone who clones it.

## Commands

| Command | What it does |
|---|---|
| `/skizl git-guard install` | Writes `scripts/hooks/pre-commit`, configures `core.hooksPath`, saves config |
| `/skizl git-guard remove` | Removes the script, unsets `core.hooksPath` |
| `/skizl git-guard check` | Runs the version check now without committing |

---

## install

### Step 1 — Gather all inputs (before any writes)

Collect everything needed upfront so the install runs without interruption.

**1a — Detect existing hook**

```bash
[ -f scripts/hooks/pre-commit ] && echo "exists" || echo "missing"
git config core.hooksPath 2>/dev/null
```

If already installed, ask: **"git-guard is already installed — reinstall? (yes / no)"**
If no, stop here.

**1b — Ask about SKILL.md inclusion**

Skills can be standalone with their own versioning cadence, independent of the plugin manifests. Ask:

> **Should SKILL.md version fields be included in the version check?**
> 1. Yes — include all `skills/*/SKILL.md` files
> 2. No — skip SKILL.md entirely (skill versions are independent)
> 3. Ask per skill — prompt for each skill found in `skills/`

If `"Ask per skill"` was chosen and multiple skills exist, list them and ask which to include.

Hold all answers in memory — **do not write any files until Step 2.**

### Step 2 — Write the hook script

Create `scripts/hooks/` if missing, then write `scripts/hooks/pre-commit`:

```bash
mkdir -p scripts/hooks
```

Write `scripts/hooks/.git-guard.json` using the answers from Step 1b. You can also manually configure `cli_version` in this file to enforce a CLI version constant (e.g. `SPECTACULAR_VERSION` in `cli/spectacular`):

```json
{
  "skill_check": "all" | "none" | "ask",
  "cli_version": {
    "file": "cli/spectacular",
    "variable": "SPECTACULAR_VERSION"
  }
}
```

If `"ask"` resolved to specific skills, save instead:

```json
{
  "skill_check": "selected",
  "skill_paths": ["skills/scrapekit/SKILL.md"],
  "cli_version": {
    "file": "cli/spectacular",
    "variable": "SPECTACULAR_VERSION"
  }
}
```

Make the hook executable:

```bash
chmod +x scripts/hooks/pre-commit
```

Script content — see **Hook script** section below.

### Step 3 — Configure git

```bash
git config core.hooksPath scripts/hooks
```

### Step 4 — Report

```
✓ git-guard installed

  Hook:    scripts/hooks/pre-commit
  Config:  scripts/hooks/.git-guard.json
  git:     core.hooksPath = scripts/hooks

  SKILL.md check: <all | none | selected: skills/scrapekit/SKILL.md>

  Anyone who clones this repo needs to run once:
    git config core.hooksPath scripts/hooks

  Note: the git tag is allowed to lag behind (you commit first, tag after).
  The hook only blocks if a tag is somehow ahead of the manifest versions.
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

# Anchor all paths to repo root so the hook works regardless of CWD
ROOT="$(git rev-parse --show-toplevel)"
CONFIG="$ROOT/scripts/hooks/.git-guard.json"
VERSIONS=()   # parallel arrays
LABELS=()
TYPES=()      # "version" | "tag"

collect() {
  local label="$1" version="$2" type="${3:-version}"
  LABELS+=("$label")
  VERSIONS+=("$version")
  TYPES+=("$type")
}

# semver_max <a> <b> — returns the higher of two semver strings
# Uses gsort -V on macOS (coreutils), falls back to sort -V on Linux.
# Pure-bash fallback for environments where neither supports -V correctly.
semver_max() {
  local a="$1" b="$2"
  local sortcmd
  if gsort --version &>/dev/null 2>&1; then
    sortcmd="gsort"
  else
    sortcmd="sort"
  fi
  # Validate that version sort actually orders 1.9 < 1.10 correctly
  if printf '1.9.0\n1.10.0\n' | "$sortcmd" -V | tail -1 | grep -q '1.10.0'; then
    printf '%s\n%s' "$a" "$b" | "$sortcmd" -V | tail -1
  else
    # Pure-bash semver compare fallback
    local IFS=.
    local -a av=($a) bv=($b)
    for i in 0 1 2; do
      local ai="${av[$i]:-0}" bi="${bv[$i]:-0}"
      if (( ai > bi )); then echo "$a"; return; fi
      if (( bi > ai )); then echo "$b"; return; fi
    done
    echo "$a"  # equal
  fi
}

get_skill_version() {
  local file="$1"
  [ -f "$file" ] || return 1

  # Extract frontmatter (lines between first --- and second ---)
  local fm
  fm=$(awk '
    BEGIN { show=0; count=0 }
    /^---$/ {
      count++
      if (count == 1) { show=1; next }
      if (count == 2) { show=0; exit }
    }
    { if (show) print }
  ' "$file")

  # Detect if both formats exist
  local has_top=0
  local has_meta=0
  local top_val=""
  local meta_val=""

  # Read top-level version
  top_val=$(echo "$fm" | awk '
    /^[[:space:]]*version:[[:space:]]*/ {
      sub(/^[[:space:]]*version:[[:space:]]*/, "")
      gsub(/^["\x27]|["\x27]$/, "")
      print $0
      exit
    }
  ')
  [ -n "$top_val" ] && has_top=1

  # Read metadata.version
  meta_val=$(echo "$fm" | awk '
    BEGIN { in_metadata=0; ver="" }
    /^metadata:[[:space:]]*$/ { in_metadata=1; next }
    /^[a-zA-Z0-9_-]+:[[:space:]]*/ { if ($0 !~ /^metadata:/) in_metadata=0 }
    in_metadata && /^[[:space:]]+version:[[:space:]]*/ {
      sub(/^[[:space:]]+version:[[:space:]]*/, "")
      gsub(/^["\x27]|["\x27]$/, "")
      ver=$0
      exit
    }
    END { print ver }
  ')
  [ -n "$meta_val" ] && has_meta=1

  if [ "$has_top" -eq 1 ] && [ "$has_meta" -eq 1 ]; then
    echo "  [CONFLICT] $file has both top-level version ($top_val) and metadata.version ($meta_val). metadata.version wins." >&2
    echo "$meta_val"
  elif [ "$has_meta" -eq 1 ]; then
    echo "$meta_val"
  else
    echo "$top_val"
  fi
}

# ── Collect all version strings ───────────────────────────────────────────────

# .claude-plugin/plugin.json
if [ -f "$ROOT/.claude-plugin/plugin.json" ]; then
  v=$(jq -r '.version // empty' "$ROOT/.claude-plugin/plugin.json" 2>/dev/null)
  [ -n "$v" ] && collect ".claude-plugin/plugin.json" "$v"
fi

# .claude-plugin/marketplace.json (metadata.version + plugins[0].version)
if [ -f "$ROOT/.claude-plugin/marketplace.json" ]; then
  v=$(jq -r '.metadata.version // empty' "$ROOT/.claude-plugin/marketplace.json" 2>/dev/null)
  [ -n "$v" ] && collect ".claude-plugin/marketplace.json (metadata)" "$v"
  v=$(jq -r '.plugins[0].version // empty' "$ROOT/.claude-plugin/marketplace.json" 2>/dev/null)
  [ -n "$v" ] && collect ".claude-plugin/marketplace.json (plugins[0])" "$v"
fi

# .codex-plugin/plugin.json
if [ -f "$ROOT/.codex-plugin/plugin.json" ]; then
  v=$(jq -r '.version // empty' "$ROOT/.codex-plugin/plugin.json" 2>/dev/null)
  [ -n "$v" ] && collect ".codex-plugin/plugin.json" "$v"
fi

# README.md badge
if [ -f "$ROOT/README.md" ]; then
  v=$(grep -oE 'version-[0-9]+\.[0-9]+\.[0-9]+' "$ROOT/README.md" | head -1 | sed 's/version-//')
  [ -n "$v" ] && collect "README.md badge" "$v"
fi

# CHANGELOG.md top entry
if [ -f "$ROOT/CHANGELOG.md" ]; then
  v=$(grep -oE '^\#\# \[[0-9]+\.[0-9]+\.[0-9]+\]' "$ROOT/CHANGELOG.md" | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
  [ -n "$v" ] && collect "CHANGELOG.md (top entry)" "$v"
fi

# Latest git tag (type "tag" — only blocks if tag is ahead of manifests)
v=$(git -C "$ROOT" tag --sort=-version:refname 2>/dev/null | grep -E '^v?[0-9]+\.[0-9]+\.[0-9]+$' | head -1 | sed 's/^v//')
[ -n "$v" ] && collect "git tag (latest)" "$v" "tag"

# SKILL.md files — controlled by config
SKILL_CHECK=$(jq -r '.skill_check // "none"' "$CONFIG" 2>/dev/null || echo "none")
if [ "$SKILL_CHECK" = "all" ]; then
  for f in "$ROOT"/skills/*/SKILL.md; do
    [ -f "$f" ] || continue
    v=$(get_skill_version "$f")
    [ -n "$v" ] && collect "${f#$ROOT/}" "$v"
  done
elif [ "$SKILL_CHECK" = "selected" ]; then
  while IFS= read -r f; do
    [ -f "$ROOT/$f" ] || continue
    v=$(get_skill_version "$ROOT/$f")
    [ -n "$v" ] && collect "$f" "$v"
  done < <(jq -r '.skill_paths[]? // empty' "$CONFIG" 2>/dev/null)
fi

# CLI constant check — controlled by config
if [ -f "$CONFIG" ]; then
  CLI_FILE=$(jq -r '.cli_version.file // empty' "$CONFIG" 2>/dev/null)
  CLI_VAR=$(jq -r '.cli_version.variable // empty' "$CONFIG" 2>/dev/null)
  if [ -n "$CLI_FILE" ] && [ -n "$CLI_VAR" ] && [ -f "$ROOT/$CLI_FILE" ]; then
    v=$(grep -E "^[[:space:]]*${CLI_VAR}=" "$ROOT/$CLI_FILE" | head -1 | cut -d'=' -f2- | sed -E 's/^[[:space:]]*["\x27]?//; s/["\x27]?[[:space:]]*$//')
    [ -n "$v" ] && collect "$CLI_FILE ($CLI_VAR)" "$v"
  fi
fi

# ── Guard: nothing to check ───────────────────────────────────────────────────

if [ ${#VERSIONS[@]} -eq 0 ]; then
  echo ""
  echo "  git-guard: no version sources found — nothing to check"
  echo ""
  exit 0
fi

# ── Find highest version ───────────────────────────────────────────────────────

HIGHEST=""
for v in "${VERSIONS[@]+"${VERSIONS[@]}"}"; do
  if [ -z "$HIGHEST" ]; then
    HIGHEST="$v"
  else
    HIGHEST=$(semver_max "$HIGHEST" "$v")
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
  type="${TYPES[$i]}"
  if [ "$type" = "tag" ]; then
    # Tag may lag (not yet released) — only flag if tag is ahead of manifests
    if [ "$(semver_max "$ver" "$HIGHEST")" = "$ver" ] && [ "$ver" != "$HIGHEST" ]; then
      mark="✗"  # tag is ahead — manifests need updating
      DRIFT=1
    else
      mark="✓"  # tag is behind or equal — fine
    fi
  else
    if [ "$ver" = "$HIGHEST" ]; then
      mark="✓"
    else
      mark="✗"
      DRIFT=1
    fi
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
- `sort -V` on macOS BSD sort does not correctly order semver (e.g. `1.9 < 1.10`). The hook uses `gsort -V` (coreutils) when available, with a pure-bash fallback for environments where neither works correctly. Install via `brew install coreutils` for reliable sorting.
- To bypass in an emergency: `git commit --no-verify` — but this should be rare
