# Changelog

All notable changes are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

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
