# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

**skizl** is a Claude Code plugin bundling four skills that together cover the full life of a skill — authoring it, optimizing it into dense micro-kernels, then managing it after it exists. The root holds only documentation and plugin manifests; every skill lives under `skills/`.

| Skill | Frontmatter `name:` | Owns |
|---|---|---|
| `skills/skill-manager/` | `skill-manager` | Post-authoring lifecycle: pack, unpack, pin, sym, diff, snapshot, bump, history, archive, fork, publish, release, git-guard |
| `skills/skill-forge/` | `skill-forge` | Building a skill properly: routed tracks, architecture workshop, fresh-context reviewer gate, evals |
| `skills/skill-draft/` | `skill-draft` | The fast lane: one-pass single-`SKILL.md` draft, no tracks or reviewer |
| `skills/skill-densify/` | `skill-densify` | Micro-kernel compressor: transforms verbose skills into high-density <=65-line kernels |

The division is deliberate: **forge, draft, and densify author and optimize content; skill-manager manages lifecycle.**

The plugin/bundle is named `skizl`, so the lifecycle commands below are invoked as `/skizl <command>`.

## 5-Layer Architectural Standard

All skills in `skizl` adhere to the 5-layer micro-kernel optimization:
1. **Telegraphic Micro-Kernel**: Front-door `SKILL.md` stays <=55-65 lines using dense decision tables.
2. **Mechanical Script Offloading**: Repetitive file / manifest inspections offload to `scripts/skizl-ops.sh`.
3. **Silent Fast-Lane Execution**: Routine operations run without chatter, emitting a standardized left-border box (`┌─ SKIZL · ... └─`).
4. **Strictly Pinned Route Enums**: Fixed command/track enums (no speculative route generation).
5. **Progressive Disclosure**: Specialized logic lives in `references/*.md` with explicit `Use this when:` activation rules.

## Skill Architecture — `skill-manager`

```
skills/skill-manager/
├── SKILL.md          ← telegraphic router micro-kernel (<60 lines, auto-loaded)
└── references/       ← per-command logic + shared knowledge, loaded explicitly when needed
    ├── sym.md
    ├── pack.md
    ├── unpack.md
    ├── pin.md
    ├── list.md
    ├── diff.md
    ├── doctor.md
    ├── fork.md
    ├── publish.md
    ├── snapshot.md
    ├── archive.md
    ├── onboard.md
    ├── git-guard.md
    └── folders.md
```

## Skill Architecture — `skill-forge`

`skill-forge` routes by **weight track** rather than by command:

```
skills/skill-forge/
├── SKILL.md          ← operation + track routing, gates, ship criteria (<70 lines)
├── GLOSSARY.md       ← shared vocabulary; also handed to the reviewer
├── reviewer.md       ← two prompts: Full-review, then issue-scoped Verification
├── tracks/           ← light.md, standard.md, empirical.md, audit.md
├── references/       ← disclosed knowledge (e.g. platforms.md host profiles)
├── templates/        ← SKILL.md.tmpl, reference.md.tmpl, evals.json.tmpl
├── scripts/check.py  ← mechanical lint, profile-aware
└── evals/            ← regression briefs, runner prompts, fixtures, trigger cases
```

## Skill Architecture — `skill-densify`

```
skills/skill-densify/
├── SKILL.md          ← micro-kernel compressor front door (<55 lines)
├── references/       ← patterns.md, rules.md
└── scripts/
    └── densify.py    ← line, token budget, and prose-filler analyzer
```

## Helper Scripts

- `scripts/skizl-ops.sh` — Single-turn deterministic helper for `sym-status`, `doctor`, `diffsum`, `guard-check`.
- `skills/skill-manager/scripts/pin.mjs` — Node.js script for pin/unpin automation.
- `skills/skill-forge/scripts/check.py` — Mechanical lint and Agent Plugins validator.
- `skills/skill-densify/scripts/densify.py` — Density analyzer and token budget auditor.

## Commands — `skill-manager`

Invoked as `/skizl <command>`:

| Command | Aliases | What it does |
|---|---|---|
| `pack` | wrap, fold, zip, bundle, forge, merge, knit | Pack standalone skills into a container |
| `unpack` | unwrap, unfold, unzip, burst, smelt, split, unravel | Restore container actions as standalone skills |
| `pin` | link, alias, tap | Create a redirect skill pointing to one container action |
| `unpin` | unlink, detach | Remove a redirect skill |
| `sym` | symlink, link-skills | Symlink `skills/` into `.claude/skills/` and `.agents/skills/` |
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
- **Front-door SKILL.md must stay under 65 lines** — move verbose content to `references/` files
- **Reference files must be explicitly loaded** — Agent reads them on demand when a route/command triggers
- **Pin shortcuts** follow the naming convention `i-<action>` and are symlinked into `.claude/skills/`
- **Version consistency is enforced at commit time** — `git-guard` pre-commit hook blocks commits unless all 7 version sites agree.
