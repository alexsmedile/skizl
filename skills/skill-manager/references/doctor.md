# doctor — Diagnose skill installation

Use this when: diagnosing broken symlinks, missing files, or manifest version drift.

Checks the health of installed skills and reports issues.

## Usage

```
/skizl doctor              # check the current project
/skizl doctor <name>       # check a specific skill
/skizl doctor --scope user # check user-level installs (~/.claude, ~/.agents, …)
/skizl doctor --scope all  # project + user + plugin/marketplace layer
```

Default scope is `project`. Skills break just as often at **user scope** and in
the **plugin layer**, and neither is visible from `$(pwd)` — see
[Plugin and marketplace health](#plugin-and-marketplace-health).

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
| Non-conformant manifest | Root `plugin.json` missing, wrong `$schema`, bad `name`, or unknown top-level fields (the Agent Plugins schema is closed) |
| Undiscoverable skill | A `skills/<name>/` folder with no immediate-child `SKILL.md` — clients do not recurse, so it silently never loads |
| Untyped MCP server | An `mcp.json` entry missing its explicit `type`, or using deprecated `sse` |
| Dead plugin variable | `PLUGIN_ROOT`/`PLUGIN_DATA` used in `command`, `url`, or headers, where they never expand |
| Missing hook script | A `hooks.json` entry pointing at a script that does not exist, or exists but is not executable — fails silently at run time |
| Unparseable vendor config | Antigravity's root `hooks.json` or `mcp_config.json` present but not valid JSON |
| Stale marketplace clone | Installed plugin version differs from the version its marketplace clone now declares |
| Local-source marketplace | Codex marketplace added from a local path — `marketplace upgrade` skips it, so its plugins never update |
| Escaping source path | A marketplace manifest whose plugin `source.path` resolves outside the marketplace root |
| Orphaned plugin folder | Plugin directory superseded by a versioned cache install and no longer referenced |

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

## User-scope checks (`--scope user`)

Same symlink logic, run against the user-level install dirs instead of `$(pwd)`.
Each harness keeps skills in its own place:

| Harness | User-level skills dir |
|---------|----------------------|
| Claude Code | `~/.claude/skills/`, agents in `~/.claude/agents/` |
| Codex | `~/.codex/skills/` |
| opencode | `~/.config/opencode/skills/` (also `agents/`, `commands/`, `plugins/`) |
| Antigravity CLI (`agy`) | `~/.gemini/antigravity-cli/plugins/`, skills in `~/.gemini/antigravity-cli/` |
| Antigravity 2.0 desktop | `~/.gemini/config/plugins/`, app skills in `~/.gemini/antigravity/skills/` |
| Shared library | `~/.agents/skills/` |

```bash
for dir in ~/.claude/skills ~/.claude/agents ~/.agents/skills \
           ~/.config/opencode/skills ~/.codex/skills; do
  [ -d "$dir" ] || continue
  find "$dir" -maxdepth 1 -type l ! -exec test -e {} \; -print 2>/dev/null \
    | while read -r link; do
        echo "  [BROKEN]  $link -> $(readlink "$link")"
      done
done
```

A dead link here is silent: the skill simply never loads, with no error. This is
the single most common breakage — a source folder gets renamed or moved and every
link into it stops resolving.

## Manifest conformance (Agent Plugins)

Run this whenever the target repo is a plugin root — it validates the portable
manifest before any vendor-specific install path is considered. A plugin whose
root `plugin.json` fails here is not installable on any conformant host, and the
failure is silent at install time on most of them.

```bash
python3 <path-to>/skill-forge/scripts/check.py <plugin-root> --plugin --profile <profile>
```

This validates, in order:

1. **Manifest** — `plugin.json` exists, parses, declares the Agent Plugins
   `$schema`, and carries a legal `name`. The schema is **closed**, so any
   unknown top-level field is an error, not a warning.
2. **`mcp.json`** — every server declares an explicit `type`; its `$schema`
   version matches `plugin.json`'s; and `PLUGIN_ROOT`/`PLUGIN_DATA` appear only
   where they actually expand (`args`, `env` values, `cwd`) — never in
   `command`, URLs, or headers, where they ship as a literal string.
3. **Skills** — each immediate child of `skills/` holding a `SKILL.md` is
   validated on its own.

Failure isolation matches the specification: a fatal manifest error rejects the
whole plugin, but one broken skill or server never disables the others. A
non-zero exit means the manifest failed **or** at least one skill did — read the
per-skill output to tell which.

> [!NOTE]
> `agents/`, `commands/`, and `hooks/` are outside the Agent Plugins
> specification and are not checked here. They are vendor surface: only the
> runtimes that define them will read them, and they do not travel between
> hosts. A clean `--plugin` run says the *portable* core is sound, not that
> every component ships everywhere.

## Vendor component health (Antigravity)

The `--plugin` run above deliberately stops at the portable core. Antigravity's
own components sit outside it and fail *silently* — a hook whose script is
missing or not executable simply never runs, with no error surfaced anywhere.

Run this at the plugin root when the plugin ships `hooks.json` or
`mcp_config.json`:

```bash
ROOT=$(pwd)
issues=0

# Antigravity root configs must parse before anything reads them
for f in "$ROOT/hooks.json" "$ROOT/mcp_config.json"; do
  [ -f "$f" ] || continue
  if ! jq empty "$f" 2>/dev/null; then
    echo "  [BAD_JSON] $(basename "$f") is not valid JSON"
    issues=$((issues + 1))
  fi
done

# Hook scripts must exist AND be executable — a non-executable hook fails silently
if [ -f "$ROOT/hooks.json" ] && jq empty "$ROOT/hooks.json" 2>/dev/null; then
  # feed the loop from a here-string, not a pipe, so it runs in this shell
  while read -r cmd; do
    [ -n "$cmd" ] || continue
    script=${cmd%% *}                     # first token; drop any arguments
    case "$script" in
      /*) path="$script" ;;
      *)  path="$ROOT/$script" ;;
    esac
    if [ -e "$path" ]; then
      [ -x "$path" ] || {
        echo "  [NOT_EXEC] hooks.json → $script exists but is not executable (chmod +x)"
        issues=$((issues + 1))
      }
    elif [ "${script#*/}" != "$script" ]; then
      # contains a slash → a real path that should resolve inside the plugin
      echo "  [NO_HOOK]  hooks.json → $script not found in plugin"
      issues=$((issues + 1))
    else
      # bare command name → resolved from PATH at run time; only note if absent here
      command -v -- "$script" >/dev/null 2>&1 \
        || echo "  [WARN]     hooks.json → '$script' not on this machine's PATH (may exist on the target)"
    fi
  done <<EOF
$(jq -r '.hooks // {} | to_entries[] | .value[]? | .hooks[]? | .command // empty' "$ROOT/hooks.json" 2>/dev/null)
EOF
fi
```

> [!NOTE]
> Antigravity's `hooks.json` and `mcp_config.json` are its own schemas at its own
> paths. They are **not** interchangeable with Claude's `hooks/hooks.json`,
> Codex's `hooks/hooks-codex.json`, or the Agent Plugins `mcp.json`. Finding one
> does not mean the others are configured.

## Plugin and marketplace health

Marketplace clones do **not** auto-refresh. A stale clone pins every plugin
installed from it, with no signal anywhere in the CLI.

Run the clone refresh first, or every version below is read from a stale copy:

```bash
# Claude — refresh each configured marketplace clone
python3 -c 'import json;print("\n".join(json.load(open("'"$HOME"'/.claude/plugins/known_marketplaces.json"))))' \
  | while read -r m; do claude plugin marketplace update "$m" >/dev/null 2>&1; done

# Codex — refreshes all Git marketplaces at once (local ones are skipped)
codex plugin marketplace upgrade >/dev/null 2>&1
```

### Stale installs (Claude)

Compares each installed plugin against the version its refreshed clone declares.

```bash
python3 - <<'PY'
import json, os

home = os.path.expanduser("~")
installed = f"{home}/.claude/plugins/installed_plugins.json"
markets   = f"{home}/.claude/plugins/marketplaces"

if not os.path.isfile(installed):
    raise SystemExit("  no installed_plugins.json — nothing to check")

def clone_version(marketplace, plugin):
    """Version declared by the clone. Layout varies, so try each known shape."""
    base = os.path.join(markets, marketplace)
    for rel in (".claude-plugin/plugin.json", "plugin.json",
                f"{plugin}/.claude-plugin/plugin.json",
                f"plugins/{plugin}/.claude-plugin/plugin.json"):
        path = os.path.join(base, rel)
        if os.path.isfile(path):
            try:
                return json.load(open(path)).get("version")
            except Exception:
                continue
    return None

issues = 0
for key, entries in sorted(json.load(open(installed)).get("plugins", {}).items()):
    plugin, _, marketplace = key.partition("@")
    for e in entries:
        have, want = e.get("version", "unknown"), clone_version(marketplace, plugin)
        if want and want != have:
            print(f"  [STALE]   {key}: {have} -> {want}")
            issues += 1
print(f"  {issues} stale plugin(s)" if issues else "  ✓ all plugins current")
PY
```

### Local-source marketplaces (Codex)

```bash
codex plugin marketplace list 2>/dev/null | tail -n +2 | while read -r name root; do
  case "$name" in openai-*) continue ;; esac          # app-managed
  if [ -d "$HOME/.codex/.tmp/marketplaces/$name/.git" ]; then
    continue                                           # git-backed, updates fine
  elif [ "$(codex plugin list 2>/dev/null | grep -c "@${name}\b")" -eq 0 ]; then
    continue                                           # empty: nothing to pin
  else
    echo "  [LOCAL]   $name ($root) — 'marketplace upgrade' skips it; plugins never update"
  fi
done
```

### Escaping `source.path`

A manifest whose plugin source resolves outside the marketplace root fails at
install with a misleading `plugin <name> was not found in marketplace <name>`.

```bash
for mf in "$HOME/.agents/plugins/marketplace.json" \
          "$HOME"/.codex/.tmp/marketplaces/*/.agents/plugins/marketplace.json; do
  [ -f "$mf" ] || continue
  python3 - "$mf" <<'PY'
import json, sys
mf = sys.argv[1]
try:
    plugins = json.load(open(mf)).get("plugins", [])
except Exception as exc:
    print(f"  [BADJSON] {mf}: {exc}"); raise SystemExit
for p in plugins:
    src = p.get("source")
    if not isinstance(src, dict) or src.get("source") != "local":
        continue
    path = src.get("path", "")
    if path.startswith("../"):
        print(f"  [ESCAPES] {mf}: {p.get('name')} -> {path}  (use \"./\")")
PY
done
```

### Orphaned plugin folders (Codex)

```bash
for d in "$HOME"/.codex/plugins/*/; do
  name=$(basename "$d")
  case "$name" in cache|.*) continue ;; esac
  if [ -d "$HOME/.codex/plugins/cache/$name" ]; then
    echo "  [ORPHAN]  ~/.codex/plugins/$name superseded by cache/$name — safe to remove"
  fi
done
```

Three failure modes these checks cover:

1. **Local-source marketplace.** `codex plugin marketplace upgrade` refreshes
   **Git** snapshots only. A marketplace added from a local path is never
   refreshed, so its plugins stay pinned at whatever version was first installed.
   Prefer a Git marketplace; re-add with `codex plugin marketplace add <owner>/<repo>`.

2. **Escaping `source.path`.** In `.agents/plugins/marketplace.json`, a plugin
   source such as `"../../plugins/<name>"` resolves outside the marketplace root
   and fails at install time with a misleading
   `plugin <name> was not found in marketplace <name>`. Use `"./"` when the
   plugin *is* the repository, or a `{"source": "url", "url": "..."}` block.

3. **Orphaned plugin folders.** Once a plugin installs to a versioned cache path
   (`~/.codex/plugins/cache/<name>/<name>/<version>/`), the old flat folder at
   `~/.codex/plugins/<name>/` is dead weight. Remove it *and* its entry from the
   marketplace manifest, or the manifest advertises a source that no longer exists.

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
| Broken user-scope link | `rm ~/.claude/skills/<name>`, then re-link from the real source |
| Stale marketplace clone | `claude plugin marketplace update <m>` then `claude plugin update <p>@<m>`; Codex: `codex plugin marketplace upgrade` |
| Local-source marketplace | Re-add as Git: `codex plugin marketplace add <owner>/<repo>`, reinstall, drop the local entry |
| Escaping source path | Set `source.path` to `"./"` in `.agents/plugins/marketplace.json` |
| Orphaned plugin folder | Delete the folder **and** prune its entry from the marketplace manifest |
