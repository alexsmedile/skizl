# Glossary — Skill Forge

The domain model for what makes a skill great. Single source of truth: tracks and the
reviewer point here, never restate. Cut rule applied: a term lives here only if SKILL.md, a
track, or the reviewer uses it.

## Root virtue

**Predictability** — the degree to which a skill makes the agent behave the same *way* every
run: the same process, not the same output (a brainstorming skill should predictably
diverge). Every other term is a lever on it.

## Invocation — how a skill is reached

**Model-invoked** — the skill keeps its **description**, so the agent can discover and fire
it autonomously (the human can still type its name, and other skills can reach it). Pays a
permanent **context load**. Pick only when the agent must reach the skill on its own.

**User-invoked** — the description is stripped (`disable-model-invocation: true`); only the
human typing its name can fire it, and no other skill can. Zero context load; the human is
the index.

**Description** — the machine-readable trigger surface, not a summary. It answers "when
should the agent reach for this?" — one trigger per real **branch**, plus near-misses that
should NOT trigger. Its presence *is* the invocation axis.

**Context load** — the cost a model-invoked skill imposes on the context window: its
description, loaded every turn, spending tokens and attention.

**Cognitive load** — the cost a user-invoked skill imposes on the human: remembering it
exists and when to reach for it. Not a cost to minimize to zero — it is the price of human
agency; spend it where human judgment matters.

**Router skill** — one user-invoked skill that names your other user-invoked skills and when
to reach for each. The cure when user-invoked skills multiply past what the human can recall.

## Structure — how content is arranged

**Steps** — the ordered actions the agent performs; the primary tier of a skill that has
them. Every step ends on a **completion criterion**.

**Reference** — material consulted on demand: definitions, rules, examples, conditional
instructions. Secondary to steps when both exist; the entire content when a skill has no
steps (a fine arrangement, not a smell).

**Branch** — a distinct way a skill can be invoked, so different runs take different paths.
A branch is real only if it changes behavior: workflow, needed context, output format,
tools, or validation. Otherwise it is a section label.

**Progressive disclosure** — moving reference out of SKILL.md behind a **context pointer**
so the top stays legible. Licensed by branching: inline what every branch needs, disclose
what only some branches reach. It protects hierarchy — it does NOT create a context
boundary; only a fresh subagent or user hand-off does.

**Context pointer** — an in-context reference naming out-of-context material and the
condition for reaching it. The pointer's *wording* decides when and how reliably the agent
loads the target — sharpen wording before pulling material back inline.

**Co-location** — keeping a concept's definition, rules, and caveats under one heading
rather than scattered, so reading one part brings its neighbours.

**Information hierarchy** — a skill's content ranked by how immediately the agent needs it:
in-file steps → in-file reference → disclosed reference behind a pointer.

## Steering — shaping runtime behavior

**Completion criterion** — the condition that tells the agent a unit of work is done. Its
*clarity* (can the agent tell done from not-done?) resists **premature completion**; its
*demand* ("every X accounted for", not "produce a list") sets **legwork**. The strongest are
checkable and exhaustive.

**Legwork** — the digging an agent does within a step: reading files, exploring, gathering
what it needs rather than offloading to the user. Raised by a demanding completion criterion
or a strong **leading word**.

**Leading word** — a compact concept already in the model's pretraining (*lesson*, *tracer
bullets*, *relentless*) that anchors a region of behavior in one token by recruiting priors.
In the body it anchors execution; in the description it anchors invocation. Collapse
restatements into one.

**Premature completion** *(failure mode)* — ending a step before it is genuinely done,
attention slipping to *being done*. Defend in order: sharpen the completion criterion first
(cheap, local); hide later steps behind a real context boundary only if the criterion is
irreducibly fuzzy and you observe the rush.

**Negation** *(failure mode)* — steering by prohibition drags the forbidden behavior into
context and makes it *more* available. Cure: state the positive target so the banned thing
is never spoken; keep a prohibition only as a hard guardrail, paired with what to do instead.

## Pruning — keeping a skill lean

**Single source of truth** — each meaning lives in exactly one authoritative place, so a
behavior change is a one-place edit.

**Duplication** *(failure mode)* — the same meaning in more than one place. Costs
maintenance and tokens, and inflates the meaning's prominence past its real rank.

**Relevance** — whether a line still bears on what the skill does. Lost by never bearing on
the task, or by going stale as the world changes.

**Sediment** *(failure mode)* — stale layers that settle because adding feels safe and
removing feels risky. The default fate of a skill without pruning discipline.

**Sprawl** *(failure mode)* — a skill simply too long, even when every line is live and
unique. Cure: disclose reference, split by branch, so each path carries only what it needs.

**No-op** *(failure mode)* — a line the model already obeys by default; you pay load to say
nothing. The test: does it change behavior versus the default? Model-relative — settled by
running the skill, never by grep. A weak leading word (*be thorough*) is a no-op; the fix is
a stronger word (*relentless*), not a different technique.

## Forge terms

**Gate zero** — the refusal step: deciding whether the request deserves to be a skill at
all, before drafting. The cheapest gate is the one that fires first.

**Smallest viable skill (MVS)** — the least package that could work — usually one SKILL.md.
Depth is added only where a track step, reviewer verdict, or failing test demands it.

**Track** — a weight-classed path through the forge (light / standard / empirical / audit),
so a small skill never pays for ceremony a heavy one needs.

**Reviewer** — the fresh-context subagent that judges a draft against this glossary without
seeing the intent conversation. The only honest gate for judgment calls (no-op, duplication,
negation); mechanical faults belong to `check.py`.

**Sizing verdict** — the reviewer's one-word calibration: **right-sized**, **underbuilt**
(missing steps, criteria, or disclosure the job needs), or **overbuilt** (files or process
weight the job never asked for).
