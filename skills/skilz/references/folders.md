# Folder Conventions

Standard subdirectory names for skill containers. Use these when they fit; add custom ones when the tool requires it — the names below are conventions, not constraints.

## Standard folders

| Folder | Purpose | When to use |
|---|---|---|
| `references/` | Per-command logic + shared knowledge, loaded on demand | Always — this is the core container pattern |
| `scripts/` | Executable helpers (shell, Python, Node) | When the skill needs to run code |
| `examples/` | Input/output samples for prompting and testing | When showing expected format helps Claude or the user |
| `assets/` | Static resources written to the project at runtime | Templates, configs, seed files the skill copies out |
| `schemas/` | JSON Schemas for structured output validation | When the skill produces machine-readable output |
| `templates/` | Reusable code snippets or boilerplate stubs | API testing, scaffolding, multi-file generation |

## Less common but valid

| Folder | Purpose |
|---|---|
| `data/` | Sample datasets or fixtures for testing without external deps |
| `configs/` | Environment or skill-specific settings, multi-client tuning |
| `boilerplate/` | Starter file packs for project scaffolding |
| `tools/` | Custom helper executables beyond scripts/ (for chained ops) |
| `agents/` | Sub-agent definitions (plugin root only, not inside a skill folder) |

## Rules

- `references/` holds both command files (`pack.md`, `unpack.md`) and shared knowledge files (`platforms.md`, `pipeline.md`) — no need to separate them into subfolders
- `scripts/` is universal and always this name
- Everything in `assets/` is meant to be written to the user's project; everything in `references/` is meant to be read by Claude
- Custom folder names are fine when none of the above fit — just document them in the master SKILL.md
