# Audit Track

Use this when: the user brings an existing skill to improve, debloat, or repair. Improving
is diagnosis, not creation — resist redrafting from scratch.

## Flow

1. **Classify.** Read the whole skill first — SKILL.md and every disclosed file. Note:
   target/host assumptions, invocation mode, line count, branch structure, which track would
   have produced it. Carry forward the global operation and decide the audit mode: **repair**
   (a real, aged, or bloated skill — trim and fix), **extend** (a completed skill receiving a
   new behavioral delta), or **harden** (a fast
   draft whose idea is validated, brought to be built up — e.g. a skill-draft output plus the
   human feedback it earned). In harden mode, thinness is the starting point, not a defect:
   don't flag "no disclosure" or "single file" as faults — add structure only where a branch,
   a failing test, or the feedback demands it. In extend mode, map the delta to affected
   branches, invariants, package elements, and regression checks before editing. On Resume,
   preserve the recovered audit mode, findings, and completed gates unless current files
   contradict them. Done when: you can state the skill's job, weight class, operation, and mode
   in two lines.
2. **Diagnose.** Walk the table below against the skill. Each row is an action, not a
   checkbox — a finding means you do the thing on the right. Record findings with file:line.
   Done when: every row has been applied and every finding has an action attached.

| Symptom | Diagnostic action |
|---|---|
| Fires when it shouldn't (overtrigger) | Add near-miss "not for:" boundaries to the description |
| Doesn't fire when it should (undertrigger) | Front-load the leading word; one trigger per real branch; if accuracy must be proven, escalate to the empirical track's optimizer |
| Invocation mode by accident | Only ever fired by hand → keep the description and add the target host's manual-only control; must fire autonomously → write a real trigger surface and remove manual-only control |
| Frontmatter mixes host dialects | Select a target profile; keep portable fields plus only that host's extensions; move portable version data under `metadata` |
| Too long; agent wades before acting (sprawl) | Move branch-only reference behind activation-ruled pointers; split real branches |
| Same meaning in two places (duplication) | Keep the most local copy, delete the other |
| Stale layers nobody dared remove (sediment) | Check every line for relevance; delete what no longer bears on the task |
| Line the model does anyway (no-op) | Delete the sentence whole — or, if it's a weak leading word, replace it with a stronger one |
| "Don't do X" steering (negation) | Rewrite as the positive target; keep a prohibition only as a hard guardrail paired with the positive |
| Vague step bounds (premature completion risk) | Rewrite each completion criterion as an observable done/not-done condition |
| Must-have material behind a weak pointer | Sharpen the pointer's wording first; inline only if that fails |
| Files no pointer reaches, or folders for show | Delete them — every file must answer: who reads this, when, and what behavior changes |
| Script surprises, broad permissions, or hidden dependencies | Align actions with stated purpose; narrow permissions; declare dependencies; add clear success/failure output and edge handling |

3. **Patch.** Smallest diffs that resolve the findings or implement the mapped delta — this is
   evolution, not a blank-page rewrite. Before
   large-scale changes, invoke the installed `skill-manager` skill and request `snapshot` (or
   `archive` for a full-folder tarball). Never run `skizl` in the shell. Done when: every
   recorded finding and feedback delta is resolved or explicitly accepted with a reason.
4. **Gates.** `check.py --profile <target>`, execute changed scripts on representative inputs,
   then the reviewer on the patched skill (see SKILL.md § Gates).
   The reviewer sees only the result — if the patch doesn't stand on its own, it isn't done.
5. **Optional eval.** If outputs are checkable and the user wants proof the patch helped,
   run empirical track steps 2–4 with old-vs-new as the baseline pair (snapshot the original
   first).

## Completion criterion

Every diagnostic row applied; every finding resolved or accepted with a reason; the patched
skill passes check.py and gets reviewer pass — with a sizing verdict no worse than the
original.
