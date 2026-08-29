# publish — Prepare a skill for publication as a plugin

Use this when: scaffolding package/plugin manifests to publish a skill across Claude, Codex, Cursor, Antigravity, and Agent Skills hosts.

Scaffolds the complete manifest structure on an existing skill folder, making it publishable via the [Agent Plugins](https://agent-plugins.org) standard (ChatGPT, Codex, Cursor, GitHub Copilot, Kiro, VS Code), the Claude Code marketplace, Google Antigravity plugin surfaces, and `npx skills` / direct Agent Skills roots.

**Portable first, vendor second.** The root `plugin.json` is the Agent Plugins manifest — the portable core that every conformant host reads. The `.claude-plugin/` and `.codex-plugin/` manifests are vendor fallbacks for runtimes that have not adopted the standard. Write the portable manifest first, then add only the sidecars the target hosts actually require.

Portable package/plugin runtimes share the same `skills/` at the package root — no duplicated runtime-specific skill trees. Note that only `skills/` (and `mcp.json`) are covered by the standard; `agents/`, `commands/`, and `hooks/` are vendor surface and do not travel between hosts. For day-to-day installation from a skill library, flatten skills into the host's canonical skill root (`<skill-root>/<skill-name>/SKILL.md`) rather than relying on nested plugin-bundle discovery.

## Usage

```
/skizl publish <skill-path> [--username <github-username>] [--name <repo-name>]
```

**Examples:**
```
/skizl publish skills/my-skill
/skizl publish skills/my-skill --username <username>
/skizl publish . --name skizl --username <username>
```

---

## What it creates

Given a skill at `skills/<name>/`, publish scaffolds these files at the **repo root** (one level above `skills/`):

```
<repo-root>/
├── .claude-plugin/
│   ├── plugin.json         ← Claude Code plugin manifest
│   └── marketplace.json    ← Claude marketplace metadata
├── .codex-plugin/
│   └── plugin.json         ← Codex plugin manifest
├── plugin.json             ← Agent Plugins manifest (root-level, portable core)
├── .agents/
│   └── plugins/
│       └── marketplace.json  ← Codex marketplace file
├── agents/                 ← auto-discovered by both runtimes
├── skills/                 ← auto-discovered by Claude; declared in Codex plugin.json
├── hooks/
│   ├── hooks.json          ← Claude hooks
│   └── hooks-codex.json    ← Codex hooks (separate file, same folder)
├── .gitignore              ← only if missing
└── README.md               ← only if missing
```

> [!IMPORTANT]
> **Repo as Governor, Skills as Self-Contained Packages**:
> The repository acts as the governor. It contains the central manifests (`.claude-plugin/`, `.codex-plugin/`, and root `plugin.json`), git hook scripts (`scripts/hooks/`), and configuration.
> Meanwhile, the skills residing in `skills/` (e.g., `skills/<name>/`) are self-contained packages. Each houses its own logic, references, scripts, and local versioned snapshots. They must never leak skill-specific config or backup directories to the repository root.

---

## Step 1 — Gather info

Read `SKILL.md` frontmatter from the skill to pre-fill as many fields as possible:
- `name:` → repo name
- `description:` → plugin description
- `version:` → plugin version (read `metadata.version` first, falling back to top-level `version:`, default `1.0.0` if missing)

Description rules:
- Codex measures the `description` value by itself; do not concatenate it with `when_to_use`, triggers, command menus, plugin interface fields, or body text for this limit.
- Codex skill descriptions have a hard 1024-character limit for that `description` field.
- Prefer a 900-character maximum for generated or rewritten `description` values so future edits have headroom.
- If the frontmatter `description:` is missing, write a concise one from the skill's purpose, commands, and trigger context before continuing.
- If the frontmatter `description:` is 901-1024 characters, warn that it is close to the Codex limit and offer to shorten it.
- If it is over 1024 characters, do not publish until it is shortened.
- Use the same checked description for plugin `description`, Codex `interface.shortDescription` or `longDescription` as appropriate, and marketplace metadata. `shortDescription` should be a one-line summary under 160 characters.

Resolve GitHub identity automatically before prompting:

```bash
# Primary: GitHub CLI (login = username, name = display name)
GH_LOGIN=$(gh api user --jq '.login' 2>/dev/null)
GH_NAME=$(gh api user --jq '.name' 2>/dev/null)

# Fallback: git config
GIT_NAME=$(git config user.name 2>/dev/null)

USERNAME="${GH_LOGIN:-}"
AUTHOR="${GH_NAME:-$GIT_NAME}"
```

Use `USERNAME` for URL fields (`homepage`, `repository`) and `AUTHOR` for `author.name` / `owner.name` fields.

Then ask the user for any missing values:

| Field | Source | Ask if missing |
|-------|--------|----------------|
| Repo name | frontmatter `name:` or folder name | yes |
| GitHub username | `gh api user .login` → `--username` flag | yes if both empty |
| Author name | `gh api user .name` → `git config user.name` | yes if both empty |
| Description | frontmatter `description:` (first line) | yes if empty |
| Version | frontmatter `metadata.version` or `version:` | no — default `1.0.0` |
| License | — | no — default `MIT` |
| Category | — | no — default `productivity` |
| Keywords | derived from name + description | show for confirmation |

**Do not proceed until repo name, username, description, and author are known.**
**Do not proceed if the skill description exceeds 1024 characters.**

---

## Step 2 — Derive keywords

Generate 6–10 keywords from the skill name, description, and category. Always include:
- `claude-code`
- the skill name (kebab-case)
- `skills`

Example for a skill named `skizl` with description about packing/unpacking:
```json
["skills", "skill-container", "pack", "unpack", "claude-code", "apm", "skizl"]
```

Show keywords to the user and ask: **"Keywords look good? (yes / edit)"**

---

## Step 3 — Check what already exists

```bash
ROOT=$(dirname <skill-path> | xargs dirname)   # two levels up from SKILL.md
# or if skill-path is the repo root, ROOT=$(pwd)
```

Check each target file. For files that already exist, ask: **"<file> already exists — overwrite? (yes / skip)"**

---

## Step 4 — Write files

### `.claude-plugin/plugin.json`

```json
{
  "name": "<repo-name>",
  "version": "<version>",
  "description": "<description>",
  "author": {
    "name": "<author>"
  },
  "homepage": "https://github.com/<username>/<repo-name>",
  "repository": "https://github.com/<username>/<repo-name>",
  "license": "<license>",
  "keywords": [<keywords>]
}
```

> `skills/` and `agents/` are auto-discovered by Claude — no explicit paths needed.  
> Optional explicit fields: `"skills"` (array), `"agents"` (array of paths), `"hooks"`, `"mcpServers"`.

### `.claude-plugin/marketplace.json`

```json
{
  "name": "<repo-name>",
  "owner": {
    "name": "<author>"
  },
  "metadata": {
    "description": "<description>",
    "version": "<version>"
  },
  "plugins": [
    {
      "name": "<repo-name>",
      "source": "./",
      "description": "<description>",
      "version": "<version>",
      "author": {
        "name": "<author>"
      },
      "license": "<license>",
      "homepage": "https://github.com/<username>/<repo-name>",
      "repository": "https://github.com/<username>/<repo-name>",
      "keywords": [<keywords>],
      "category": "<category>"
    }
  ]
}
```

> Do NOT add `skills` or `agents` keys — causes schema validation errors.

### `.codex-plugin/plugin.json`

```json
{
  "name": "<repo-name>",
  "version": "<version>",
  "description": "<description>",
  "skills": "./skills/",
  "hooks": "./hooks/hooks-codex.json",
  "interface": {
    "displayName": "<repo-name>",
    "shortDescription": "<one-line summary>",
    "longDescription": "<full description>",
    "developerName": "<author>",
    "category": "Productivity",
    "capabilities": ["Read", "Write"],
    "websiteURL": "https://github.com/<username>/<repo-name>",
    "defaultPrompt": [
      "<example prompt 1>",
      "<example prompt 2>"
    ],
    "brandColor": "#000000"
  }
}
```

> `skills` and `hooks` are required fields. `interface` is optional but recommended.  
> Additional optional fields: `"rules": "./.codex-plugin/rules/"`, `"mcpServers": "./.codex-plugin/mcp.json"`.  
> `interface` extras: `"logo"`, `"composerIcon"` (paths to `.codex-plugin/assets/`); `"privacyPolicyURL"`, `"termsOfServiceURL"` (any URL — local or external).  
> Codex auto-discovers `agents/` — do not add an `agents` field.

### `plugin.json` (repo root — Agent Plugins)

This is the **portable core**: the [Agent Plugins](https://agent-plugins.org) manifest, an open
vendor-neutral standard (TSC: AWS, Cursor, Microsoft, OpenAI, Vercel; Google as Core Maintainer).
One conformant file makes the repo installable on ChatGPT, Codex, Cursor, GitHub Copilot, Kiro,
and VS Code. Write this first; the vendor manifests below are fallbacks for hosts that have not
adopted the standard yet.

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "<repo-name>",
  "version": "<version>",
  "description": "<description>",
  "author": { "name": "<author>", "url": "<author-url>" },
  "homepage": "https://github.com/<username>/<repo-name>",
  "repository": "https://github.com/<username>/<repo-name>",
  "license": "MIT",
  "keywords": ["<keyword>"],
  "extensions": {
    "com.google.antigravity": { "description": "<antigravity-description>" }
  }
}
```

> [!IMPORTANT]
> **The schema is closed** (`additionalProperties: false`) — only `$schema`, `name`, `version`,
> `description`, `author`, `homepage`, `repository`, `license`, `keywords`, and `extensions` are
> legal at the top level. Anything else fails validation. `$schema` and `name` are the only
> required fields; everything else is optional.
>
> `name` must be 1–64 characters: lowercase alphanumeric plus hyphens and periods, no leading or
> trailing separator, and no `--` or `..` runs. The schema enforces this as a regex pattern —
> see the published schema for the exact expression.
>
> `author` accepts only `name`, `email`, and `url`.
>
> **Vendor-specific data goes in `extensions`**, keyed by reverse-domain namespace
> (`com.google.antigravity`, `com.example.client`). This is the spec's official escape hatch:
> clients read their own namespace and ignore the rest, so vendor extras never break portability.
> Extension contents are entirely client-defined — the standard assigns them no meaning.

**Portable core vs. vendor surface.** The standard covers **skills and MCP servers only**.
`skills/<name>/SKILL.md` and `mcp.json` travel to every conformant host. `agents/`, `commands/`,
and `hooks/` are **not** in the specification and do not travel — they are read only by the
specific runtimes that define them. Do not assume a plugin's full surface is portable just
because its manifest validates.

Skill discovery is fixed and shallow: an immediate child of `skills/` counts as a skill when it
contains `SKILL.md`. Clients do not recurse deeper, and an invalid skill is skipped without
affecting the others.

This same shallow rule is the practical installation contract for skill-library installs: expose
each skill as a direct child of the harness skill root (`.agents/skills/<name>/SKILL.md`,
`~/.gemini/config/skills/<name>/SKILL.md`, etc.). Plugin directories package bundles; they are
not a universal substitute for top-level `/skill` discovery.

> **Antigravity note.** Antigravity previously used its own root manifest
> (`$schema: https://antigravity.google/schemas/v1/plugin.json`). Since only one `$schema` value
> can occupy the field, the Agent Plugins schema takes it and Antigravity data moves under
> `extensions["com.google.antigravity"]`. Google is a Core Maintainer of the standard, so
> convergence is expected — but **verify the Antigravity install path still resolves** before
> relying on it for a release.
> Antigravity auto-discovers `skills/<name>/SKILL.md`, `agents/*.md`, `commands/*.md`, and `rules/*.md` inside the plugin folder, plus root `hooks.json` and `mcp_config.json`. It does NOT read `.claude-plugin/`, `.codex-plugin/`, or `hooks/` — those are inert for Antigravity.
> For Alessandro's central skills library, prefer direct global app installs under
> `~/.gemini/config/skills/<name>/SKILL.md` when `/skill` autocomplete reliability matters. Keep
> plugin install paths for bundle validation/distribution.
#### Antigravity components (optional — scaffold only when the plugin ships them)

Antigravity auto-loads four things from the plugin root. Each is Antigravity's own schema at
Antigravity's own path — none is interchangeable with the Claude or Codex equivalent, and none
is part of the Agent Plugins standard. **Skip all of these by default**; empty scaffolds are
noise, not a starting point.

| Component | Path | Loads when |
|-----------|------|-----------|
| Skills | `skills/<name>/SKILL.md` | always — shared with the portable core |
| Agents | `agents/*.md` | plugin ships subagents |
| Commands | `commands/*.md` | plugin ships slash commands — **converted to skills** on load |
| Rules | `rules/*.md` | markdown injected into agent context while the plugin is active |
| Hooks | `hooks.json` (root) | plugin ships lifecycle hooks |
| MCP servers | `mcp_config.json` (root) | plugin bundles MCP tool integrations |

Verify any of this with `agy plugin validate <path>`, which reports each component
class it actually processed. Confirmed against `agy` 1.1.13: `agents/` and
`commands/` **are** loaded, and `commands/` entries are converted into skills
rather than kept as a separate type.

> [!IMPORTANT]
> **`agents/` and `commands/` are CLI-verified only.** Neither appears in the
> Antigravity 2.0 plugin specification, which documents exactly four components:
> skills, rules, hooks, and MCP servers. Treat them as an `agy` CLI capability,
> not a guaranteed part of the plugin contract — a plugin that *depends* on them
> may silently lose that surface in the desktop app or in a future release.
> Anything load-bearing belongs in `skills/`, which both surfaces are specified
> to read.

**Enabled by default — unless you ship it off.** A discovered plugin is active
without any user action. To ship one switched off, declare it in `plugin.json`:

```json
{ "name": "<plugin-name>", "disabled": true }
```

The user's choice is recorded separately, in `config.json` under a `plugins` map
keyed by the plugin's **directory name** (not its manifest `name`, if they
differ):

