# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

**skizl** is a Claude Code meta-skill that manages the lifecycle of skill containers. It packs multiple standalone skills into a unified container architecture (`references/`), unpacks containers back to standalone skills, manages lightweight redirect shortcuts (pins), and provides tooling to symlink, inspect, diff, fork, publish, version (snapshot/bump/history), and archive skills.

The actual skill lives at `skills/skill-manager/` (its frontmatter `name:` is `skill-manager`) — the root holds only this documentation. The plugin/bundle is still named `skizl`, so it is invoked as `/skizl <command>`.

## Skill Architecture

The skill uses a **container pattern** where a lean master `SKILL.md` routes to on-demand action files:

```
skills/skill-manager/
├── SKILL.md          ← routing + command table (<500 lines, auto-loaded)
├── references/       ← per-command logic + shared knowledge, loaded explicitly when needed
│   ├── sym.md
│   ├── pack.md
│   ├── unpack.md
│   ├── pin.md
│   ├── list.md
│   ├── diff.md
│   ├── doctor.md
│   ├── fork.md
│   ├── publish.md
│   ├── snapshot.md
│   ├── archive.md
│   ├── onboard.md
│   ├── git-guard.md
│   └── folders.md
└── scripts/
    └── pin.mjs       ← Node.js script for pin/unpin automation
```

`SKILL.md` is the only file Claude loads automatically. `references/` files are read explicitly when a command is invoked.

## Commands

| Command | Aliases | What it does |
|---------|---------|--------------|
| `pack` | wrap, fold, zip, bundle, forge, merge, knit | Pack standalone skills into a container |
| `unpack` | unwrap, unfold, unzip, burst, smelt, split, unravel | Restore container actions as standalone skills |
| `pin` | link, alias, tap | Create a redirect skill pointing to one container action |
| `unpin` | unlink, detach | Remove a redirect skill |
| `sym` | symlink, link-skills | Symlink `skills/` into `.claude/skills/` and `.agents/skills/` (`in` / `out` / `status`) |
| `list` | ls, installed | Show installed skills with their symlink state |
| `diff` | compare, changes | Compare two versions of a skill |
| `doctor` | check, diagnose | Diagnose broken symlinks, missing files, orphaned entries |
| `fork` | clone, copy | Clone a skill (local or GitHub URL) as a personal variant |
| `publish` | scaffold | Scaffold plugin manifests to publish a skill on GitHub |
| `release` | ship | Make a verified, atomic plugin release |
| `snapshot` | save, checkpoint, freeze | Save SKILL.md as a versioned snapshot in `versions/` |
| `bump` | version, semver, increment | Increment `version:` in frontmatter (patch/minor/major) |
| `history` | log, versions, changelog | List, show, or diff versioned snapshots |
| `archive` | backup, tar, zip-full | Archive the entire skill folder as a timestamped tarball |
| `status` | info | Inspect a container's structure and active pins |
| `onboard` | help, intro, explain | Explain how skizl works and guide first use |
| `git-guard` | version-guard, hook, drift | Install/remove/check pre-commit version consistency hook |

## Key Design Rules

- **Pack and unpack are copy operations** — source skills/containers are never modified or deleted
- **Master SKILL.md must stay under 500 lines** — move verbose content to `references/` files
- **Reference files must be explicitly loaded** — Claude reads them on demand when a command is invoked
- **Pin shortcuts** follow the naming convention `i-<action>` and are symlinked into `.claude/skills/`

## scripts/pin.mjs

Node.js script (no external dependencies) for automating pin/unpin. Key flags:

```bash
node scripts/pin.mjs --list                        # show active pins for a container
node scripts/pin.mjs <container-path> <action>     # create pin
node scripts/pin.mjs --remove <container-path> <action>  # remove pin
node scripts/pin.mjs --skills-dir <dir> ...        # override skills directory
```

The script reads `SKILL.md` frontmatter (YAML) to extract `name`, `allowed-tools`, and the action's description from the commands table.

## Installation

```bash
npx skills add alexsmedile/skizl        # project-scoped
npx skills add alexsmedile/skizl -g     # global
npx skills add alexsmedile/skizl -a claude-code  # target specific agent
```

After install, invoke as `/skizl <command>` — e.g. `/skizl sym in`, `/skizl pack ...`, `/skizl publish ...`.

