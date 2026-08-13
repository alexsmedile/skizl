# Regression brief — empirical track

Runner prompt: [prompts/empirical.md](prompts/empirical.md).

## Expected shape

- Routed to **empirical** track (file transform, objectively checkable, correctness matters)
- Passes the entry test: expectations are writable (schema validity, column mapping, date normalization)
- 3–5 realistic eval prompts + 1–2 near-misses saved to evals/evals.json
- With-skill vs baseline loop run per prompt, outputs graded against the expectations
- If every test run writes the same parsing helper → bundled into scripts/
- Reviewer verdict: pass, right-sized

## Failure signals

- Evals skipped because "the skill looks right" → the whole point missed
- With-skill outputs graded without a paired baseline run to compare against
