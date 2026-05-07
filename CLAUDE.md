# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

**skilz** is a Claude Code meta-skill that manages the lifecycle of skill containers. It packs multiple standalone skills into a unified container architecture (`actions/` + `knowledge/`), unpacks containers back to standalone skills, and manages lightweight redirect shortcuts (pins).

The actual skill lives at `skills/skilz/` — the root holds only this documentation.

## Skill Architecture

The skill uses a **container pattern** where a lean master `SKILL.md` routes to on-demand action files:

```
skills/skilz/
├── SKILL.md          ← routing + command table (<500 lines, auto-loaded)
├── references/       ← per-command logic + shared knowledge, loaded explicitly when needed
│   ├── pack.md
│   ├── unpack.md
│   ├── pin.md
│   └── onboard.md
└── scripts/
    └── pin.mjs       ← Node.js script for pin/unpin automation
```

`SKILL.md` is the only file Claude loads automatically. `references/` files are read explicitly when a command is invoked.

## Commands

| Command | Aliases | What it does |
|---------|---------|--------------|
| `pack`   | wrap, fold, zip, bundle, forge, merge, knit | Pack standalone skills into a container |
| `unpack` | unwrap, unfold, unzip, burst, smelt, split, unravel | Restore container actions as standalone skills |
| `pin`    | link, alias, tap | Create a redirect skill pointing to one container action |
| `unpin`  | unlink, detach | Remove a redirect skill |
| `status` | info, ls, list | Inspect a container's structure |

## Key Design Rules

- **Pack and unpack are copy operations** — source skills/containers are never modified or deleted
- **Master SKILL.md must stay under 500 lines** — move verbose content to `knowledge/` files
- **Knowledge files must be explicitly referenced** from action files to be loaded
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
npx skills add alexsmedile/skilz        # project-scoped
npx skills add alexsmedile/skilz -g     # global
npx skills add alexsmedile/skilz -a claude-code  # target specific agent
```

After install, invoke as `/skilz pack ...` or `/skilz unpack ...`.

