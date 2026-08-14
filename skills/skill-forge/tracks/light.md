# Light Track

Use this when: the skill is small — reference-only, manual-only, a personal or style rule,
a small workflow capture, or the user said "just draft it". No tools, no branches, no
complex output validation.

## Flow

1. **Contract.** From the three captured answers (do / trigger / output), write a one-line
   job statement, boundary, and single capability; record that no runtime branch or extra file
   is justified, then select a target profile. Do not expand the architecture workshop into a
   separate artifact for this track. Done when: you have written one realistic
   working prompt against it and can name the host validator profile; this prompt need not ship
   for a subjective skill.
2. **Invocation.** Manual-only when the human should control timing; model-invoked only when
   it must fire autonomously (a style rule the agent should apply unprompted). Keep `name` and
   `description`, then encode the choice using the selected host profile. State the choice and
   why in one line. If the user already has several manual-only skills, mention the
   router-skill cure once — their call.
3. **Draft the smallest SKILL.md** from [../templates/SKILL.md.tmpl](../templates/SKILL.md.tmpl).
   Default: ONE file. A reference file must earn its place (a genuinely long peer-set of
   rules that would bury the top); when it does, give it a `Use this when:` line. Done when:
   the skill runs from SKILL.md alone.
4. **Prune.** Apply the runtime budget to every line; run the no-op test sentence by
   sentence and delete identified no-ops whole, not word by word. Done when: every identified
   no-op is removed and every remaining line has a behavioral purpose.
5. **Gates.** `check.py`, then the reviewer (see SKILL.md § Gates). Fix or explicitly accept
   each verdict.
6. **Final.** Hand the file(s) to the user with the invocation choice stated. Test prompts
   only if the output is checkable — for subjective skills (style, taste), one or two usage
   examples instead. Offer the ship step (skizl) only if the user wants versioning.

## Completion criterion

The result is one SKILL.md — plus a reference file only if it clearly earned its place —
with a reviewer verdict of pass + right-sized.
