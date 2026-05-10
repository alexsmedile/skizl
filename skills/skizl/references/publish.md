# publish — Prepare a skill for publication as a plugin

Scaffolds the complete plugin manifest structure on an existing skill folder, making it installable via Claude Code marketplace, Codex, and `npx skills` (skills only).

Both runtimes share the same `skills/`, `agents/`, and `hooks/` at the plugin root — no duplication, no runtime-specific trees.

## Usage

```
skizl publish <skill-path> [--username <github-username>] [--name <repo-name>]
```

**Examples:**
```
skizl publish skills/my-skill
skizl publish skills/my-skill --username <username>
skizl publish . --name skizl --username <username>
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

---

## Step 1 — Gather info

Read `SKILL.md` frontmatter from the skill to pre-fill as many fields as possible:
- `name:` → repo name
- `description:` → plugin description
- `version:` → plugin version (default `1.0.0` if missing)

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
| Version | frontmatter `version:` | no — default `1.0.0` |
| License | — | no — default `MIT` |
| Category | — | no — default `productivity` |
| Keywords | derived from name + description | show for confirmation |

**Do not proceed until repo name, username, description, and author are known.**

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
> 2. Codex — `npx codex-marketplace add ... --plugin`
> 3. `npx skills add` — Vercel skills CLI (**skills only** — installs `skills/`, does NOT install `agents/`, `hooks/`, or MCP config; reads `.claude-plugin/plugin.json` to discover skill paths but ignores all other plugin components)
> 4. `git clone` — manual clone
> 5. All of the above

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

- **Missing** → run `skizl git-guard install` automatically (follow `references/git-guard.md`)
- **Present** → run `skizl git-guard check` and report results

This ensures every published plugin repo has version drift protection from day one.

---

## Step 6 — Report

After writing all files and installing git-guard:

```
✓ Published: <repo-name>

Files created:
  .claude-plugin/plugin.json
  .claude-plugin/marketplace.json
  .codex-plugin/plugin.json
  .agents/plugins/marketplace.json
  hooks/hooks.json
  hooks/hooks-codex.json
  scripts/hooks/pre-commit   (git-guard — version drift protection)
  .gitignore  (already existed — skipped)
  README.md

Next steps:
  Test (Claude):  claude --plugin-dir ./
  Test (Codex):   npx codex-marketplace add ./ --plugin  &&  codex /plugins
  Create repo:    gh repo create <username>/<repo-name> --public
  Push:           git add . && git commit -m "feat: initial plugin scaffold" && git push -u origin main

  Install (Claude Code):
    /plugin marketplace add <username>/<repo-name>
    /plugin install <repo-name>@<repo-name>

  Install (Codex):
    npx codex-marketplace add <username>/<repo-name> --plugin
    codex /plugins  (then browse and install)

  Install (npx skills — skills only, no agents/hooks/MCP):
    npx skills add <username>/<repo-name>
    # reads .claude-plugin/plugin.json for skill paths; ignores agents/, hooks/, .mcp.json

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
- Install (repo-root): `npx codex-marketplace add <username>/<repo> --plugin` then `codex /plugins`
- Install (multi-plugin): `npx codex-marketplace add <username>/<repo> --plugins` then `codex /plugins`
- `codex plugin install` and `codex plugin marketplace add` are **not valid commands** — always use `npx codex-marketplace`

**Both:**
- Bump `version` in all `plugin.json` and `.claude-plugin/marketplace.json` on each release
- Hooks split by runtime: `hooks/hooks.json` for Claude, `hooks/hooks-codex.json` for Codex — same folder, different files
- Both runtimes share `skills/`, `agents/`, `hooks/` at the plugin root — no duplication
- If the repo already has a `.git/` with a remote, extract `username` and `repo-name` automatically:
  ```bash
  git remote get-url origin 2>/dev/null | sed 's/.*github.com[:/]\([^/]*\)\/\([^.]*\).*/\1 \2/'
  ```
