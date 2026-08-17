#!/usr/bin/env python3
"""Mechanical lint for a skill folder. Mechanical faults ONLY —
semantic quality (no-ops, duplication, trigger accuracy) belongs to the
reviewer and evals. A script cannot grep its way into good skill design.

Frontmatter uses a strict dependency-free YAML subset: top-level mappings, quoted or plain
scalars, block scalars, inline collections, and one indented metadata mapping. Unsupported or
malformed syntax fails closed instead of being guessed.

Usage: python3 check.py <skill-dir> [--profile portable|claude|codex|cursor|gemini|skizl]
Exit: 0 clean (warnings allowed), 1 errors found.
"""
import argparse
import json
import re
from pathlib import Path

MAX_LINES = 500
SKIP_DIRS = {"versions", "docs", "node_modules", ".git"}
# dirs holding disclosed material the SKILL.md/tracks read on demand — each .md must
# open with an activation rule so a pointer knows when to fire it.
DISCLOSED_DIRS = {"references", "tracks", "workflows", "prompts"}
NO_ACTIVATION_NEEDED = {"SKILL.md", "README.md", "GLOSSARY.md", "CHANGELOG.md"}
LINK = re.compile(r"\]\(([^)]+)\)")
CAPS = re.compile(r"\b(ALWAYS|NEVER|MUST NOT|MUST)\b")
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PORTABLE_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
PROFILE_FIELDS = {
    "portable": PORTABLE_FIELDS,
    "codex": PORTABLE_FIELDS,
    "gemini": PORTABLE_FIELDS,
    "cursor": PORTABLE_FIELDS | {"paths", "disable-model-invocation"},
    "claude": PORTABLE_FIELDS
    | {
        "when_to_use",
        "argument-hint",
        "arguments",
        "disable-model-invocation",
        "user-invocable",
        "model",
        "context",
        "agent",
    },
}
PROFILE_FIELDS["skizl"] = PROFILE_FIELDS["claude"] | {
    "version",
    "category",
    "status",
    "tags",
}

# --- Agent Plugins 1.0.0 (https://agent-plugins.org) ---
# The manifest schema is CLOSED: unknown top-level keys are a validation failure,
# so this set is exhaustive by design, not a convenience subset.
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
PLUGIN_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
PLUGIN_NAME = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
AUTHOR_FIELDS = {"name", "email", "url"}
REVERSE_DOMAIN = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)+$")
MCP_TRANSPORTS = {"stdio", "streamable-http", "sse"}
# PLUGIN_ROOT/PLUGIN_DATA expand textually in args, env values, and cwd — never in
# command, urls, or headers. Substituting them elsewhere silently ships a literal.
PLUGIN_VARS = re.compile(r"\$\{?(PLUGIN_ROOT|PLUGIN_DATA)\}?")


def validate_inline_yaml(value, line_number):
    if not value:
        return
    pairs, closing = {"[": "]", "{": "}"}, {"}", "]"}
    stack, quote, escaped, index, previous_token = [], None, False, 0, None
    top_quoted = value[0] in {'"', "'"}
    top_collection = value[0] in pairs
    while index < len(value):
        char = value[index]
        if quote:
            if quote == '"' and escaped:
                escaped = False
            elif quote == '"' and char == "\\":
                escaped = True
            elif char == quote:
                if quote == "'" and index + 1 < len(value) and value[index + 1] == "'":
                    index += 2
                    continue
                quote, previous_token = None, "quoted"
            index += 1
            continue
        quote_can_start = index == 0 or (stack and previous_token in {"[", "{", ",", ":"})
        if char in {'"', "'"} and quote_can_start:
            quote = char
        elif char in pairs:
            stack.append(pairs[char])
            previous_token = char
        elif char in closing:
            if not stack or char != stack.pop():
                raise ValueError(f"mismatched inline collection (frontmatter line {line_number})")
            previous_token = char
        elif not stack and top_collection and not char.isspace():
            raise ValueError(f"trailing content after inline collection (frontmatter line {line_number})")
        elif not stack and top_quoted and index > 0 and not char.isspace():
            raise ValueError(f"trailing content after quoted scalar (frontmatter line {line_number})")
        elif not char.isspace():
            previous_token = char if char in {",", ":"} else "plain"
        index += 1
    if quote:
        raise ValueError(f"unterminated quoted scalar (frontmatter line {line_number})")
    if stack:
        raise ValueError(f"unterminated inline collection (frontmatter line {line_number})")


