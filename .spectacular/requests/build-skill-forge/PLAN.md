---
status: active
priority: high
owner: alex
updated: 2026-07-08
build: b1
summary: "Build skill-forge: the definitive skill-that-writes-skills — lean router + weight tracks + fresh-eye reviewer, reusing skill-creator's eval loop, writing-great-skills' glossary, and skizl shipping"
related:
  - PRD.md
---

# Plan — build-skill-forge

## 1. Goal

Ship `skills/skill-forge/` — a router + tracks + reviewer whose root virtue is **predictability** (the produced skill makes the agent take the same *process* every run, not the same output): classify the skill by weight, draft the smallest viable package, force a fresh-eye reviewer to fail it before the user sees it, and run evals only when the skill earns them.

## 2. Constraints

- **Reuse, don't absorb** — the empirical track is a thin wrapper over skill-creator's scripts (eval loop, baseline comparison, description optimizer, viewer); shipping is a pointer to skizl. The forge owns only: router, 4 tracks, reviewer prompt, minimal templates, `check.py`.
- **Self-consistency is a hard requirement** — router SKILL.md ≤ ~140 lines; ONE co-located GLOSSARY.md; depth behind pointers; MVS-first (no folder created until a track or verdict demands it); forge prose steers by positive targets (prohibitions only as hard guardrails, always paired with the positive behavior).
- **Honest gates only** — judgment checks (no-op, negation, duplication, sizing) go to the fresh-context reviewer; `check.py` gets only mechanical checks. Never pretend a script can lint a no-op.
- **Test only when testable** — evals for objectively checkable outputs (files, code, data, fixed formats); reviewer-only for subjective skills (style, taste, advisory). No ritual benchmarking.
- **Language before scripts** — every track must work as plain markdown first; `check.py` and the empirical wrapper land only after the tracks read right.
- **Deliberately not built** — plugin framework, package-manifest system, mandatory phases, L0–L7 naming, default high-risk branch, no-op linter, custom eval viewer, second glossary, universal skill template.
- **Build only, no deploy** — no install/symlink without explicit ask (global skill policy).

## Understanding

### How it works now

Four skills each cover one slice and none enforces the others' discipline: `skills/skill-creator/` (479-line eval loop: with-skill vs baseline subagents, grading, viewer, description optimizer), `skills/writing-great-skills/` (83-line reference + 202-line GLOSSARY defining the vocabulary and 6 failure modes), `skills/progressive-skill-builder/` (L0–L7 scaffold checklist, unenforced), `skills/skizl/` (post-authoring lifecycle: pack/pin/sym/snapshot/bump/publish). A generator can skip pruning and testing; self-audit is self-certification; and every existing generator forces the same process weight on every skill regardless of size.

### What changes

One new folder `skills/skill-forge/` is added. Nothing else: the four source skills are read-only inputs (glossary text adapted from writing-great-skills; eval scripts and skizl invoked by pointer).

### What stays the same

The four existing skills — no edits, no moves, no wrappers around them. The skizl container/`references/` convention. The repo's install policy (forge is built, not deployed).

## Decisions

- Chose **weight tracks (light / standard / empirical / audit)** over state-routed workflows (create/audit/triggering/ship) — because evals are expensive and must be an explicit opt-in route, not a tail every skill passes through; a reference skill must not pay for branch-mapping and benchmarks. *Reverses the earlier call that "MVS-first subsumes tracks" — wrong for the empirical case* (final merge, 2026-07-07).
- Chose **fresh-context reviewer subagent** over self-audit checklists — the glossary licenses only a real context boundary as a defense against premature completion; self-certified gates are not gates. Reviewer verdict includes a one-word sizing call: **right-sized / underbuilt / overbuilt**.
- Chose **test-only-when-testable** over evals-for-everything — evals when outputs can be judged objectively; reviewer when quality is subjective. skill-creator itself warns against forcing assertions onto subjective skills.
- Chose **language-before-scripts build order** over gates-early — a bad skill with scripts is still bad; tracks must work as plain files before `check.py` and the empirical wrapper exist.
- Chose **one GLOSSARY.md** over per-topic reference files — fragmenting one domain model violates co-location; tracks point at it, never restate it.
- Chose **description written twice** (rough before body, rewritten after) in every creating track; the heavy 60/40 optimizer loop lives only in empirical.
- Chose **gate zero at router level** over scope-check-in-reviewer only — refusing a skill that shouldn't exist is cheapest before drafting; the reviewer re-checks it as backstop.
- Chose home `skizl/skills/skill-forge/` over `skills_db/skill-forge/` — sources live here, `skizl sym` covers linking; revisit at ship time.

