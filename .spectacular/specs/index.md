---
version: 1.2
updated: 2026-07-12
summary: "Index of what this system actually is and how it behaves right now"
related:
  - ../PRD.md
  - ../ARCHITECTURE.md
---

# skizl — System Spec

skizl is a meta-skill interpreted and executed by AI coding agents that manages the lifecycle of skill containers and plugins for Claude Code, Codex, and Google Antigravity. It is built as a set of markdown-based command specifications.

## What this system is

skizl provides an automated suite of commands for packaging, linking, inspecting, versioning, and releasing AI agent skills. It automates manifest creation, implements pre-commit version-drift validation, and handles GitHub release publication safely.

## Capabilities

- **Container Management**: Pack multiple standalone skills into unified references-based containers (`pack`), unpack containers back to standalone skills (`unpack`), and manage lightweight redirect shortcuts (`pin`/`unpin`).
- **Symlinking & Install**: Create relative symlinks from `skills/` to agent runtime directories (`sym`), show installed skills (`list`), and diagnose health issues like broken symlinks, orphaned entries, or long descriptions (`doctor`).
- **Cloning & Scaffolding**: Clone local or remote skill repositories (`fork`), and scaffold plugin manifests for Claude Code, Codex, and Google Antigravity (`publish`).
- **Version Management**: Save versioned snapshots of skills (`snapshot`), view history (`history`), increment frontmatter versions (`bump`), and archive skill directories (`archive`).
- **Git-Guard Hook**: Install a pre-commit drift protection hook (`git-guard`) that checks manifest versions, `metadata.version` in skill frontmatter, and custom CLI version constants (e.g. `SPECTACULAR_VERSION`).
- **Release Automation**: Automate plugin releases (`release`) as an atomic, verified, and resumable workflow with GitHub auth preflighting, scoped execution, testing, and distribution checking.

## How to extend this file

- Add a bullet when a new capability ships (request → verified)
- Promote a bullet to `specs/<capability>.md` when it grows past one line
- Snapshot before major rewrites: `spectacular snapshot .spectacular/specs/index.md`
