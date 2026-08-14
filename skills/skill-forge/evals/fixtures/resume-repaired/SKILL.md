---
name: release-note
description: |
  Write concise user-facing release notes from a bounded set of product changes. Use when a
  release needs a publishable summary. Not for commit messages, pull-request descriptions, or
  general documentation.
---

# Release Note

Turn a supplied change set into a concise release note for product users.

## Workflow

1. **Select.** Read the complete change set and identify every change that affects users. Done
   when: each supplied change is classified as user-facing or internal, with a reason.
2. **Write.** Summarize the user-facing changes and include upgrade action only where required.
   Done when: every user-facing change appears once, internal detail is excluded, and each
   required user action is explicit.

## Output

Return a short release-note heading followed by the user-facing changes and any required upgrade
action.

## Done

The note accounts for the complete supplied change set and contains no commit-message,
pull-request, or general-documentation content.
