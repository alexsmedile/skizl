# Regression brief — resume operation

Runner prompt: [prompts/resume.md](prompts/resume.md).

## Expected shape

- Selects **Resume** operation and returns to the recorded audit/harden track
- Verifies the forge record against the supplied files without asking the user to repeat accepted
  contract or architecture decisions
- Continues at `scoped-verification`; it does not run another full audit or full review
- Supplies the verifier only the repaired skill, glossary, and original issue IDs `INV-01` and
  `STP-01`
- Updates the forge record with dispositions, evidence, and the next action

## Failure signals

- Restarts at Gate zero, architecture brainstorming, or audit diagnosis despite reliable state
- Launches a new fresh-eye full review and allows the reviewer to invent a new advisory list
- Treats the completed skill receiving a future new requirement as Resume rather than Update
