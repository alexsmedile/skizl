---
name: skill-manager
description: |
  Manage the lifecycle of skills that already exist: pack/unpack references-based containers,
  pin shortcuts, symlink into .claude/skills/, snapshot/bump/diff versions, fork, archive, and
  publish plugin manifests (Claude, Codex, Antigravity). Invoked as /skizl <command>. Not for
  authoring a skill's content — use skill-forge or skill-draft for that.
argument-hint: "pack|unpack|pin|unpin|sym|list|diff|doctor|fork|publish|release|snapshot|bump|history|archive|status|onboard|git-guard"
allowed-tools: [Bash, Read, Write, Edit]
version: 1.8.0
category: devtools
status: current
tags: [meta, skills, management, lifecycle]
---

# Skill Manager

Lifecycle governor for skill containers, symlinks, snapshots, versions, and manifests.
*Never execute `skizl` as a shell command — it is an agent meta-skill.*

## 1. Quick Guard & Fast-Paths

Mechanical inspection scripts for single-turn discovery:
```bash
SKIZL_OPS="${CLAUDE_SKILL_DIR:-<skill-dir>}/scripts/skizl-ops.sh"
bash "$SKIZL_OPS" sym-status   # check .claude / .agents symlink matrix
bash "$SKIZL_OPS" doctor       # check broken symlinks, missing files, sync
bash "$SKIZL_OPS" guard-check  # audit 7 version sites across manifests
bash "$SKIZL_OPS" diffsum <path> # 3-line version diff summary
```

## 2. Command Routing Matrix

Route enum strictly pinned to: `pack | unpack | pin | unpin | sym | list | diff | doctor | fork | publish | release | snapshot | bump | history | archive | status | onboard | git-guard`.

| Commands | Accepted Aliases | Action / Reference |
|---|---|---|
| `pack` / `unpack` | wrap, fold, zip, bundle / burst, smelt, split | Read [references/pack.md](references/pack.md) or [unpack.md](references/unpack.md) |
| `pin` / `unpin` | link, alias, tap / unlink, detach | Read [references/pin.md](references/pin.md) -> Manage redirect skills |
| `sym` | symlink, link-skills, install-skills | Read [references/sym.md](references/sym.md) -> Link `skills/` to `.claude`/`.agents` |
| `list` / `status` | ls, installed / info | Read [references/list.md](references/list.md) or inspect container structure |
| `diff` / `doctor` | compare, changes / check, diagnose, health | Read [references/diff.md](references/diff.md) or [doctor.md](references/doctor.md) |
| `snapshot` / `bump` / `history` | save, freeze / semver, increment / log | Read [references/snapshot.md](references/snapshot.md) -> Version management |
| `fork` / `archive` | clone, copy, branch / backup, tar, zip-full | Read [references/fork.md](references/fork.md) or [archive.md](references/archive.md) |
| `publish` / `release` | scaffold, plugin / ship | Read [references/publish.md](references/publish.md) or [release.md](references/release.md) |
| `git-guard` | version-guard, hook, drift | Read [references/git-guard.md](references/git-guard.md) -> Pre-commit hook |
| `onboard` | help, intro, explain, tour, howto | Read [references/onboard.md](references/onboard.md) -> First-time guide |

## 3. Fast-Lane Execution & Report Box

For deterministic operations, execute silently and emit only the completion box:
```text
┌─ SKIZL · <command> · <target>
│ effect    <concrete changes made / files created>
│ status    <clean summary state>
│ next      <safe follow-up or ready>
└─
```

## 4. Invariants

- **Non-Destructive**: `pack`/`unpack` are copy operations; never delete source files.
- **Separation**: `skill-forge`/`skill-draft` author content; `skill-manager` never authors.
- **Version Parity**: All 7 manifest and documentation version locations must stay in sync.
