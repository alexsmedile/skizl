# unpack

Restore a container's actions as standalone skills.

**Usage:** `/skizl unpack <container-path> [--dest <directory>]`
**Example:** `/skizl unpack skills/cs --dest skills/`

**Core rule: the source container is never modified or deleted.
`unpack` is a copy operation — it reads the actions and creates new standalone skills in `--dest`.
The original container remains intact.**

Skills are created in `--dest <directory>` if specified, otherwise in the CWD.
If a skill with the same name already exists in `--dest`, ask for confirmation before overwriting.

## Step 0 — Preliminary inspection and user questions

Before creating any files, read the container and report situations that require a decision.

### Actions with complex structure

If a reference file contains very long sections or multiple distinct "sub-skills" (e.g. a `study` reference with separate ingest/extract/classify phases), ask:

> "`<name>` contains multiple distinct phases (e.g. `<list>`). Do you want to:
> 1. Create a single standalone skill `<name>` with all the content (faithful to the original)
> 2. Create a separate skill for each phase (`<name>-ingest`, `<name>-extract`, etc.)
> 3. Create `<name>` as a mini-container with its own references"

### References that reference other references

If a reference file references another file in the same container (e.g. "then run `generate`"), report:

> "`<name>` references `<other>`. In standalone form these references will become `/other` — do you want me to update them in the text or leave them as-is?"

### Destination with existing skills

If `--dest` already contains a directory with the same name as an action:

> "`<dest>/<name>/` already exists. Overwrite, skip, or rename the new one as `<name>-unpacked`?"

Ask for a single answer that applies to all conflicts, or case by case if there are only a few.

### Refactoring question (optional but offered)

After inspection, before proceeding:

> "Do you want me to expand shared knowledge files inline in each skill (more self-contained, more verbose), or leave them as external references and copy the `references/` folder to the dest (lighter, but dependent)?"

Default if the user does not answer: expand inline.

---

## Step 1 — Read the container

```bash
ls <container-path>/references/
cat <container-path>/SKILL.md
```

Identify the name and description for each command from the menu in the master SKILL.md.

## Step 2 — For each reference, create the standalone skill

For each `references/<name>.md`:

1. Create `<dest>/<name>/SKILL.md`
2. Reconstruct the frontmatter: `name` and `description` from the master menu, `triggers: [/<name>]`, `allowed-tools` from the container
3. Copy the operational body intact — do not rewrite, do not summarize
4. Expand shared knowledge inline: if the file contains `See [references/platforms.md]`, replace that line with the full content of the corresponding file

```markdown
---
name: <name>
description: <description from master menu>
triggers:
  - /<name>
allowed-tools:
  - Bash
  - Read
  - Write
---

<body from the action file, with knowledge expanded inline>
```

## Edge cases

| Situation | Behavior |
|---|---|
| Container without `references/` | Not a valid container — report and stop |
| Reference file with multiple distinct phases | Ask in Step 0 — do not split automatically |
| Reference file that references another reference | Ask in Step 0 whether to update the references |
| Skill already exists in `--dest` | Ask for confirmation before overwriting |
| Referenced shared knowledge file is missing | Report in the output, leave the broken reference visible in the output file |
| `references/` is empty | Warn — nothing to unpack |
| Command name collides with Claude Code built-ins (`plan`, `status`) | Report as a warning — the skill will be created but may not trigger correctly |

## Step 3 — Report

```
Unpack complete: <N> standalone skills created in <dest>

  ✓ <dest>/explore/SKILL.md
  ✓ <dest>/outline/SKILL.md
  ✓ <dest>/generate/SKILL.md

Knowledge expanded inline where referenced.
Original container: untouched (<container-path> intact)
```
