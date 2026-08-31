---
name: skill-densify
description: >-
  Compress verbose agent skills into high-density 5-layer micro-kernels. Replaces conversational
  prose with decision matrices, direct negative constraints ("DO NOT"), consolidated CLI palettes,
  and deterministic scripts. Triggers on "densify", "compress skill", "make skill compact",
  "skill micro-kernel", or "token optimize skill".
version: 1.1.0
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
| `kernel` | Compress a prose-heavy `SKILL.md` into a router | Read [references/patterns.md](references/patterns.md) -> build decision matrix & CLI palette |
| `offload` | Replace multi-turn LLM exploration with scripts | Read [references/patterns.md](references/patterns.md) -> scaffold `scripts/` helper |
| `prune` | Strip no-ops, conversational preambles, weak negation | Read [references/rules.md](references/rules.md) -> enforce direct DO NOT constraints |
| `disclose` | Extract situational logic into on-demand references | Move branch logic to `references/*.md` with `Use this when:` |

## 3. High-Density Micro-Kernel Heuristics

1. **Micro-Kernel Sizing**: Size the front door to its branches. Express workflows as decision tables or pipelines (`a → b · c → d`).
2. **Direct Negative Constraints ("DO NOT")**: State strict negative boundaries directly (e.g. *"Do not edit files during review"*). LLMs follow direct prohibitions with 75% fewer tokens and higher fidelity than polite suggestions.
3. **Consolidated CLI Palette**: Consolidate tool API surfaces into a single parameter-annotated code block (`cmd [--flag] <arg>`).
4. **Frontmatter Trigger Matching**: Embed literal trigger phrases (`"start mission"`, `"review"`, `"audit"`) directly in `description:` for immediate turn-0 routing.
5. **Auto-Default Identifiers**: Design CLI/scripts to auto-derive standard identities (`--by`, `--operator`, `--from`) from workspace config, eliminating flag boilerplate.
6. **Mechanical Offload**: Wrap repetitive multi-turn file/CLI discovery in deterministic scripts in `scripts/`.
7. **Silent Fast-Lane & Peeking**: Routine deterministic tasks execute silently with standard left-border reports. Provide non-mutating preview flags (`--peek`, `--dry-run`).
8. **Progressive Disclosure**: Disclose branch-only context via pointers with explicit `Use this when:` triggers.

| Band | Body lines | Read as |
|---|---|---|
| `THIN` | ≤ 60 + ≥3 refs | Over-disclosed — inline what every run needs |
| `COMPACT` | ≤ 60 | Single-purpose kernel |
| `NORMAL` | ≤ 150 | Typical routed skill with references |
| `LARGE` | ≤ 300 | Check for branch-only detail to disclose |
| `REVIEW` | > 300 | Likely several skills, or inlined reference material |

A working 150-line skill beats a 60-line one whose steps live behind links the agent has to chase mid-task. Bands measure the **body** — frontmatter is the trigger surface and is never compressed. Densely tabular *and* disclosed is healthy at any size; prose filler is the real defect.

## 4. Report Format

```text
┌─ DENSIFY · <operation> · <skill-name>
│ original  <N> lines (~<T1> tokens)
│ kernel    <M> lines (~<T2> tokens) · <Savings>% reduction (or ALREADY_DENSE)
│ changes   <matrices added; scripts offloaded; references split; or NONE>
│ next      run check.py or test prompts
└─
```
