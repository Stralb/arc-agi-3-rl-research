"""Standard-library tests for the public, non-privileged repository subset."""
from pathlib import Path
import csv
import json
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class PublishedRepoTests(unittest.TestCase):
    def test_offline_integrity(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/verify_repository.py")],
            cwd=ROOT, capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_public_game_count(self):
        with (ROOT / "data/outputs/benchmarks/n114_public25_matrix.csv").open(newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 25)
        self.assertEqual(sum(int(r["l2"]) for r in rows), 1)
        self.assertEqual(sum(int(r["l3plus"]) for r in rows), 0)

    def test_frozen_baseline_is_separate(self):
        base = ROOT / "src/baselines/frozen_n093.py"
        candidate = ROOT / "src/best_public_agent.py"
        self.assertTrue(base.exists() and candidate.exists())
        self.assertNotEqual(base.read_bytes(), candidate.read_bytes())

    def test_notebooks_parse(self):
        for name in ("frozen_n093_submission.ipynb", "local_effect_best_public.ipynb"):
            data = json.loads((ROOT / "notebooks" / name).read_text())
            self.assertEqual(data["nbformat"], 4)

    def test_local_markdown_links_resolve(self):
        import re
        for md in ROOT.rglob("*.md"):
            source = md.read_text(encoding="utf-8")
            for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", source):
                relative = target.split("#", 1)[0].split("?", 1)[0].strip("<>")
                if not relative or relative.startswith(("http://", "https://", "mailto:", "/", "#")):
                    continue
                resolved = (md.parent / relative).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT.resolve()), f"Outside repository: {md}: {target}")
                self.assertTrue(resolved.exists(), f"Broken relative link: {md}: {target}")

    def test_e126_release_integrity(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/verify_e126_release.py")],
            cwd=ROOT, capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_summary_includes_the_versioned_e126_result(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/summarize_results.py")],
            cwd=ROOT, capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("E126 policy seed 76:", result.stdout)
        self.assertIn("hybrid=16 levels", result.stdout)

    def test_svg_plots_parse(self):
        plots = sorted((ROOT / "data/outputs/plots").glob("*.svg"))
        self.assertGreaterEqual(len(plots), 5)
        for path in plots:
            root = ET.parse(path).getroot()
            self.assertTrue(root.tag.endswith("svg"), path)

if __name__ == "__main__":
    unittest.main()
