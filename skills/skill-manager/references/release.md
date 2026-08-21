# release — Make a verified, atomic plugin release

Use this when: making a verified, atomic plugin release.

Runs a verified, atomic release workflow for a plugin repository. It coordinates version updates across all manifests, ensures git status hygiene, performs project checks, handles authentication preflights, pushes code and tags, and creates the GitHub Release.

## Usage

```
/skizl release [--dry-run] [--scope <file1,file2,...>] [--bump <patch|minor|major|version>]
```

**Examples:**
```
/skizl release
/skizl release --dry-run
/skizl release --scope plugin.json,README.md,skills/skill-manager/SKILL.md --bump minor
```

---

## Command Flow

The agent must walk through the following 6 stages sequentially. If any stage fails, the agent must abort, report the error clearly, and suggest the command to resume from the failure point.

### Stage 1 — Git Hygiene & Scope Preflight

1. **Check Git Status:**
   Run `git status --porcelain` to check for modified, untracked, or deleted files.
2. **Handle Release Scope:**
   - If `--scope` is provided:
     - Identify any modified files that are **not** in the comma-separated scope list.
     - If there are modified files outside the scope, **refuse the release** and instruct the user to either commit them, stash them, or expand the `--scope` argument.
     - The workflow must leave these excluded WIP files untouched.
   - If `--scope` is not provided:
     - If there are modified files in the workspace, ask the user to confirm: **"Modified files found. Do you want to include all of them in the release? (yes / stash / specify-scope / abort)"**
     - If `stash`: Run `git stash push -m "skizl-release-wip"` to temporarily stash WIP changes before proceeding.
     - If `specify-scope`: Ask the user for the scope list and restart Stage 1 with it.

### Stage 2 — Auth Preflights

1. **Verify GitHub CLI Authentication:**
   Run `gh auth status` or `gh api user` to check if `gh` is authenticated.
   - If authentication is expired or missing:
     - **Refuse to proceed.**
     - Report:
       ```
       ✗ GitHub CLI authentication check failed.
       Please run: gh auth login
       Once authenticated, re-run the release command.
       ```
       Do not make any file updates, commits, tags, or pushes.

### Stage 3 — Project Checks

Run tests/lints/checks for the project to ensure the code is stable.
1. Check if the project has validation tests (e.g. `npm test`, a Python check suite, or other checks).
2. If dependencies required for the tests are missing (e.g., `PyYAML` for Python release checks, or `node_modules` for JS checks):
   - Attempt to run the check in an isolated or temporary environment (e.g., using `npx`, a temporary `virtualenv`, or a sandbox).
   - If dependencies cannot be satisfied, warn the user and ask: **"Dependencies missing for checks. Bypass checks and proceed? (yes / abort)"**
3. If checks run and fail, abort and print the test log. Do not proceed with the release.

### Stage 4 — Version Sync & Bump

Collect all version sources across the repository and apply the SemVer bump.

1. **Collect Current Version Sources:**
   - `.claude-plugin/plugin.json` (`.version`)
   - `.claude-plugin/marketplace.json` (`.metadata.version` and `.plugins[0].version`)
   - `.codex-plugin/plugin.json` (`.version`)
   - `README.md` version badge (`version-X.Y.Z`)
   - `CHANGELOG.md` top entry (`## [X.Y.Z]`)
   - `skills/*/SKILL.md` (read both `metadata.version` and top-level `version:` frontmatter; `metadata.version` takes precedence)
   - CLI version constant if configured (e.g., `SPECTACULAR_VERSION` in `cli/spectacular`).
2. **Determine Target Version:**
   - If the sources disagree, find the highest version.
   - If `--bump` is provided, calculate the new version from the highest source using SemVer rules (`patch`/`minor`/`major`/explicit).
   - If `--bump` is not provided, derive it from `CHANGELOG.md` or ask the user interactively: **"Select release type: (patch / minor / major / explicit)"**