```json
{ "plugins": { "<directory-name>": { "enabled": false } } }
```

`config.json` always wins over the manifest, so a user's toggle survives
reinstalling or updating the plugin — Antigravity never writes the preference
back into the plugin folder. A plugin with no `config.json` entry falls back to
its own `disabled` declaration, which is how a plugin that ships off stays off
until switched on. Users toggle from the settings UI or `agy plugin enable` /
`agy plugin disable`. A disabled plugin still appears in the list, but none of
its skills, rules, hooks, or MCP servers load.

> [!NOTE]
> `disabled` is an Antigravity field. The Agent Plugins schema is closed and does
> **not** permit it in the portable root manifest — adding it there fails
> validation. Ship `disabled` only in an Antigravity-specific plugin manifest, or
> keep the plugin enabled and let users toggle it.

**`rules/AGENTS.md`** — plugin-scoped standing context. Write rules only if the plugin needs
behavior applied for its whole active session; a skill that should fire on a trigger belongs in
`skills/`, not here.

```markdown
# <plugin-name> rules

<Standing guidance Antigravity should apply whenever this plugin is active.>
```

**`hooks.json`** (repo root — Antigravity) — distinct from Claude's `hooks/hooks.json` and
Codex's `hooks/hooks-codex.json`. Do not copy either into this path.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "<tool-name-pattern>",
        "hooks": [
          { "type": "command", "command": "<script>", "timeout": 30 }
        ]
      }
    ]
  }
}
```

Referenced scripts must exist and be executable (`chmod +x`) — a missing or non-executable hook
script fails silently at run time.

**`mcp_config.json`** (repo root — Antigravity) — separate from the standard's `mcp.json`. If the
plugin ships MCP servers for both, maintain both files; they are not aliases.

```json
{
  "mcpServers": {
    "<server-name>": {
      "command": "<executable>",
      "args": ["<arg>"]
    }
  }
}
```

### `.agents/plugins/marketplace.json`

```json
{
  "name": "<repo-name>",
  "interface": {
    "displayName": "<repo-name>"
  },
  "plugins": [
    {
      "name": "<repo-name>",
      "source": {
        "source": "local",
        "path": "./"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_USE"
      },
      "category": "Productivity"
    }
  ]
}
```

> `source.path` resolves relative to the **repo root** — not to `.agents/plugins/`.  
> Repo-root plugin: `"./"`. Multi-plugin nested: `"./plugins/<name>"`.  
> For public GitHub distribution: `"source": "url"` + `"url": "https://github.com/<username>/<repo>.git"`.  
> `policy` block is optional but recommended for public marketplace listings.

### `hooks/hooks.json` (Claude — only if missing)

```json
{
  "hooks": {}
}
```

### `hooks/hooks-codex.json` (Codex — only if missing)

```json
{
  "hooks": {}
}
```

> Both files live in the same `hooks/` folder. Claude loads `hooks.json` automatically; Codex loads `hooks-codex.json` via the `"hooks"` field in `.codex-plugin/plugin.json`.

### `.gitignore` (only if missing)

```
.DS_Store
**/.DS_Store
_archive/
_backups/
*.zip
```

### `README.md` (only if missing)

Before generating, ask:

> **Which install methods should the README include?**
> 1. Claude Code — `/plugin marketplace add` + `/plugin install`
> 2. Codex — `npx codex-marketplace add <user>/<repo> --plugin` (one command, activates directly); or native CLI `codex plugin marketplace add <user>/<repo>` then `codex plugin add <repo>@<repo>`
> 3. Antigravity — clone/symlink into `.agents/plugins/` (workspace, both surfaces), `~/.gemini/config/plugins/` (2.0 desktop, global), or `~/.gemini/antigravity-cli/plugins/` (`agy` CLI, global)
> 4. `npx skills add` — Vercel skills CLI (**skills only** — installs `skills/`, does NOT install `agents/`, `hooks/`, or MCP config; reads `.claude-plugin/plugin.json` to discover skill paths but ignores all other plugin components)
> 5. `git clone` — manual clone
> 6. All of the above

If the target repo is private (or the skill is meant for a team rather than the
public), also include a short auth note in the README — the marketplace commands
themselves are identical, only credentials differ:

> Private repos install exactly like public ones. Both Claude Code and Codex
> `git clone` over HTTPS and inherit git's existing credentials, so each
> teammate needs `gh auth login` && `gh auth setup-git` once per machine.
> Access is then governed by GitHub repo/org-team permissions.
> Add `--scope project` to commit the marketplace declaration to the project,
> `--sparse` to narrow a monorepo checkout, or Codex's `--ref` to pin a branch/tag.

Wait for the user's answer, then generate a README with:
- `# <repo-name>` heading
- Description paragraph
- Install section with only the chosen methods
- After Install section listing skills as `/<repo-name>:<skill-name>`
- License section

