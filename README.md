<div align="center">
  <img src="docs/assets/skizl-icon-v2.svg" width="80" alt="skizl icon" />
</div>

# skizl

![License](https://img.shields.io/badge/license-MIT-blue)
![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)
![Agent Plugins](https://img.shields.io/badge/Agent%20Plugins-1.0.0-orange)
![Version](https://img.shields.io/badge/version-1.10.1-green)

**From scattered slash commands to a versioned, publishable skill library.**

Pack. Version. Publish. One skill to manage them all.

---

> Your Claude Code skills deserve better than a flat folder.

As your skill library grows, flat folders stop working. You end up with 20 loose `SKILL.md` files — no shared context, no version history, no way to publish, no way to know what's installed where.

`skizl` is a cross-host skill lifecycle manager. It gives your skills the same workflows you'd expect from any serious package: organize into containers, wire up shortcuts, diff versions, snapshot before big changes, and publish to supported plugin formats through an agent workflow.

---

## ⚡ Quick Start

**Install:**

```bash
npx skills add alexsmedile/skizl
```

**Pack related skills into a container:**

```
/skizl pack write, summarize, and proofread skills into writing skill container
```

**Wire every skill into Claude Code at once:**

```
/skizl sym in
```

**Snapshot before a big change:**

```
/skizl snapshot skills/writing
```

**Publish to the Claude + Codex marketplace:**

```
/skizl publish skills/writing --username your-github-username
```

`/skizl` is a skill/plugin invocation shown to the agent host, not a terminal executable.
Do not run `skizl ...` in a shell. In Codex, invoke the installed `skizl:skill-manager`
skill and request the same lifecycle action in natural language.

### Build skills with Skill Forge

This plugin also includes `skill-forge`, the full authoring and audit workflow for skills that
need branches, progressive disclosure, a fresh-context review gate, or measurable evals. It
targets portable Agent Skills by default and has explicit profiles for Claude Code, Codex,
Cursor, Gemini CLI, and skizl.

Use `skill-draft` for a small one-file skill. Use `skill-forge` to design a non-trivial skill,
harden a validated draft, or audit and debloat an existing one. Versioning and publishing then
hand off to `skill-manager`; installing or symlinking remains an explicit deployment action.

Each run picks an **operation** — `Create` (no usable skill yet), `Update` (a completed skill
needs a behavioral delta), or `Resume` (an unfinished run continues from its recorded state).
The operation says where the run starts; the track still says how much process the work needs.
Resume reads a **forge record** kept outside the skill folder, so a new session picks up at the
first incomplete gate instead of restarting or reopening settled decisions.

Before any folders are chosen, an **architecture workshop** maps boundaries, capability clusters,
real runtime branches, and routing — so the scaffold follows how the skill actually runs rather
than mirroring topic headings. It scales to the decision surface: a single-rule skill gets one
paragraph, not a table. The review gate then runs a fresh-context full review, and — only if it
found blockers — one issue-scoped verification, with two reviewer calls as the hard default.

---

## 📦 The Container Pattern

Instead of N folders with duplicated context, one container routes to on-demand action files. Only `SKILL.md` is loaded automatically — everything else is pulled when needed.

**Before:**
```
skills/
├── draft/SKILL.md
├── revise/SKILL.md
├── summarize/SKILL.md
└── proofread/SKILL.md
```

**After:**
```
skills/writing/
├── SKILL.md              ← routing + menu (<500 lines, auto-loaded)
├── references/
│   ├── draft.md          ← loaded on demand
│   ├── revise.md
│   ├── summarize.md
│   └── style-guide.md   ← shared knowledge, one place
└── scripts/
    └── pin.mjs
```

Benefits:
- One slash command (`/writing`) instead of four
- Shared knowledge lives in `references/` — no duplication
- Master `SKILL.md` stays lean — no context bloat
- Pack and unpack are reversible copy operations — nothing is ever destroyed

---

## 🔧 Commands

| Command | Aliases | What it does |
|---------|---------|--------------|
| `pack` | wrap, fold, bundle, forge | Pack standalone skills into a container |
| `unpack` | unwrap, unfold, burst, smelt | Restore container actions as standalone skills |
| `pin` | link, alias, tap | Create an `/i-<action>` shortcut for one container action |
| `unpin` | unlink, detach | Remove a shortcut |
| `sym` | symlink, link-skills | Symlink `skills/` into `.claude/skills/` and `.agents/skills/` |
| `list` | ls, installed | Show installed skills with their symlink state |
| `diff` | compare, changes | Compare two versions of a skill's `SKILL.md` |
| `doctor` | check, diagnose | Diagnose broken symlinks, missing files, orphaned entries |
| `fork` | clone, copy | Clone a skill (local or GitHub URL) as a personal variant |
| `publish` | scaffold | Scaffold plugin manifests for Claude, Codex + Antigravity |
| `release` | ship | Make a verified, atomic plugin release |
| `snapshot` | save, checkpoint, freeze | Save `SKILL.md` as `versions/SKILL@x.y.z.md` |
| `bump` | version, semver, increment | Increment `version:` in frontmatter (patch/minor/major) |
| `history` | log, versions, changelog | List, show, or diff versioned snapshots |
| `archive` | backup, tar, zip-full | Archive the entire skill folder as a timestamped tarball |
| `status` | info | Inspect a container's structure and active pins |
| `onboard` | help, intro, explain | Explain how skizl works and guide first use |
| `git-guard` | version-guard, hook, drift | Install/remove/check pre-commit version consistency hook |

All operations are **non-destructive**. Pack and unpack are copy operations — source files are never modified or deleted.

---

## 🧠 How It Works

<img src="docs/assets/skizl-flow.svg" width="100%" alt="skizl flow diagram" />

skizl covers the full skill lifecycle in four phases:

**Organize** — `pack` collapses N standalone skills into one container with a `references/` folder. `unpack` reverses it. `pin` creates a shortcut redirect so any container action is reachable as its own slash command.

**Wire** — `sym in` symlinks your entire `skills/` directory into `.claude/skills/` and `.agents/skills/` using portable relative symlinks. `list` and `doctor` show you what's installed, linked, broken, or missing.

**Version** — `snapshot` saves the current `SKILL.md` as `versions/SKILL@x.y.z.md` before changes. `bump` increments the version field and offers to snapshot. `diff` compares two versions — and offers to snapshot if local is ahead. `history` lists all snapshots with `--show` and `--diff` flags. `archive` tarballs the whole skill folder when a diff shows large-scale changes.

**Distribute** — `fork` clones a skill from a local path or GitHub URL. `publish` scaffolds all plugin manifests (`.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/`, root `plugin.json` for Antigravity) from your `SKILL.md` frontmatter in one pass. `release` executes an atomic, verified, and resumable plugin release to GitHub and Codex.

---

## 📌 pin.mjs

`scripts/pin.mjs` automates pin/unpin without manual file creation. No external dependencies — standard Node.js only.

```bash
node scripts/pin.mjs --list skills/writing          # show active pins
node scripts/pin.mjs skills/writing draft           # create /i-draft pin
node scripts/pin.mjs --remove skills/writing draft  # remove pin
node scripts/pin.mjs --skills-dir ~/.claude/skills skills/writing draft
```

The script reads `SKILL.md` frontmatter to extract `name`, `allowed-tools`, and the action description. Pins are automatically symlinked into `.claude/skills/` if that directory exists.

---

## 💾 Install

skizl ships a conformant [Agent Plugins 1.0.0](https://agent-plugins.org) manifest
at its repo root — the open, vendor-neutral packaging standard maintained by AWS,
Cursor, Microsoft, OpenAI, and Vercel, with Google as a Core Maintainer. Any host
that reads the standard can install it directly from the repository. The
per-runtime instructions below cover hosts that use their own format.

### Claude Code — marketplace

```bash
/plugin marketplace add alexsmedile/skizl
/plugin install skizl@skizl
```

Or open the interactive `/plugin` manager and browse from there.

### Codex — marketplace

Fastest — one command, activates the plugin directly:

```bash
npx codex-marketplace add alexsmedile/skizl --plugin
```

Or via the native Codex CLI — two commands, no interactive step:

```bash
codex plugin marketplace add alexsmedile/skizl
codex plugin add skizl@skizl
```

Or add the marketplace and browse interactively with `codex /plugins`.

> Prefer a Git marketplace over a local one. `codex plugin marketplace upgrade`
> refreshes **Git** snapshots only — a marketplace added from a local path never
> updates, and its plugins stay pinned at the version you first installed.

### Google Antigravity

Antigravity ships both a CLI and an app. Plugins are discovered from a scan
directory, so cloning or symlinking into one installs the plugin:

```bash
# workspace-level (this workspace only) — read by BOTH the app and the CLI
git clone https://github.com/alexsmedile/skizl .agents/plugins/skizl

# global — Antigravity 2.0 desktop app
git clone https://github.com/alexsmedile/skizl ~/.gemini/config/plugins/skizl

# global — agy CLI (separate state tree from the app)
git clone https://github.com/alexsmedile/skizl ~/.gemini/antigravity-cli/plugins/skizl
```

The app and the CLI keep independent global roots, so a global install in one is
not visible to the other. The workspace path is the only location both scan.

### npx skills

```bash
npx skills add alexsmedile/skizl       # project-scoped
npx skills add alexsmedile/skizl -g    # global
```

### Test locally (no install)

```bash
git clone https://github.com/alexsmedile/skizl
claude --plugin-dir ./skizl                  # Claude Code
npx codex-marketplace add ./skizl --plugin   # Codex
```

Invoke as `/skizl <command>` after install. Run `/skizl onboard` if it's your first time.

### Private repos and team sharing

Marketplaces are not public-only. Claude Code and Codex both `git clone` over
HTTPS, so a private repo installs exactly like a public one as long as git can
already authenticate. Once per machine:

```bash
gh auth login
gh auth setup-git    # routes HTTPS github.com clones through your gh token
```

Then the usual commands work unchanged against a private repo:

```bash
/plugin marketplace add yourorg/private-skills
/plugin install toolkit@private-skills
```

To share a skill with a team, publish it to a private org repo and grant access
by GitHub team membership — distribution is governed by repo permissions, not by
anything plugin-specific. Useful extras:

| Flag | Effect |
|------|--------|
| `--scope project` | Declares the marketplace in the project's committed `.claude/settings.json`, so teammates get it on clone (they still need repo access). |
| `--sparse <paths>` | Limits the checkout to given directories — for skills living inside a larger monorepo. |
| `--ref <ref>` | Codex only. Pins the marketplace to a branch or tag, so the team tracks `stable` instead of `main`. |

> Teammates who skip `gh auth setup-git` see a failure that reads like a missing
> repo rather than a permission error — worth calling out, since it looks like a
> typo in the owner or repo name.

---

## Who It's For

- Agent-skill authors with growing libraries who want structure without overhead
- Anyone building a skill container library to share or reuse
- Developers who want to author for Claude Code, Codex, Cursor, or Gemini and publish supported plugin formats

## Who It's Not For

- Users with just a few skills — a flat folder works fine at small scale
- Workflows that require a standalone `skizl` terminal binary — skizl is an agent skill/plugin, not a CLI
