# Regression brief — standard track

## Prompt

"Turn my incident-response runbook into a skill: triage (is it a real incident?), then either
quick-mitigate or full postmortem path — those need different context. It should trigger when
I paste an alert or say something's down."

## Expected shape

- Routed to **standard** track (model-invoked, real branches: mitigate vs postmortem change workflow AND context)
- Branch map produced before prose; triage inline (every run needs it), per-path detail disclosed behind `Use this when:` pointers
- Description rewritten after body: triggers (alert pasted, "X is down") + near-misses (general reliability questions ≠ incident)
- Every step ends on a checkable criterion
- Reviewer verdict: pass, right-sized

## Failure signals

- "Mitigate" and "postmortem" inlined as one giant file → no disclosure
- Fake third branch by topic (e.g. "database incidents" with identical workflow) survives the branch test
