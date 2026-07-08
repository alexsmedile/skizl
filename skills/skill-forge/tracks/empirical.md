# Empirical Track

Use this when: the skill's outputs can be judged objectively — file transforms, code
generation, data extraction, fixed output formats, repeatable business workflows — or
triggering accuracy matters enough to measure.

**Entry test:** can you write an assertion a script or grader could check against the
output? If not, this is a subjective skill — route back to light or standard and let the
reviewer carry quality. Benchmarking taste produces numbers, not truth.

## Flow

1. **Draft via the standard track** — all eight steps, gates included. Arrive here with a
   reviewed draft, not an idea.
2. **Eval prompts.** Write 3–5 realistic task prompts — concrete and messy, the way users
   actually type: file names, personal context, typos, abbreviations — plus 1–2 near-misses
   that should NOT trigger the skill. Save to `evals/evals.json` from
   [../templates/evals.json.tmpl](../templates/evals.json.tmpl). Done when: each prompt
   names what good output looks like.
3. **Run the with-skill vs baseline loop.** For each eval prompt, spawn two fresh subagents
   in the same turn: one with the draft skill available, one without (baseline). Draft the
   pass/fail assertion for each prompt while the runs execute. Grade both outputs against the
   assertion, then compare: the skill earns its keep only where with-skill beats baseline.
   Show the user the paired outputs and the win/loss tally. Done when: the user has seen the
   outputs and the tally.
4. **Iterate on feedback.** Generalize from complaints rather than overfitting to the test
   set; read the transcripts, not just the outputs. If every run independently wrote the
   same helper script, bundle it in `scripts/` and point the skill at it. Repeat step 3
   until feedback is clean or progress stalls.
5. **Description optimization (optional).** When triggering accuracy is the concern, split
   the eval prompts (train/test), draft several candidate descriptions, and score each on the
   held-out prompts by whether the skill fires when it should and stays silent on near-misses.
   Keep the description with the best fire/silence balance.
6. **Gates.** `check.py`, then the reviewer on the final iteration — evals prove the skill
   works; the reviewer still owns sizing and prose quality.

## Completion criterion

With-skill beats baseline on the eval set, the user has reviewed the outputs, near-miss
prompts do not trigger the skill, and the reviewer verdict is pass + right-sized.
