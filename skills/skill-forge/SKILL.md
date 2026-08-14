---
name: skill-forge
description: |
  Build a skill properly — routed tracks, a fresh-context reviewer gate, progressive
  disclosure, and evals when outputs are checkable. Use to create a non-trivial skill, update
  an existing skill, resume an unfinished skill-forge run or review, audit, debloat, or repair
  a skill, or optimize its activation boundaries. For a quick single-file skill with no
  ceremony, use skill-draft; not for one-off prompts, general agent questions, or human-facing
  docs.
version: 1.4.0
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

A skill earns existence only when the work recurs and either has repeatable decisions needing
steering or requires bundled context/reference. When it doesn't, recommend the cheaper thing
in one line and stop: a one-off prompt, a script, a template, a checklist, or a memory entry.

## Recover the operation

Choose the **operation** before the track; they answer different questions. The operation says
where this run starts, while the track says how much evidence and process the work needs.

| Operation | Use this when | First action |
|---|---|---|
| **Create** | No usable skill exists | Recover a provisional contract from the request or demonstrated workflow |
| **Update** | A completed skill exists and behavior, scope, or support must change | Read the whole package, preserve its current contract, and express the request as a behavioral delta |
| **Resume** | A prior forge run stopped with a draft, decisions, evidence, or review issues | Recover the **forge record**, verify it against current files, and continue from the first incomplete gate |

If a resume has no reliable forge record, reconstruct one from the skill, review output, test
evidence, and conversation; mark uncertainty. Do not restart merely because the prior session
ended. A completed skill receiving a new request is Update, not Resume.

Maintain a compact forge record outside the distributable skill folder so process state cannot
be mistaken for runtime content. Keep: operation, target/profile, contract, architecture
decisions, track, completed gates, feedback deltas, review issue IDs and dispositions, evidence,
and next action. A handoff may carry the same fields inline when no state file is warranted.

## Architecture workshop

Extract what the conversation already gave. Infer safe defaults. Ask only when a missing
answer would change the architecture — draft a provisional contract and mark assumptions
rather than interviewing.

If the user demonstrated the workflow, treat the trace as primary evidence: recover tools,
ordering, corrections, inputs, outputs, and approval boundaries before asking them to restate it.

Start with three things:

1. What should the skill make the agent do?
2. When should it trigger?
3. What should the output look like?

Also identify the target host(s). If the user did not name one, default to a portable Agent
Skills package and keep host extensions out. Read [references/platforms.md](references/platforms.md)
when choosing locations, frontmatter, invocation controls, UI metadata, or distribution.

Before choosing folders or writing prose, build the smallest architecture map that answers:

1. **Boundary.** Name the owned outcome, explicit non-goals, and adjacent skills or ordinary
   agent behavior that should remain separate.
2. **Capability clusters.** Group requested behavior by shared inputs, tools, permissions,
   outputs, validation, and update cadence. Decide whether each cluster is a step, a real
   **branch**, disclosed reference, helper, separate skill, or router destination.
3. **Runtime modes and branches.** A mode earns a route only when it changes workflow, context,
   tools, output, permissions, or validation. Collapse presentation-only variants.
4. **Rules.** Express normal behavior as positive operating rules. Keep prohibitions for hard
   guardrails and trigger near-misses, paired with the safe alternative.
5. **Routing.** For every surviving branch, record its condition, inputs/context, tools and
   approval boundaries, output, validation, failure recovery, and safe resume behavior.
6. **Package plan.** Only now choose `SKILL.md`, references, scripts, templates, or evals. Every
   proposed file must name the branch that reads it and the behavior it changes.

For Update, map the requested delta onto this architecture: affected branches, invariants to
preserve, required migrations, and regression surface. For Resume, reuse accepted decisions and
reopen them only when new evidence or feedback contradicts them.

Classify incoming feedback before acting: architecture-changing feedback returns to the affected
workshop decisions; local implementation corrections join one repair batch; preference-only
refinements are advisory. Record the delta and its disposition so later sessions do not rediscover
or relitigate it. Done when: the contract, routes, and package plan explain every requested
capability, and no proposed mode, cluster, or file exists only for organizational symmetry.

Scale the workshop to the decision surface: for a Light skill it may be one compact paragraph;
do not manufacture tables, modes, or clusters for a single-rule workflow.

## Choose a track

