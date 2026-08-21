# Changelog

All notable changes are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---

## [Unreleased]

## [1.11.0] — 2026-08-21

### Added
- **`skill-densify` skill**: High-density 5-layer micro-kernel compressor that transforms verbose conversational skills into ≤65-line kernels with compact decision tables, mechanical script offloading, silent fast-lanes, and progressive disclosure boundaries. Includes `densify.py` automated density analyzer and token budget auditor.
- **`scripts/skizl-ops.sh`**: Deterministic mechanical helper script providing single-turn CLI execution for `sym-status`, `doctor`, `diffsum`, and `guard-check` (saving up to 96% tokens on exploration turns).

### Changed
- **Micro-Kernel Refactoring across all bundle skills**:
  - `skill-manager`: Compressed from 291 lines down to 56 lines (~80% reduction) using telegraphic micro-kernel routing and silent fast-lane execution format.
  - `skill-forge`: Compressed from 195 lines down to 69 lines (~65% reduction) with tabular operation/track matrices.
  - `skill-draft`: Compressed from 163 lines down to 48 lines (~70% reduction) into a compact single-pass decision engine.
- **Antigravity Safeguards**: Documented critical warning against executing `agy plugin install` on a symlinked plugin target (destructive towards link target). Either symlink/clone directly or install, never both.

## [1.10.1] — 2026-08-17

### Added
- **`sym declare` / `sym json`** — registers skills through Antigravity's declarative `.agents/skills.json` (and `.agents/plugins.json`) instead of symlinks. Full schema documented: `entries`, `inherits`, `include_only`, `exclude`, and the absolute / home-relative / repo-root path resolution rules. Use where git will not store symlinks, on Windows, or to commit the registration so teammates get skills on clone. Merges into an existing file rather than overwriting.
- `publish` documents Antigravity's **plugin enable/disable model**: `"disabled": true` ships a plugin switched off, while the user's choice is recorded in `config.json` under a `plugins` map keyed by *directory* name and always wins. Notes the trade-off — `disabled` is rejected by the closed Agent Plugins schema, so it belongs only in an Antigravity-specific manifest (verified: `check.py --plugin` errors on it, `agy` accepts it).

### Changed
- `agents/` and `commands/` are now marked **CLI-verified only**. Both load under `agy` 1.1.13, but neither appears in the Antigravity 2.0 plugin specification, which documents four components (skills, rules, hooks, MCP servers). Load-bearing behavior belongs in `skills/`, which both surfaces are specified to read.
- `platforms.md` records that Antigravity's authoritative customization reference ships **inside the app** at `~/.gemini/antigravity/builtin/skills/agy-customizations/` and is more complete than the public docs site — the declarative-config schema appears only there. It also notes that Agent Plugins conformance is now confirmed on the **Antigravity 2.0 desktop app** (2.8.1), not just the `agy` CLI: installed at `~/.gemini/config/plugins/`, all three skills load and are listed as `Plugin: skizl`.

## [1.10.0] — 2026-08-17

