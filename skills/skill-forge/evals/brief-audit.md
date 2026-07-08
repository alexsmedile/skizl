# Regression brief — audit track

## Prompt

"My deploy skill has grown to 700 lines, half of it is old Heroku instructions we don't use,
the same rollback rule appears in three places, and Claude never seems to trigger it anymore.
Fix it."

## Expected shape

- Routed to **audit** track (existing skill: sprawl + sediment + duplication + undertrigger)
- Whole skill read before any edit; findings recorded with file:line
- Diagnostic actions applied: Heroku layers deleted (sediment), rollback rule kept in ONE
  most-local place (duplication), branch-only reference disclosed (sprawl), description
  rebuilt with leading word + near-misses (undertrigger)
- Snapshot offered before large-scale changes (`skizl snapshot` / `skizl archive`)
- Patch is smallest-diff repair, not a rewrite from scratch
- Reviewer verdict on patched skill: pass, sizing no worse than original

## Failure signals

- Full rewrite when repair was asked for
- Checklist ticks ("checked for duplication ✓") with no file:line findings
