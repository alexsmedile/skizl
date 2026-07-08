# Regression brief — empirical track

## Prompt

"Make a skill that converts our messy CSV exports (inconsistent headers, mixed date formats)
into our canonical JSON schema. It has to be right every time — column mapping mistakes cost
us real money."

## Expected shape

- Routed to **empirical** track (file transform, objectively checkable, correctness matters)
- Passes the entry test: assertions are writable (schema validity, column mapping, date normalization)
- 3–5 realistic eval prompts + 1–2 near-misses saved to evals/evals.json
- With-skill vs baseline loop run per prompt, outputs graded against the assertions
- If every test run writes the same parsing helper → bundled into scripts/
- Reviewer verdict: pass, right-sized

## Failure signals

- Evals skipped because "the skill looks right" → the whole point missed
- With-skill outputs graded without a paired baseline run to compare against
