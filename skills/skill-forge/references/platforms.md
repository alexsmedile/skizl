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
| `gemini` | `.agents/skills/` or `.gemini/skills/`; workspace overrides user | Prefer portable frontmatter; activation asks for consent and grants the skill directory | Test discovery with `/skills`, activation consent, and bundled resource access; package/link with Gemini tooling when requested |
| `skizl` | Plugin skill under `skills/` | Claude-compatible fields plus library `version`, `category`, `status`, and `tags` conventions | Validate with `--profile skizl`; lifecycle uses skizl commands only on explicit request |

Official host references:

- Claude: https://code.claude.com/docs/en/skills
- OpenAI: https://learn.chatgpt.com/docs/build-skills
- Cursor: https://cursor.com/docs/skills
- Gemini CLI: https://geminicli.com/docs/cli/skills/

## Selection rules

1. Use `portable` for cross-host delivery and add no vendor extensions.
2. Use one host profile when the user needs its invocation, path-scoping, UI, dependency, or
   packaging behavior. A multi-host package may include separate host sidecars, but SKILL.md
   stays portable.
3. Treat pre-approved tools as permission grants, not capability restrictions. Minimize them;
   disclose network, filesystem, credential, and side-effect requirements in the contract.
4. Create only directories that contain needed resources. Host scaffolds that create empty
   `scripts/`, `references/`, or `assets/` folders are starting points, not a shipping shape.

Return to SKILL.md and continue from the step that sent you here.
