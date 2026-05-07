# pack

Create a container from a set of standalone skills.

**Usage:** `skilz pack <container-name> <skill1> <skill2> ...`
**Example:** `skilz pack cs brainstorm strategize generate design-pass`

**Core rule: source skills are never modified, moved, or deleted.
`pack` is a copy operation — it reads the originals and builds something new in `--dest`.**

The container is created in `--dest <directory>` if specified, otherwise in the CWD under `<container-name>/`.
The original skills remain untouched in their location.

## Step 0 — Preliminary inspection and user questions

Before doing anything, read all source skills and report situations that require a decision.

### Skills that are already containers

If a source skill already has a `references/` subdirectory with command files, it is already a container — not a standalone.

Ask the user how to proceed:

> "`<name>` looks like a container already (has a `references/` folder with command files). How do you want to proceed?
> 1. Include its master SKILL.md as a single reference in the new container (treat it as opaque)
> 2. Unpack its references and include them individually in the new container (merge)
> 3. Exclude `<name>` from the pack"

Do not proceed until the user has answered for each ambiguous skill.

### Skills with unusual structure

If a skill has subdirectories other than `references/`, `scripts/`, `examples/`, `assets/`, `schemas/`, `templates/` (e.g. `docs/`, custom folders) — report it:

> "`<name>` has non-standard subdirectories: `<list>`. Do you want to include them in the container or ignore them?"

### Name conflicts

If two source skills have the same `name` in their frontmatter — ask which name to use for the action in the container.

### Refactoring question (optional but offered)

After inspection, before proceeding, offer:

> "Do you want me to suggest how to organize the actions by category in the master menu, or should I proceed in the order you listed the skills?"

If the user wants suggestions: propose a grouping by category (e.g. Creation / Review / Publishing) based on the skill content. The user approves or modifies before Step 5 generates the master.

---

## Step 1 — Read the source skills

For each specified skill, find the SKILL.md:

```bash
for name in <skill-list>; do
  find . ~/.claude/skills -maxdepth 3 -name "SKILL.md" -path "*/$name/*" 2>/dev/null | head -1
done
```

Read each SKILL.md. Extract:
- `name` and `description` from the frontmatter
- The full body (the operational instructions)

## Step 2 — Create the container structure

```bash
BASE=<destination>   # e.g. skills/<container-name> or specified path
mkdir -p "$BASE/references" "$BASE/scripts"
```

## Step 3 — Write the references

For each source skill, write a copy in `references/<name>.md` in the new container:
- Remove the YAML frontmatter (name, description, triggers, allowed-tools) — that info lives in the master
- Copy the full operational body intact, word for word — do not rewrite, do not summarize
- Add `# <name>` at the top if not present

The source skills are not touched.

## Step 4 — Extract shared knowledge

Identify blocks that are identical or nearly identical across more than one of the **newly created reference files** (not in the sources).

For each shared block found:
1. Create `references/<topic>.md` with that content
2. In the files that contain it, replace the block with: `See [references/<topic>.md](references/<topic>.md)`

Do not modify the original source skills.

Typical shared knowledge topics:
- Platform limits / social accounts → `references/platforms.md`
- Copy density rules → `references/density.md`
- Pipeline sequence → `references/pipeline.md`
- Brand tokens / palette → `references/brand.md`
- Builder template types → `references/templates.md`

## Step 5 — Write the master SKILL.md

Generate a lean master with:
1. Frontmatter: `name`, aggregated `description`, `allowed-tools` (union of all skills)
2. Command menu grouped by category
3. Alias → canonical table with all aliases
4. Routing in 3 rules
5. Explicit `Read references/<name>.md` pointers for each command

Master template:

```markdown
---
name: <container-name>
description: |
  <aggregated description>
allowed-tools:
  - <union of allowed-tools>
---

<one-line role sentence>

## Commands

| Command | Category | Description |
|---|---|---|
| `<name>` | <category> | <description> |

## Routing

1. **No argument** — print the commands table and ask what to do
2. **First word = command or alias** — normalize to canonical, load `references/<canonical>.md` and follow
3. **Free text** — interpret the intent, choose the most likely action, ask for confirmation before proceeding

## References

- [<command>](references/<command>.md)
- [<shared-topic>](references/<shared-topic>.md)
```

## Step 6 — Copy pin.mjs

```bash
cp <skilz-skill-dir>/scripts/pin.mjs "$BASE/scripts/pin.mjs"
```

`<skilz-skill-dir>` is the directory of this skill (`skilz`).

## Edge cases

| Situation | Behavior |
|---|---|
| Source skill not found | Report the missing name, ask whether to continue with the remaining ones or stop |
| Skill already a container (`references/` with command files present) | Ask in Step 0 — do not proceed automatically |
| Non-standard subdirectory in source | Ask in Step 0 whether to include it |
| `references/<name>.md` already exists in dest | Ask for confirmation before overwriting |
| Container dest already exists | Warn the user, ask whether to overwrite, append, or cancel |
| No shared blocks found in Step 4 | Skip shared knowledge files, still create the container |
| Skills with very different `allowed-tools` | Include the union but flag it in the report |
| Skills with duplicate `name` across sources | Ask in Step 0 which name to use for the reference file |

## Step 7 — Report

```
Pack complete: <container-name>
Container created in: <dest-path>
Source skills: untouched

References created (N):
  ✓ explore.md     ← brainstorm  (from: skills/brainstorm/)
  ✓ outline.md     ← strategize  (from: skills/strategize/)
  ✓ generate.md    ← generate    (from: skills/generate/)

Shared knowledge extracted (N):
  ✓ pipeline.md    (found in 3 reference files)
  ✓ platforms.md   (found in 2 reference files)

Master SKILL.md: <path>
Pin script: <path>/scripts/pin.mjs

To create a shortcut: /<container-name> pin <action>
To verify: skilz status <dest-path>
```
