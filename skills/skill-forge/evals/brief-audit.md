# Regression brief — audit track

Runner prompt: [prompts/audit-repair.md](prompts/audit-repair.md).

## Expected shape

- Routed to **audit** track, repair mode (existing skill: sediment + duplication + undertrigger)
- Whole skill read before any edit; findings recorded with file:line
- Diagnostic actions applied: Heroku layers deleted (sediment), rollback rule kept in ONE
  most-local place (duplication), description rebuilt with leading word + near-misses
  (undertrigger), and no reference file added because the surviving workflow has no real branch
- Snapshot offered before large-scale changes by invoking `skill-manager`; no shell command
  named `skizl` is proposed
- Patch is smallest-diff repair, not a rewrite from scratch
- Reviewer verdict on patched skill: pass, sizing no worse than original

## Failure signals

- Full rewrite when repair was asked for
- Checklist ticks ("checked for duplication ✓") with no file:line findings
