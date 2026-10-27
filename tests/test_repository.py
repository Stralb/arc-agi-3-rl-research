"""Offline tests for the lecturer-facing ARC-AGI-3 repository."""
from pathlib import Path
import json
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

def run(relative):
    return subprocess.run([sys.executable, str(ROOT / relative)], cwd=ROOT,
                          capture_output=True, text=True)

class RepositoryTests(unittest.TestCase):
    def test_original_baseline_evidence(self):
        p = run("scripts/verify_repository.py")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_e126_release(self):
        p = run("scripts/verify_e126_release.py")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_summary_mentions_all_versions(self):
        p = run("scripts/summarize_results.py")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        for term in ("N093:", "N117:", "E126 seed 76:", "hybrid=16", "not private Kaggle"):
            self.assertIn(term, p.stdout)

    def test_readme_and_results_links(self):
        for md in ROOT.rglob("*.md"):
            for link in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", md.read_text(encoding="utf-8")):
                target = link.split("#", 1)[0].split("?", 1)[0].strip("<>")
                if not target or target.startswith(("http://", "https://", "mailto:", "/", "#")):
                    continue
                destination = (md.parent / target).resolve()
                self.assertTrue(destination.is_relative_to(ROOT.resolve()), target)
                self.assertTrue(destination.exists(), f"Broken link: {md.relative_to(ROOT)} -> {target}")

    def test_notebooks(self):
        notebooks = list((ROOT / "notebooks").glob("*.ipynb"))
        self.assertEqual(len(notebooks), 1)
        nb = json.loads(notebooks[0].read_text(encoding="utf-8"))
        self.assertEqual(nb["nbformat"], 4)

    def test_plots(self):
        images = list((ROOT / "results/plots").glob("*.svg"))
        self.assertGreaterEqual(len(images), 4)
        for file in images:
            self.assertTrue(ET.parse(file).getroot().tag.endswith("svg"), str(file))

    def test_archive_not_cluttering_main(self):
        for historical in ("experiments", "reports", "data", "docs"):
            self.assertFalse((ROOT / historical).exists(), historical)
        self.assertIn("archive/full-research-2026-10-27", (ROOT / "README.md").read_text())

if __name__ == "__main__":
    unittest.main()
