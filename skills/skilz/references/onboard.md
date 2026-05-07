# onboard

Walk the user through how skilz works and guide them to their first action.

## What to explain

### The problem skilz solves

As your Claude Code skill library grows, flat folders become unmanageable. You end up with dozens of
standalone skills that have no shared structure, duplicated context, and no way to group related ones.

### The container pattern

skilz introduces the **container**: a single master skill that routes to on-demand action files.

**Instead of:**
```
skills/
├── brainstorm/SKILL.md
├── generate/SKILL.md
└── design/SKILL.md
```

**You get:**
```
skills/<master-skill>/
├── SKILL.md          ← routing + command menu (auto-loaded, <500 lines)
├── actions/          ← per-command logic, loaded only when invoked
│   ├── brainstorm.md
│   ├── generate.md
│   └── design.md
├── knowledge/        ← shared facts loaded by actions that need them
│   └── platforms.md
└── scripts/
    └── pin.mjs
```

Only `SKILL.md` is loaded automatically. Actions and knowledge are pulled on demand — context stays lean.

### The four operations

| Command | What it does |
|---|---|
| `pack` | Combine standalone skills into a container |
| `unpack` | Restore container actions as standalone skills |
| `pin` | Create an `i-<action>` shortcut that delegates to one container action |
| `unpin` | Remove a shortcut |

All operations are **non-destructive** — pack and unpack are copy operations. Nothing is ever deleted or modified.

### Routing in any container

Every container built by skilz follows the same routing:
1. **No argument** — show menu
2. **Known command** — load and run that action
3. **Free text** — infer intent, suggest the most likely action, ask for confirmation

### Pins

A pin is a lightweight redirect skill named `i-<action>`. It lets you invoke a single container
action directly with `/<action>` instead of `/<container> <action>`.

```
/i-brainstorm  →  /cs brainstorm
```

Pins are symlinked into `.claude/skills/` automatically if that directory exists.

---

## After the explanation

Ask the user which of these applies to them:

> "What would you like to do?
> 1. **Pack** — I have standalone skills I want to consolidate into a container
> 2. **Unpack** — I have a container I want to break back into standalone skills
> 3. **Pin** — I want a direct shortcut to one action in an existing container
> 4. **Status** — I want to inspect an existing container"

Load the corresponding action file and proceed.
