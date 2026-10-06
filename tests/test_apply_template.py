"""Observable application guarantees, including unchanged existing projects."""
from __future__ import annotations

from pathlib import Path
import os
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from apply_template import KIT_ROOT, MANIFEST, TemplateError, apply_plan, plan_template


class ApplyTemplateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory(prefix="workflow-kit-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.destination = self.base / "project"

    def apply(self, exclusions=None):
        destination, entries = plan_template(self.destination, set(exclusions or []))
        apply_plan(destination, entries)
        return entries

    def test_cli_default_preview_creates_nothing(self):
        result = subprocess.run(
            [sys.executable, str(KIT_ROOT / "scripts/apply_template.py"), str(self.destination)],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PREVIEW", result.stdout)
        self.assertFalse(self.destination.exists())

    def test_export_has_only_payload_and_empty_spec_directories(self):
        self.apply()
        actual = {path.relative_to(self.destination).as_posix()
                  for path in self.destination.rglob("*") if path.is_file()}
        self.assertEqual(actual, set(MANIFEST))
        self.assertEqual(list((self.destination / "openspec/changes").iterdir()), [])
        self.assertEqual(list((self.destination / "openspec/specs").iterdir()), [])
        self.assertFalse((self.destination / "LICENSE").exists())
        self.assertEqual((self.destination / "docs/workflow-kit-LICENSE").read_bytes(),
                         (KIT_ROOT / "LICENSE").read_bytes())

    def test_conflict_stops_all_writes_and_preserves_existing_content(self):
        self.destination.mkdir()
        target = self.destination / "AGENTS.md"
        target.write_text("Existing project rules\n", encoding="utf-8")
        destination, entries = plan_template(self.destination, set())
        with self.assertRaises(TemplateError):
            apply_plan(destination, entries)
        self.assertEqual(target.read_text(encoding="utf-8"), "Existing project rules\n")
        self.assertEqual({path.name for path in self.destination.iterdir()}, {"AGENTS.md"})

    def test_late_manifest_conflict_also_stops_all_writes(self):
        target = self.destination / "docs/workflow-kit-LICENSE"
        target.parent.mkdir(parents=True)
        target.write_text("Existing notice", encoding="utf-8")
        destination, entries = plan_template(self.destination, set())
        with self.assertRaises(TemplateError):
            apply_plan(destination, entries)
        self.assertFalse((self.destination / "AGENTS.md").exists())
        self.assertEqual(target.read_text(encoding="utf-8"), "Existing notice")

    def test_existing_readme_license_and_git_configuration_are_preserved(self):
        self.destination.mkdir()
        for name in ("README.md", "LICENSE"):
            (self.destination / name).write_text("Project content: " + name, encoding="utf-8")
        git = self.destination / ".git"
        git.mkdir()
        (git / "config").write_text("Existing remote", encoding="utf-8")
        self.apply()
        self.assertEqual((self.destination / "LICENSE").read_text(), "Project content: LICENSE")
        self.assertEqual((self.destination / "README.md").read_text(), "Project content: README.md")
        self.assertEqual((git / "config").read_text(), "Existing remote")

    def test_repeat_apply_keeps_file_content_and_modification_times(self):
        self.apply()
        before = {path: (path.read_bytes(), path.stat().st_mtime_ns)
                  for path in self.destination.rglob("*") if path.is_file()}
        entries = self.apply()
        self.assertTrue(all(entry.status == "SAME" for entry in entries))
        for path, state in before.items():
            self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns), state)

    def test_exact_exclusion_preserves_manual_merge_and_applies_others(self):
        self.destination.mkdir()
        (self.destination / "AGENTS.md").write_text("Merged rules", encoding="utf-8")
        self.apply({"AGENTS.md"})
        self.assertEqual((self.destination / "AGENTS.md").read_text(), "Merged rules")
        self.assertTrue((self.destination / "openspec/config.yaml").is_file())

    def test_unknown_exclusion_is_rejected_without_write(self):
        with self.assertRaises(TemplateError):
            plan_template(self.destination, {"../AGENTS.md"})
        self.assertFalse(self.destination.exists())

    def test_source_and_nested_destination_are_rejected(self):
        for destination in (KIT_ROOT, KIT_ROOT / "new-project"):
            with self.subTest(destination=destination), self.assertRaises(TemplateError):
                plan_template(destination, set())
        self.assertFalse((KIT_ROOT / "new-project").exists())

    def test_directory_in_place_of_output_file_blocks_every_write(self):
        (self.destination / "AGENTS.md").mkdir(parents=True)
        destination, entries = plan_template(self.destination, set())
        with self.assertRaises(TemplateError):
            apply_plan(destination, entries)
        self.assertEqual({path.name for path in self.destination.iterdir()}, {"AGENTS.md"})

    def test_file_in_place_of_parent_directory_blocks_every_write(self):
        self.destination.mkdir()
        (self.destination / "docs").write_text("Must stay", encoding="utf-8")
        destination, entries = plan_template(self.destination, set())
        with self.assertRaises(TemplateError):
            apply_plan(destination, entries)
        self.assertFalse((self.destination / "AGENTS.md").exists())
        self.assertEqual((self.destination / "docs").read_text(), "Must stay")

    def test_symlink_parent_cannot_write_outside_destination(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.destination.mkdir()
        try:
            (self.destination / "docs").symlink_to(outside, target_is_directory=True)
        except OSError as error:
            self.skipTest("Symlink creation unavailable: " + str(error))
        destination, entries = plan_template(self.destination, set())
        with self.assertRaises(TemplateError):
            apply_plan(destination, entries)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.destination / "AGENTS.md").exists())

    @unittest.skipUnless(os.name == "nt", "Windows junction behavior")
    def test_windows_junction_parent_cannot_escape_destination(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.destination.mkdir()
        environment = dict(os.environ, WORKFLOW_KIT_LINK=str(self.destination / "docs"),
                           WORKFLOW_KIT_TARGET=str(outside))
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
             "$ErrorActionPreference = 'Stop'; New-Item -ItemType Junction "
             "-Path $env:WORKFLOW_KIT_LINK -Target $env:WORKFLOW_KIT_TARGET | Out-Null"],
            env=environment, capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if result.returncode:
            self.skipTest("Junction creation unavailable: " + result.stderr)
        destination, entries = plan_template(self.destination, set())
        with self.assertRaises(TemplateError):
            apply_plan(destination, entries)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.destination / "AGENTS.md").exists())

    def test_new_conflict_after_preview_is_not_overwritten(self):
        destination, entries = plan_template(self.destination, set())
        self.destination.mkdir()
        (self.destination / "AGENTS.md").write_text("Changed since preview", encoding="utf-8")
        with self.assertRaises(TemplateError):
            apply_plan(destination, entries)
        self.assertEqual((self.destination / "AGENTS.md").read_text(), "Changed since preview")
        self.assertFalse((self.destination / "openspec").exists())


if __name__ == "__main__":
    unittest.main()
