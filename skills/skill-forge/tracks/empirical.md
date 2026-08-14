# Empirical Track

Use this when: the skill's outputs can be judged objectively — file transforms, code
generation, data extraction, fixed output formats, repeatable business workflows — or
triggering accuracy matters enough to measure.

**Entry test:** can you write an assertion a script or grader could check against the
output? If not, this is a subjective skill — route back to light or standard and let the
reviewer carry quality. Benchmarking taste produces numbers, not truth.

## Flow

1. **Draft via the standard track** — steps 1–8 only. Arrive here with a pruned draft, not an
   idea; defer the reviewer gate until empirical evidence exists.
2. **Eval contract.** Separate two questions: behavior (does the skill improve the result?)
   and discovery (does the description fire correctly?). Write 3–5 realistic behavior prompts
   — concrete and messy, with files/context/typos where natural — and an objective expectation
   for each. Add 1–2 difficult near-misses to a separate trigger set; irrelevant negatives
   prove nothing. Save all cases to `evals/evals.json` from
   [../templates/evals.json.tmpl](../templates/evals.json.tmpl). Done when:
   every expectation is discriminating: a plausible baseline can fail it and a grader can cite
   evidence for pass/fail.
3. **Run paired, uncontaminated trials.** Keep workspaces outside the skill folder. For each
   behavior prompt, launch fresh-context with-skill and baseline runs together: no skill for a
   new package, or an untouched snapshot for a repair. Give each run only the task, inputs,
   output path, and relevant skill; never leak the intended fix. Grade with scripts where
   possible and an independent grader otherwise. Repeat noisy or high-stakes trials enough to
   expose variance; record pass rate plus time/token cost when available. Done when: every pair
   has raw outputs, evidence-backed grades, and no run could inspect another run's artifacts.
4. **Human + analyst review.** Present paired outputs before revising. Ask the user to judge
   qualities that expectations cannot capture. Inspect transcripts for wasted work, expectations
   that both configurations always pass, regressions hidden by an average, and time/token
   tradeoffs. For a consequential close call, blind the labels and use an independent
   comparator. Done when: the user has seen representative outputs and every metric has a
   qualitative explanation.
5. **Iterate without overfitting.** Generalize from failures, rerun the full set into a clean
   iteration, and keep the baseline stable. If independent runs repeatedly create the same
   helper, bundle and test it. Stop when feedback is clean, the skill shows no meaningful gain,
   or further edits trade one covered behavior for another.
6. **Description optimization (when discovery matters).** Build balanced should-trigger and
   difficult should-not-trigger queries. Keep substantive real-user phrasing; split train from
   held-out test; evaluate repeated trials when selection is stochastic. Choose on held-out
   precision/recall balance, not training score. Done when: the final description beats the
   original on held-out cases without expanding into adjacent skills.
7. **Gates.** `check.py`, then the reviewer on the final iteration — evals prove the skill
   works; the reviewer still owns sizing and prose quality.

## Completion criterion

With-skill beats a stable baseline on discriminating expectations, the user has reviewed the
paired outputs, held-out near-misses stay silent, variance/cost are reported when relevant,
and the reviewer verdict is pass + right-sized.
