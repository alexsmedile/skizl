# Regression briefs

Use these when: the forge itself changes and its routing, sizing, or package behavior needs a
fresh-context regression check.

1. Snapshot the untouched forge as the baseline. Build sanitized runtime copies of baseline
   and candidate that exclude the entire `evals/` directory; a verbal instruction not to read
   hidden labels or oracles is not isolation.
2. Give each fresh runner only one file from `prompts/`, its listed fixture inputs, and the
   matching sanitized forge. Do not expose the intended track or prior conclusions.
3. Run the same prompt and fixtures against the untouched snapshot. Keep workspaces isolated.
4. Give an independent grader the two raw results and the matching hidden `brief-*.md` oracle.
5. Report pass/fail per expectation and any behavioral regression; do not reward mere wording
   similarity to the oracle.

| Runner prompt | Fixture inputs | Hidden grading oracle |
|---|---|---|
| [prompts/light.md](prompts/light.md) | none | [brief-light.md](brief-light.md) |
| [prompts/standard.md](prompts/standard.md) | [fixtures/incident-runbook.md](fixtures/incident-runbook.md) | [brief-standard.md](brief-standard.md) |
| [prompts/empirical.md](prompts/empirical.md) | [fixtures/messy-export.csv](fixtures/messy-export.csv), [fixtures/canonical-schema.json](fixtures/canonical-schema.json) | [brief-empirical.md](brief-empirical.md) |
| [prompts/audit-repair.md](prompts/audit-repair.md) | [fixtures/audit-repair/SKILL.md](fixtures/audit-repair/SKILL.md) | [brief-audit.md](brief-audit.md) |
| [prompts/audit-harden.md](prompts/audit-harden.md) | [fixtures/audit-harden/SKILL.md](fixtures/audit-harden/SKILL.md) | [brief-audit-harden.md](brief-audit-harden.md) |

Run [trigger-cases.json](trigger-cases.json) separately. For every case, pass only the query to
isolated candidate and snapshot selectors whose forge copies exclude `evals/`; never expose the
label. Repeat trials when selection is stochastic and record activation evidence. Done when:
every case has candidate/baseline evidence and comparative precision and recall are reported.
Trigger cases measure only activation; they do not execute track workflows.
