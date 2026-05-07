# publish — Prepare a skill for publication as a plugin

Scaffolds the complete plugin manifest structure on an existing skill folder, making it installable via Claude Code marketplace, Codex, and `npx skills`.

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
│   └── plugin.json         ← Codex plugin manifest (minimal)
├── .agents/
│   └── plugins/
│       └── marketplace.json  ← Codex marketplace file
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

### `.codex-plugin/plugin.json`

Codex requires `name`, `version`, `description`, and `skills` path:

```json
{
  "name": "<repo-name>",
  "version": "<version>",
  "description": "<description>",
  "skills": "./skills/"
}
```

### `.agents/plugins/marketplace.json`

Codex marketplace file — separate schema from Claude's. `source.path` is relative to `.agents/plugins/` and must be `./`-prefixed:

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
        "path": "../../"
      },
      "category": "Productivity"
    }
  ]
}
```

> `source.path` is `../../` because it resolves relative to `.agents/plugins/`, pointing back to the repo root where `.codex-plugin/` lives.

### `.gitignore` (only if missing)

```
.DS_Store
**/.DS_Store
output/*
!output/.gitkeep
_archive/
_backups/
*.zip
```

### `README.md` (only if missing)

Before generating, ask:

> **Which install methods should the README include?**
> 1. Claude Code marketplace — `/plugin marketplace add <username>/<repo>` then `/plugin install <repo>@<username>-<repo>`
> 2. Codex — `codex plugin marketplace add <username>/<repo>` then `codex /plugins` to install
> 3. `npx skills add <username>/<repo>` — vercel skills CLI (global / project-scoped / agent-targeted)
> 4. `git clone` — manual clone + symlink
> 5. All of the above

Wait for the user's answer, then generate a README with:
- `# <repo-name>` heading
- Description paragraph
- Install section with only the chosen methods
- After Install section listing skills as `/<repo-name>:<skill-name>`
- License section

---

## Step 5 — Report

After writing all files:

```
✓ Published: <repo-name>

Files created:
  .claude-plugin/plugin.json
  .claude-plugin/marketplace.json
  .codex-plugin/plugin.json
  .agents/plugins/marketplace.json
  .gitignore  (already existed — skipped)
  README.md

Next steps:
  Test (Claude):  claude --plugin-dir ./
  Test (Codex):   codex plugin marketplace add ./  &&  codex /plugins
  Create repo:    gh repo create <username>/<repo-name> --public
  Push:           git add . && git commit -m "feat: initial plugin scaffold" && git push -u origin main

  Install (Claude Code):
    /plugin marketplace add <username>/<repo-name>
    /plugin install <repo-name>@<username>-<repo-name>

  Install (Codex):
    codex plugin marketplace add <username>/<repo-name>
    codex /plugins  (then browse and install)

  Install (npx skills):
    npx skills add <username>/<repo-name>
```

---

## Notes

**Claude Code:**
- `skills/` and `agents/` at the plugin root are **auto-discovered** — no paths needed in `.claude-plugin/plugin.json`
- Do NOT add `skills` or `agents` keys to `.claude-plugin/marketplace.json` — causes schema validation errors
- Install: `/plugin marketplace add <username>/<repo>` then `/plugin install <repo>@<username>-<repo>`
- Marketplace name is `<username>-<repo>` (hyphenated owner-repo)
- Reload after changes: `/reload-plugins`

**Codex:**
- `.codex-plugin/plugin.json` requires `name`, `version`, `description`, and `skills` path
- `.agents/plugins/marketplace.json` is the Codex marketplace file — different schema from Claude's, never swap them
- `source.path` in `.agents/plugins/marketplace.json` resolves relative to `.agents/plugins/` — use `../../` to point to repo root
- Install: `codex plugin marketplace add <username>/<repo>` then `codex /plugins` to browse and install
- `codex plugin install` is **not a valid command** — always use marketplace add + browser

**Both:**
- Bump `version` in all `plugin.json` and `marketplace.json` files on each release
- If the repo already has a `.git/` with a remote, extract `username` and `repo-name` automatically:
  ```bash
  git remote get-url origin 2>/dev/null | sed 's/.*github.com[:/]\([^/]*\)\/\([^.]*\).*/\1 \2/'
  ```
