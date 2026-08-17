---
name: skill-manager
description: |
  Manage the lifecycle of skills that already exist: pack/unpack references-based containers,
  pin shortcuts, symlink into .claude/skills/, snapshot/bump/diff versions, fork, archive, and
  publish plugin manifests (Claude, Codex, Antigravity). Invoked as /skizl <command>. Not for
  authoring a skill's content — use skill-forge or skill-draft for that.
argument-hint: "pack|unpack|pin|unpin|sym|list|diff|doctor|fork|publish|snapshot|bump|history|archive|status|onboard"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
version: 1.7.0
---

> [!IMPORTANT]
> `skizl` is NOT a CLI binary installed on the system shell. It is a meta-skill interpreted and executed by the AI agent. The user invokes commands using the slash command `/skizl <command>` in the chat UI, and the AI agent performs the operations by reading these instructions. The AI agent must *never* try to execute a `skizl` command in the shell.

Manages the lifecycle of skill containers: pack, unpack, pin, unpin.

## Commands

| Command | Accepted aliases | What it does |
|---|---|---|
| `pack` | wrap, fold, zip, bundle, forge, merge, knit | Create a container from standalone skills |
| `unpack` | unwrap, unfold, unzip, burst, smelt, split, unravel | Restore container actions as standalone skills |
| `pin` | link, alias, tap | Create a redirect skill that delegates to the container |
| `unpin` | unlink, detach | Remove a redirect skill |
| `sym` | symlink, link-skills, install-skills | Symlink skills/ into .claude/skills/ and .agents/skills/ |
| `list` | ls, installed | Show installed skills with their symlink state |
| `diff` | compare, changes | Compare two versions of a skill |
| `doctor` | check, diagnose, health | Diagnose skill installation issues |
| `fork` | clone, copy, branch | Clone a skill (local or GitHub URL) as a personal variant |
| `publish` | scaffold, plugin | Scaffold plugin manifests to publish a skill on GitHub |
| `release` | ship | Make a verified, atomic plugin release |
| `snapshot` | save, checkpoint, freeze | Save current SKILL.md as a versioned snapshot in versions/ |
| `bump` | version, semver, increment | Bump version: field in frontmatter (patch/minor/major) |
| `history` | log, versions, changelog | List or inspect snapshots for a skill |
| `archive` | backup, tar, zip-full, freeze-all | Archive the entire skill folder as a tarball |
| `status` | info | Inspect a container's structure and active pins |
| `onboard` | help, intro, explain, tour, howto | Explain how skizl works and guide first use |
| `git-guard` | version-guard, hook, drift | Install/remove/check pre-commit version consistency hook |

## Routing

1. **No argument** — print the commands table above and ask what to do
2. **First word = command or alias** — normalize to canonical, load `references/<canonical>.md` and follow
3. **Free text** — interpret the intent, choose the most likely action, ask for confirmation before proceeding

**Alias → canonical normalization:**
- wrap / fold / zip / bundle / forge / merge / knit → `pack`
- unwrap / unfold / unzip / burst / smelt / split / unravel → `unpack`
- link / alias / tap → `pin`
- unlink / detach → `unpin`
- symlink / link-skills / install-skills → `sym`
- ls / installed → `list`
- compare / changes → `diff`
- check / diagnose / health → `doctor`
- clone / copy / branch → `fork`
- scaffold / plugin → `publish`
- ship → `release`
- save / checkpoint / freeze → `snapshot`
- version / semver / increment → `bump`
- log / versions / changelog → `history`
- backup / tar / zip-full / freeze-all → `archive`
- info → `status`
- help / intro / explain / tour / howto → `onboard`
- version-guard / hook / drift → `git-guard`

---

## PACK

Read `references/pack.md` for full instructions.

**Quick usage:** `/skizl pack <container-name> <skill1> <skill2> ...`

**Example:** `/skizl pack cs brainstorm strategize generate design-pass`

---

## UNPACK

Read `references/unpack.md` for full instructions.

**Quick usage:** `/skizl unpack <container-path> [--dest <directory>]`

**Example:** `/skizl unpack skills/cs --dest skills/`

---

## PIN

Read `references/pin.md` for full instructions.

**Quick usage:** `/skizl pin <container-path> <action>`

Or from inside a container: `/<container-name> pin <action>`

---

## UNPIN

**Usage:** `/skizl unpin <container-path> <action>`

```bash
SKILLS_DIR=$(dirname <container-path>)
rm -rf "$SKILLS_DIR/i-<action>"
[ -L ".claude/skills/i-<action>" ] && rm ".claude/skills/i-<action>"
echo "Unpinned: /<action> removed"
```

---

## SYM

Read `references/sym.md` for full instructions.

