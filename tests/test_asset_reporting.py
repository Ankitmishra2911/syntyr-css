"""Deterministic, size-only diagnostics — no arbitrary gzip ceilings."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AssetReportContract(unittest.TestCase):
    def test_report_accounts_for_all_generated_distributions(self):
        from scripts.asset_report import measure_distributions
        from scripts.build import distributions

        report = measure_distributions(ROOT / "dist")
        self.assertEqual(set(report), set(distributions()))
        for filename, stats in report.items():
            with self.subTest(filename=filename):
                self.assertEqual(stats["raw_bytes"], (ROOT / "dist" / filename).stat().st_size)
                self.assertGreater(stats["gzip_bytes"], 0)
                self.assertGreater(stats["raw_bytes"], stats["gzip_bytes"])
                self.assertLessEqual(stats["gzip_bytes"], stats["raw_bytes"])
                self.assertEqual(stats["sources"], list(distributions()[filename]))

    def test_report_supports_optional_json_baseline_without_failing_growth(self):
        from scripts.asset_report import compare_reports, measure_distributions
        now = measure_distributions(ROOT / "dist")
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "baseline.json"
            baseline = {"distributions": {
                "syntyr.core.css": {"gzip_bytes": 10, "raw_bytes": 10}
            }}
            path.write_text(json.dumps(baseline), encoding="utf-8")
            changes = compare_reports(now, json.loads(path.read_text())["distributions"])
            self.assertEqual(changes["syntyr.core.css"]["gzip_bytes_delta"],
                             now["syntyr.core.css"]["gzip_bytes"] - 10)
            self.assertNotIn("syntyr.semantic.css", changes)

    def test_report_serializes_reproducibly(self):
        from scripts.asset_report import measure_distributions, render_report
        data = measure_distributions(ROOT / "dist")
        one = render_report(data, as_json=True)
        self.assertEqual(one, render_report(data, as_json=True))
        parsed = json.loads(one)
        self.assertIn("syntyr.all.css", parsed["distributions"])
        self.assertNotIn("budget", one.lower())


if __name__ == "__main__":
    unittest.main()
