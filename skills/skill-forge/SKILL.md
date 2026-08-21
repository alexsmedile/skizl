---
name: skill-forge
description: |
  Build a skill properly — routed tracks, a fresh-context reviewer gate, progressive
  disclosure, and evals when outputs are checkable. Use to create a non-trivial skill, update
  an existing skill, resume an unfinished skill-forge run or review, audit, debloat, or repair
  a skill, or optimize its activation boundaries. For a quick single-file skill with no
  ceremony, use skill-draft; not for one-off prompts, general agent questions, or human-facing
  docs.
version: 1.5.0
category: devtools
status: current
tags: [meta, skills, authoring]
---

# Skill Forge

Architectural engine for predictable agent skills. A skill is a compact decision system, not a knowledge base.
Forge establishes clear structure, informational hierarchy, logic, and content distribution.

Read [GLOSSARY.md](GLOSSARY.md) before execution: every bold term is applied as defined there.

## 1. Gate Zero: Skill Necessity Test

A skill earns existence ONLY if work recurs and needs repeatable decision steering or bundled context. Otherwise, recommend the cheaper alternative (prompt, script, template, checklist) and halt.

## 2. Operation & Track Selection

### Operation Matrix
| Operation | Condition | First Action |
|---|---|---|
| `Create` | No usable skill exists | Extract contract (Do / Trigger / Output) & target host profile |
| `Update` | Completed skill exists; delta requested | Read package, preserve invariants, map delta to branches |
| `Resume` | Unfinished forge run or open issues | Recover forge record outside skill dir; resume first open gate |

### Track Matrix
| Track | Trigger Condition | Reference |
|---|---|---|
| `light` | Small skill, style rule, manual-only, "just draft it" | Read [tracks/light.md](tracks/light.md) |
| `standard` | Steps, branches, progressive disclosure, templates | Read [tracks/standard.md](tracks/standard.md) |
| `empirical` | Objectively checkable outputs, testable accuracy | Read [tracks/empirical.md](tracks/empirical.md) |
| `audit` | Existing skill to debloat, repair, extend, or harden | Read [tracks/audit.md](tracks/audit.md) |

*Rule: When torn between two tracks, take the lighter one; escalate only if complexity demands it.*

## 3. Architecture & Information Hierarchy

- **Boundary Mapping**: Name the owned outcome, explicit non-goals, and boundary invariants.
- **Capability Clusters**: Group behavior by inputs, tools, and outputs. Map clusters to real runtime branches, helpers, or references.
- **Content Distribution (Inline vs Disclosed)**: Keep always-needed triggers, operational steps, finish lines, and critical guardrails in `SKILL.md`. Disclose branch-only material to `references/*.md` with explicit `Use this when:` activation rules.
- **Verifiable Finish Lines**: Every step must end on a checkable completion criterion (done vs not-done decidable).
- **Match Freedom to Fragility**: Use prose where several approaches are valid, scripts where determinism/safety is critical.

## 4. Quality Gates & Shipping

1. **Lint**: Run `python3 <skill-forge-dir>/scripts/check.py <skill-dir> --profile <target>`.
2. **Review Gate**: Spawn fresh-context subagent with ONLY the Full-review prompt from [reviewer.md](reviewer.md), GLOSSARY.md, and draft skill path. Resolve blocking issues in one repair batch.
3. **Verification**: If blockers occurred, spawn verifier subagent with Verification prompt from [reviewer.md](reviewer.md) to check issue dispositions.
4. **Ship**: When ready to version or publish, hand off to installed `skill-manager` (`/skizl snapshot` or `/skizl publish`).

## 5. Report Format

```text
┌─ FORGE · <operation> · <track> · <skill-name>
│ verdict   pass · right-sized
│ gates     check.py [clean] · reviewer [0 blockers]
│ package   <N> files (<M> lines total)
│ next      run test prompts or ship via /skizl
└─
```
