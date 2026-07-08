---
status: active
updated: 2026-07-08
related:
  - PLAN.md
---

# Tasks — build-skill-forge

## v1

### M1 — Minimal invocable forge
- [ ] Adapt `skills/writing-great-skills/GLOSSARY.md` into `skill-forge/GLOSSARY.md` (keep co-location; cut rule: a term stays only if SKILL.md, a track, or the reviewer uses it; add: gate zero, MVS, track, reviewer, sizing verdict)
- [ ] Write `SKILL.md` router: frontmatter (description with its OWN near-miss boundaries: one-off prompt ≠ skill, general agent advice ≠ skill, docs ≠ runtime skill) + opening thesis (predictability — same process every run, not same output) + first move (extract → infer → ask only architecture-changing blanks; capture do/trigger/output) + gate zero + track chooser + global rules (MVS-first, inline/move-out lists, invocation rule, runtime budget) + completion bar
- [ ] Stub the four track files so every pointer resolves
- [ ] → check: ≤140 lines, frontmatter parses, pointers resolve; gate-zero NO-case exits in one line; 4 sample briefs route to 4 different tracks

### M2 — Light track end-to-end
- [ ] Write `templates/SKILL.md.tmpl` (frontmatter + when-to-use + workflow-with-criteria + output + pointers + done)
- [ ] Write `templates/reference.md.tmpl` ("Use this when: <activation rule>" — pointer wording is first-class)
- [ ] Write `tracks/light.md`: contract → smallest SKILL.md → prune → reviewer → final; test prompts only if useful
- [ ] Run a small subjective brief through it
- [ ] → check: exactly one SKILL.md out, zero test prompts, zero folders (negative test for ceremony)

### M3 — Reviewer gate
- [ ] Write `reviewer.md`: fresh-context prompt — sees draft + GLOSSARY only; 6 sections (invocation, scope, hierarchy, steps, pruning, package shape); returns pass/revise + right-sized/underbuilt/overbuilt + top-5 issues with line citations + exact edits where obvious
- [ ] Decide reviewer dispatch: Agent tool vs `context: fork` sub-skill (test both, pick one)
- [ ] Seed a draft with 3 planted judgment flaws; run the gate
- [ ] Seed an overbuilt package (5 files for a 1-file job); run the gate
- [ ] → check: all 3 flaws cited with line numbers; overbuilt package gets verdict "overbuilt"; light track now runs gated end-to-end

### M4 — Standard + audit tracks
- [ ] Write `tracks/standard.md`: contract → invocation choice → branch map (branch = behavior change: workflow/context/output/tools/validation — else it's a section) → draft → disclose → description rewrite (trigger-rich WITH near-miss should-NOT-trigger boundaries, not just should-trigger cases) → prune → reviewer
- [ ] Write `tracks/audit.md`: classify → diagnose (one diagnostic-ACTION per failure mode) → patch → reviewer → optional eval
- [ ] Run audit track against one of the four source skills
- [ ] → check: audit yields actions not ticks; standard track rejects a fake topic-label branch

### M5 — Mechanical lint + empirical track + self-evals
- [ ] Write `scripts/check.py`: frontmatter validity, name/description presence (unless user-invoked), line count, broken/orphaned links, missing referenced files, linked reference file lacking a "Use this when:" activation-rule line (greppable thanks to the template), evals JSON validity, empty dirs, ALL-CAPS scan — nothing semantic
- [ ] Write `templates/evals.json.tmpl`
- [ ] Write `tracks/empirical.md`: thin wrapper — eval prompts (3–5 realistic + 1–2 near-misses) → skill-creator's baseline loop → optional description optimizer (`run_loop.py`); entry test = outputs objectively checkable
- [ ] Write 4 regression briefs into `evals/` — one per track: small user-invoked style skill (light), model-invoked multi-branch skill (standard), file-workflow skill with checkable outputs (empirical), bloated existing skill to repair (audit) — with expected-shape notes
- [ ] → check: check.py catches seeded fixtures (>500 lines, broken pointer, bad JSON); empirical loop completes on a checkable output; the M2 subjective brief is refused eval scaffolding

### M6 — Dogfood + ship tail
- [ ] Document skizl handoff (snapshot/bump, publish optional) as the closing step of every track
- [ ] Run the forge on itself: check.py + reviewer + completion bar
- [ ] Run the forge on one fresh real brief start-to-finish
- [ ] Fix whatever hurt; fold lessons into the tracks; save dogfood artifact under `evals/`
- [ ] → check: forge passes its own gates with verdict "right-sized"

## v2 (deferred)

- [ ] Decide final home: keep in `skizl/skills/` vs move to `skills_db/skill-forge/` (ship-time call, user decides)
- [ ] Description optimization run on skill-forge's own description (skill-creator's 60/40 loop)
- [ ] High-risk checks reference file — only if the forge gets used for safety-sensitive skills
- [ ] Publish via skizl (plugin manifests) if the forge proves out