### Added
- **Agent Plugins 1.0.0 conformance.** The root `plugin.json` is now a conformant [Agent Plugins](https://agent-plugins.org) manifest (`$schema: https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`) — the open, vendor-neutral packaging standard governed by AWS, Cursor, Microsoft, OpenAI, and Vercel, with Google as Core Maintainer. This makes skizl installable on ChatGPT, Codex, Cursor, GitHub Copilot, Kiro, and VS Code from one manifest.
- `git-guard` now checks the root `plugin.json` for version drift, bringing the count to seven version sites. The Agent Plugins schema makes `version` optional, so the file is only checked when it declares one.
- **Plugin-layer validation.** `check.py --plugin` validates an Agent Plugins root: manifest `$schema`, the `name` pattern, the closed top-level field set, `author` sub-keys, `keywords` typing, and reverse-domain `extensions` namespacing. It then validates `mcp.json` — explicit per-server `type`, transport-required fields, `$schema` version agreement with `plugin.json`, and misuse of `PLUGIN_ROOT`/`PLUGIN_DATA` in `command`, URLs, or headers, where they never expand — and finally each discovered skill. Failure isolation follows the spec: a fatal manifest error rejects the plugin, but one broken skill or server never disables the others.
- `doctor` gained four manifest-conformance checks (non-conformant manifest, undiscoverable skill, untyped MCP server, dead plugin variable) and a section documenting the `--plugin` run and what it deliberately does not cover.
- `doctor` gained a **vendor component health** pass for Antigravity: root `hooks.json` and `mcp_config.json` must parse, and every hook script must exist and be executable. A hook script that is missing or non-executable fails silently at run time, so nothing else surfaces it. Bare command names are reported as warnings only, since PATH differs on the target machine.
- `publish` now documents Antigravity's four auto-loaded root components — `skills/`, `rules/*.md`, `hooks.json`, `mcp_config.json` — with templates for each, and states plainly that none is interchangeable with the Claude, Codex, or Agent Plugins equivalent. They stay opt-in: empty scaffolds are noise.
- `platforms.md` gained an **Agent Plugins packaging** section establishing the standard as the portable packaging target, plus guidance on carrying Antigravity as a namespaced `extensions` entry rather than a competing root manifest.

### Changed
- The root `plugin.json` previously carried Antigravity's private schema. Since only one `$schema` value can occupy the field, the Agent Plugins schema takes it and Antigravity-specific data moves to `extensions["com.google.antigravity"]` — the standard's reverse-domain escape hatch for client-specific data. Verified with `agy plugin validate` (CLI 1.1.13): the conformant and the old Antigravity-style manifest validate identically (`[ok]`, all skills processed), while a missing or unparseable `plugin.json` errors. Antigravity ignores `$schema` entirely, so conformance costs nothing there.
- `publish` now scaffolds **portable-first**: the Agent Plugins manifest is the core, and `.claude-plugin/` / `.codex-plugin/` are documented as vendor fallbacks for hosts that have not adopted the standard. `publish.md` also records the closed-schema field list, the `name` pattern constraint, the `extensions` namespacing rule, and the boundary between the portable surface (`skills/`, `mcp.json`) and the vendor-only surface (`agents/`, `commands/`, `hooks/`).
- Antigravity install guidance now distinguishes **two products with separate state trees**. The published plugin docs sit under the Antigravity 2.0 section, so their `~/.gemini/config/plugins/` path describes the desktop app; the `agy` CLI installs to `~/.gemini/antigravity-cli/plugins/`, and the two keep independent skill directories. Both surfaces read the workspace path `.agents/plugins/<name>/`, now documented as the preferred install location.
- `CLAUDE.md` documents all three bundled skills (`skill-manager`, `skill-forge`, `skill-draft`) instead of describing skizl as a single-skill repository, states the authoring/lifecycle boundary between them, and adds a `skill-forge` architecture section covering package layout, the operation-vs-track distinction, `check.py` profile guidance, and the six-brief regression protocol.

### Fixed
- **Incomplete Antigravity install instructions** in `publish.md`, `doctor.md`, and `README.md`. Each named a single global root when there are two — one per surface — so a user following them could install into the tree their Antigravity does not scan. All three now list the desktop root, the CLI root, and the workspace path both surfaces read.
- `publish.md` claimed Antigravity ignores `agents/`. It does not: `agy plugin validate` confirms `agents/` and `commands/` both load, and `commands/` entries are converted to skills. Neither appears in the published documentation.
- `publish.md` claimed the root `plugin.json` carries no version and there was "nothing to bump". It does now, and git-guard checks it — corrected in the release checklist.
- `platforms.md` replaced the stale `gemini` row (which cited `geminicli.com` and a `.gemini/skills/` root) with the documented Antigravity discovery roots and the official `antigravity.google` references. Also corrected the frontmatter guidance: Antigravity documents only `name` and `description`, and `name` defaults to the folder name.

### Notes
- Verified on the `agy` CLI (1.1.13) only. The **Antigravity 2.0 desktop** app has a separate state tree and was not exercised — its plugin loading is documented but untested here.
- Declarative `.agents/skills.json` / `plugins.json` (with `entries`/`inherits`/`include_only`/`exclude`) is not implemented: the format does not appear in the published Antigravity skills, plugins, or CLI reference documentation. Revisit if a specification surfaces.

## [1.9.0] — 2026-08-14

### Added
- Skill Forge **operations** (`Create` / `Update` / `Resume`) — a lifecycle dimension orthogonal to the existing weight tracks. The operation decides where a run starts; the track still decides how much evidence and process the work needs. A completed skill receiving a new request is an Update, not a Resume.
- **Forge record**: compact continuation state (operation, contract, architecture decisions, track, completed gates, feedback deltas, review issue dispositions, evidence, next action) kept outside the distributable skill folder, so process state is never mistaken for runtime content. A new session resumes from the first incomplete gate instead of restarting or relitigating settled decisions.
- **Architecture workshop**: a pre-draft pass over boundary, capability clusters, runtime modes and branches, rules, routing, and only then package shape. Every proposed file must name the branch that reads it and the behavior it changes. Deliberately scale-aware — for a Light skill it stays one compact paragraph and is never expanded into a separate artifact.
- Two-phase review: the reviewer's single prompt splits into a **Full-review prompt** and an issue-scoped **Verification prompt** that checks disposition of a closed issue list without reopening general review.
- Issue **severity and stable IDs** — `blocking` vs `advisory`, with an explicit calibration rule tied to concrete consequence rather than section label. Two reviewer calls are the default maximum; a third requires a major structural rewrite and a recorded reason.
- `extend` mode on the audit track, for a completed skill receiving a new behavioral delta.
- Sixth regression scenario covering the Resume operation: `evals/brief-resume.md`, `evals/prompts/resume.md`, and fixtures (`resume-forge-record.yaml`, `resume-repaired/`), plus a held-out trigger case for resuming an unfinished review.

### Changed
- The standard track reorders around the workshop: contract and architecture map are confirmed first, routing is validated before prose, and the package plan is committed as its own step (8 steps → 9). The empirical track's cross-reference follows to "steps 1–8".
- Reviewer checks expanded with failure recovery, safe resume and rerun idempotency, explicit approval boundaries before consequential actions, tool availability and declared fallbacks, portable path and environment assumptions, output-contract explicitness, evidence-backed completion claims, and proportional evaluation effort with a stopping condition.
- `pass` now always pairs with **right-sized** — an underbuilt or overbuilt verdict requires a blocking issue naming the missing behavior or unjustified process weight. Blockers are never truncated; advisories cap at five.
- Every regression brief now asserts the selected operation before the track, and the light and standard briefs test that workshop output stays proportional to the decision surface.
- Skill Forge bumped 1.1.0 → 1.4.0. Its description now covers create, update, resume, audit, debloat, repair, and activation-boundary tuning. (1.2.0 and 1.3.0 were development increments and were never released separately.)

### Fixed
- `.gitignore` now excludes local secrets (`.env*`, with `*.example` re-included), Python build artifacts, Skill Forge continuation state (`/.skill-forge/`), and local feedback, planning, and article drafts that were never part of the plugin.

## [1.8.0] — 2026-08-13

### Added
- Skill Forge host profiles for the portable Agent Skills specification plus Claude Code, Codex, Cursor, Gemini CLI, and skizl conventions, with official documentation links and explicit portability rules.
- Executable Skill Forge regression fixtures, isolated prompt briefs, a held-out trigger suite, and profile-aware validation for portable and host-specific packages.

### Changed
- Skill Forge now recovers demonstrated workflows before interviewing, preserves descriptions for manual-only skills, chooses instruction rigidity by task fragility, applies least-surprise security rules, and evaluates empirical skills against isolated baselines.
- The fresh-context reviewer now checks host compatibility, invocation behavior, permissions, script dependencies, and evidence quality in addition to sizing and progressive disclosure.
- Expanded Skill Forge guidance, templates, and evals from four illustrative briefs to a repeatable five-scenario regression protocol covering light, standard, empirical, repair, and hardening workflows.

### Fixed
- Replaced shell-looking `skizl` lifecycle examples with an explicit handoff to the installed `skill-manager` skill; `skizl` is a plugin/meta-skill namespace, not a CLI binary.
- Corrected host-specific invocation guidance so portable skills stay portable and vendor-only fields are emitted only for their target host.

## [1.7.0] — 2026-07-12

### Added
- `release` command (`ship`): an atomic, verified, and resumable plugin release workflow supporting scope checks, auth preflights, test suites, and distribution verification.

### Changed
- Upgraded `git-guard` pre-commit hook to support parsing `metadata.version` in skill frontmatter with fallback to top-level `version:`, and validation of arbitrary CLI version constants (e.g. `SPECTACULAR_VERSION` in `cli/spectacular`).

## [1.6.1] — 2026-07-08

### Added
- `skill-forge` skill — a standalone skill-that-writes-skills: a lean router (`SKILL.md`) over four weight tracks (light / standard / empirical / audit), a fresh-context reviewer gate, a co-located `GLOSSARY.md`, minimal templates, and a mechanical `check.py` lint. Self-contained: the empirical track runs its own with-skill-vs-baseline eval loop rather than depending on another skill.
- `skill-draft` skill — the fast lane: sketch a small skill in one pass (single `SKILL.md`, no tracks/reviewer/evals), meant to pair with `skill-forge` for the heavy build.

### Changed
- Renamed the packaged skill `skizl` → `skill-manager`: folder `skills/skizl/` → `skills/skill-manager/` and frontmatter `name:` updated. Invocation is unchanged — the plugin namespace stays `skizl`, so `/skizl <command>` and all `skizl <verb>` commands work as before.
- Leaner, non-overlapping descriptions across the three skills to stop them colliding on triggering: `skill-draft` = quick single-file draft, `skill-forge` = full tracked build with reviewer + evals (each names the other as the off-ramp), `skill-manager` = post-authoring lifecycle only (no "create" verb; dropped the redundant trigger list). `skill-manager` bumped to 1.6.0.
- `skill-forge` learns the draft→forge handoff: its audit track now forks into **repair** mode (trim/fix an aged or bloated skill) and **harden** mode (build up a validated fast draft, e.g. a `skill-draft` output plus human feedback). In harden mode, thinness is the starting point, not a defect — no ceremony is added unless a branch, a failing test, or the feedback demands it. Added the `brief-audit-harden.md` regression brief.

### Removed
- Archived `skill-creator`, `writing-great-skills`, and `progressive-skill-builder` into the repo-root `_archive/` — their doctrine (vocabulary, eval loop, scaffold weighting) is now folded into `skill-forge`, which no longer references them.

---

## [1.6.0] — 2026-07-07

### Added
- Google Antigravity plugin support: `publish` now scaffolds a root `plugin.json` manifest (conforming to the [Antigravity plugin spec](https://antigravity.google/docs/cli/plugins), including the required `$schema` field and description) alongside the Claude and Codex manifests, documents Antigravity's component discovery (`skills/`, `rules/`, root `hooks.json`, root `mcp_config.json`), and reports install paths — workspace `.agents/plugins/` / `_agents/plugins/` and global `~/.gemini/antigravity-cli/plugins/`. Docs are explicit that Antigravity has no marketplace/install CLI for third-party plugins — install is always manual (clone or symlink into a scan directory).
- README: Antigravity install section; skizl repo itself now ships a root `plugin.json` so it installs as an Antigravity plugin directly.

### Changed
- `.gitignore`: excluded `skills/skill-creator/`, `skills/progressive-skill-builder/`, `skills/writing-great-skills/` — local-only skills not part of the skizl plugin.

---

## [1.5.4] — 2026-06-20

### Added
- Description-field safeguards for Codex's 1024-character skill description limit: `pack` now generates and reports bounded frontmatter `description` values, `publish` blocks over-limit descriptions and can produce missing ones, and `doctor` checks installed/source skills for missing, near-limit, or over-limit descriptions. The check applies to `description` alone, not `description` plus `when_to_use`.

### Changed
- Shortened the active skizl skill description so it stays comfortably under the Codex limit.
- `pin.mjs` now normalizes generated shortcut descriptions and caps them before writing redirect skills.

---

## [1.5.3] — 2026-05-16

### Changed
- Install docs: clarified the two Codex install paths — `npx codex-marketplace add … --plugin` (external helper, adds marketplace *and* activates) vs. the native `codex plugin marketplace add` CLI (registers the marketplace only; activate afterward from the in-app `/plugins` browser).
- Corrected `publish.md`: `codex plugin marketplace add` is a valid command (previous docs said otherwise); there is still no `codex plugin install` subcommand.
- Restructured README install section with per-target headings and a "test locally" block.

---

## [1.5.2] — 2026-05-10

### Fixed
- `git-guard` hook: git tag is now allowed to lag behind manifest versions (commit first, tag after is normal workflow). Hook only blocks if a tag is somehow *ahead* of manifests — a genuinely broken state. Tag uses a new `TYPES` parallel array; `collect` accepts optional third arg `"tag"` to opt into this relaxed check.
- Removed the `--no-verify` bootstrap workaround from the install report — no longer needed.

---

## [1.5.1] — 2026-05-10

### Fixed
- `git-guard install`: gather all inputs (existing hook check + SKILL.md question) upfront before writing any files, so the install flow runs without mid-process interruptions
- `git-guard install` Step 4 report: added ⚠ git tag bootstrap note — on the very first commit after install, `--no-verify` is required once (the tag cannot exist before its commit); suggested commands included

---

## [1.5.0] — 2026-05-10

### Added
- `git-guard` command (`version-guard`, `hook`, `drift`): installs a `pre-commit` hook via `core.hooksPath` that collects versions from all 6 locations (manifests, README badge, CHANGELOG, git tag, optional SKILL.md), takes the highest as truth, prints a ✓/✗ table, and blocks the commit if anything diverges
- `references/git-guard.md`: full spec for `install`, `remove`, and `check` sub-commands, including the complete hook script and `.git-guard.json` config
- `publish` Step 5 now auto-runs `git-guard install` when no hook exists, so every published repo gets the guard automatically

### Fixed
- Hook script: empty `VERSIONS` array + `set -u` could crash on bash < 4.4 — replaced `${VERSIONS[@]:-}` with safe `${VERSIONS[@]+"${VERSIONS[@]}"}` expansion
- Hook script: all file paths now anchored to `$(git rev-parse --show-toplevel)` so the hook works correctly when invoked outside the repo root
- Hook script: `sort -V` on macOS BSD sort misorders semver across major digit boundaries (e.g. `1.9 < 1.10`) — added `gsort -V` detection with a pure-bash semver fallback
- Hook script: zero version sources found now prints an explicit notice and exits 0 instead of silently claiming "all consistent"

---

## [1.4.0] — 2026-05-10

### Added
- `snapshot` command: save `SKILL.md` as `versions/SKILL@<version>.md`; auto-triggered on `publish` (if `version:` present) and on `diff` when local is ahead of global installed
- `bump` command: increment `version:` frontmatter (patch/minor/major or explicit), with optional snapshot after bump
- `history` command: list snapshots in `versions/` sorted by semver descending; `--show <ver>` to read, `--diff <ver>` to diff current vs snapshot
- `archive` command: tar the entire skill folder as a timestamped tarball (`_backups/<name>@YYYYMMDD-HHMM[--tag].tar.gz`); always manual, suggested by diff on large-scale changes
- `references/snapshot.md`: full spec for snapshot, bump, and history sub-commands
- `references/archive.md`: full spec for archive including intent-detection table and large-diff heuristic

### Changed
- `diff` now offers to snapshot when local version is ahead of global installed
- `publish` reference updated: `source.path` corrected to `"./"` (relative to repo root), hybrid layout removed, Codex install commands corrected to `npx codex-marketplace add ... --plugin`

---

## [1.3.0] — 2026-05-07

### Added
- `.codex-plugin/plugin.json` enriched with optional `interface` block (displayName, shortDescription, longDescription, developerName, category, capabilities, websiteURL, defaultPrompt, brandColor) for Codex browser UI
- `publish` reference and `create-plugin` skill updated to document the `interface` block as optional, with warning against adding `privacyPolicyURL`/`termsOfServiceURL` unless those files exist

### Changed
- `publish` reference updated with verified Claude Code and Codex install methods from official docs
- Claude Code install key format clarified as `{plugin-name}@{marketplace-key}` — `{marketplace-key}` is the top-level `"name"` in `.claude-plugin/marketplace.json`, `{plugin-name}` is `plugins[0].name`; they are often the same but can differ (e.g. `codex@openai-codex`)
- README install command corrected from `skizl@alexsmedile-skizl` to `skizl@skizl`
- Quick Start examples replaced with generic `writing` container (removed project-specific `cs` container)
- Icon replaced with v2 squircle design matching Blip-style app icon aesthetic

### Fixed
- `.codex-plugin/plugin.json` missing required `version`, `description`, and `skills` fields
- `.agents/plugins/marketplace.json` `source.path` corrected from `"./"` to `"../../"` (resolves relative to `.agents/plugins/`)

---

## [1.2.0] — 2026-05-07

### Fixed
- Removed hardcoded GitHub username from examples in `SKILL.md`, `references/publish.md`, and `references/fork.md` — replaced with generic `<username>` placeholder
- Removed personal file paths from `references/list.md` output example — replaced with `/path/to/...`
- `publish` command now resolves GitHub identity via `gh api user` (login for URL fields, full name for `author.name`) with `git config user.name` as fallback
- `author.name` / `owner.name` in all plugin manifests corrected to full display name

---

## [1.1.0] — 2026-05-07

### Added
- `sym` command with sub-commands `init` / `in`, `migrate` / `out`, `status` — symlinks `skills/` into `.claude/skills/` and `.agents/skills/` using portable relative symlinks
- `list` command — shows installed skills across global, project, and source locations with symlink state (linked / broken / direct / source)
- `diff` command — compares two versions of a skill's `SKILL.md`, with version field extraction from frontmatter
- `doctor` command — diagnoses broken symlinks, missing `SKILL.md`, direct directories, orphaned agent links, and unlinked source skills
- `fork` command — clones a skill from a local path or GitHub URL into `skills/<name>/` and symlinks it; strips git history on clone
- `publish` command — scaffolds `.claude-plugin/`, `.codex-plugin/`, and `.agents/plugins/` manifests from `SKILL.md` frontmatter; generates `README.md` if missing
- `IDEAS.md` — name brainstorm and action backlog

### Changed
- Skill renamed from `skilz` to `skizl`
- `references/` architecture replaces `actions/` + `knowledge/` layout
- `list` promoted from alias of `status` to standalone command
- `status` alias list updated (removed `list`, kept `info`)
- Command order in `SKILL.md` reordered: `sym` first, `status` and `onboard` last

## [1.0.0] — 2026-05-07

### Added
- Initial release: `pack`, `unpack`, `pin`, `unpin`, `status`, `onboard` commands
- `scripts/pin.mjs` for pin/unpin automation
- Plugin manifests for Claude Code and Codex
