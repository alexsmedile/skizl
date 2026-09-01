# Telegraphic Micro-Kernel Rules & Style Guide

Use this when: pruning prose, editing front-door SKILL.md files, or eliminating token waste.

## 1. The Runtime Budget Filter

Every line in a front-door `SKILL.md` must pass at least one criterion:
1. **Changes Action**: Alters what tool or command the model executes next.
2. **Chooses Route**: Selects an exclusive branch or reference file.
3. **Defines Finish Line**: Provides an observable done/not-done verification check.
4. **Blocks a Failure**: Prevents a documented, known model failure mode (`DO NOT`).

*If a sentence passes none of the above, delete it whole.*

---

## 2. Zero-Ambiguity Compression Guard

Unlike human summarization (which can smooth away nuance), agent skills are **step-by-step operational programs**. Compression must preserve absolute operational precision:

- **Order-Critical Sequences**: Keep explicit step numbers (`1.`, `2.`, `3.`) or sequential pipelines (`a → b → c`). Never collapse multi-step dependencies into vague prose.
- **Fail-Closed States**: Always specify what happens when a check fails (e.g. `mismatch → halt & prompt`).
- **Tool Invariants**: Explicitly state which tool handles which step; do not leave tool selection to chance.
- **Pre/Post-Conditions**: State the condition required before executing, and the verifiable state after.

---

## 3. The `docs/` vs `skills/` Law (Anti-Lecturing)

- **`docs/` is for humans**: Concept overviews, background rationale, tutorials, and narrative explanations.
- **`skills/` is for agents**: Strict operational rules, input $\to$ output transforms, exact syntax matrices, and direct negative constraints (`DO NOT`).

**Never explain what a concept is in a skill.** The model already possesses broad CS/domain knowledge. Strip textbook definitions ("An ER diagram is a blueprint...") and replace with deterministic execution parameters.

---

## 4. Expansion Handoff Contracts

When an operation reaches beyond the skill's single responsibility, do not bloat the skill or offer half-baked instructions. Define an **Expansion Handoff Table** that delegates to dedicated companion skills.

---

## 5. Anti-Prose & Anti-Wrapper Heuristics

| Verbose Habit | Telegraphic Fix |
|---|---|
| Preamble ("It is important to remember...") | Cut preamble; state the operational rule directly. |
| Output Framing ("Here is the result of...") | Strip wrapper; emit only the standardized box or artifact. |
| Pedagogical Lecturing ("X is a visual blueprint...") | Delete definition; provide the dialect syntax matrix directly. |
| Explaining rationale ("We do this because...") | Keep only the constraint; move rationale to references if essential. |
| Convoluted negation ("Avoid forgetting to not...") | State direct negative constraint ("DO NOT edit files during review"). |
| Conversational transitions ("Now that we have...") | Use tabular sequence or step numbers. |
| Weak modal verbs ("You should try to ensure...") | Use direct imperative verbs ("Inspect", "Validate", "Emit"). |
| Generic advice ("Write clean code", "Be careful") | Delete completely (zero behavioral impact). |

---

## 6. Density Checklist

- [ ] Front-door `SKILL.md` body is a high-density micro-kernel (`OPTIMAL`, `COMPACT`, or `NORMAL`).
- [ ] Description carries explicit trigger phrases for turn-0 classification.
- [ ] Core workflow is represented as a compact decision table or pipeline.
- [ ] Direct negative constraints ("DO NOT") are used for strict boundaries instead of polite prose.
- [ ] Out-of-scope capabilities declare explicit Expansion Handoff delegates.
- [ ] Tool API surfaces use a single consolidated parameter-annotated CLI palette.
- [ ] Discovery actions use deterministic helper scripts in `scripts/`.
- [ ] Routine executions use silent fast-lane execution with non-mutating preview (`--peek`, `--dry-run`).
- [ ] Completion reports use a standard left-border text box.
- [ ] Situational logic is moved to `references/*.md` with `Use this when:` activation rules.
- [ ] Every reference link resolves to a file that exists.
