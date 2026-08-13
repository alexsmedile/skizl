# Standard Track

Use this when: the skill has real steps, branches, progressive disclosure, output templates,
or validation — regardless of invocation mode — but its outputs are not objectively checkable
enough for the empirical track.

## Flow

1. **Contract.** The three captured answers, target host/profile, plus what this track needs:
   inputs, tools, known failure modes, examples of good output where the conversation offers
   them. Inventory side effects, network access, dependencies, and needed permissions. Done
   when: you have written one realistic test prompt against it (reuse it later in gates/evals)
   and every requested capability is explained by the skill's stated job.
2. **Invocation choice.** Model-invoked (pays context load) vs manual-only (pays cognitive
   load). Write a *rough* description now — it gets rewritten in step 6 — and encode policy
   using the chosen host profile. Done when: the mode, mechanism, and a one-line why appear in
   the draft.
3. **Branch map — before any prose.** List the distinct ways the skill will be invoked, then
   apply the glossary's **branch** test to each: a candidate that changes no behavior is a
   section, collapse it. Done when: every branch names the behavior it changes, and you know
   what every branch needs (goes inline) versus what only some reach (goes behind a pointer).
4. **Draft.** Choose high/medium/low freedom for each fragile decision, then write steps in
   SKILL.md, each ending on a checkable completion criterion — prefer
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
7. **Prune.** Runtime budget on every line; no-op test sentence by sentence; delete identified
   no-ops whole. Done when: every identified no-op is removed and every remaining line has a
   behavioral purpose.
8. **Gates.** Run `check.py` with the target profile, test every bundled script at least once
   (representative samples for a family), then run the reviewer (see SKILL.md § Gates). Fix or
   explicitly accept each verdict.

## Completion criterion

SKILL.md carries steps with checkable criteria and pointers with activation rules; every
disclosed file is reached by some branch; the description names its branches and its
near-misses; reviewer verdict is pass + right-sized.