def metadata_value_is_string(value):
    if len(value) >= 2 and value[0] in {'"', "'"} and value[-1] == value[0]:
        return True
    typed_plain = re.compile(
        r"^(?:null|true|false|yes|no|on|off|~|[-+]?(?:"
        r"0[xX][0-9a-fA-F_]+|0[oO][0-7_]+|0[bB][01_]+|"
        r"(?:\d[\d_]*)(?:\.\d[\d_]*)?(?:[eE][-+]?\d+)?|"
        r"\.\d[\d_]*(?:[eE][-+]?\d+)?|\.inf|\.nan)|"
        r"\d{4}-\d{2}-\d{2}(?:[Tt ][0-9:.+-]+[Zz]?)?)$",
        re.IGNORECASE,
    )
    return not typed_plain.fullmatch(value)


def md_files(root):
    for p in sorted(root.rglob("*.md")):
        parts = set(p.relative_to(root).parts[:-1])
        if parts & SKIP_DIRS or any(x.startswith("_") for x in p.relative_to(root).parts):
            continue
        yield p


def frontmatter(lines):
    if not lines or lines[0].strip() != "---":
        return None, None
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return None, None

    raw = lines[1:end]
    fields = {}
    indented_context = None
    for index, line in enumerate(raw):
        if "\t" in line:
            raise ValueError(f"tab indentation is not allowed (frontmatter line {index + 2})")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0].isspace():
            if indented_context == "block":
                continue
            if indented_context == "metadata":
                nested = re.match(r"^ +([A-Za-z][A-Za-z0-9_.-]*):\s*(.+)$", line)
                if not nested:
                    raise ValueError(f"malformed metadata mapping (frontmatter line {index + 2})")
                validate_inline_yaml(nested.group(2).strip(), index + 2)
                continue
            raise ValueError(f"unexpected indented content (frontmatter line {index + 2})")
        indented_context = None
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if not match:
            raise ValueError(f"malformed top-level YAML (frontmatter line {index + 2})")
        key, value = match.group(1), (match.group(2) or "").strip()
        if key in fields:
            raise ValueError(f"duplicate frontmatter field '{key}'")
        validate_inline_yaml(value, index + 2)
        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            indented_context = "block"
            body = []
            for continuation in raw[index + 1 :]:
                if continuation and not continuation[0].isspace():
                    break
                body.append(continuation.strip())
            value = "\n".join(body).strip()
        elif key == "metadata" and not value:
            indented_context = "metadata"
        fields[key] = value.strip('"\'')
    return fields, "\n".join(raw)


def check_mcp(root, errors, warns, plugin_schema_version):
    """Validate mcp.json against the Agent Plugins server contract."""
    mcp_path = root / "mcp.json"
    if not mcp_path.exists():
        return
    try:
        mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        errors.append(f"mcp.json: invalid JSON — {error}")
        return
    if not isinstance(mcp, dict):
        errors.append("mcp.json: top level must be an object")
        return

    schema = mcp.get("$schema")
    if schema and plugin_schema_version and schema != plugin_schema_version:
        errors.append(
            "mcp.json: $schema version must match plugin.json's "
            f"(plugin.json={plugin_schema_version}, mcp.json={schema})"
        )

    servers = mcp.get("mcpServers")
    if servers is None:
        warns.append("mcp.json: no 'mcpServers' object — file has no effect")
        return
    if not isinstance(servers, dict):
        errors.append("mcp.json: 'mcpServers' must be an object")
        return

    for server_name, config in sorted(servers.items()):
        label = f"mcp.json: server '{server_name}'"
        if not isinstance(config, dict):
            errors.append(f"{label}: entry must be an object")
            continue
        transport = config.get("type")
        if not transport:
            errors.append(f"{label}: missing required 'type' — transport must be declared explicitly")
        elif transport not in MCP_TRANSPORTS:
            errors.append(
                f"{label}: unknown type '{transport}' — expected one of {', '.join(sorted(MCP_TRANSPORTS))}"
            )
        elif transport == "sse":
            warns.append(f"{label}: 'sse' is the deprecated HTTP+SSE transport — prefer 'streamable-http'")

        if transport == "stdio" and not config.get("command"):
            errors.append(f"{label}: stdio transport requires 'command'")
        if transport in {"streamable-http", "sse"} and not config.get("url"):
            errors.append(f"{label}: {transport} transport requires 'url'")

        # Plugin variables expand ONLY in args, env values, and cwd.
        for field in ("command", "url"):
            value = config.get(field)
            if isinstance(value, str) and PLUGIN_VARS.search(value):
                errors.append(
                    f"{label}: PLUGIN_ROOT/PLUGIN_DATA do not expand in '{field}' — "
                    "they ship as a literal string"
                )
        headers = config.get("headers")
        if isinstance(headers, dict):
            for key, value in headers.items():
                if isinstance(value, str) and PLUGIN_VARS.search(value):
                    errors.append(
                        f"{label}: PLUGIN_ROOT/PLUGIN_DATA do not expand in headers['{key}'] — "
                        "they ship as a literal string"
                    )