---

## Step 5 — git-guard

After writing all manifest files, check whether `scripts/hooks/pre-commit` exists:

```bash
[ -f scripts/hooks/pre-commit ] && echo "installed" || echo "missing"
```

- **Missing** → load `references/git-guard.md` and follow its steps to install git-guard automatically.
- **Present** → run the pre-commit script manually via bash (`bash scripts/hooks/pre-commit --check`) and report results.

This ensures every published plugin repo has version drift protection from day one.

---

## Step 6 — Report

After writing all files and installing git-guard:

```
✓ Published: <repo-name>
Description length: <n> chars (Codex limit: 1024)

Files created:
  .claude-plugin/plugin.json
  .claude-plugin/marketplace.json
  .codex-plugin/plugin.json
  plugin.json                (Agent Plugins manifest — portable core)
  .agents/plugins/marketplace.json
  hooks/hooks.json
  hooks/hooks-codex.json
  scripts/hooks/pre-commit   (git-guard — version drift protection)
  .gitignore  (already existed — skipped)
  README.md

Next steps:
  Test (Claude):  claude --plugin-dir ./
  Test (Codex):   npx codex-marketplace add ./ --plugin
  Create repo:    gh repo create <username>/<repo-name> --public
  Push:           git add . && git commit -m "feat: initial plugin scaffold" && git push -u origin main

  Install (Claude Code):
    /plugin marketplace add <username>/<repo-name>
    /plugin install <repo-name>@<repo-name>

  Install (Codex):
    npx codex-marketplace add <username>/<repo-name> --plugin   (one command, activates directly)
    or: codex plugin marketplace add <username>/<repo-name>
        codex plugin add <repo-name>@<repo-name>
    (Git marketplace — `codex plugin marketplace upgrade` refreshes Git snapshots
     only; a local-path marketplace never updates.)

  Install (npx skills — skills only, no agents/hooks/MCP):
    npx skills add <username>/<repo-name>
    # reads .claude-plugin/plugin.json for skill paths; ignores agents/, hooks/, .mcp.json

  Install (Antigravity — workspace):
    git clone https://github.com/<username>/<repo-name> .agents/plugins/<repo-name>
    # or symlink an existing local clone:
    ln -s ../../<relative-path-to-repo> .agents/plugins/<repo-name>

  Install (Antigravity — global, all workspaces):
    # Antigravity 2.0 desktop (restart app after adding):
    git clone https://github.com/<username>/<repo-name> ~/.gemini/config/plugins/<repo-name>
    # or symlink local dev repo:
    ln -s "$(pwd)" ~/.gemini/config/plugins/<repo-name>
    # agy CLI (separate state tree):
    git clone https://github.com/<username>/<repo-name> ~/.gemini/antigravity-cli/plugins/<repo-name>
    # or symlink local dev repo:
    ln -s "$(pwd)" ~/.gemini/antigravity-cli/plugins/<repo-name>

  New clones — activate git-guard:
    git config core.hooksPath scripts/hooks
```

