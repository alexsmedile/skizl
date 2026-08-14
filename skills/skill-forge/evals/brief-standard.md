# Regression brief — standard track

Runner prompt: [prompts/standard.md](prompts/standard.md).

## Expected shape

- Selects **Create**, then routes to **standard** track (model-invoked, real branches: mitigate
  vs postmortem change workflow AND context)
- Produces a pre-draft architecture map: triage is shared behavior; mitigate and postmortem are
  real branches; topic-only variants collapse
- Chooses the package plan from routing before prose: triage inline (every run needs it), per-path
  detail disclosed behind `Use this when:` pointers
- Description rewritten after body: triggers (alert pasted, "X is down") + near-misses (general reliability questions ≠ incident)
- Every step ends on a checkable criterion
- Reviewer verdict: pass, right-sized

## Failure signals

- "Mitigate" and "postmortem" inlined as one giant file → no disclosure
- Fake third branch by topic (e.g. "database incidents" with identical workflow) survives the branch test
