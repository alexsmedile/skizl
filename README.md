<div align="center">
  <img src="docs/assets/skizl-icon-v2.svg" width="80" alt="skizl icon" />
</div>

# skizl

![License](https://img.shields.io/badge/license-MIT-blue)
![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)
![Version](https://img.shields.io/badge/version-1.3.0-green)

**Turn a pile of standalone skills into a clean, organized skill library in one command.**

---

As your Claude Code skill library grows, flat folders become unmanageable. `skizl` introduces the **container pattern** — a single master skill that routes to on-demand action files, keeping context lean and structure clear.

Pack 10 skills into 1 container. Unpack any container back to standalone. Pin shortcuts so any action is one slash command away. Symlink, inspect, diff, fork, and publish your skill library.

---

## ⚡ Quick Start

**Install via [skills](https://github.com/vercel-labs/skills):**

```bash
npx skills add alexsmedile/skizl
```

**Pack a group of standalone skills into a container:**

```bash
/skizl pack writing draft revise summarize proofread
```

**Unpack a container back to standalone:**

```bash
/skizl unpack skills/writing --dest skills/
```

**Pin a single action as its own shortcut:**

```bash
/skizl pin skills/writing draft
# Creates /i-draft → delegates to writing container
```

**Symlink all skills into Claude Code in one command:**

```bash
/skizl sym in
```

---

## 📦 Container Architecture

A container is a master skill that loads action logic on demand — only `SKILL.md` is read automatically; everything else is pulled when needed.

**Instead of:**

```
skills/
├── brainstorm/
│   └── SKILL.md
├── generate/
│   └── SKILL.md
└── design/
    └── SKILL.md
```

**You get:**

```
skills/<master-skill>/
├── SKILL.md           ← routing + command menu (<500 lines, auto-loaded)
├── references/        ← per-command logic + shared knowledge, loaded on demand
│   ├── brainstorm.md
│   ├── generate.md
│   ├── design.md
│   └── platforms.md  ← shared knowledge lives here too, same folder
└── scripts/
    └── pin.mjs        ← pin/unpin automation
```

<img src="docs/assets/skizl-flow.svg" width="100%" alt="skizl flow diagram" />

**Why containers?**
- One folder instead of N folders for related skills
- Shared knowledge in `references/` — no duplication across command files
- Master `SKILL.md` stays under 500 lines — no context bloat
- Each command file is independently readable and editable

---

## 🔧 Commands

| Command | Aliases | What it does |
|---------|---------|--------------|
| `pack` | wrap, fold, zip, bundle, forge, merge, knit | Pack standalone skills into a container |
| `unpack` | unwrap, unfold, unzip, burst, smelt, split, unravel | Restore container actions as standalone skills |
| `pin` | link, alias, tap | Create an `i-<action>` redirect skill for one container action |
| `unpin` | unlink, detach | Remove a redirect skill |
| `sym` | symlink, link-skills | Symlink `skills/` into `.claude/skills/` and `.agents/skills/` (`in` / `out` / `status`) |
| `list` | ls, installed | Show installed skills with their symlink state |
| `diff` | compare, changes | Compare two versions of a skill |
| `doctor` | check, diagnose | Diagnose broken symlinks, missing files, orphaned entries |
| `fork` | clone, copy | Clone a skill (local or GitHub URL) as a personal variant |
| `publish` | release, scaffold | Scaffold plugin manifests to publish a skill on GitHub |
| `status` | info | Inspect a container's structure and active pins |
| `onboard` | help, intro, explain | Explain how skizl works and guide first use |

All operations are **non-destructive** — pack and unpack are copy operations. Source files are never modified or deleted.

---

## 📄 pin.mjs

`scripts/pin.mjs` automates pin/unpin without manual file creation. No external dependencies — standard Node.js only.

```bash
# List active pins for a container
node scripts/pin.mjs --list skills/cs

# Create a pin
node scripts/pin.mjs skills/cs brainstorm

# Remove a pin
node scripts/pin.mjs --remove skills/cs brainstorm

# Specify a custom skills directory
node scripts/pin.mjs --skills-dir ~/.claude/skills skills/cs brainstorm
```

The script reads the container's `SKILL.md` frontmatter to extract `name`, `allowed-tools`, and the action's description from the commands table. Pins are automatically symlinked into `.claude/skills/` if that directory exists.

---

## 💾 Installation

**Via Claude Code plugin marketplace:**

```
/plugin marketplace add alexsmedile/skizl
/plugin install skizl@skizl
```

**Via Codex:**

Add as a marketplace source, then install via the plugin browser:

```bash
codex plugin marketplace add alexsmedile/skizl
```

Then run `codex /plugins` to open the browser and install.

**Via npx skills (global):**

```bash
npx skills add alexsmedile/skizl -g
```

**Via npx skills (project-scoped):**

```bash
npx skills add alexsmedile/skizl
```

**Target a specific agent:**

```bash
npx skills add alexsmedile/skizl -a claude-code
```

Invoke as `/skizl <command>` after install.

---

## Who It's For

- Claude Code users managing 10+ skills who want structure
- Anyone building or maintaining a skill container library
- Developers who want to expose individual container actions as top-level shortcuts

## Who It's Not For

- Users with just a few skills (flat structure is fine)
- Non-Claude-Code environments