---

## Notes

**Claude Code:**
- `skills/` and `agents/` at the plugin root are **auto-discovered** — no explicit paths required in `.claude-plugin/plugin.json`
- Optional explicit fields in `.claude-plugin/plugin.json`:
  ```json
  "skills": ["./skills/"],
  "agents": ["./agents/reviewer.md", "./agents/planner.md"],
  "hooks": "./hooks/hooks.json",
  "mcpServers": { "server-name": { "type": "http", "url": "..." } }
  ```
- Do NOT add `skills` or `agents` keys to `.claude-plugin/marketplace.json` — causes schema validation errors
- Install: `/plugin marketplace add <username>/<repo>` then `/plugin install <repo>@<repo>`
- Reload after changes: `/reload-plugins`

**Codex:**
- `.codex-plugin/plugin.json` requires `name`, `version`, `description`, and `skills` path
- `hooks` field in `.codex-plugin/plugin.json` points to `"./hooks/hooks-codex.json"` — Claude and Codex load different hook files from the same `hooks/` folder
- Optional fields in `.codex-plugin/plugin.json`:
  ```json
  "rules": "./.codex-plugin/rules/",
  "mcpServers": "./.codex-plugin/mcp.json"
  ```
- `interface` block: `composerIcon` and `logo` accept paths to assets in `.codex-plugin/assets/`; `privacyPolicyURL`/`termsOfServiceURL` accept any URL
- Codex auto-discovers `agents/` — do not add an `agents` field to `.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json` is the Codex marketplace file — different schema from Claude's, never swap them
- `source.path` resolves relative to the **repo root** — use `"./"` for repo-root plugins, `"./plugins/<name>"` for nested
- Install (repo-root): `npx codex-marketplace add <username>/<repo> --plugin` (one command, activates directly); or native CLI `codex plugin marketplace add <username>/<repo>` then `codex /plugins`
- Install (multi-plugin): same as above; ensure `.agents/plugins/marketplace.json` lists each plugin with the correct `source.path`
- Two Codex install paths: `npx codex-marketplace add … --plugin` is the external helper — it adds the marketplace *and* activates the plugin. The native CLI (`codex plugin marketplace add|upgrade|remove`) only registers the marketplace; there is no `codex plugin install` subcommand, so after a native `add` you must activate from the in-app `/plugins` browser.

