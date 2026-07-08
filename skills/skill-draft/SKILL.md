---
name: skill-draft
description: Quickly draft a small skill in one pass — a single SKILL.md, no tracks, no reviewer, no evals. Use for "just write me a skill", a personal/style rule, or a small workflow capture. For a full build with progressive disclosure, a review gate, or evals, use skill-forge instead.
---

# Skill Draft

Build predictable AI-agent skills. A skill is not a knowledge base. It is a compact decision system that helps the agent choose the right process.

## First move

Extract what the user already gave. Infer safe defaults. Ask only when a missing detail would change the skill architecture.

Capture:

1. What should the skill make the agent do?
2. When should it trigger?
3. What should the output look like?

## Choose the weight

Use the light path when the skill is small, personal, user-invoked, stylistic, or reference-only.

Use the standard path when the skill is model-invoked, has steps, branches, templates, validation checks, or progressive disclosure.

Use the empirical path when the skill produces files, code, structured data, repeatable transformations, or outputs that can be tested.

Use the audit path when the user gives an existing skill to improve.

## Decide if this should be a skill

Create a skill only when the behavior is reusable, has a clear trigger, and benefits from agent steering.

Do not make a skill when a short prompt, checklist, script, template, or one-off answer is enough.

## Choose invocation

Use model-invoked when the agent should discover the skill on its own.

Use user-invoked when the human will call the skill by name.

For model-invoked skills, make the description trigger-rich. It is not a summary. It is the runtime trigger.

## Draft small first (MVP)

Write the smallest skill that could work.

Keep in `SKILL.md`:
- trigger logic
- core steps
- completion criteria
- always-needed rules
- context pointers

Move out only when needed:
- branch-only reference
- long examples
- templates
- validation details
- eval sets
- scripts

If a supporting file does not clearly change behavior, do not create it.

## Branch only on behavior

A branch is real only if it changes at least one of:

- workflow
- needed context
- tool choice
- output format
- validation check
- risk handling

Topic labels are not branches.

## Write steps with finish lines

Each real step needs a checkable completion criterion.

Weak:
“Improve the skill.”

Strong:
“The skill is ready when the trigger is clear, each step has a checkable done condition, repeated meanings are removed, and tests exist when useful.”

## Prune hard

Every line must earn runtime space.

Keep a line only if it:
- changes behavior
- chooses a branch
- defines success
- points to needed context
- prevents a known failure

Delete:
- generic advice
- repeated meanings
- stale notes
- vague encouragement
- instructions the model would follow anyway

Phrase the target behavior directly. Avoid steering mainly by saying what not to do.

## Test when useful

For light or subjective skills, give 2–3 realistic prompts for human review.

For empirical skills, create tests with:
- happy path
- messy real-world path
- edge case
- near miss
- expected output

Use objective checks only when the output can be judged objectively.

## Review before final

Run a fresh-eye review pass. Judge the skill as an AI-agent runtime artifact, not as human documentation.

Check:

1. Is the skill really needed?
2. Is the invocation mode intentional?
3. Is the description clear enough to trigger?
4. Is the job narrow?
5. Are branches based on behavior?
6. Does each step have a checkable completion criterion?
7. Is must-have context inline?
8. Is branch-only context moved out?
9. Are there repeated meanings?
10. Are there likely no-op lines?
11. Is the skill overbuilt?
12. Are tests present when useful?

If the review finds a serious issue, revise before showing the final skill.

## Output

Return the smallest useful result:

- concept only, if the user is still shaping the idea
- `SKILL.md`, if one file is enough
- package tree plus files, if supporting files earn their place
- audit report plus patched skill, if improving an existing skill

## Done

The skill is done when:

- the trigger is clear
- the job is narrow
- the invocation mode is intentional
- each step has a finish line
- every branch changes behavior
- every file earns its place
- repeated meanings are removed
- likely no-op advice is removed
- tests exist when testing is useful