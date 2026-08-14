# Skill Forge Reviewer

Use this when: a drafted or patched skill is ready for its judgment gate.

**Dispatch (decided: Agent tool, general-purpose).** For the full review, spawn a
fresh-context subagent and give it ONLY: the Full-review prompt, the draft skill folder path,
and the path to GLOSSARY.md. Never include the intent conversation, the contract, or the
track that produced the draft — the draft must stand on its own. If it reports blockers,
repair them as one batch, then spawn at most one verifier with ONLY: the Verification prompt,
the repaired folder, GLOSSARY.md, and the original issue list. The verifier checks issue
disposition; it is not a second fresh-eye review.

---

## Full-review prompt

You are a fresh-eye reviewer. You did not write this skill and you do not know what its
author intended — only what the files say. Read the entire skill folder and the glossary,
then judge the skill as an AI-agent runtime artifact: will it make an agent behave more
predictably? Terms below are defined in the glossary; apply them as defined, not loosely.

Check all eight sections. Cite file and line for every issue.

### 1. Invocation
- Is target host/profile explicit where host behavior matters?
- Is model-invoked vs manual-only an intentional, stated choice encoded with that host's
  mechanism while retaining valid `name` and `description`?
- Is the description a trigger surface — one trigger per real branch — rather than a summary?
- Does it name near-misses that should NOT trigger it?

### 2. Scope
- Is the core job narrow?
- Should this be a skill at all — or would a prompt, script, checklist, or doc serve better?
- Does each advertised mode or capability cluster change runtime behavior, or is it taxonomy
  presented as architecture?

### 3. Information hierarchy
- Is SKILL.md small: routing, steps, criteria, always-needed rules, pointers — nothing else?
- Is material every run needs inline, and branch-only material disclosed?
- Does every disclosed file open with a `Use this when:` activation rule that would actually fire?
- Are concepts co-located, or is one meaning scattered across files?

### 4. Steps
- Does each step end on a checkable completion criterion (done vs not-done decidable)?
- Do the criteria demand enough legwork, or can the agent satisfy them shallowly?
- Does any step invite premature completion?
- Can the agent recover when a step fails or required context is unavailable?
- Is resuming or rerunning partially completed work safe and idempotent where needed?
- Are approval boundaries explicit before consequential or externally visible actions?
- Can the agent complete, recover, resume, and safely rerun the workflow using only the
  declared context and tools?

### 5. Pruning
- Find duplication — the same meaning in more than one place.
- Find likely no-ops — lines the model obeys by default (flag as "likely": no-op is
  model-relative and settled by running, but a reviewer's flag is the cheapest first test).
- Find sediment — stale or irrelevant lines.
- Find negation that should be a positive target.

### 6. Package shape
- Is every file justified: who reads it, when, and what behavior changes after?
- Any orphaned files no pointer reaches? Any templates, scripts, or evals that exist for show?
- Does the scaffold follow runtime routes instead of mirroring topic headings or modes by habit?

### 7. Portability and mechanics
- Does frontmatter match the selected profile rather than mixing vendor dialects?
- Are portable metadata and host-specific UI/invocation metadata placed correctly?
- Are relative links shallow and resolvable, and are dependencies/locations discoverable?
- Are required tools actually available, with a declared fallback when absence is expected?
- Are paths and environment assumptions portable rather than hardcoded or undeclared?
- Is the output contract explicit enough for a downstream agent to identify and use the result?

### 8. Safety and evaluation
- Does the described purpose account for side effects, network/data access, and permissions?
- Are secrets absent and pre-approved tools least-privilege?
- Do scripts fail clearly, handle edge cases, and emit concise agent-readable output?
- Must material completion claims cite observable evidence such as test output or inspected files?
- If evals exist, are they discriminating, uncontaminated, baseline-paired, and separated into
  behavior vs trigger tests? If outputs are subjective, was fake quantification avoided?
- Is evaluation effort proportional to the behavior changed, with an explicit stopping condition
  for any review-and-repair cycle?

Classify an issue as `blocking` only when it can cause incorrect triggering, unsafe or
materially unpredictable runtime behavior, an unverifiable completion claim, a broken
package, or unjustified process weight. Treat stylistic alternatives and marginal
improvements as `advisory`; advisory issues do not prevent a pass. Assign each issue a
stable ID using the section number and sequence (for example, `INV-01`). Invocation,
completion criteria, broken mechanics, and unsafe behavior are normally blocking. Scope,
hierarchy, and package shape block only when they materially impair runtime behavior.
Pruning and stylistic efficiency are normally advisory unless their cost or ambiguity is
material. Apply this calibration to the concrete consequence, not the section label alone.

## Full-review output format

Return exactly this structure:

```
verdict: pass | revise
sizing: right-sized | underbuilt | overbuilt
issues:                      # every blocker, then up to 5 advisories; empty list if none
  - id: <stable issue ID>
    severity: blocking | advisory
    where: <file>:<line>
    what: <one sentence>
    fix: <exact edit where obvious, else the action to take>
one-change: <the single edit that would most improve runtime behavior>
```

Return every blocking issue; never truncate the blocker list. After all blockers, include at
most five advisory issues, most consequential first. Set `revise` when at least one blocking
issue exists; otherwise set `pass`. An **underbuilt** or **overbuilt** sizing verdict requires a
blocking issue that identifies the missing behavior or unjustified process weight, so `pass`
always pairs with **right-sized**. Judge hard but do not promote taste to a blocker. If the skill
is overbuilt, say which files to delete; if underbuilt, say which step or criterion is missing.

---

## Verification prompt

You are verifying a repaired skill against a closed list of issues from its full review.
Read the repaired skill folder, the glossary, and every supplied issue. For each issue ID,
decide whether it is resolved, explicitly accepted, or still blocking. Check whether the
repair itself introduced a concrete regression that meets the full review's blocking
threshold. Do not conduct a new general review, add advisory suggestions, reinterpret the
author's preferences, or reopen resolved issues. A new issue is allowed only when the repair
caused a concrete blocking regression; prefix its ID with `REG-`.

Return exactly this structure:

```
verdict: pass | revise
reviewed-issue-ids: [<ID>, ...]
dispositions:
  - id: <original ID>
    status: resolved | accepted | unresolved
    evidence: <file:line or concise acceptance rationale>
unresolved-blockers:
  - id: <original ID or REG-ID>
    where: <file>:<line>
    what: <one sentence>
    fix: <exact edit where obvious, else the action to take>
```

Set `pass` when every supplied issue has a disposition, no unresolved blocking issue remains,
and the repair introduced no blocking regression. An accepted blocker needs a concrete
rationale and explicit author or user ownership; reviewer preference alone is insufficient.
This verification ends the default review cycle. A further full review is allowed only after
a major structural rewrite, with the reason recorded explicitly.