**Antigravity (Google):**
- Docs: https://antigravity.google/docs/plugins
- **No marketplace, no registry, no install CLI.** The docs define exactly two ways to add a plugin: (1) Google's own bundled plugins, browsable/addable from the Antigravity UI's Customizations page — third-party plugins are never listed there; (2) manually placing a plugin folder in a scan directory. For any repo you or someone else publishes (including skizl), option 2 is the only path — there is nothing equivalent to `/plugin marketplace add` (Claude) or `codex plugin marketplace add` (Codex). Installing from GitHub means `git clone` (or symlink) into a scan dir yourself; Antigravity has no command that fetches a repo for you
- A plugin is any folder with a root `plugin.json` marker — `{"name": "..."}` is the whole documented schema (`name` optional, defaults to folder name)
- Components Antigravity loads from the plugin folder: `skills/<name>/SKILL.md`, `agents/*.md`, `commands/*.md` (converted to skills), `rules/*.md`, root `hooks.json` (hooks), root `mcp_config.json` (MCP servers). It ignores `.claude-plugin/`, `.codex-plugin/`, and `hooks/`
- Verify with `agy plugin validate <path>` — it prints every component class it processed, and errors on a missing or unparseable `plugin.json`
- Install locations (Antigravity auto-scans these). **Antigravity is two products** — the 2.0 desktop app and the `agy` CLI keep separate state trees, and the published plugin docs sit under the 2.0 section, so their paths describe the desktop app:
  - Workspace (**both surfaces**): `<workspace>/.agents/plugins/<plugin-name>/` or `<workspace>/_agents/plugins/<plugin-name>/`
  - Global, Antigravity 2.0 desktop: `~/.gemini/config/plugins/<plugin-name>/` (scanned on app startup; restart Antigravity to pick up new or changed plugins)
  - Global, `agy` CLI: `~/.gemini/antigravity-cli/plugins/<plugin-name>/`
  - Prefer the workspace path when the plugin is project-scoped — it is the one location both surfaces read.
  - The 2.0 desktop also exposes bundled plugins through its **Customizations** page.
