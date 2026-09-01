#!/usr/bin/env python3
"""densify.py — Automated density and micro-kernel analyzer for agent skills.

Measures line counts, estimates token budgets, flags conversational filler / wrappers / lecturing,
and checks progressive disclosure, table density, direct negative invariants, and expansion handoffs.

Usage: python3 densify.py <skill-dir-or-SKILL.md>
"""

import sys
import re
from pathlib import Path

FILLER_PATTERNS = [
    (r"\b(it is important to note that|please note that|remember that|keep in mind that)\b", "Conversational preamble"),
    (r"\b(as an ai language model|as an agent|as mentioned earlier|as stated above)\b", "Meta filler"),
    (r"\b(make sure to|be sure to|ensure that you always|try to|take care to)\b", "Weak steering (replace with direct imperative verb)"),
    (r"\b(in order to|with the purpose of|so as to)\b", "Verbose phrasing (use 'to')"),
    (r"\b(feel free to|you may also|if you want|if you like)\b", "Advisory hedging"),
    (r"\b(here is a|here is the|in this section|the following is)\b", "Output wrapper / preamble"),
    (r"\b(is an? (visual )?(blueprint|concept|framework|methodology|tool|standard) (used|designed) to)\b", "Pedagogical lecturing (move to docs/ or prune)"),
    (r"\b(refers to the concept of|can be defined as|is widely used in (the )?industry)\b", "Textbook explanation (move to docs/)"),
    (r"\b(allows (the )?(user|developer) to|enables users to)\b", "Feature marketing prose (use direct action verb)"),
]

BANDS = [
    (60, "COMPACT", "Single-purpose kernel."),
    (150, "NORMAL", "Typical for a routed skill with references."),
    (300, "LARGE", "Check for branch-only detail that could be disclosed."),
    (float("inf"), "REVIEW", "Likely several skills, or reference material inlined."),
]


def classify(body_lines, structured, ref_count, unresolved):
    """Judge a skill on structure, not on line count alone."""
    density = structured / body_lines if body_lines else 0

    # High structure with references is optimal regardless of line count
    if density >= 0.25 and ref_count >= 1:
        return "OPTIMAL", "Dense micro-kernel with structured tables & disclosed references."

    for ceiling, band, note in BANDS:
        if body_lines <= ceiling:
            break

    if body_lines > 150:
        if density >= 0.15 and ref_count:
            note = "Structured and disclosed -- size is carrying real branches."
        elif density < 0.08:
            note = "Mostly prose -> convert forks to decision tables first."
        else:
            note = "Check for branch-only detail that could be disclosed."

    if body_lines <= 60 and ref_count >= 3 and density < 0.20:
        band, note = "THIN", "Small but low internal density -> inline what every run needs."
    return band, note


def strip_fences(body):
    """Drop fenced code blocks -- links inside them are sample output, not links."""
    out, in_fence = [], False
    for line in body:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return out


def broken_links(skill_md, body):
    """Reference links in SKILL.md that point at files which do not exist."""
    missing = []
    for target in re.findall(r"\]\((?!https?:)([^)#]+\.md)\)", "\n".join(strip_fences(body))):
        if not (skill_md.parent / target).exists():
            missing.append(target)
    return sorted(set(missing))


def analyze_skill(target_path):
    target = Path(target_path).resolve()
    if target.is_dir():
        skill_md = target / "SKILL.md"
    else:
        skill_md = target

    if not skill_md.exists():
        print(f"Error: {skill_md} not found", file=sys.stderr)
        return 1

    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    total_lines = len(lines)

    body = lines
    fm_lines = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                body, fm_lines = lines[i + 1:], i + 1
                break
    body_lines = len(body)
    est_tokens = len(text) // 4
    
    table_lines = sum(1 for line in body if line.strip().startswith("|") and line.strip().endswith("|"))
    structured = table_lines + sum(1 for line in body if " → " in line or " -> " in line)
    table_ratio = (table_lines / body_lines * 100) if body_lines > 0 else 0
    pipeline_lines = sum(1 for line in body if " → " in line or " -> " in line)

    ref_count = len(list(skill_md.parent.glob("references/*.md")))
    has_scripts = any(skill_md.parent.glob("scripts/*"))

    # Invariant and negative constraints detection
    has_negative_invariants = any("DO NOT" in line for line in body)
    has_handoffs = any("Handoff" in line or "Out-of-Scope" in line or "Delegate" in line for line in body)

    # Scan for filler / lecturing
    findings = []
    for idx, line in enumerate(lines, start=1):
        for pattern, label in FILLER_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append((idx, label, line.strip()))

    unresolved = broken_links(skill_md, body)
    band, verdict = classify(body_lines, structured, ref_count, unresolved)

    print("┌─ SKIZL · densify analysis")
    print(f"│ target:    {skill_md.name} ({skill_md.parent.name})")
    print(f"│ volume:    {body_lines} body lines + {fm_lines} frontmatter (~{est_tokens} tokens)")
    print(f"│ density:   {table_lines} table lines ({table_ratio:.1f}%), {pipeline_lines} pipeline line(s)"
          f"{f', {ref_count} reference(s)' if ref_count else ''}")
    print(f"│ [{band}]{' ' * max(1, 10 - len(band))}{verdict}")

    features = []
    if has_negative_invariants:
        features.append("DO NOT invariants present")
    if has_handoffs:
        features.append("expansion handoffs declared")
    if features:
        print(f"│ [FEATURES] {', '.join(features)}")

    if unresolved:
        print(f"│ [BROKEN]   {len(unresolved)} reference link(s) point at missing files:")
        for target in unresolved[:4]:
            print(f"│   -> {target}")
    elif ref_count:
        print(f"│ [PASS]     All reference links resolve")

    if findings:
        print(f"│ [DETECT]   {len(findings)} conversational filler / lecturing phrase(s):")
        for line_no, label, sample in findings[:4]:
            sample_trunc = sample[:55] + "..." if len(sample) > 55 else sample
            print(f"│   L{line_no}: [{label}] \"{sample_trunc}\"")
        if len(findings) > 4:
            print(f"│   ... and {len(findings) - 4} more")
    else:
        print("│ [PASS]     No conversational filler or pedagogical lecturing detected")
        
    print("└─")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 densify.py <skill-dir-or-file>")
        sys.exit(1)
    sys.exit(analyze_skill(sys.argv[1]))
