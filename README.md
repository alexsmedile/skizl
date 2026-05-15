<div align="center">
  <img src="docs/assets/skizl-icon-v2.svg" width="80" alt="skizl icon" />
</div>

# skizl

![License](https://img.shields.io/badge/license-MIT-blue)
![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)
![Version](https://img.shields.io/badge/version-1.5.3-green)

**From scattered slash commands to a versioned, publishable skill library.**

Pack. Version. Publish. One skill to manage them all.

---

> Your Claude Code skills deserve better than a flat folder.

As your skill library grows, flat folders stop working. You end up with 20 loose `SKILL.md` files — no shared context, no version history, no way to publish, no way to know what's installed where.

`skizl` is the skill lifecycle manager Claude Code was missing. It gives your skills the same workflows you'd expect from any serious package: organize into containers, wire up shortcuts, diff versions, snapshot before big changes, and publish to the marketplace in one command.

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
| `publish` | release, scaffold | Scaffold plugin manifests for Claude + Codex marketplaces |
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

**Distribute** — `fork` clones a skill from a local path or GitHub URL. `publish` scaffolds all plugin manifests (`.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/`) from your `SKILL.md` frontmatter in one pass.

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

Or via the built-in plugin manager:

```bash
codex plugin marketplace add alexsmedile/skizl
# then: codex /plugins → browse and install
```

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

---

## Who It's For

- Claude Code users with 10+ skills who want structure without overhead
- Anyone building a skill container library to share or reuse
- Developers who want to publish skills to the Claude and Codex marketplaces

## Who It's Not For

- Users with just a few skills — a flat folder works fine at small scale
- Non-Claude-Code environments — skizl is Claude Code-native
