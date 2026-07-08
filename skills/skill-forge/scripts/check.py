#!/usr/bin/env python3
"""Mechanical lint for a skill folder. Mechanical faults ONLY —
semantic quality (no-ops, duplication, trigger accuracy) belongs to the
reviewer and evals. A script cannot grep its way into good skill design.

Usage: python3 check.py <skill-dir>
Exit: 0 clean (warnings allowed), 1 errors found.
"""
import json
import re
import sys
from pathlib import Path

MAX_LINES = 500
SKIP_DIRS = {"versions", "docs", "node_modules", ".git"}
# dirs holding disclosed material the SKILL.md/tracks read on demand — each .md must
# open with an activation rule so a pointer knows when to fire it.
DISCLOSED_DIRS = {"references", "tracks", "workflows", "prompts"}
NO_ACTIVATION_NEEDED = {"SKILL.md", "README.md", "GLOSSARY.md", "CHANGELOG.md"}
LINK = re.compile(r"\]\(([^)]+)\)")
CAPS = re.compile(r"\b(ALWAYS|NEVER|MUST NOT|MUST)\b")


def md_files(root):
    for p in sorted(root.rglob("*.md")):
        parts = set(p.relative_to(root).parts[:-1])
        if parts & SKIP_DIRS or any(x.startswith("_") for x in p.relative_to(root).parts):
            continue
        yield p


def main(skill_dir):
    root = Path(skill_dir).resolve()
    errors, warns = [], []

    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        print(f"ERROR: {root}/SKILL.md missing")
        return 1
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()

    # --- frontmatter ---
    fm = ""
    if lines and lines[0].strip() == "---":
        try:
            end = lines[1:].index("---") + 1
            fm = "\n".join(lines[1:end])
        except ValueError:
            errors.append("SKILL.md: frontmatter opened but never closed")
    else:
        errors.append("SKILL.md: no frontmatter block")
    user_invoked = "disable-model-invocation" in fm
    if fm and "description" not in fm and not user_invoked:
        errors.append("SKILL.md: no description and not user-invoked — it can never trigger")

    # --- line count ---
    if len(lines) > MAX_LINES:
        errors.append(f"SKILL.md: {len(lines)} lines > {MAX_LINES} — disclose or split")

    all_md = list(md_files(root))
    corpus = {p: p.read_text(encoding="utf-8") for p in all_md}

    # --- local links resolve ---
    for p, body in corpus.items():
        for m in LINK.finditer(body):
            target = m.group(1).split("#")[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "${")):
                continue
            if not (p.parent / target).exists():
                errors.append(f"{p.relative_to(root)}: broken link -> {target}")

    # --- orphans: md file mentioned nowhere else ---
    for p in all_md:
        name = p.name
        if name in NO_ACTIVATION_NEEDED:
            continue
        mentioned = any(name in body for q, body in corpus.items() if q != p)
        if not mentioned:
            warns.append(f"{p.relative_to(root)}: orphaned — no other file mentions it")

    # --- activation rule in disclosed dirs ---
    for p in all_md:
        rel = p.relative_to(root)
        if rel.parts[0] in DISCLOSED_DIRS and "Use this when" not in corpus[p]:
            errors.append(f"{rel}: disclosed file missing a 'Use this when:' activation rule")

    # --- evals JSON validity ---
    for j in sorted(root.glob("evals/*.json")):
        try:
            json.loads(j.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{j.relative_to(root)}: invalid JSON — {e}")

    # --- empty dirs ---
    for d in sorted(root.rglob("*")):
        if d.is_dir() and not any(d.iterdir()) and d.name not in SKIP_DIRS:
            warns.append(f"{d.relative_to(root)}/: empty directory — delete or fill")

    # --- ALL-CAPS steering smell (warning: sometimes earned, usually negation) ---
    for p, body in corpus.items():
        hits = CAPS.findall(body)
        if hits:
            warns.append(f"{p.relative_to(root)}: ALL-CAPS steering ({', '.join(sorted(set(hits)))}) — prefer positive targets")

    for e in errors:
        print(f"ERROR: {e}")
    for w in warns:
        print(f"warn:  {w}")
    print(f"\n{root.name}: {len(errors)} error(s), {len(warns)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