## 3. Milestones

- M1 — **Minimal invocable forge**: `SKILL.md` router (gate zero, tiny contract capture, track chooser, global rules, completion bar) + `GLOSSARY.md`. Routes correctly with tracks stubbed.
- M2 — **Light track end-to-end**: `tracks/light.md` + `templates/SKILL.md.tmpl` + `templates/reference.md.tmpl`. A small brief goes in; one SKILL.md comes out (a reference file only if it earns its place), no unrequested folders.
- M3 — **Reviewer gate**: `reviewer.md` — fresh-context, draft + GLOSSARY only, 6-section review, verdict pass/revise + right-sized/underbuilt/overbuilt + top-5 issues with line citations. Light track now runs gated: the full MVS path works.
- M4 — **Standard + audit tracks**: `tracks/standard.md` (invocation choice → branch map [branch = behavior change only] → draft → disclose → prune) + `tracks/audit.md` (diagnostic-action per failure mode, patch, reviewer).
- M5 — **Mechanical lint + empirical track + self-evals**: `scripts/check.py` (deterministic only) + `tracks/empirical.md` (thin wrapper: eval prompts → skill-creator's baseline loop → optional description optimizer) + `templates/evals.json.tmpl` + `evals/` with 4 regression briefs (one per track, incl. a bloated-skill audit brief).
- M6 — **Dogfood + ship tail**: run the forge on itself and on one fresh brief; fix what hurts; skizl handoff (snapshot/bump) documented as the closing step of every track.

## 4. Tasks

See `TASKS.md`.

## 5. Dependencies

- `skills/skill-creator/` — eval loop (`scripts.aggregate_benchmark`, `run_loop.py`), eval-viewer, grader/analyzer prompts. Read-only reuse via the empirical track.
- `skills/writing-great-skills/GLOSSARY.md` — source text for the forge's glossary. Read-only.
- `skills/skizl/` — ship handoff target (snapshot / bump / publish). Read-only reference.
- No blocking decisions.

## 6. Validation

- M1 — assertable: `wc -l SKILL.md` ≤ 140; frontmatter parses; every track pointer resolves (stubs OK). Judgable: a "shouldn't be a skill" brief exits at gate zero with the cheaper-thing recommendation in one line; four sample briefs route to four different tracks.
- M2 — observable: a small subjective brief (e.g. a personal style rule) yields exactly one SKILL.md, zero test prompts, zero folders — the negative test for ritual ceremony.
- M3 — run: a draft seeded with 3 planted judgment flaws (no-op line, ALL-CAPS negation, duplicated rule) → reviewer cites all three with line numbers and returns a sizing verdict; a deliberately overbuilt package (5 files for a 1-file job) → verdict "overbuilt".
- M4 — judgable: audit track run against one of the four source skills yields diagnostic-actions ("if X then do Y"), not checklist ticks; standard track rejects a fake branch (topic label with no behavior change).
- M5 — run: `check.py` catches a >500-line body, a broken pointer, and invalid evals JSON on seeded fixtures; empirical track on M2-style output completes skill-creator's loop; the subjective brief from M2 is *refused* eval scaffolding (test-only-when-testable holds).
- M6 — run + judgable: forge run on itself passes `check.py`, reviewer verdict "right-sized", and every clause of its own completion bar; fresh-brief run completes with skizl handoff commands printed (not executed).

## 7. Deliverables

- `skills/skill-forge/` — `SKILL.md`, `GLOSSARY.md`, `tracks/{light,standard,empirical,audit}.md`, `reviewer.md`, `templates/{SKILL.md.tmpl,reference.md.tmpl,evals.json.tmpl}`, `scripts/check.py`, `evals/` (4 regression briefs, one per track).
- One dogfood artifact under `evals/` proving the forge passed its own gates.
