# pin

Use this when: creating or removing redirect shortcut skills.

Create a lightweight redirect skill that delegates to the container.

**Usage:** `/skizl pin <container-path> <action> [--skills-dir <dir>]`
**From inside the container:** `/<container-name> pin <action>`

## Step 1 — Run the pin script

```bash
node <container-path>/scripts/pin.mjs <action> [--skills-dir <dir>]
```

If `scripts/pin.mjs` does not exist, create the redirect manually (Step 2).

## Step 2 — Manual creation (fallback)

```bash
DEST=${skills_dir:-$(dirname <container-path>)}
mkdir -p "$DEST/i-<action>"
```

Before writing frontmatter, build a concise description:
- Start with `Shortcut for /<container-name> <action>.`
- Append the command description copied from the master menu.
- Add that it delegates to the parent container only if there is room.
- Keep the final `description:` under 900 characters where possible, and never over Codex's 1024-character limit.

Write `$DEST/i-<action>/SKILL.md`:

```markdown
---
name: i-<action>
description: <checked shortcut description under 1024 chars>
triggers:
  - /<action>
allowed-tools:
  - <same as container>
---

Redirect to `/<container-name> <action>`.

Invoke `/<container-name> <action>` with the same arguments and target.
Load `<container-path>/references/<action>.md` and follow its instructions.
```

## Step 3 — Symlink into .claude/skills/ if present

```bash
[ -d .claude/skills ] && ln -sf "../../skills/i-<action>" ".claude/skills/i-<action>"
```

## Step 4 — Confirm

```
Pin created: /<action> → /<container-name> <action>
File: <dest>/i-<action>/SKILL.md

To remove: /skizl unpin <container-path> <action>
```
