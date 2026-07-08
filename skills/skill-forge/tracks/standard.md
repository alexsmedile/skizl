# Standard Track

Use this when: the skill is model-invoked with real steps, branches, progressive disclosure,
output templates, or validation — but its outputs are not objectively checkable enough for
the empirical track.

## Flow

1. **Contract.** The three captured answers, plus what this track needs: inputs, tools,
   known failure modes, examples of good output where the conversation offers them. Done
   when: you have written one realistic test prompt against it (reuse it later in gates/evals).
2. **Invocation choice.** Model-invoked (pays context load) vs user-invoked (pays cognitive
   load). Write a *rough* description now — it gets rewritten in step 6. Done when: the mode
   and a one-line why appear in the draft.
3. **Branch map — before any prose.** List the distinct ways the skill will be invoked, then
   apply the glossary's **branch** test to each: a candidate that changes no behavior is a
   section, collapse it. Done when: every branch names the behavior it changes, and you know
   what every branch needs (goes inline) versus what only some reach (goes behind a pointer).
4. **Draft.** Steps in SKILL.md, each ending on a checkable completion criterion — prefer
   exhaustive bounds ("every X accounted for") over list-producing ones. Reference that only
   some branches need gets flagged, not inlined. Hunt for leading words: a triad restated in
   three places collapses into one pretrained token. Done when: the skill runs from SKILL.md
   for its main branch.
5. **Disclose.** For each flagged chunk: does *every* branch need it? No → move it to
   `references/<name>.md` from [../templates/reference.md.tmpl](../templates/reference.md.tmpl),
   opening with its `Use this when:` activation rule. If a must-have target sits behind a
   pointer that might not fire, sharpen the pointer's wording first; inline only if that
   fails. Done when: SKILL.md holds routing, steps, criteria, always-needed rules, and
   pointers — nothing else.
6. **Description rewrite — against the finished body.** Front-load the leading word; one
   trigger per real branch (synonyms restating a branch collapse); add the near-misses that
   should NOT trigger. Done when: the description answers "when should the agent reach for
   this?" without duplicating the body.
7. **Prune.** Runtime budget on every line; no-op test sentence by sentence; delete failing
   sentences whole. Done when: the draft got shorter and every survivor changes behavior.
8. **Gates.** `check.py`, then the reviewer (see SKILL.md § Gates). Fix or explicitly accept
   each verdict.

## Completion criterion

SKILL.md carries steps with checkable criteria and pointers with activation rules; every
disclosed file is reached by some branch; the description names its branches and its
near-misses; reviewer verdict is pass + right-sized.