3. **Update Version Sources:**
   - If `--dry-run` is active:
     - Log: `[Dry Run] Would update version from <current> to <target> in:` and list all files.
     - Do not modify any files.
   - Otherwise:
     - Update all plugin manifests (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`).
     - Update `README.md` badge.
     - Update `CHANGELOG.md` top entry (e.g., replace `[Unreleased]` or update the top release header).
     - Update `skills/*/SKILL.md` frontmatter:
       - If the skill uses `metadata.version`, update that key.
       - If it uses top-level `version:`, update that line.
       - If both are present, update `metadata.version`, warn about the conflict, and suggest removing the top-level key.
     - Update the CLI version constant (e.g., rewrite `SPECTACULAR_VERSION="X.Y.Z"` in `cli/spectacular`).

### Stage 5 — Git Commit & Tag

1. **Dry Run Check:**
   - If `--dry-run` is active, log:
     ```
     [Dry Run] Would create commit: "chore(release): v<version>"
     [Dry Run] Would create tag: "v<version>"
     ```
     Skip actual execution.
2. **Execute Commit & Tag:**
   - Add only the files within the release scope (or the modified version sources):
     `git add <files>`
   - Create the release commit:
     `git commit -m "chore(release): v<version>"`
   - Create the annotated tag:
     `git tag -a v<version> -m "Release v<version>"`

### Stage 6 — Push & GitHub Release (Resumable)

This stage involves network operations and publishing. It must be executed atomically: if the push succeeds but the GitHub Release fails (e.g. sudden token expiry or network drop), the release must not be reported as complete.

1. **Verify Auth Again (Safety Check):**
   Ensure auth is still valid.
2. **Push to Remote:**
   - If `--dry-run` is active, log:
     ```
     [Dry Run] Would run: git push origin <branch>
     [Dry Run] Would run: git push origin v<version>
     ```
   - Otherwise, push the commit and the tag:
     ```bash
     git push origin $(git branch --show-current)
     git push origin v<version>
     ```
3. **Create GitHub Release:**
   - Extract the release notes from the top entry of `CHANGELOG.md`.
   - If `--dry-run` is active, log:
     ```
     [Dry Run] Would run: gh release create v<version> --title "v<version>" --notes-file changelog_notes.txt
     ```
   - Otherwise, attempt to create the GitHub Release:
     ```bash
     gh release create v<version> --title "v<version>" --notes-file <(awk '/^## \[[0-9]+\.[0-9]+\.[0-9]+\]/{show=1; print; next} /^## \[[0-9]/{show=0} show' CHANGELOG.md)
     ```
   - **If the GitHub Release creation fails:**
     - **Do NOT mark the release as complete.**
     - Save the state. Inform the user:
       ```
       ✗ Git commit and tag v<version> were pushed successfully, but the GitHub Release creation failed.
       Reason: <error details>

       To complete the release manually after correcting authentication or network issues, run:
         gh release create v<version> --title "v<version>" --notes "Release v<version>"
       ```
       Abort execution with an error status.

### Stage 7 — Verify Distribution

Once the push and release commands succeed, verify the release has propagated.

1. **Verify Tag Visibility:**
   Run `git ls-remote --tags origin v<version>` to confirm the tag is visible on the remote repository.
2. **Verify Codex Marketplace / Raw Manifest Resolve:**
   - Fetch the raw manifest from GitHub using curl to verify it contains the correct version:
     ```bash
     curl -s "https://raw.githubusercontent.com/<username>/<repo>/v<version>/.claude-plugin/plugin.json" | jq -r .version
     ```
   - Verify it returns `<version>`.
   - If the Codex CLI is available, run:
     ```bash
     codex plugin marketplace refresh
     ```
3. **Clean Up:**
   If we stashed WIP changes in Stage 1, restore them:
   `git stash pop`
4. **Report Success:**
   Print a summary of the completed release, including all verified targets.
