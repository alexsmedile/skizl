# Densification Patterns & 5-Layer Transformation Guide

Use this when: refactoring an existing skill into a high-density, token-efficient architecture.

## 1. The 5-Layer Architecture Model

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Telegraphic Micro-Kernel (Prose Compression & Matrices)   │  <= 55-65 lines in SKILL.md
├─────────────────────────────────────────────────────────────┤
│ 2. Mechanical Script Offloading (Discovery -> Scripts)      │  Single-turn CLI tools in scripts/
├─────────────────────────────────────────────────────────────┤
│ 3. Silent Fast-Lane Execution & Box Reports                 │  Skip chatter; emit compact result box
├─────────────────────────────────────────────────────────────┤
│ 4. Strictly Pinned Routing Enums                            │  Fixed route set; no invented routes
├─────────────────────────────────────────────────────────────┤
│ 5. Progressive Disclosure Boundaries                        │  Deep logic loaded only on demand
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Transformation Patterns

### Pattern A: Conversational Advice → Decision Matrix

**Before (Verbose Prose, ~80 tokens):**
> When working with git branches, you should always check if the branch is dirty first. If there are uncommitted changes, ask the user what to do. If the branch is clean and it's a feature branch, you can proceed directly to commit. If there are conflicts, stop immediately and begin conflict resolution.

**After (Dense Matrix, ~25 tokens):**
| Situation / State | Route | Action |
|---|---|---|
| Clean feature branch | `execute` | Fast-lane commit & push |
| Dirty uncommitted tree | `plan-work` | Halt -> prompt user for stash or commit |
| Unresolved conflicts | `recover` | Load `references/recover.md` -> resolve |

---

### Pattern B: Minor Forks → Inline Pipeline Notation

When a full 4-column markdown table is overkill for a simple 1-line dispatch:

**Before (Bulleted Explanations):**
> If the user provided a raw file path, use the file reading tool. If they provided a URL, use the web fetch tool. If they provided no arguments, check the previous conversation turn.

**After (Inline Pipeline):**
`path → read · URL → fetch · "this"/∅ → previous turn · many files → prompt which`

*Rule: Use pipeline notation (`a → b · c → d`) ONLY when the operations are self-contained and non-branching. If operations have prerequisites or error handling, use a decision table.*

---

### Pattern C: Multi-Turn Probing → Mechanical Script Offload

**Before (LLM Shell Probing, 5 turns, ~1,200 tokens):**
- Turn 1: `ls -la .claude/skills`
- Turn 2: `ls -la .agents/skills`
- Turn 3: `cat plugin.json`
- Turn 4: `git status`
- Turn 5: LLM summarizes findings in 3 paragraphs.

**After (Deterministic Script Call, 1 turn, ~35 tokens):**
`bash scripts/skizl-ops.sh sym-status`
Emits a structured 4-line matrix directly into agent context.

---

### Pattern D: Conversational Status → Left-Border Box

**Before (Markdown Chatter):**
> Great! I have created the snapshot of your skill at versions/SKILL@1.5.0.md. You can now make further modifications or bump the version when ready. Let me know if you need anything else!

**After (Standardized Fast-Lane Box):**
```text
┌─ SKIZL · snapshot · skill-forge
│ target    skills/skill-forge/SKILL.md
│ snapshot  versions/SKILL@1.5.0.md (74 lines)
│ status    clean checkpoint saved
│ next      ready for edits or bump
└─
```

---

### Pattern E: Monolithic File → Progressive Disclosure

1. Identify sections that only fire under specific conditions (e.g. disaster recovery, onboarding, deep publishing).
2. Move them into `references/<topic>.md`.
3. Ensure every reference file opens with: `Use this when: <clear trigger condition>`.
4. Leave only a 1-line pointer in the `SKILL.md` routing table.

---

### Pattern F: Preservation Guard ("Keep What Carries the Decision")

High density must **never** introduce operational ambiguity or skip process steps:

| Keep Verbatim (Carries the Decision) | Cut Aggressively (Prose Fluff) |
|---|---|
| Exact CLI flags, tool names, parameters | Preamble ("Here is what we will do next...") |
| Exit codes, status enums, route constants | Meta wrappers ("As an AI assistant...") |
| Checkable done/not-done finish lines | Advisory hedging ("Feel free to", "You can") |
| Error handling, halts, and recovery steps | Generic explanations ("Writing tests is good") |
| Explicit user approval boundaries | Duplicate alias maps and restated rules |
