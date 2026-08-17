# Target host profiles

Use this when: selecting skill location, frontmatter, invocation controls, UI metadata, or
distribution for a specific host. Re-check the linked official docs when compatibility is a
release requirement; host extensions evolve faster than the open standard.

## Portable Agent Skills

Default here when the user names no host. Require `name` and `description`; allow only
`license`, `compatibility`, `metadata`, and experimental `allowed-tools` in addition. Put
version/author/category data under `metadata` as string values. Match the directory name to a
1–64 character lowercase-hyphen name, keep description within 1024 characters, use relative
skill-root paths, and keep reference chains one level deep.

Official reference: https://agentskills.io/specification

## Host extensions

| Profile | Authoring/discovery | Invocation and metadata | Distribution/testing |
|---|---|---|---|
| `claude` | `.claude/skills/` or plugin `skills/`; also supports `.agents/skills/` | `disable-model-invocation`, `user-invocable`, `when_to_use`, arguments, `context`, `agent`, `model`, and `allowed-tools`; manual-only keeps `description` | Test via direct `/name` and fresh auto-trigger prompts; plugin skills are namespaced |
| `codex` | Repository/user `.agents/skills/`; optional `agents/openai.yaml` | Keep SKILL.md portable; put UI, implicit-invocation policy, and MCP dependencies in `agents/openai.yaml` | Local/repo skills for authoring; plugins for reusable distribution; test `$name` plus implicit prompts |
| `cursor` | `.agents/skills/` or `.cursor/skills/`; nested roots scope monorepos | `paths`, `disable-model-invocation`, `metadata`; legacy `globs` is compatibility-only | Test slash invocation, automatic relevance, and file-path scoping |
| `gemini` | Workspace `.agents/skills/<name>/` (legacy `.agent/skills/` still read); user `~/.gemini/config/skills/<name>/` | Only `name` and `description` are documented, and `name` defaults to the folder name — keep frontmatter portable. Write `description` in third person with the trigger keywords the agent should match | Test discovery, activation, and bundled resource access; ship as a plugin (see below) rather than hand-linking |
| `skizl` | Plugin skill under `skills/` | Claude-compatible fields plus library `version`, `category`, `status`, and `tags` conventions | Validate with `--profile skizl`; lifecycle uses skizl commands only on explicit request |

Official host references:

- Claude: https://code.claude.com/docs/en/skills
- OpenAI: https://learn.chatgpt.com/docs/build-skills
- Cursor: https://cursor.com/docs/skills
- Google Antigravity — skills: https://antigravity.google/docs/skills
- Google Antigravity — plugins: https://antigravity.google/docs/plugins

## Packaging: Agent Plugins is the portable target

[Agent Plugins 1.0.0](https://agent-plugins.org) is the open, vendor-neutral packaging standard
(TSC: AWS, Cursor, Microsoft, OpenAI, Vercel; Google as Core Maintainer). One conformant plugin
installs on ChatGPT, Codex, Cursor, GitHub Copilot, Kiro, and VS Code. Prefer it over any
per-host packaging.

```
plugin-name/
├── plugin.json          ← required; $schema + name. Closed schema — unknown fields fail.
├── skills/<name>/SKILL.md
├── mcp.json             ← optional; each server declares an explicit type
└── com.example.client/  ← optional reverse-domain client extensions
```

The standard covers **skills and MCP servers only**. `agents/`, `commands/`, `hooks/`, and
`rules/` are vendor surface: real, but read only by the runtimes that define them. A conformant
plugin says the portable core travels — not that every component does.

Vendor-specific data belongs in `extensions`, keyed by reverse-domain namespace, or in a
matching top-level directory. That is the spec's sanctioned escape hatch; use it instead of a
competing root manifest.

### Antigravity as a namespaced extension

Antigravity marks a plugin with a root `plugin.json` too, and its documented manifest is just
`{"name": "..."}` — `name` is optional (it defaults to the directory name) and no `$schema` is
documented. Since one file cannot hold two `$schema` values, give the field to Agent Plugins and
put Antigravity data under `extensions["com.google.antigravity"]`. Antigravity reads `name` and
then auto-discovers its own components regardless.

What an Antigravity plugin auto-loads from its root: `skills/`, `rules/` (markdown injected as
context when the plugin is active), `hooks.json`, and `mcp_config.json`. Note these are
Antigravity's own schemas at Antigravity's own paths — distinct from Claude's `hooks/hooks.json`
and from the standard's `mcp.json`. Create them only when the plugin actually ships them.

**Antigravity is two products with separate state trees.** The `agy` CLI and the
Antigravity 2.0 desktop app keep independent global roots and independent skill
directories. The docs at `antigravity.google/docs/plugins` sit under the
**Antigravity 2.0** section, so their paths describe the desktop app — not the CLI.
A path documented for one is not automatically read by the other.

| Surface | Global plugin root | Notes |
|---|---|---|
| Antigravity 2.0 desktop | `~/.gemini/config/plugins/` | as documented; app state lives in `~/.gemini/antigravity/` with its own `skills/` |
| `agy` CLI | `~/.gemini/antigravity-cli/plugins/` | where CLI installs actually land; separate `skills/` tree |

Both surfaces read the **workspace** path, so it is the portable answer:
`.agents/plugins/<name>/` (also `_agents/plugins/`). Prefer it over either global
root when a plugin should apply to one project.

Verify rather than trust: `agy plugin validate <path>` reports exactly which
component classes were loaded. Confirmed against `agy` 1.1.13 — `skills/`,
`agents/`, `commands/` (converted to skills), `mcp_config.json`, and `hooks.json`
all load, and `$schema` is ignored entirely, so an Agent Plugins manifest
validates identically to an Antigravity-style one. Note that `agents/` and
`commands/` do **not** appear in the published documentation; treat the doc list
as incomplete rather than authoritative.

## Selection rules

1. Use `portable` for cross-host delivery and add no vendor extensions. For packaging, that means
   an Agent Plugins root manifest, with host specifics confined to namespaced extensions.
2. Use one host profile when the user needs its invocation, path-scoping, UI, dependency, or
   packaging behavior. A multi-host package may include separate host sidecars, but SKILL.md
   stays portable.
3. Treat pre-approved tools as permission grants, not capability restrictions. Minimize them;
   disclose network, filesystem, credential, and side-effect requirements in the contract.
4. Create only directories that contain needed resources. Host scaffolds that create empty
   `scripts/`, `references/`, or `assets/` folders are starting points, not a shipping shape.

Return to SKILL.md and continue from the step that sent you here.
