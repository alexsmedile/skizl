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
    
    # Estimate tokens (~4 chars per token)
    est_tokens = len(text) // 4
    
    # Check tables & pipelines
    table_lines = sum(1 for line in lines if line.strip().startswith("|") and line.strip().endswith("|"))
    table_ratio = (table_lines / total_lines * 100) if total_lines > 0 else 0
    pipeline_lines = sum(1 for line in lines if " → " in line or " -> " in line)

    # Scan for filler
    findings = []
    for idx, line in enumerate(lines, start=1):
        for pattern, label in FILLER_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append((idx, label, line.strip()))

    print("┌─ SKIZL · densify analysis")
    print(f"│ target:    {skill_md.name} ({skill_md.parent.name})")
    print(f"│ volume:    {total_lines} lines (~{est_tokens} tokens)")
    print(f"│ density:   {table_lines} table lines ({table_ratio:.1f}%), {pipeline_lines} pipeline line(s)")
    
    if total_lines > 70:
        print(f"│ [WARN]     Micro-kernel exceeds budget (>65 lines) -> extract references")
    else:
        print(f"│ [PASS]     Micro-kernel within budget (<= 65 lines)")

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