- Direct symlinking into both `~/.gemini/config/plugins/` and `~/.gemini/antigravity-cli/plugins/` is safe and ideal for live development across surfaces, but **never run `agy plugin install` over a symlink** (as the install command is destructive toward the symlink target).
- Coexistence note: `.agents/plugins/` is also where the Codex `marketplace.json` **file** lives. Antigravity only picks up **directories** containing a `plugin.json`, so the Codex marketplace file is ignored — they share the dir safely. In a consuming workspace, an installed plugin folder sits at `.agents/plugins/<name>/` right next to any Codex marketplace file
- The root `plugin.json` is inert for Claude Code (which reads `.claude-plugin/plugin.json`) and Codex (`.codex-plugin/plugin.json`) — no conflicts

**All runtimes:**
- Bump `version` in all `plugin.json` and `.claude-plugin/marketplace.json` on each release. The root Agent Plugins `plugin.json` carries a `version` too (optional in that schema, but recommended and checked by git-guard when present) — bump it with the rest
- Hooks split by runtime: `hooks/hooks.json` for Claude, `hooks/hooks-codex.json` for Codex, root `hooks.json` for Antigravity (only if needed)
- Claude, Codex, and Antigravity all share `skills/` at the plugin root; Claude and Codex additionally share `agents/` and `hooks/` — no duplication
- If the repo already has a `.git/` with a remote, extract `username` and `repo-name` automatically:
  ```bash
  git remote get-url origin 2>/dev/null | sed 's/.*github.com[:/]\([^/]*\)\/\([^.]*\).*/\1 \2/'
  ```
