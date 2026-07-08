# Regression brief — light track

## Prompt

"I keep re-explaining my commit message style to Claude every session — imperative mood,
scope prefix, no trailing period, max 60 chars. Make that a skill so I stop repeating myself."

## Expected shape

- Routed to **light** track (style rule, no tools, no branches)
- Output: exactly ONE SKILL.md — zero folders, zero test prompts (subjective output → usage examples instead)
- Invocation choice stated (model-invoked is defensible here: the rule should apply unprompted)
- Reviewer verdict: pass, right-sized

## Failure signals

- A `references/` or `evals/` folder appears → ceremony
- 3 test prompts scaffolded for a taste-based skill → ritual benchmarking
