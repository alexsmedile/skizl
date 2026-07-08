# Light Track

Use this when: the skill is small — reference-only, user-invoked, a personal or style rule,
a small workflow capture, or the user said "just draft it". No tools, no branches, no
complex output validation.

## Flow

1. **Contract.** From the three captured answers (do / trigger / output), write a one-line
   job statement. Done when: you have written one realistic test prompt against it.
2. **Invocation.** User-invoked (`disable-model-invocation: true`) when the human will call
   it by name; model-invoked only when it must fire autonomously (a style rule the agent
   should apply unprompted). State the choice and why in one line. If the user already has
   several user-invoked skills, mention the router-skill cure once — their call.
3. **Draft the smallest SKILL.md** from [../templates/SKILL.md.tmpl](../templates/SKILL.md.tmpl).
   Default: ONE file. A reference file must earn its place (a genuinely long peer-set of
   rules that would bury the top); when it does, give it a `Use this when:` line. Done when:
   the skill runs from SKILL.md alone.
4. **Prune.** Apply the runtime budget to every line; run the no-op test sentence by
   sentence and delete failing sentences whole, not word by word. Done when: every remaining
   line changes behavior, and the draft got shorter.
5. **Gates.** `check.py`, then the reviewer (see SKILL.md § Gates). Fix or explicitly accept
   each verdict.
6. **Final.** Hand the file(s) to the user with the invocation choice stated. Test prompts
   only if the output is checkable — for subjective skills (style, taste), one or two usage
   examples instead. Offer the ship step (skizl) only if the user wants versioning.

## Completion criterion

The result is one SKILL.md — plus a reference file only if it clearly earned its place —
with a reviewer verdict of pass + right-sized.
