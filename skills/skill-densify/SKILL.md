---
name: skill-densify
description: |
  Compress verbose agent skills into high-density 5-layer micro-kernels. Replaces conversational
  prose with decision matrices, offloads multi-turn discovery to deterministic scripts, pins route
  enums, and extracts progressive disclosure boundaries.
version: 1.0.0
category: devtools
status: current
tags: [meta, skills, optimization, compression, micro-kernel]
---

# Skill Densify

Transform verbose, conversational skills into high-density, token-efficient micro-kernels (saving 60–80% context).

## 1. Quick Guard & Off-Switch

Run density analysis before taking any action:
```bash
python3 "${CLAUDE_SKILL_DIR:-<skill-dir>}/scripts/densify.py" <path/to/SKILL.md>
```

**Off-Switch (Check before transforming)**:
- If band is `COMPACT` or `NORMAL`, `filler == 0`, and forks are already tabular → emit `ALREADY_DENSE` box, do NOT restructure, halt.
- Size alone is never a defect. A `LARGE`/`REVIEW` skill reported as *structured and disclosed* is healthy — halt too.
- If skill is already telegraphic and unambiguous → preserve as-is; never compress for compression's sake.

## 2. Operation Matrix

| Operation | Condition / Trigger | Action & Reference |
|---|---|---|
| `audit` | Inspect volume, token budget, prose filler, tables | Run `densify.py` -> report findings box |
| `kernel` | Compress a prose-heavy `SKILL.md` into a router | Read [references/patterns.md](references/patterns.md) -> build decision matrix |
| `offload` | Replace multi-turn LLM exploration with scripts | Read [references/patterns.md](references/patterns.md) -> scaffold `scripts/` helper |
| `prune` | Strip no-ops, conversational preambles, weak negation | Read [references/rules.md](references/rules.md) -> apply runtime budget filter |
| `disclose` | Extract situational logic into on-demand references | Move branch logic to `references/*.md` with `Use this when:` |

## 3. 5-Layer Micro-Kernel Protocol

1. **Micro-Kernel**: Size the front door to its branches — see bands below. Express workflows as decision tables or pipelines (`a → b · c → d`). Never cut behavior to hit a number.

| Band | Body lines | Read as |
|---|---|---|
| `THIN` | ≤ 60 + ≥3 refs | Over-disclosed — inline what every run needs |
| `COMPACT` | ≤ 60 | Single-purpose kernel |
| `NORMAL` | ≤ 150 | Typical routed skill with references |
| `LARGE` | ≤ 300 | Check for branch-only detail to disclose |
| `REVIEW` | > 300 | Likely several skills, or inlined reference material |

A working 150-line skill beats a 60-line one whose steps live behind links the agent has to chase mid-task. `[BROKEN]` flags reference links pointing at missing files — a disclosed skill that cannot reach its own references is worse than an undisclosed one.

Bands measure the **body** — frontmatter is the trigger surface and is never compressed. Above 150 lines the verdict weighs structure over size: densely tabular *and* disclosed is healthy at any size; mostly prose is the real defect at any size.
2. **Mechanical Offload**: Wrap repetitive CLI/file discovery in deterministic scripts in `scripts/`.
3. **Silent Fast-Lane**: For routine deterministic actions, execute silently and return standard left-border box.
4. **Pinned Routes**: Restrict routing to an explicit, closed enum (never invent speculative routes).
5. **Progressive Disclosure**: Disclose branch-only context via pointers with explicit activation triggers.

## 4. Report Format

```text
┌─ DENSIFY · <operation> · <skill-name>
│ original  <N> lines (~<T1> tokens)
│ kernel    <M> lines (~<T2> tokens) · <Savings>% reduction (or ALREADY_DENSE)
│ changes   <matrices added; scripts offloaded; references split; or NONE>
│ next      run check.py or test prompts
└─
```
