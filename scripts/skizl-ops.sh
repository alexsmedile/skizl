#!/usr/bin/env bash
# skizl-ops.sh — Deterministic mechanical helper for skizl
# Fast, token-efficient command offloading for sym-status, doctor, diffsum, and guard-check.

set -euo pipefail

SKIZL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="${SKIZL_ROOT}/skills"
CLAUDE_SKILLS="${SKIZL_ROOT}/.claude/skills"
AGENTS_SKILLS="${SKIZL_ROOT}/.agents/skills"

cmd="${1:-help}"
shift || true

case "$cmd" in
  sym-status)
    echo "┌─ SKIZL · symlink matrix"
    if [ ! -d "$SKILLS_DIR" ]; then
      echo "│ error: skills/ directory not found"
      echo "└─"
      exit 1
    fi
    for sdir in "$SKILLS_DIR"/*; do
      [ -d "$sdir" ] || continue
      sname="$(basename "$sdir")"
      claude_st="unlinked"
      agents_st="unlinked"
      if [ -L "${CLAUDE_SKILLS}/${sname}" ]; then
        [ -e "${CLAUDE_SKILLS}/${sname}" ] && claude_st="linked" || claude_st="broken"
      fi
      if [ -L "${AGENTS_SKILLS}/${sname}" ]; then
        [ -e "${AGENTS_SKILLS}/${sname}" ] && agents_st="linked" || agents_st="broken"
      fi
      printf "│ %-18s │ claude: %-8s │ agents: %-8s\n" "$sname" "$claude_st" "$agents_st"
    done
    echo "└─"
    ;;

  doctor)
    errors=0
    warnings=0
    echo "┌─ SKIZL · doctor diagnosis"
    # 1. Broken symlinks in .claude/skills
    if [ -d "$CLAUDE_SKILLS" ]; then
      for link in "$CLAUDE_SKILLS"/*; do
        [ -L "$link" ] || continue
        if [ ! -e "$link" ]; then
          echo "│ [ERR] Broken symlink: .claude/skills/$(basename "$link")"
          errors=$((errors + 1))
        fi
      done
    fi
    # 2. Broken symlinks in .agents/skills
    if [ -d "$AGENTS_SKILLS" ]; then
      for link in "$AGENTS_SKILLS"/*; do
        [ -L "$link" ] || continue
        if [ ! -e "$link" ]; then
          echo "│ [ERR] Broken symlink: .agents/skills/$(basename "$link")"
          errors=$((errors + 1))
        fi
      done
    fi
    # 3. Missing SKILL.md in skills/*
    if [ -d "$SKILLS_DIR" ]; then
      for sdir in "$SKILLS_DIR"/*; do
        [ -d "$sdir" ] || continue
        if [ ! -f "$sdir/SKILL.md" ]; then
          echo "│ [ERR] Missing SKILL.md in skills/$(basename "$sdir")"
          errors=$((errors + 1))
        fi
      done
    fi
    if [ "$errors" -eq 0 ] && [ "$warnings" -eq 0 ]; then
      echo "│ status: all symlinks, skills, and manifests healthy"
    fi
    echo "└─ result: ${errors} error(s), ${warnings} warning(s)"
    [ "$errors" -eq 0 ]
    ;;

  diffsum)
    target="${1:-}"
    if [ -z "$target" ]; then
      echo "Usage: skizl-ops.sh diffsum <skill-dir-or-file> [<other-file>]" >&2
      exit 1
    fi
    file1="$target"
    [ -d "$file1" ] && file1="$file1/SKILL.md"
    file2="${2:-}"
    if [ -z "$file2" ]; then
      # Search for latest snapshot in versions/
      skill_dir="$(dirname "$file1")"
      if [ -d "$skill_dir/versions" ]; then
        latest="$(ls -1t "$skill_dir/versions"/SKILL@*.md 2>/dev/null | head -n 1 || true)"
        file2="$latest"
      fi
    else
      [ -d "$file2" ] && file2="$file2/SKILL.md"
    fi
    echo "┌─ SKIZL · diff summary"
    if [ ! -f "$file1" ]; then
      echo "│ target file not found: $file1"
      echo "└─"
      exit 1
    fi
    if [ -z "$file2" ] || [ ! -f "$file2" ]; then
      echo "│ current: $file1 ($(wc -l < "$file1" | tr -d ' ') lines)"
      echo "│ compare: (no previous snapshot found)"
      echo "└─"
      exit 0
    fi
    l1=$(wc -l < "$file1" | tr -d ' ')
    l2=$(wc -l < "$file2" | tr -d ' ')
    diff_stats=$(diff -u "$file2" "$file1" | grep -E "^[+-][^+-]" | wc -l | tr -d ' ' || echo "0")
    echo "│ src: $(basename "$file2") ($l2 lines) -> $(basename "$file1") ($l1 lines)"
    echo "│ changed lines: ~$diff_stats"
    echo "└─"
    ;;

  guard-check)
    echo "┌─ SKIZL · git-guard version audit"
    v_root=""
    v_claude=""
    v_market=""
    v_codex=""
    v_readme=""
    v_change=""
    
    [ -f "${SKIZL_ROOT}/plugin.json" ] && v_root=$(grep -o '"version": *"[^"]*"' "${SKIZL_ROOT}/plugin.json" | head -n 1 | cut -d'"' -f4 || true)
    [ -f "${SKIZL_ROOT}/.claude-plugin/plugin.json" ] && v_claude=$(grep -o '"version": *"[^"]*"' "${SKIZL_ROOT}/.claude-plugin/plugin.json" | head -n 1 | cut -d'"' -f4 || true)
    [ -f "${SKIZL_ROOT}/.claude-plugin/marketplace.json" ] && v_market=$(grep -o '"version": *"[^"]*"' "${SKIZL_ROOT}/.claude-plugin/marketplace.json" | head -n 1 | cut -d'"' -f4 || true)
    [ -f "${SKIZL_ROOT}/.codex-plugin/plugin.json" ] && v_codex=$(grep -o '"version": *"[^"]*"' "${SKIZL_ROOT}/.codex-plugin/plugin.json" | head -n 1 | cut -d'"' -f4 || true)
    [ -f "${SKIZL_ROOT}/README.md" ] && v_readme=$(grep -o 'version-[0-9.]*' "${SKIZL_ROOT}/README.md" | head -n 1 | cut -d'-' -f2 || true)
    [ -f "${SKIZL_ROOT}/CHANGELOG.md" ] && v_change=$(grep -E '## \[[0-9.]+' "${SKIZL_ROOT}/CHANGELOG.md" | head -n 1 | grep -o '[0-9.]\+' | head -n 1 || true)
    
    echo "│ plugin.json:        ${v_root:-n/a}"
    [ -n "$v_claude" ] && echo "│ .claude-plugin:     $v_claude"
    [ -n "$v_market" ] && echo "│ marketplace.json:   $v_market"
    [ -n "$v_codex" ]  && echo "│ .codex-plugin:      $v_codex"
    [ -n "$v_readme" ] && echo "│ README badge:       $v_readme"
    [ -n "$v_change" ] && echo "│ CHANGELOG top:      $v_change"

    mismatch=0
    base="${v_root:-$v_claude}"
    for v in "$v_claude" "$v_market" "$v_codex" "$v_readme" "$v_change"; do
      if [ -n "$v" ] && [ -n "$base" ] && [ "$v" != "$base" ]; then
        mismatch=1
      fi
    done

    if [ "$mismatch" -eq 1 ]; then
      echo "│ [ERR] Version mismatch detected across manifest sources!"
      echo "└─ status: BLOCKED"
      exit 1
    else
      echo "└─ status: ALIGNED (${base:-unknown})"
    fi
    ;;

  help|*)
    echo "skizl-ops.sh: [sym-status | doctor | diffsum <path> | guard-check]"
    ;;
esac
