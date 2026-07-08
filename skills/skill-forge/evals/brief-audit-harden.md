# Regression brief — audit track (harden mode)

## Prompt

"I sketched this skill fast with skill-draft and tried it on a few real prompts — a teammate
said the trigger fires too eagerly and the one long step should really be two. Here's the
file. Can you harden it into something we'd actually ship?"

## Expected shape

- Routed to **audit** track, **harden** mode (validated fast draft brought to build up — not a
  from-scratch build, not a bloated skill to trim)
- Whole draft read first; the human feedback is treated as the primary work list
- Thinness is NOT flagged as a defect: single-file / no-disclosure is the starting point, not
  a finding — structure is added only where feedback or a branch demands it
- The two named issues are acted on: over-eager trigger → description tightened with near-miss
  should-NOT-trigger cases; the long step → split into two steps each with a checkable
  completion criterion
- Reviewer gate run on the hardened result; verdict pass + right-sized
- Result is the draft built up, not replaced

## Failure signals

- Discards the draft and rebuilds from a blank page ("blank-page" instead of "build-up")
- Flags "no progressive disclosure" / "only one file" as defects and adds ceremony the
  feedback never asked for
- Ignores the human feedback in favor of a generic audit pass
