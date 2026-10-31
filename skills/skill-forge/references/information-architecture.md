# Information architecture across skills and modules

Use this when: creating or updating a multi-skill package, consolidating scattered
procedures, auditing routing/disclosure, or separating reusable methods from providers.
Apply the glossary's definitions of branch, capability cluster, context pointer,
co-location and single source of truth; this reference supplies the decision procedure.

## Map ownership before moving content

For each requested capability identify its outcome, inputs, decisions, output,
validation, state writer and downstream consumer. Reuse existing owners and IDs.
A capability crossing specialists needs explicit handoffs, not necessarily a new
skill. Split into another skill only when a recurring independently invocable job
has distinct decisions or contracts; a topic heading alone does not justify one.

Classify each passage by its authoritative role:

| Role | Place and reader |
|---|---|
| Invocation, owned outcome, routing, common rules, finish line | SKILL.md; every invocation |
| Task-specific procedure, techniques and exceptions | Owning skill's reference; selected task only |
| Shared cross-skill contract | Existing shared reference; participating specialists |
| Runtime schema, commands, supported bindings and recovery | Application/adapter contract; execution branch |
| Source evidence and reusable findings | Existing knowledge store; retrieval/study branch |
| Current inputs, choices, revisions and acceptance | Project-owned artifacts; current production |
| Historical decisions and qualification evidence | Existing history/evidence owner; relevant audit/recovery |

These are logical roles, not a required directory scaffold. Keep a concept's rules
and exceptions together at its owner. Replace duplicate definitions with conditional
pointers; retain genuinely different responsibilities and compatibility anchors.
Consolidate a procedure when one reader needs it as a unit; keep distinct writers
and domains separate even when their names overlap. Avoid adding a universal manifest
or coordinator merely to make the folder tree look unified.

## Validate a working route

For each real branch state the entry condition, needed context, owning specialist,
required tools, returned artifact and completion check. A link names when to read
its target and which decision it enables; it does not require recursive loading.
Keep path-selection rules available before the choice and detailed mechanics behind
the selected pointer. Sharpen ambiguous pointers before inlining their targets.

For procedural skills, make the principal use case executable from its entry:

- **Give an ordered path, not only an owner list.** Connect the request to required
  reads, actions/tools, files to create or modify, returned artifacts and exit checks.
  A specialist link alone does not explain how its output feeds the next step.
- **Make mechanics concrete at their owner.** Give verified commands/API calls,
  input/output locations or resolution rules, and the actual result to inspect.
  Keep executable schemas and syntax in one authoritative place; link the exact
  procedure/section rather than making the agent search a broad manual. For
  reasoning-only steps, identify the decision and evidence instead of inventing a CLI.
- **Disclose by branch, preserve the working sequence.** Keep path selection in
  the entry and co-locate the selected procedure. Splitting every small step into
  another reference can shorten the entry while increasing navigation and inference.
  Specialization is useful when handoffs carry inputs, outputs and completion evidence.
- **Specify revision entry points.** Map common feedback to its owning source,
  first step to repeat, preserved decisions and dependent checks. Separate the
  smallest logical correction from what the actual backend must recompute; reuse
  valid outputs and approvals only within their recorded scope.
- **Compare execution effort, not just text size.** Trace one normal request and
  one correction: can an agent act without guessing commands, editable files,
  ordering or success evidence? Record unresolved joins and unnecessary reads.
  A shorter document or a static trace alone does not prove runtime/token savings
  or better output quality; those claims require observed runs.

Trace representative tasks end to end, including resume and one failure case:
can the agent select the route, reach required rules and execute without missing
context or reading unrelated stages? Recover relevant truncated sections. Reuse a
summary only while its source revision, coverage and applicable overrides are valid.
Readability, line/link counts and file count are diagnostics, not architecture scores;
compare context needed for a working route and actual behavior before claiming gains.

## Separate method, implementation and provider

Keep reusable decisions and semantic handoffs in the product/skill's own contracts;
put provider schemas, credentials, models, transport and version pins behind explicit
adapters loaded for their execution branch. A local wrapper around purchased code
still depends on that implementation; imported source, local execution, service
independence and replaceability are separate properties.

When native operation or provider independence is required, map actual dependencies
and prioritize qualified internal routes. Ordinary local libraries need not be
rewritten. Keep optional providers from blocking unrelated branches, and retain
existing capabilities until a replacement passes representative regression checks.
Preserve requested provider choices and explicit unsupported bindings. Source
availability, implementation, tested scope and human acceptance are separate claims.

Done when: each capability and authoritative fact has a named owner, each branch
reaches sufficient context through explicit pointers, adapters expose actual limits,
and representative route traces support the claimed consolidation. Record findings
in the existing forge record; no extra architecture artifact is mandatory.
