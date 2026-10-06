---
schema: make-a-change/todo/v1
extensions:
  - "octopus:all"
---

# TODO

- convert /skizl to command that routes / dispatches

---

skill status taxonomy:

stable        — battle-tested, │
  2. Let me redefine it myself    │  all modes, real usage         │
                                  │ published     — complete, less │
                                  │  field-tested                  │
                                  │ draft         — functional,    │
                                  │ gaps remain                    │
                                  │ experimental  — early, expect  │
                                  │ change                         │
                                  │ stale         — needs a        │
                                  │ revisit                        │
                                  │ archived      — superseded,    │
                                  │ moved out                      │

---

Skizl handoff prompt:

  Update Skizl to support modern Codex skill versions stored at:

  metadata:
    version: "1.1.0"

  Repository:
  the skizl checkout inside the local skills library

  Before editing, snapshot the current Skizl skill according to its own workflow.

  Requirements:

  1. Find every place Skizl reads, compares, bumps, snapshots, publishes, or reports a skill version.
  2. Support both formats:
     - Preferred: metadata.version
     - Legacy fallback: top-level version
  3. Preserve backward compatibility with existing skills.
  4. Do not automatically rewrite legacy skill front matter.
  5. Update snapshot, bump, history, diff, publish, doctor, and version-guard behavior where applicable.
  6. Ensure version discovery ignores files inside versions/ when inspecting the active skill.
  7. When bumping a modern skill, update metadata.version without introducing an invalid top-level key.
  8. Add tests or fixtures covering:
     - metadata.version only
     - legacy top-level version only
     - missing version
     - both formats present
     - snapshot directories containing older versions
  9. Define deterministic precedence when both formats exist: metadata.version wins, and report the conflict.
  10. Update Skizl’s workflow documentation and examples.
  11. Run all validation and tests.
  12. Recommend the appropriate semantic version bump, but do not publish or push unless explicitly authorized.

  Context: Codex’s current skill validator rejects top-level `version:` but accepts `metadata.version`. Skizl currently assumes `grep '^version:'`, so it fails to
  detect valid modern skill versions.
---

Frontmatter spec conformance across the library (review, not urgent):

Verified 2026-08-18 against https://agentskills.io/specification and
https://code.claude.com/docs/en/skills.

The spec allows exactly six top-level keys: name, description, license,
compatibility, metadata, allowed-tools. `metadata` is defined as a map from
string keys to *string* values. Anything else is a hard error when packaging for
claude.ai, the Skills API, or package_skill.py:

  Unexpected key(s) in SKILL.md frontmatter: argument-hint.
  Allowed properties are: allowed-tools, compatibility, description, license,
  metadata, name

Skizl's check.py `portable` profile already enforces this correctly, including
rejecting list-valued metadata (spec says string values). No skizl change needed
for correctness — this entry is about the library, and about whether skizl should
report the gap.

Current state of the local skills library (215 SKILL.md files carry non-spec
top-level keys):

  version 184, status 109, category 105, tags 86, title 34, purpose 34,
  source 10, references 3, compatible_with 1, triggers 1
      -> custom bookkeeping; belongs under `metadata:`. Safe to migrate.

  when_to_use 89, argument-hint 48, user-invocable 12,
  disable-model-invocation 1, effort 1, agent 1, context 1
      -> real Claude Code extensions. Work locally, fail claude.ai upload, and
         have no spec equivalent. Moving them into `metadata` would make Claude
         Code ignore them, so migrating this group LOSES behavior. Leave alone
         unless the skill is actually destined for claude.ai.

Consequence today: none for local Claude Code use. Only bites on claude.ai /
Skills API upload.

Related fix already applied (skills_db, not skizl): _scripts/build_index.py had
no nested-map parsing, so `metadata:` was read as None and its indented children
were silently promoted to top level — nested metadata appeared to work by
accident and broke on any non-scalar value. Added `metadata` to FRONTMATTER_KEYS
plus one-level nested-map parsing with a top-level-first fallback. Recovered
version 110 -> 167, status 95 -> 101, category 92 -> 97 across 299 skills.

Open questions for a future pass:
  - Migrate group 1 (bookkeeping -> metadata) in a batch? ~184 files, mechanical
    and reversible, no behavior change. Not yet done — needs explicit go-ahead.
  - Should `skizl doctor` / check.py warn when a skill uses Claude-Code-only keys,
    so the claude.ai-upload limitation is visible before someone hits the hard
    error at package time?
  - Should the skizl profile stay permissive for library bookkeeping, or should
    it steer authors toward `metadata:` so skills stay upload-portable by default?

---

## /skill-densify & Micro-Kernel Compression Design Patterns (from Orca & Spectacular lessons)

Feedback and design heuristics for `/skill-densify` to achieve ultra-dense, token-efficient skill kernels:

1. **Ultra-dense, unambiguous operational rules & clear "DO NOT" constraints**:
   - LLMs follow direct negative constraints with higher fidelity and 75% fewer tokens than explanatory prose tutorials.
   - Strip conversational rationale; state strict invariants and prohibitions directly.
2. **Explicit string triggers in YAML frontmatter**:
   - Include literal phrase matches (e.g. `"hand off"`, `"supervise"`, `"wait"`, `"review"`) directly in `description:` so agent routing resolves immediately on turn 0 without secondary classification.
3. **Consolidated CLI Palette with Parameter Grammar**:
   - Consolidate entire command surface into a compact parameter code block rather than repeating command definitions across multiple sections.
4. **Inline State Matrices**:
   - Use compact Markdown tables or bullet state taxonomies (e.g. `[SUPERVISED]`, `[HANDOFF]`, `[TAKEOVER]`) instead of multi-paragraph narrative explanations.
5. **Atomic Commands**:
   - Combine multi-step workflows into single atomic CLI calls (e.g. check + ack + wait in one operation).
6. **Automatic Identity Resolution (Zero Parameter Waste)**:
   - Auto-resolve `--by`, `--from`, `--operator` from workspace configuration (`config.yaml` / git config) rather than requiring repetitive CLI flags.
7. **Non-Mutating Peeking**:
   - Provide read-only / preview flags (`--peek`, `--dry-run`) so agents can inspect queue/history without triggering transaction changes.
