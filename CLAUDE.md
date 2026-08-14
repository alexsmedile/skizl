# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

**skizl** is a Claude Code plugin bundling three skills that together cover the full life of a skill — authoring it, then managing it after it exists. The root holds only documentation and plugin manifests; every skill lives under `skills/`.

| Skill | Frontmatter `name:` | Owns |
|-------|--------------------|------|
| `skills/skill-manager/` | `skill-manager` | Post-authoring lifecycle: pack, unpack, pin, sym, diff, snapshot, bump, history, archive, fork, publish, release, git-guard |
| `skills/skill-forge/` | `skill-forge` | Building a skill properly: routed tracks, architecture workshop, fresh-context reviewer gate, evals |
| `skills/skill-draft/` | `skill-draft` | The fast lane: one-pass single-`SKILL.md` draft, no tracks or reviewer |

The division is deliberate and load-bearing: **forge and draft author content; skill-manager never does.** skill-manager handles a skill only once it exists. Route "create/audit/repair a skill" to `skill-forge` (or `skill-draft` for something small), and "version/publish/symlink a skill" to `skill-manager`.

The plugin/bundle is named `skizl`, so the lifecycle commands below are invoked as `/skizl <command>`.

## Skill Architecture — `skill-manager`

`skill-manager` uses a **container pattern** where a lean master `SKILL.md` routes to on-demand action files:

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

## Skill Architecture — `skill-forge`

`skill-forge` routes by **weight track** rather than by command:

```
skills/skill-forge/
├── SKILL.md          ← operation + track routing, gates, ship criteria (<500 lines)
├── GLOSSARY.md       ← shared vocabulary; also handed to the reviewer
├── reviewer.md       ← two prompts: Full-review, then issue-scoped Verification
├── tracks/           ← light.md, standard.md, empirical.md, audit.md
├── references/       ← disclosed knowledge (e.g. platforms.md host profiles)
├── templates/        ← SKILL.md.tmpl, reference.md.tmpl, evals.json.tmpl
├── scripts/check.py  ← mechanical lint, profile-aware
└── evals/            ← regression briefs, runner prompts, fixtures, trigger cases
```

Two orthogonal dimensions, easy to conflate:

- **Operation** — where a run *starts*: `Create` (no usable skill), `Update` (behavioral delta to a finished skill), `Resume` (continue an unfinished run from its **forge record**).
- **Track** — how much process the work *needs*: light / standard / empirical / audit.

A finished skill receiving a new request is an **Update**, not a Resume. The forge record lives **outside** the distributable skill folder (gitignored `/.skill-forge/`) so process state is never mistaken for runtime content.

Validate a skill with the profile that matches its target host:

```bash
python3 skills/skill-forge/scripts/check.py <skill-dir> --profile <target>
# profiles: portable | claude | codex | cursor | gemini | skizl
```

Skills in this repo carry skizl metadata (`category`, `status`, `tags`, `version`), so use `--profile skizl`. The `portable` profile rejects those fields by design — a failure there is a profile mismatch, not a defect.

`check.py` catches mechanical faults only. Behavioral changes to the forge itself require the regression protocol in [evals/README.md](skills/skill-forge/evals/README.md): run all six briefs against a sanitized baseline snapshot, with `evals/` excluded from both copies so the oracles stay hidden.

## Commands — `skill-manager`

These are `skill-manager`'s lifecycle commands, invoked as `/skizl <command>`. `skill-forge` and `skill-draft` are not command-driven — they are invoked by intent ("build me a skill", "audit this skill"). Note that the `pack` alias `forge` is unrelated to the `skill-forge` skill.

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
- **Authoring and lifecycle stay separate** — `skill-forge`/`skill-draft` write skill content; `skill-manager` never authors, it only acts on skills that already exist
- **Version consistency is enforced at commit time** — a `git-guard` pre-commit hook blocks the commit unless all six version sites agree: `.claude-plugin/plugin.json`, both `.claude-plugin/marketplace.json` fields (`metadata` and `plugins[0]`), `.codex-plugin/plugin.json`, the README badge, and the top CHANGELOG entry. Bump all of them together; `marketplace.json` holds two and is the one most often missed.

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

