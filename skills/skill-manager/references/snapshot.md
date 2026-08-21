# snapshot — Version management for skills

Use this when: creating a versioned snapshot, bumping semver, or inspecting version history.

Manages versioning snapshots, version bumps, and history for skills.

Three sub-commands: `snapshot`, `bump`, `history`.

---

## snapshot

Save the current `SKILL.md` as a timestamped snapshot in `versions/`.

### Usage

```
/skizl snapshot <skill-path>
/skizl snapshot <skill-path> --version 1.2.0     # use explicit version tag
/skizl snapshot <skill-path> --message "reason"  # annotate the snapshot
```

### Behavior

1. **Read Version:**
   Read the version from `SKILL.md` frontmatter:
   - Look for `metadata.version` (indented under the `metadata:` block).
   - Fall back to the top-level `version:` key (unindented).
   - If both formats exist, use `metadata.version` as the winner, print a warning to the user about the conflict, and suggest removing the duplicate top-level key.
   - If missing in both, default to `1.0.0`.
   - Ensure files inside the `versions/` subdirectory are ignored during active skill version checks.
2. Resolve destination: `<skill-path>/versions/SKILL@<version>.md`
3. If the file already exists, ask: **"SKILL@<version>.md already exists — overwrite? (yes / skip)"**
4. Copy `SKILL.md` to `versions/SKILL@<version>.md` verbatim (no modification).
5. Report:

```
✓ Snapshot saved: versions/SKILL@1.2.0.md
```

### Auto-trigger rules

- **On `/skizl publish` (publish action)**: before writing any manifest files, snapshot the current `SKILL.md` if it has a version. Skip silently if no version.
- **On `/skizl diff` (diff action)**: if the local version is ahead of the global installed version (newer semver), offer: **"Local is ahead — snapshot current version? (yes / skip)"**

---

## bump

Increment the version field in `SKILL.md` frontmatter and optionally snapshot.

### Usage

```
/skizl bump <skill-path>              # interactive: ask patch/minor/major
/skizl bump <skill-path> patch        # 1.2.3 → 1.2.4
/skizl bump <skill-path> minor        # 1.2.3 → 1.3.0
/skizl bump <skill-path> major        # 1.2.3 → 2.0.0
/skizl bump <skill-path> 2.1.0        # set explicit version
```

### Behavior

1. **Read Version:**
   Read current version from frontmatter using the same lookup rules as `snapshot` (checking `metadata.version` first, falling back to top-level `version:`, and flagging conflicts). If missing, treat as `1.0.0`.
2. Compute new version based on bump type.
3. Ask: **"Bump version <old> → <new>? (yes / edit / cancel)"**
4. **Edit File In-Place:**
   - If the skill has `metadata.version` (or both are present), update the `version:` line under the `metadata:` key in-place. Do not introduce a top-level key.
   - If the skill only has top-level `version:`, update the top-level `version:` line.
   - If neither exists, insert a top-level `version: <new_version>` line.
5. Ask: **"Snapshot this version? (yes / skip)"**
   - If yes: run `snapshot <skill-path>` with the new version.
6. Report:

```
✓ Version bumped: 1.2.3 → 1.2.4
✓ Snapshot saved: versions/SKILL@1.2.4.md
```

### Semver rules

| Type | Rule |
|------|------|
| `patch` | increment Z in X.Y.Z → X.Y.(Z+1) |
| `minor` | increment Y, reset Z → X.(Y+1).0 |
| `major` | increment X, reset Y and Z → (X+1).0.0 |
| explicit | replace with given string as-is |

---

## history

List all available snapshots for a skill.

### Usage

```
/skizl history <skill-path>
/skizl history <skill-path> --show 1.2.0    # print a specific snapshot
/skizl history <skill-path> --diff 1.1.0    # diff current vs snapshot
```

### Behavior

1. Check `<skill-path>/versions/` — if empty or missing, report "No snapshots yet."
2. List all `SKILL@*.md` files sorted by semver descending.
3. Read `version:` from current `SKILL.md` and mark it.

### Example output

```
Skill: skills/my-skill
Current version: 1.3.0

Snapshots:
  SKILL@1.3.0.md   (current)
  SKILL@1.2.1.md
  SKILL@1.2.0.md
  SKILL@1.0.0.md

Use `/skizl history skills/my-skill --show 1.2.0` to read a snapshot.
Use `/skizl history skills/my-skill --diff 1.2.0` to diff current vs that snapshot.
```

### --show

Print the snapshot file content directly (use `Read` tool).

### --diff

Run `diff` between current `SKILL.md` and the snapshot:

```bash
diff --color=always -u "<skill-path>/versions/SKILL@<version>.md" "<skill-path>/SKILL.md" || true
```

---

## versions/ folder convention

Snapshots live at `<skill-path>/versions/SKILL@x.y.z.md`.

- Named after the version in frontmatter at the time of snapshot.
- `apm` skips this folder during scans (it is in the exclusion list).
- Never edit snapshots manually — they are read-only historical records.
- No limit on number of snapshots — they are small text files.