def check_plugin(plugin_dir, profile):
    """Validate an Agent Plugins 1.0.0 plugin root, then each discovered skill.

    Failure isolation mirrors the spec: a fatal manifest error rejects the plugin,
    but one invalid skill or server never disables the others.
    """
    root = Path(plugin_dir).resolve()
    errors, warns = [], []

    manifest_path = root / "plugin.json"
    if not manifest_path.exists():
        print(f"ERROR: {root}/plugin.json missing — an Agent Plugin requires a root manifest")
        print(f"\n{root.name}: 1 error(s), 0 warning(s)")
        return 1
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        print(f"ERROR: plugin.json: invalid JSON — {error}")
        print(f"\n{root.name}: 1 error(s), 0 warning(s)")
        return 1
    if not isinstance(manifest, dict):
        print("ERROR: plugin.json: top level must be an object")
        print(f"\n{root.name}: 1 error(s), 0 warning(s)")
        return 1

    schema = manifest.get("$schema")
    if not schema:
        errors.append("plugin.json: required '$schema' is missing")
    elif schema != PLUGIN_SCHEMA:
        errors.append(f"plugin.json: $schema must be {PLUGIN_SCHEMA} (found '{schema}')")

    name = manifest.get("name")
    if not name:
        errors.append("plugin.json: required 'name' is missing")
    elif not isinstance(name, str):
        errors.append("plugin.json: 'name' must be a string")
    else:
        if not 1 <= len(name) <= 64:
            errors.append(f"plugin.json: name is {len(name)} characters; must be 1-64")
        if not PLUGIN_NAME.fullmatch(name):
            errors.append(
                "plugin.json: name must be lowercase alphanumeric with hyphens or periods, "
                "no leading/trailing separator and no '--' or '..' runs"
            )

    unknown = sorted(set(manifest) - PLUGIN_FIELDS)
    if unknown:
        errors.append(
            f"plugin.json: unknown top-level fields (schema is closed): {', '.join(unknown)}"
        )

    author = manifest.get("author")
    if author is not None:
        if not isinstance(author, dict):
            errors.append("plugin.json: 'author' must be an object")
        else:
            extra = sorted(set(author) - AUTHOR_FIELDS)
            if extra:
                errors.append(f"plugin.json: 'author' allows only name/email/url; found {', '.join(extra)}")

    keywords = manifest.get("keywords")
    if keywords is not None and (
        not isinstance(keywords, list) or not all(isinstance(k, str) for k in keywords)
    ):
        errors.append("plugin.json: 'keywords' must be an array of strings")

    extensions = manifest.get("extensions")
    if extensions is not None:
        if not isinstance(extensions, dict):
            errors.append("plugin.json: 'extensions' must be an object")
        else:
            for key, value in sorted(extensions.items()):
                if not REVERSE_DOMAIN.fullmatch(key):
                    errors.append(
                        f"plugin.json: extension key '{key}' must be a reverse-domain "
                        "namespace (e.g. com.example.client)"
                    )
                if not isinstance(value, dict):
                    errors.append(f"plugin.json: extension '{key}' must be an object")

    check_mcp(root, errors, warns, schema if isinstance(schema, str) else None)

    # --- skills: immediate children of skills/ holding a SKILL.md ---
    skills_dir = root / "skills"
    discovered = []
    if not skills_dir.is_dir():
        warns.append("skills/: no skills directory — plugin ships no Agent Skills")
    else:
        for child in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            if (child / "SKILL.md").exists():
                discovered.append(child)
            else:
                warns.append(
                    f"skills/{child.name}/: no SKILL.md — not discovered as a skill "
                    "(clients do not recurse deeper)"
                )
        if not discovered:
            warns.append("skills/: no discoverable skills (each needs an immediate-child SKILL.md)")

    for e in errors:
        print(f"ERROR: {e}")
    for w in warns:
        print(f"warn:  {w}")
    print(f"\n{root.name} [plugin]: {len(errors)} error(s), {len(warns)} warning(s)")

    # Skills validate independently — one failure never disables the others.
    failed = []
    for skill in discovered:
        print(f"\n── skills/{skill.name}")
        if main(str(skill), profile) != 0:
            failed.append(skill.name)
    if failed:
        print(f"\nskills with errors: {', '.join(failed)}")
    return 1 if errors or failed else 0


