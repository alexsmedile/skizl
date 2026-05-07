---
name: skilz
description: |
  Pack multiple standalone skills into a single skill container (references/ + references/ architecture),
  or unpack a container back to standalone skills. Also manages pin/unpin of shortcut skills.
  Use when: consolidating skills into a master skill, migrating standalone skills to the
  container format, restoring skills to standalone, or creating/removing shortcut redirects.
  Triggers: "pack skills", "unpack skill", "create skill container", "pin skill", "unpin skill",
  "/skilz", "how does skilz work", "explain skilz", "onboard skilz".
argument-hint: "pack|unpack|pin|unpin|status|onboard"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

Manages the lifecycle of skill containers: pack, unpack, pin, unpin.

## Commands

| Command | Accepted aliases | What it does |
|---|---|---|
| `pack` | wrap, fold, zip, bundle, forge, merge, knit | Create a container from standalone skills |
| `unpack` | unwrap, unfold, unzip, burst, smelt, split, unravel | Restore container actions as standalone skills |
| `pin` | link, alias, tap | Create a redirect skill that delegates to the container |
| `unpin` | unlink, detach | Remove a redirect skill |
| `status` | info, ls, list | Inspect a container's structure and active pins |
| `onboard` | help, intro, explain, tour, howto | Explain how skilz works and guide first use |

## Routing

1. **No argument** — print the commands table above and ask what to do
2. **First word = command or alias** — normalize to canonical, load `references/<canonical>.md` and follow
3. **Free text** — interpret the intent, choose the most likely action, ask for confirmation before proceeding

**Alias → canonical normalization:**
- wrap / fold / zip / bundle / forge / merge / knit → `pack`
- unwrap / unfold / unzip / burst / smelt / split / unravel → `unpack`
- link / alias / tap → `pin`
- unlink / detach → `unpin`
- info / ls / list → `status`
- help / intro / explain / tour / howto → `onboard`

---

## PACK

Read `references/pack.md` for full instructions.

**Quick usage:** `skilz pack <container-name> <skill1> <skill2> ...`

**Example:** `skilz pack cs brainstorm strategize generate design-pass`

---

## UNPACK

Read `references/unpack.md` for full instructions.

**Quick usage:** `skilz unpack <container-path> [--dest <directory>]`

**Example:** `skilz unpack skills/cs --dest skills/`

---

## PIN

Read `references/pin.md` for full instructions.

**Quick usage:** `skilz pin <container-path> <action>`

Or from inside a container: `/<container-name> pin <action>`

---

## UNPIN

**Usage:** `skilz unpin <container-path> <action>`

```bash
SKILLS_DIR=$(dirname <container-path>)
rm -rf "$SKILLS_DIR/i-<action>"
[ -L ".claude/skills/i-<action>" ] && rm ".claude/skills/i-<action>"
echo "Unpinned: /<action> removed"
```

---

## STATUS

**Usage:** `skilz status <container-path>`

```bash
echo "=== Container: <name> ==="
echo "References:"; ls <container-path>/references/ 2>/dev/null || echo "(none)"
echo "Scripts:"; ls <container-path>/scripts/ 2>/dev/null || echo "(none)"
echo "Active pins:"
SKILLS_DIR=$(dirname <container-path>)
ls "$SKILLS_DIR" | grep "^i-" || echo "(none)"
```

---

## ONBOARD

Read `references/onboard.md` for full instructions.

---

## References

- [pack](references/pack.md)
- [unpack](references/unpack.md)
- [pin](references/pin.md)
- [onboard](references/onboard.md)
- [Folder conventions](references/folders.md)

---

## Common errors

| Symptom | Fix |
|---|---|
| Source skill not found | Specify the absolute path or verify it is in `.claude/skills/` or `skills/` |
| Master SKILL.md > 500 lines | Move verbose sections to `references/` and link them |
| Pin not triggering | Verify the redirect skill is in `.claude/skills/` as a symlink |
| Knowledge not loaded | Add an explicit reference in the action file (`See [file](../references/file.md)`) |
