#!/usr/bin/env node
/**
 * pin.mjs — create or remove a redirect skill that delegates to a container action
 *
 * Usage:
 *   node pin.mjs <action>               # pin: create redirect skill
 *   node pin.mjs <action> --remove      # unpin: remove redirect skill
 *   node pin.mjs <action> --skills-dir <dir>   # custom output dir
 *   node pin.mjs --list                 # list active pins
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CONTAINER_DIR = path.resolve(__dirname, '..');
const CONTAINER_SKILL = JSON.parse(
  fs.readFileSync(path.join(CONTAINER_DIR, 'SKILL.md'), 'utf8')
    .match(/^---\n([\s\S]*?)\n---/)?.[1]
    ?.replace(/^name:\s*(.+)$/m, '"name": "$1"')
    || '{"name":"cs"}'
);

// Parse container name from SKILL.md frontmatter
function getContainerName() {
  const raw = fs.readFileSync(path.join(CONTAINER_DIR, 'SKILL.md'), 'utf8');
  const match = raw.match(/^name:\s*(.+)$/m);
  return match ? match[1].trim() : path.basename(CONTAINER_DIR);
}

// Parse action description from container menu table
function getActionDescription(containerName, action) {
  const raw = fs.readFileSync(path.join(CONTAINER_DIR, 'SKILL.md'), 'utf8');
  const row = raw.match(new RegExp(`\\|\\s*\`?${action}\`?\\s*\\|[^|]*\\|\\s*([^|\\n]+)`));
  return row ? row[1].trim() : `Shortcut for /${containerName} ${action}.`;
}

// Get allowed-tools from container frontmatter
function getAllowedTools() {
  const raw = fs.readFileSync(path.join(CONTAINER_DIR, 'SKILL.md'), 'utf8');
  const block = raw.match(/^allowed-tools:\n((?:\s+-\s+.+\n?)+)/m);
  if (!block) return ['Bash', 'Read', 'Write'];
  return block[1].match(/^\s+-\s+(.+)$/gm).map(l => l.replace(/^\s+-\s+/, '').trim());
}

function resolveSkillsDir(override) {
  if (override) return path.resolve(override);
  // Try .claude/skills/ relative to cwd, then sibling of container
  const cwdClaude = path.join(process.cwd(), '.claude', 'skills');
  if (fs.existsSync(cwdClaude)) return cwdClaude;
  return path.dirname(CONTAINER_DIR);
}

function pin(action, skillsDir) {
  const containerName = getContainerName();
  const description = getActionDescription(containerName, action);
  const tools = getAllowedTools();
  const pinName = `i-${action}`;
  const pinDir = path.join(skillsDir, pinName);

  if (fs.existsSync(pinDir)) {
    console.log(`Already pinned: /${action} → /${containerName} ${action}`);
    return;
  }

  fs.mkdirSync(pinDir, { recursive: true });

  const actionPath = path.join(CONTAINER_DIR, 'actions', `${action}.md`);
  if (!fs.existsSync(actionPath)) {
    console.error(`Action not found: actions/${action}.md`);
    process.exit(1);
  }

  const relativeContainer = path.relative(pinDir, CONTAINER_DIR);

  const content = `---
name: ${pinName}
description: >
  Shortcut for /${containerName} ${action}. ${description}
  Delegates to the parent container — updates to the container flow through automatically.
triggers:
  - /${action}
allowed-tools:
${tools.map(t => `  - ${t}`).join('\n')}
---

Redirect: invoke \`/${containerName} ${action}\` with the same arguments.

Load \`${relativeContainer}/actions/${action}.md\` and follow its instructions exactly.
The target is everything the user passed after \`/${action}\`.
`;

  fs.writeFileSync(path.join(pinDir, 'SKILL.md'), content);

  // Symlink into .claude/skills/ if it exists in cwd
  const claudeSkills = path.join(process.cwd(), '.claude', 'skills');
  if (fs.existsSync(claudeSkills) && skillsDir !== claudeSkills) {
    const linkPath = path.join(claudeSkills, pinName);
    if (!fs.existsSync(linkPath)) {
      const rel = path.relative(claudeSkills, pinDir);
      fs.symlinkSync(rel, linkPath);
      console.log(`Symlinked: .claude/skills/${pinName}`);
    }
  }

  console.log(`Pinned: /${action} → /${containerName} ${action}`);
  console.log(`File: ${pinDir}/SKILL.md`);
  console.log(`Remove with: node ${path.relative(process.cwd(), __filename)} ${action} --remove`);
}

function unpin(action, skillsDir) {
  const pinName = `i-${action}`;
  const pinDir = path.join(skillsDir, pinName);

  let removed = false;
  if (fs.existsSync(pinDir)) {
    fs.rmSync(pinDir, { recursive: true });
    removed = true;
  }

  const claudeLink = path.join(process.cwd(), '.claude', 'skills', pinName);
  if (fs.existsSync(claudeLink) || fs.lstatSync(claudeLink).isSymbolicLink?.()) {
    fs.rmSync(claudeLink, { force: true });
    removed = true;
  }

  console.log(removed ? `Unpinned: /${action}` : `Not found: /${action} (nothing to remove)`);
}

function list(skillsDir) {
  const containerName = getContainerName();
  const entries = fs.existsSync(skillsDir)
    ? fs.readdirSync(skillsDir).filter(n => n.startsWith('i-'))
    : [];

  if (entries.length === 0) {
    console.log(`No pins active for /${containerName}`);
    return;
  }
  console.log(`Active pins for /${containerName}:`);
  entries.forEach(e => console.log(`  /${e.replace(/^i-/, '')} → /${containerName} ${e.replace(/^i-/, '')}`));
}

// --- CLI ---
const args = process.argv.slice(2);

if (args[0] === '--list') {
  const skillsDirIdx = args.indexOf('--skills-dir');
  list(resolveSkillsDir(skillsDirIdx >= 0 ? args[skillsDirIdx + 1] : null));
  process.exit(0);
}

const action = args[0];
if (!action || action.startsWith('--')) {
  console.error('Usage: node pin.mjs <action> [--remove] [--skills-dir <dir>]');
  console.error('       node pin.mjs --list [--skills-dir <dir>]');
  process.exit(1);
}

const remove = args.includes('--remove');
const skillsDirIdx = args.indexOf('--skills-dir');
const skillsDir = resolveSkillsDir(skillsDirIdx >= 0 ? args[skillsDirIdx + 1] : null);

if (remove) {
  unpin(action, skillsDir);
} else {
  pin(action, skillsDir);
}