| Track | Use this when |
|---|---|
| [tracks/light.md](tracks/light.md) | Small skill: reference-only, manual-only, personal/style rule, small workflow capture, or "just draft it" |
| [tracks/standard.md](tracks/standard.md) | Skill with real steps, **branches**, progressive disclosure, or output templates, regardless of invocation mode |
| [tracks/empirical.md](tracks/empirical.md) | Outputs are objectively checkable (files, code, data, fixed formats), or triggering accuracy matters enough to measure |
| [tracks/audit.md](tracks/audit.md) | The user brings an existing skill to improve, debloat, or repair — including a fast draft (e.g. from skill-draft) whose idea is validated and ready to harden |

When torn between two tracks, take the lighter one — a track can escalate mid-run; ceremony
can't refund itself.

Create and Update choose a track from the table. Resume returns to the recorded track and next
incomplete gate; route to Audit only when the recovered work itself needs diagnosis or repair.

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
  the skill on its own (pays **context load**); **manual-only** when the human controls timing
  (pays **cognitive load**). State which and why in the draft, then encode it with the target
  host's mechanism. Keep `name` and `description` in every generated SKILL.md.
- **Steps end on checkable completion criteria** — the agent must be able to tell done from
  not-done.
- **Match freedom to fragility.** Use prose where several approaches are valid, parameterized
  scripts where one pattern is preferred, and narrow deterministic scripts where mistakes are
  costly or the sequence is fragile.
- **Least-surprise package.** A skill's described purpose must account for its actions, files,
  network use, and tool permissions. Keep secrets out; pre-approve only the narrowest tools;
  make scripts self-contained, dependency-explicit, and concise on stdout/stderr.
- **Prefer causal steering.** Explain why a non-obvious constraint matters when that helps the
  agent generalize; reserve rigid absolute language for true invariants and safety gates.

## Gates — before the user sees the draft

1. Resolve this forge's directory, then run
   `python3 <skill-forge-dir>/scripts/check.py <skill-dir> --profile <target>` — mechanical
   faults only. Profiles: `portable`, `claude`, `codex`, `cursor`, `gemini`, `skizl`.
2. Dispatch a fresh-context subagent with ONLY the Full-review prompt from
   [reviewer.md](reviewer.md), the draft folder path, and GLOSSARY.md — no intent conversation;
   the draft must stand on its own. It returns pass/revise, a **sizing verdict**, and line-cited
   blocking or advisory issues. Resolve or disposition every blocking issue in one repair batch;
   advisory issues do not prevent shipping.
3. If the first review found blockers, dispatch one issue-scoped verification with the
   ONLY the Verification prompt from reviewer.md, original issue list, repaired draft folder
   path, and GLOSSARY.md. It checks those issue IDs and concrete regressions only — it does not
   perform another general review. Stop when no original blocker remains. Two reviewer calls are
   the default maximum; a third requires a major structural rewrite and an explicit reason
   recorded in the handoff.

On Resume, honor the recorded review state. Open blockers return to batch repair; a completed
repair awaiting verification goes directly to the scoped verifier. Do not replace an existing
closed issue list with another full review. Feedback that causes a major structural rewrite
starts a new full-review cycle, linked to the superseded issue dispositions in the forge record.

When modifying the forge itself, follow [evals/README.md](evals/README.md): run all six prompt
briefs without exposing the hidden oracle, then compare against an untouched forge snapshot.

## Ship

When the user wants the skill versioned or published, invoke the installed `skill-manager`
skill and request its `snapshot`, `bump`, or `publish` action for the skill path. Never execute
`skizl` as a shell command: it is a plugin/meta-skill namespace, not a CLI binary. The forge
builds; the lifecycle skill ships. Installing or symlinking requires an explicit user ask.

## Completion bar

A generated skill is ready only when:

- gate zero was passed deliberately — this deserves to be a skill
- operation and forge record make the starting state, accepted decisions, and next action clear
- architecture maps every capability to a justified route and package element
- target host/profile and invocation mode are intentional and stated
- the description is trigger-rich and names near-misses that should NOT trigger
- the job is narrow and each step has a checkable completion criterion
- branch-only reference sits behind activation-ruled pointers
- repeated meanings and **no-op** lines are gone (reviewer-verified)
- test prompts exist when outputs are checkable — and don't when they aren't
- bundled scripts declare dependencies, fail clearly, and request no broader permissions than
  the workflow needs
- `check.py` passes, the full review is **right-sized**, and no reviewed blocker remains
