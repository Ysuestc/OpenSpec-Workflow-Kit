#!/usr/bin/env python3
"""Validate schema integrity, skill metadata, templates and local references."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys

import yaml

from apply_template import EMPTY_DIRECTORIES, KIT_ROOT, MANIFEST

LINK = re.compile(r"\[[^\]\n]*\]\(([^)\n]+)\)")
IGNORED = {".git", ".venv", "venv", "node_modules", "__pycache__", ".workflow-kit-cache"}


def anchors(text: str) -> set[str]:
    result: set[str] = set()
    seen: Counter[str] = Counter()
    for match in re.finditer(r"^#{1,6}\s+(.+)$", text, re.MULTILINE):
        heading = match.group(1).rstrip("#").strip().lower()
        slug = re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")
        index = seen[slug]
        seen[slug] += 1
        result.add(slug if index == 0 else slug + "-" + str(index))
    return result


def local_links(path: Path) -> list[tuple[Path, str]]:
    references = []
    for match in LINK.finditer(path.read_text(encoding="utf-8")):
        value = match.group(1).strip().strip("<>")
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", value):
            continue
        relative, _, anchor = value.partition("#")
        references.append(((path.parent / relative).resolve() if relative else path.resolve(), anchor))
    return references


def validate() -> tuple[list[str], int, int]:
    errors: list[str] = []
    schema_dir = KIT_ROOT / "openspec/schemas/workflow-spec-driven"
    schema = yaml.safe_load((schema_dir / "schema.yaml").read_text(encoding="utf-8"))
    config = yaml.safe_load((KIT_ROOT / "openspec/config.yaml").read_text(encoding="utf-8"))
    if schema.get("name") != schema_dir.name or config.get("schema") != schema.get("name"):
        errors.append("Schema/config names do not match the local directory.")
    artifacts = schema.get("artifacts", [])
    identifiers = [item.get("id") for item in artifacts]
    if len(identifiers) != len(set(identifiers)) or any(not value for value in identifiers):
        errors.append("Artifact IDs must be unique and nonempty.")
    dependencies = {item["id"]: item.get("requires", []) for item in artifacts}
    for item in artifacts:
        template = (schema_dir / "templates" / item.get("template", "")).resolve()
        if not template.is_relative_to(schema_dir) or not template.is_file():
            errors.append("Missing or unsafe artifact template: " + item["id"])
        if not item.get("generates") or not item.get("instruction"):
            errors.append("Missing artifact generation/instructions: " + item["id"])
        if any(name not in identifiers for name in item.get("requires", [])):
            errors.append("Unknown dependency: " + item["id"])
    pending = dict(dependencies)
    completed: set[str] = set()
    while pending:
        ready = [name for name, required in pending.items() if set(required) <= completed]
        if not ready:
            errors.append("Artifact dependency graph is cyclic or invalid.")
            break
        for name in ready:
            completed.add(name)
            del pending[name]
    if set(config.get("rules", {})) - set(identifiers):
        errors.append("Config rules refer to unknown artifacts.")
    if set(schema.get("apply", {}).get("requires", [])) - set(identifiers):
        errors.append("Apply refers to unknown artifacts.")

    skill = KIT_ROOT / ".agents/skills/openspec-workflow/SKILL.md"
    text = skill.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    metadata = yaml.safe_load(match.group(1)) if match else {}
    if metadata.get("name") != skill.parent.name or not metadata.get("description"):
        errors.append("Skill frontmatter needs a matching name and description.")

    paths = [path for path in KIT_ROOT.rglob("*.md")
             if not any(part in IGNORED for part in path.relative_to(KIT_ROOT).parts)]
    link_count = 0
    for path in paths:
        for target, anchor in local_links(path):
            link_count += 1
            if not target.is_relative_to(KIT_ROOT) or not target.exists():
                errors.append(str(path.relative_to(KIT_ROOT)) + ": missing local reference " + str(target))
            elif anchor and target.is_file() and anchor not in anchors(target.read_text(encoding="utf-8")):
                errors.append(str(path.relative_to(KIT_ROOT)) + ": missing anchor " + anchor)

    outputs = set(MANIFEST)
    for output, source in MANIFEST.items():
        path = KIT_ROOT / source
        if not path.is_file():
            errors.append("Missing payload source: " + source)
            continue
        if path.suffix != ".md":
            continue
        for target, _ in local_links(path):
            if not target.is_relative_to(KIT_ROOT):
                continue
            reference = target.relative_to(KIT_ROOT).as_posix()
            if reference not in outputs and reference not in EMPTY_DIRECTORIES and not any(
                name.startswith(reference.rstrip("/") + "/") for name in outputs
            ):
                errors.append(output + ": reference is not in exported payload: " + reference)
    return errors, len(paths), link_count


def main() -> int:
    try:
        errors, documents, links = validate()
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print("ERROR: " + error, file=sys.stderr)
        return 1
    print(f"PASS: schema, skill, payload closure, {documents} Markdown files and {links} local links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
