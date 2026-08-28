#!/usr/bin/env python3
"""densify.py — Automated density and micro-kernel analyzer for agent skills.

Measures line counts, estimates token budgets, flags conversational filler / wrappers / no-ops,
and checks progressive disclosure and table density.

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
]

# Size bands, measured on body lines. These are calibrated against real skill
# libraries: skills that have already applied progressive disclosure cluster
# around a 120-150 line body, so a single low ceiling flags healthy skills.
# Size alone is never a defect -- it is a prompt to check whether the content
# is structured and whether branch-only detail has been disclosed.
BANDS = [
    (60, "COMPACT", "Single-purpose kernel."),
    (150, "NORMAL", "Typical for a routed skill with references."),
    (300, "LARGE", "Check for branch-only detail that could be disclosed."),
    (float("inf"), "REVIEW", "Likely several skills, or reference material inlined."),
]


def classify(body_lines, structured, ref_count, unresolved):
    """Judge a skill on structure, not on line count alone."""
    for ceiling, band, note in BANDS:
        if body_lines <= ceiling:
            break

    # A large skill that is densely structured is doing its job; an
    # unstructured one of the same size is the actual problem.
    if body_lines > 150:
        density = structured / body_lines if body_lines else 0
        if density >= 0.15 and ref_count:
            note = "Structured and disclosed -- size is carrying real branches."
        elif density < 0.08:
            note = "Mostly prose -> convert forks to decision tables first."
        else:
            note = "Check for branch-only detail that could be disclosed."

    # Over-disclosure: small only because the operational content was pushed
    # out of reach. A working 150-line skill beats a 60-line one whose steps
    # live behind links the agent must chase mid-task.
    if body_lines <= 60 and ref_count >= 3:
        band, note = "THIN", "Small but heavily disclosed -> inline what every run needs."
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

    # Measure the body only. Frontmatter is the trigger surface -- a rich
    # description is what makes a skill fire correctly, so counting it would
    # penalize the one part that should never be compressed.
    body = lines
    fm_lines = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                body, fm_lines = lines[i + 1:], i + 1
                break
    body_lines = len(body)

    # Estimate tokens (~4 chars per token)
    est_tokens = len(text) // 4
    
    # Check tables & pipelines (body only -- frontmatter holds neither)
    table_lines = sum(1 for line in body if line.strip().startswith("|") and line.strip().endswith("|"))
    structured = table_lines + sum(1 for line in body if " → " in line or " -> " in line)
    table_ratio = (table_lines / body_lines * 100) if body_lines > 0 else 0
    pipeline_lines = sum(1 for line in body if " → " in line or " -> " in line)

    # Progressive disclosure already applied?
    ref_count = len(list(skill_md.parent.glob("references/*.md")))
    has_scripts = any(skill_md.parent.glob("scripts/*"))

    # Scan for filler
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

    if unresolved:
        print(f"│ [BROKEN]   {len(unresolved)} reference link(s) point at missing files:")
        for target in unresolved[:4]:
            print(f"│   -> {target}")
    elif ref_count:
        print(f"│ [PASS]     All reference links resolve")

    if findings:
        print(f"│ [DETECT]   {len(findings)} conversational filler / wrapper phrase(s):")
        for line_no, label, sample in findings[:4]:
            sample_trunc = sample[:55] + "..." if len(sample) > 55 else sample
            print(f"│   L{line_no}: [{label}] \"{sample_trunc}\"")
        if len(findings) > 4:
            print(f"│   ... and {len(findings) - 4} more")
    else:
        print("│ [PASS]     No conversational filler phrases detected")
        
    print("└─")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 densify.py <skill-dir-or-file>")
        sys.exit(1)
    sys.exit(analyze_skill(sys.argv[1]))
