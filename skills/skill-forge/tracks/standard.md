# Standard Track

Use this when: the skill has real steps, branches, progressive disclosure, output templates,
or validation — regardless of invocation mode — but its outputs are not objectively checkable
enough for the empirical track.

## Flow

1. **Confirm the contract and architecture map.** Carry forward the workshop's job, boundaries,
   clusters, routes, package plan, and target host/profile. Add inputs, tools, known failure
   modes, side effects, dependencies, permissions, and examples of good output where available.
   For Update, name the invariant behavior and regression surface. Write one realistic test
   prompt against the result (reuse it later in gates/evals). Done when: every requested
   capability has one justified route and the prompt exercises the main one.
2. **Invocation choice.** Model-invoked (pays context load) vs manual-only (pays cognitive
   load). Write a *rough* description now — it gets rewritten in step 6 — and encode policy
   using the chosen host profile. Done when: the mode, mechanism, and a one-line why appear in
   the draft.
3. **Validate routing before prose.** Apply the glossary's **branch** test to the workshop map;
   collapse any candidate that changes no behavior. Confirm each route's inputs, context, tools,
   approvals, output, validation, recovery, and resume behavior. Done when: every branch names
   the behavior it changes and what every branch needs versus what only some reach.
4. **Commit the package plan.** Assign always-needed routing and steps to SKILL.md; branch-only
   knowledge to references; deterministic or fragile work to scripts; fixed output shapes to
   templates; and objective behavior checks to evals. Delete any proposed file with no named
   reader and behavior change. Done when: the scaffold follows runtime routing rather than topic
   symmetry.
5. **Draft.** Choose high/medium/low freedom for each fragile decision, then write steps in
   SKILL.md, each ending on a checkable completion criterion — prefer
   exhaustive bounds ("every X accounted for") over list-producing ones. Reference that only
   some branches need gets flagged, not inlined. Hunt for leading words: a triad restated in
   three places collapses into one pretrained token. Done when: the skill runs from SKILL.md
   for its main branch.
6. **Disclose.** For each flagged chunk: does *every* branch need it? No → move it to
   `references/<name>.md` from [../templates/reference.md.tmpl](../templates/reference.md.tmpl),
   opening with its `Use this when:` activation rule. If a must-have target sits behind a
   pointer that might not fire, sharpen the pointer's wording first; inline only if that
   fails. Done when: SKILL.md holds routing, steps, criteria, always-needed rules, and
   pointers — nothing else.
7. **Description rewrite — against the finished body.** Front-load the leading word; one
   trigger per real branch (synonyms restating a branch collapse); add the near-misses that
   should NOT trigger. Done when: the description answers "when should the agent reach for
   this?" without duplicating the body.
8. **Prune.** Runtime budget on every line; no-op test sentence by sentence; delete identified
   no-ops whole. Done when: every identified no-op is removed and every remaining line has a
   behavioral purpose.
9. **Gates.** Run `check.py` with the target profile, test every bundled script at least once
   (representative samples for a family), then run the reviewer (see SKILL.md § Gates). Fix or
   explicitly accept each verdict.

## Completion criterion

SKILL.md carries steps with checkable criteria and pointers with activation rules; every
disclosed file is reached by some branch; the description names its branches and its
near-misses; reviewer verdict is pass + right-sized.
