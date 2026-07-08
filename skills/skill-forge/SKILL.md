---
name: skill-forge
description: |
  Build a skill properly — routed tracks, a fresh-context reviewer gate, progressive
  disclosure, and evals when outputs are checkable. Use to design a non-trivial skill, or to
  audit, debloat, or repair an existing one. For a quick single-file skill with no ceremony,
  use skill-draft; not for one-off prompts, general agent questions, or human-facing docs.
version: 1.0.0
category: devtools
status: draft
tags: [meta, skills, authoring]
---

# Skill Forge

Build predictable agent skills. A skill is a compact decision system, not a knowledge base:
it exists to make the agent take the same *process* every run, not the same output.

Read [GLOSSARY.md](GLOSSARY.md) before executing any track: every **bold term** below is
applied exactly as defined there, and the operations the tracks depend on — the no-op test,
the branch test, the sizing verdict — live only there. It is the single source of truth;
nothing else restates it.

This skill is model-invoked because the agent must reach it whenever skill-authoring work
appears, unprompted — the description below is its trigger surface.

## Gate zero — should this be a skill?

A skill earns existence only when the workflow recurs, has repeatable decisions, and needs
steering or bundled context. When it doesn't, recommend the cheaper thing in one line and
stop: a one-off prompt, a script, a template, a checklist, or a memory entry.

## First move

Extract what the conversation already gave. Infer safe defaults. Ask only when a missing
answer would change the architecture — draft a provisional contract and mark assumptions
rather than interviewing.

Capture three things:

1. What should the skill make the agent do?
2. When should it trigger?
3. What should the output look like?

## Choose a track

| Track | Use this when |
|---|---|
| [tracks/light.md](tracks/light.md) | Small skill: reference-only, user-invoked, personal/style rule, small workflow capture, or "just draft it" |
| [tracks/standard.md](tracks/standard.md) | Model-invoked skill with real steps, **branches**, progressive disclosure, or output templates |
| [tracks/empirical.md](tracks/empirical.md) | Outputs are objectively checkable (files, code, data, fixed formats), or triggering accuracy matters enough to measure |
| [tracks/audit.md](tracks/audit.md) | The user brings an existing skill to improve, debloat, or repair — including a fast draft (e.g. from skill-draft) whose idea is validated and ready to harden |

When torn between two tracks, take the lighter one — a track can escalate mid-run; ceremony
can't refund itself.

**Draft-first is a supported on-ramp.** A common flow: someone sketches a skill fast with
skill-draft, validates the idea with a human, then brings it here to harden. Route that to the
audit track — it's an existing skill to build up, not a blank page.

## Global rules

- **Smallest viable skill first.** Draft the least that could work. Add a file only when a
  track step, a reviewer verdict, or a failing test demands it.
- **Runtime budget.** A line stays in a generated SKILL.md only if it changes the next
  action, chooses a **branch**, defines a **completion criterion**, points at deeper
  context, or blocks a known failure. Everything else moves down or dies.
- **Inline what every run needs; disclose what only some branches need.** Every disclosed
  file opens with a `Use this when:` activation rule
  ([templates/reference.md.tmpl](templates/reference.md.tmpl)).
- **Invocation is a choice, not a default.** **Model-invoked** when the agent must discover
  the skill on its own (pays **context load**); **user-invoked** when the human calls it by
  name (pays **cognitive load**). State which and why in the draft.
- **Steps end on checkable completion criteria** — the agent must be able to tell done from
  not-done.

## Gates — before the user sees the draft

1. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/check.py <skill-dir>` — mechanical faults only.
2. Dispatch [reviewer.md](reviewer.md) as a fresh-context subagent with ONLY the draft
   folder and GLOSSARY.md — no intent conversation; the draft must stand on its own. It
   returns pass/revise, a **sizing verdict**, and line-cited issues. Fix or explicitly
   accept each one.

When modifying the forge itself, re-run the four track briefs indexed in
[evals/README.md](evals/README.md) and confirm each still routes and sizes as described.

## Ship

When the user wants the skill versioned or published, hand off to skizl —
`skizl snapshot <path>` · `skizl bump <path>` · `skizl publish <path>`. The forge builds;
skizl ships. Installing or symlinking a skill requires an explicit user ask.

## Completion bar

A generated skill is ready only when:

- gate zero was passed deliberately — this deserves to be a skill
- invocation mode is intentional and stated
- the description is trigger-rich and names near-misses that should NOT trigger
- the job is narrow and each step has a checkable completion criterion
- branch-only reference sits behind activation-ruled pointers
- repeated meanings and **no-op** lines are gone (reviewer-verified)
- test prompts exist when outputs are checkable — and don't when they aren't
- `check.py` passes and the reviewer says **pass** + **right-sized**