**Sub-commands:**
- `/skizl sym init` / `/skizl sym in` — link all skills from `skills/` into `.claude/skills/` and `.agents/skills/`
- `/skizl sym migrate` / `/skizl sym out` — move real dirs from `.claude/skills/` into `skills/` and re-link
- `/skizl sym status` — show what's linked, what's missing
- `/skizl sym declare` / `/skizl sym json` — register skills via `.agents/skills.json` instead of symlinks (Antigravity; works where symlinks don't)

---

## LIST

Read `references/list.md` for full instructions.

**Quick usage:** `/skizl list`

Lists all skills in `skills/`, `~/.claude/skills/`, and `.claude/skills/` with their symlink state (linked / unlinked / broken).

---

## DIFF

Read `references/diff.md` for full instructions.

**Quick usage:** `/skizl diff <skill-path> [<other-skill-path>]`

Compares two versions of a skill's `SKILL.md`. If only one path is given, diffs against the installed global version.

---

## DOCTOR

Read `references/doctor.md` for full instructions.

**Quick usage:** `/skizl doctor [<skill-name>]`

Checks for broken symlinks, missing SKILL.md, version mismatches, and orphaned entries in `.claude/skills/`.

---

## FORK

Read `references/fork.md` for full instructions.

**Quick usage:** `/skizl fork <source> [--name <new-name>]`

`<source>` can be a local path or a GitHub URL (e.g. `https://github.com/user/repo`). Clones the skill into `skills/<new-name>/` and symlinks it.

---

## PUBLISH

Read `references/publish.md` for full instructions.

**Quick usage:** `/skizl publish <skill-path> [--username <github-username>]`

**Example:** `/skizl publish skills/my-skill --username <username>`

Reads `SKILL.md` frontmatter to pre-fill name, description, and version. Creates `.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/`, and a root `plugin.json` (Antigravity marker) at the repo root. Generates a `README.md` if missing.

---

## RELEASE

Read `references/release.md` for full instructions.

**Quick usage:** `/skizl release [--dry-run] [--scope <paths>] [--bump <type>]`

**Example:** `/skizl release --dry-run`

Runs a verified, atomic release workflow for the plugin repository. It ensures Git hygiene, runs checks, bumps all version sources (including CLI constants), commits, tags, pushes, creates the GitHub Release, and verifies remote distribution.

---

## SNAPSHOT

Read `references/snapshot.md` for full instructions.

**Quick usage:** `/skizl snapshot <skill-path>`

Saves the current `SKILL.md` as `versions/SKILL@<version>.md`. Auto-triggered on `publish` (before writing manifests) and after `diff` when local is ahead.

---

## BUMP

Read `references/snapshot.md` for full instructions.

**Quick usage:** `/skizl bump <skill-path> [patch|minor|major|<version>]`

Increments `version:` in frontmatter, then offers to snapshot. If bump type is omitted, asks interactively.

---

## HISTORY

Read `references/snapshot.md` for full instructions.

**Quick usage:** `/skizl history <skill-path>`

Lists all snapshots in `versions/`. Use `--show <ver>` to read one, `--diff <ver>` to diff current vs snapshot.

---

## ARCHIVE

Read `references/archive.md` for full instructions.

**Quick usage:** `/skizl archive <skill-path> [--dest <directory>]`

Archives the entire skill folder (including `references/`, `scripts/`, `versions/`, etc.) as a timestamped tarball. Always manual — never auto-triggered. Skizl may suggest it when a diff shows large-scale changes.

---

## STATUS

**Usage:** `/skizl status <container-path>`

```bash
echo "=== Container: <name> ==="
echo "References:"; ls <container-path>/references/ 2>/dev/null || echo "(none)"
echo "Scripts:"; ls <container-path>/scripts/ 2>/dev/null || echo "(none)"
echo "Active pins:"
SKILLS_DIR=$(dirname <container-path>)
ls "$SKILLS_DIR" | grep "^i-" || echo "(none)"
```

---

## ONBOARD

Read `references/onboard.md` for full instructions.

---

## GIT-GUARD

Read `references/git-guard.md` for full instructions.

**Quick usage:** `/skizl git-guard install`

Installs a `pre-commit` git hook (via `core.hooksPath`) that checks all version strings in the repo agree before every commit — manifests, README badge, CHANGELOG, git tag, and optionally SKILL.md. Blocks commits when versions diverge and prints exactly which files are out of sync.

---

## References

- [sym](references/sym.md)
- [pack](references/pack.md)
- [unpack](references/unpack.md)
- [pin](references/pin.md)
- [list](references/list.md)
- [diff](references/diff.md)
- [doctor](references/doctor.md)
- [fork](references/fork.md)
- [publish](references/publish.md)
- [release](references/release.md)
- [snapshot / bump / history](references/snapshot.md)
- [archive](references/archive.md)
- [onboard](references/onboard.md)
- [Folder conventions](references/folders.md)
- [git-guard](references/git-guard.md) — pre-commit version drift protection

---

## Common errors

| Symptom | Fix |
|---|---|
| Source skill not found | Specify the absolute path or verify it is in `.claude/skills/` or `skills/` |
| Master SKILL.md > 500 lines | Move verbose sections to `references/` and link them |
| Pin not triggering | Verify the redirect skill is in `.claude/skills/` as a symlink |
| Knowledge not loaded | Add an explicit reference in the action file (`See [file](../references/file.md)`) |
