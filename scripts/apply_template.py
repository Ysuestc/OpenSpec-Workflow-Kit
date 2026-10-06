#!/usr/bin/env python3
"""Preview or apply the explicit workflow payload without overwriting files."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import os
import stat
import sys

KIT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_FILES = (
    "AGENTS.md",
    "docs/project-context.md",
    "docs/workflow.md",
    "docs/lessons.md",
    ".agents/skills/openspec-workflow/SKILL.md",
    ".agents/roles/coordinator.md",
    ".agents/roles/designer.md",
    ".agents/roles/spec-reviewer.md",
    ".agents/roles/implementer.md",
    ".agents/roles/code-reviewer.md",
    ".agents/roles/verifier-archiver.md",
    "openspec/config.yaml",
    "openspec/schemas/workflow-spec-driven/schema.yaml",
    "openspec/schemas/workflow-spec-driven/templates/proposal.md",
    "openspec/schemas/workflow-spec-driven/templates/spec.md",
    "openspec/schemas/workflow-spec-driven/templates/design.md",
    "openspec/schemas/workflow-spec-driven/templates/tasks.md",
    "openspec/schemas/workflow-spec-driven/templates/processing/status.md",
    "openspec/schemas/workflow-spec-driven/templates/processing/spec-review.md",
    "openspec/schemas/workflow-spec-driven/templates/processing/code-review.md",
    "openspec/schemas/workflow-spec-driven/templates/processing/verification.md",
)
MANIFEST = {name: name for name in WORKFLOW_FILES}
MANIFEST["docs/workflow-kit-LICENSE"] = "LICENSE"
EMPTY_DIRECTORIES = ("openspec/specs", "openspec/changes")


class TemplateError(ValueError):
    """A deterministic preflight failure; the destination has not been changed."""


@dataclass(frozen=True)
class Entry:
    relative: str
    status: str
    content: bytes | None = None
    reason: str = ""
    directory: bool = False


def is_linked(path: Path) -> bool:
    """Treat Windows junctions/reparse points like symbolic links."""
    if path.is_symlink():
        return True
    try:
        attributes = path.lstat().st_file_attributes
    except (FileNotFoundError, AttributeError):
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def path_conflict(destination: Path, relative: str, *, directory: bool = False) -> str:
    """Reject symlinks, non-directory parents and incompatible leaf types."""
    parts = Path(relative).parts
    current = destination
    if is_linked(current):
        return "destination is a symlink"
    if current.exists() and not current.is_dir():
        return "destination is not a directory"
    for index, part in enumerate(parts):
        current = current / part
        leaf = index == len(parts) - 1
        if is_linked(current):
            return "symlink on output path"
        if not current.exists():
            continue
        if not leaf or directory:
            if not current.is_dir():
                return "expected directory"
        elif not current.is_file():
            return "expected regular file"
    return ""


def plan_template(
    destination: Path, exclusions: set[str], source: Path = KIT_ROOT
) -> tuple[Path, list[Entry]]:
    source = source.resolve()
    destination = Path(os.path.abspath(destination.expanduser()))
    if destination.resolve().is_relative_to(source):
        raise TemplateError("Destination must be outside the kit source.")
    unknown = exclusions - MANIFEST.keys()
    if unknown:
        raise TemplateError("Unknown exclusion: " + ", ".join(sorted(unknown)))

    entries: list[Entry] = []
    for relative, source_relative in MANIFEST.items():
        if relative in exclusions:
            entries.append(Entry(relative, "EXCLUDED"))
            continue
        source_path = source / source_relative
        if is_linked(source_path) or not source_path.is_file():
            raise TemplateError("Missing or linked source file: " + source_relative)
        if not source_path.resolve().is_relative_to(source):
            raise TemplateError("Source path escapes the kit: " + source_relative)
        content = source_path.read_bytes()
        reason = path_conflict(destination, relative)
        target = destination / relative
        if reason:
            entries.append(Entry(relative, "CONFLICT", reason=reason))
        elif target.exists():
            if target.read_bytes() == content:
                entries.append(Entry(relative, "SAME"))
            else:
                entries.append(Entry(relative, "CONFLICT", reason="different content"))
        else:
            entries.append(Entry(relative, "CREATE", content=content))

    for relative in EMPTY_DIRECTORIES:
        reason = path_conflict(destination, relative, directory=True)
        status = "CONFLICT" if reason else ("SAME" if (destination / relative).exists() else "CREATE")
        entries.append(Entry(relative, status, reason=reason, directory=True))
    return destination, entries


def apply_plan(destination: Path, entries: list[Entry]) -> None:
    if any(entry.status == "CONFLICT" for entry in entries):
        raise TemplateError("Conflicts found; nothing was written.")
    # Preflight the complete plan once more before the first write. This does not
    # provide a concurrency lock: callers must not modify the destination mid-run.
    for entry in entries:
        if entry.status != "CREATE":
            continue
        reason = path_conflict(destination, entry.relative, directory=entry.directory)
        if reason or (destination / entry.relative).exists():
            raise TemplateError("Destination changed after preflight: " + entry.relative)
    for entry in entries:
        if entry.status != "CREATE":
            continue
        target = destination / entry.relative
        if entry.directory:
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            # Exclusive creation avoids truncating a file created by another process.
            with target.open("xb") as stream:
                stream.write(entry.content)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="target project directory")
    parser.add_argument("--apply", action="store_true", help="write after conflict-free preflight")
    parser.add_argument("--exclude", action="append", default=[], metavar="PATH",
                        help="skip an exact output path after manual integration; repeatable")
    args = parser.parse_args(argv)
    try:
        destination, entries = plan_template(args.destination, set(args.exclude))
        print(("APPLY" if args.apply else "PREVIEW") + ": " + str(destination))
        for entry in entries:
            suffix = " (" + entry.reason + ")" if entry.reason else ""
            print(entry.status + " " + entry.relative + suffix)
        if any(entry.status == "CONFLICT" for entry in entries):
            raise TemplateError("Conflicts found; nothing was written.")
        if args.apply:
            apply_plan(destination, entries)
            print("Applied workflow files; no Git or agent actions were performed.")
        else:
            print("Preview only; use --apply after reviewing the plan.")
        return 0
    except (TemplateError, OSError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
