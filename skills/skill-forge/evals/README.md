# Regression briefs

At least one brief per track (audit has two — repair and harden). When the forge itself is
modified, run each through the forge and confirm it still routes to the named track and earns
the expected sizing verdict — a dogfood test that the forge obeys its own doctrine.

- [brief-light.md](brief-light.md) — small style rule → light track, one SKILL.md, no ceremony
- [brief-standard.md](brief-standard.md) — branching runbook → standard track, real branches + disclosure
- [brief-empirical.md](brief-empirical.md) — CSV→JSON transform → empirical track, evals over baseline
- [brief-audit.md](brief-audit.md) — bloated 700-line skill → audit track (repair mode), repair not rewrite
- [brief-audit-harden.md](brief-audit-harden.md) — validated skill-draft output → audit track (harden mode), build up don't rebuild
