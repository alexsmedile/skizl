---
name: skill-draft
description: |
  Quickly draft a small skill in one pass — a single SKILL.md, no tracks, no reviewer, no evals.
  Use for "just write me a skill", a personal/style rule, or a small workflow capture. For a full
  build with progressive disclosure, a review gate, or evals, use skill-forge instead.
version: 1.2.0
category: devtools
status: current
tags: [meta, skills, draft, authoring]
---

# Skill Draft

Fast single-pass drafting engine for compact, predictable AI-agent skills.

## 1. Extract Contract

Capture from request or workflow trace:
1. **Outcome**: What must the skill make the agent do?
2. **Trigger**: When should it fire? (Rich trigger surface for model-invoked; command for user-invoked).
3. **Output**: What must the final output structure look like?

## 2. Weight & Sizing Decision

| Weight | Indicators | Structure |
|---|---|---|
| **Light** | Small, personal, manual-only, style/reference rule, "just draft it" | Single `SKILL.md` (<50 lines) |
| **Standard** | Multi-step workflow, real branches, output templates | Draft `SKILL.md` or route to `skill-forge` |
| **Empirical** | Code, data transformation, testable artifacts | Draft MVP + test prompts, or route to `skill-forge` |
| **Audit** | Improving, debloating, or hardening existing skill | Diagnostic patch or route to `skill-forge` |

## 3. Micro-Kernel Rules

- **Inline vs Disclose**: Keep core triggers, operational steps, finish lines, and critical guardrails in `SKILL.md`. Move heavy references out only when branch-specific.
- **Telegraphic Pruning**: Keep a line only if it changes action, selects a branch, defines completion, or blocks a failure. Cut conversational prose, generic tips, and no-ops.
- **Finish Lines**: Every step must end on a verifiable, checkable completion criterion (done vs not-done).

## 4. Report Format

```text
┌─ DRAFT · <skill-name>
│ file      <path/to/SKILL.md> (<N> lines)
│ trigger   <one-line trigger summary>
│ status    ready for immediate execution
│ next      use directly, or harden via /skizl forge
└─
```