def main(skill_dir, profile):
    root = Path(skill_dir).resolve()
    errors, warns = [], []

    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        print(f"ERROR: {root}/SKILL.md missing")
        return 1
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()

    # --- frontmatter ---
    parse_failed = False
    try:
        fields, fm = frontmatter(lines)
    except ValueError as error:
        errors.append(f"SKILL.md: invalid frontmatter — {error}")
        fields, fm = {}, ""
        parse_failed = True
    if fields is None:
        errors.append("SKILL.md: no frontmatter block")
        fields, fm = {}, ""

    name = fields.get("name", "")
    description = fields.get("description", "")
    for field_name in ("name", "description", "compatibility"):
        value = fields.get(field_name, "")
        if value.startswith(("[", "{")) or value in {"true", "false", "null", "~"}:
            errors.append(f"SKILL.md: '{field_name}' must be a string")
    if not parse_failed:
        if not name:
            errors.append("SKILL.md: required 'name' is missing")
        elif len(name) > 64 or not NAME.fullmatch(name):
            errors.append("SKILL.md: name must be 1-64 lowercase letters/digits/hyphens without edge or repeated hyphens")
        elif name != root.name:
            errors.append(f"SKILL.md: name '{name}' must match parent directory '{root.name}'")
        if not description:
            errors.append("SKILL.md: required 'description' is missing or empty")
        elif len(description) > 1024:
            errors.append(f"SKILL.md: description is {len(description)} characters; maximum is 1024")
    metadata_lines = []
    in_metadata = False
    for line in fm.splitlines():
        if line == "metadata:":
            in_metadata = True
            continue
        if in_metadata and line and not line[0].isspace():
            break
        if in_metadata and line.strip():
            metadata_lines.append(line.strip())
    for line in metadata_lines:
        if ":" not in line:
            errors.append("SKILL.md: metadata must be a string-to-string mapping")
            continue
        value = line.split(":", 1)[1].strip()
        if not value or value.startswith(("[", "{")) or not metadata_value_is_string(value):
            errors.append("SKILL.md: metadata values must be non-empty strings")
    compatibility = fields.get("compatibility", "")
    if compatibility and len(compatibility) > 500:
        errors.append(f"SKILL.md: compatibility is {len(compatibility)} characters; maximum is 500")

    unknown = sorted(set(fields) - PROFILE_FIELDS[profile])
    if unknown:
        errors.append(f"SKILL.md: fields unsupported by {profile} profile: {', '.join(unknown)}")
    if profile == "portable" and "allowed-tools" in fields:
        warns.append("SKILL.md: allowed-tools is experimental and may not work across hosts")
    if profile == "codex" and (root / "agents" / "openai.yaml").exists():
        warns.append("agents/openai.yaml: Codex sidecar detected; validate UI, policy, and dependency values separately")

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
    parser = argparse.ArgumentParser(
        description="Mechanically validate an Agent Skill folder, or an Agent Plugins root with --plugin."
    )
    parser.add_argument("skill_dir", help="skill folder, or plugin root when --plugin is set")
    parser.add_argument("--profile", choices=sorted(PROFILE_FIELDS), default="portable")
    parser.add_argument(
        "--plugin",
        action="store_true",
        help="validate the target as an Agent Plugins 1.0.0 plugin root (manifest, mcp.json, skills/)",
    )
    args = parser.parse_args()
    if args.plugin:
        raise SystemExit(check_plugin(args.skill_dir, args.profile))
    raise SystemExit(main(args.skill_dir, args.profile))
