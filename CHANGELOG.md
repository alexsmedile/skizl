# Changelog

All notable changes are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

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
