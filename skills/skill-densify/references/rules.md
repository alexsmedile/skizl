# Telegraphic Micro-Kernel Rules & Style Guide

Use this when: pruning prose, editing front-door SKILL.md files, or eliminating token waste.

## 1. The Runtime Budget Filter

Every line in a front-door `SKILL.md` must pass at least one criterion:
1. **Changes Action**: Alters what tool or command the model executes next.
2. **Chooses Route**: Selects an exclusive branch or reference file.
3. **Defines Finish Line**: Provides an observable done/not-done verification check.
4. **Blocks a Failure**: Prevents a documented, known model failure mode.

*If a sentence passes none of the above, delete it whole.*

---

## 2. Zero-Ambiguity Compression Guard

Unlike human summarization (which can smooth away nuance), agent skills are **step-by-step operational programs**. Compression must preserve absolute operational precision:

- **Order-Critical Sequences**: Keep explicit step numbers (`1.`, `2.`, `3.`) or sequential pipelines (`a → b → c`). Never collapse multi-step dependencies into vague prose.
- **Fail-Closed States**: Always specify what happens when a check fails (e.g. `mismatch → halt & prompt`).
- **Tool Invariants**: Explicitly state which tool handles which step; do not leave tool selection to chance.
- **Pre/Post-Conditions**: State the condition required before executing, and the verifiable state after.

---

## 3. Anti-Prose & Anti-Wrapper Heuristics

| Verbose Habit | Telegraphic Fix |
|---|---|
| Preamble ("It is important to remember...") | Cut preamble; state the operational rule directly. |
| Output Framing ("Here is the result of...") | Strip wrapper; emit only the standardized box or artifact. |
| Explaining rationale ("We do this because...") | Keep only the constraint; move rationale to references if essential. |
| Negation ("Do not forget to avoid doing X...") | State the positive operational target ("Perform X with Y"). |
| Conversational transitions ("Now that we have...") | Use tabular sequence or step numbers. |
| Weak modal verbs ("You should try to ensure...") | Use direct imperative verbs ("Inspect", "Validate", "Emit"). |
| Generic advice ("Write clean code", "Be careful") | Delete completely (zero behavioral impact). |

---

## 4. Density Checklist

- [ ] Front-door `SKILL.md` is ≤ 65 lines.
- [ ] Core workflow is represented as a compact decision table or pipeline.
- [ ] Discovery actions use deterministic helper scripts in `scripts/`.
- [ ] Routine executions use silent fast-lane execution.
- [ ] Completion reports use a standard left-border text box.
- [ ] Situational logic is moved to `references/*.md` with `Use this when:` activation rules.
- [ ] All CLI flags, parameters, and done conditions remain exact and unambiguous.
