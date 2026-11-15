"""Offline, reproducible browser benchmark contracts (stdlib tests)."""
from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/perf_benchmark.py"


def load_script():
    spec = importlib.util.spec_from_file_location("syntyr_perf_benchmark", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PerformanceBenchmarkContract(unittest.TestCase):
    def test_dashboard_and_table_have_comparable_dom_for_render_deferral(self):
        tool = load_script()
        for kind in ("dashboard", "long-table"):
            with self.subTest(kind=kind):
                css = "/* inline local CSS */"
                plain = tool.make_fixture(css, kind=kind, rows=90, sections=6, deferred=False)
                deferred = tool.make_fixture(css, kind=kind, rows=90, sections=6, deferred=True)
                self.assertIn(css, plain)
                self.assertIn(css, deferred)
                self.assertIn('<main', plain)
                self.assertIn('<table', plain)
                self.assertEqual(plain.count("<tr"), deferred.count("<tr"))
                self.assertEqual(plain.count("<article"), deferred.count("<article"))
                self.assertNotIn("syn-defer-section", plain)
                self.assertIn("syn-defer-section", deferred)
                self.assertNotIn("http://", deferred)
                self.assertNotIn("https://", deferred)
                self.assertNotIn("<script", deferred)
                self.assertEqual(plain.count('data-syn-fixture='), 1)
                self.assertIn('class="syn-root syn-page"', deferred)

    def test_browser_variants_rotate_to_reduce_order_bias(self):
        tool = load_script()
        cases = ["standard", "deferred"]
        self.assertEqual(tool.trial_order(cases, 0), cases)
        self.assertEqual(tool.trial_order(cases, 1), cases[::-1])
        self.assertEqual(tool.trial_order(cases, 2), cases)

    def test_metrics_report_median_none_for_unsupported_timings_and_includes_context(self):
        tool = load_script()
        samples = {"standard": [
            {"navigation_ms": 60, "fcp_ms": None, "lcp_ms": 30, "cls": 0, "style_recalc_ms": None, "layout_ms": None, "paint_ms": None},
            {"navigation_ms": 20, "fcp_ms": 18, "lcp_ms": 20, "cls": 0, "style_recalc_ms": None, "layout_ms": None, "paint_ms": None},
            {"navigation_ms": 40, "fcp_ms": 28, "lcp_ms": 25, "cls": 0, "style_recalc_ms": None, "layout_ms": None, "paint_ms": None},
        ]}
        report = tool.summarize(samples, browser="webkit", viewport="mobile", fixture="long-table", runs=3, rows=90, sections=6)
        self.assertEqual(report["results"]["standard"]["navigation_ms"], 40)
        self.assertEqual(report["results"]["standard"]["fcp_ms"], 23)
        self.assertEqual(report["results"]["standard"]["style_recalc_ms"], None)
        self.assertEqual(report["browser"], "webkit")
        self.assertEqual(report["viewport"], "mobile")
        self.assertEqual(report["fixture"]["kind"], "long-table")
        self.assertIn("limitations", report)
        self.assertNotIn("real_user_inp", report)
        self.assertIn("scroll_reveal_ms", report["results"]["standard"])
        self.assertIn("scroll_cls", report["results"]["standard"])

    def test_pending_observer_entries_are_flushed_at_every_snapshot(self):
        tool = load_script()
        from inspect import getsource
        source = getsource(tool.sample)
        self.assertIn("takeRecords()", tool.INIT_JS)
        self.assertIn("state.flush = () =>", tool.INIT_JS)
        self.assertGreaterEqual(source.count("flush?.()"), 3)

    def test_unsupported_layout_shift_is_not_reported_as_zero(self):
        tool = load_script()
        self.assertIn("cls: null", tool.INIT_JS)
        self.assertIn("PerformanceObserver.supportedEntryTypes", tool.INIT_JS)

    def test_user_guide_explains_benchmark_and_limits(self):
        guide = (ROOT / "docs/performance-and-polish.md").read_text()
        for text in ("scripts/perf_benchmark.py", "scroll", "real-user",
                     "Playwright", "Chrome", "WebKit"):
            self.assertIn(text, guide)

    def test_invalid_counts_and_unknown_fixture_are_rejected(self):
        tool = load_script()
        with self.assertRaises(ValueError):
            tool.make_fixture("", kind="garbage", rows=12, sections=2, deferred=False)
        with self.assertRaises(ValueError):
            tool.make_fixture("", kind="dashboard", rows=-1, sections=2, deferred=False)
        with self.assertRaises(ValueError):
            tool.make_fixture("", kind="dashboard", rows=10, sections=-1, deferred=False)


if __name__ == "__main__":
    unittest.main()
