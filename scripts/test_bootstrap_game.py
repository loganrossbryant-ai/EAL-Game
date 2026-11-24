#!/usr/bin/env python3
"""Read-only safety tests for the new-title scaffold."""
from pathlib import Path
import tempfile
import unittest

from bootstrap_game import bootstrap_game, COPIES

class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        t = self.root / "studio/templates"
        t.mkdir(parents=True)
        for src in COPIES:
            (t / src).write_text("template\n", encoding="utf-8")

    def test_school_scaffold(self):
        d = bootstrap_game(self.root, "new-world", "New World", "school")
        self.assertEqual(d, self.root / "games/new-world")
        self.assertTrue((d / "DESIGN_BRIEF.md").is_file())
        self.assertIn("NO APPROVED REUSABLE ENGINE", (d/"README.md").read_text())

    def test_tutoring_scaffold(self):
        d = bootstrap_game(self.root, "beginner-world", "Beginner World", "tutoring")
        self.assertIn("tutoring-games/games", str(d))
        self.assertTrue((d / "AUDIO_LINE_MANIFEST.csv").is_file())

    def test_never_overwrite(self):
        bootstrap_game(self.root, "already", "Already", "school")
        with self.assertRaises(FileExistsError):
            bootstrap_game(self.root, "already", "Replacement", "school")

    def test_reject_bad_slug(self):
        for value in ("../private", "Upper", "bad name", "--", "", "file/other"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                bootstrap_game(self.root, value, "Game", "school")
        self.assertFalse((self.root / "games").exists())

if __name__ == "__main__":
    unittest.main()
