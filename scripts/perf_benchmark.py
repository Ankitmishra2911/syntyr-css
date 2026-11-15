"""Offline browser rendering benchmark for realistic Syntyr SaaS layouts.

  python3 scripts/perf_benchmark.py --runs 3 --rows 1200 --sections 12
  python3 scripts/perf_benchmark.py --browsers chromium,firefox,webkit --output /tmp/report.json

Playwright is developer-only, NOT a Syntyr runtime dependency. The benchmark
compares the same HTML and CSS with/without opt-in content-visibility on
below-fold sections. Browser timings are noisy; never present synthetic LCP
or FCP as real-user Web Vitals. Firefox/WebKit cannot expose Chrome CDP metrics.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import statistics
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
BROWSERS = ("chromium", "firefox", "webkit")
VIEWPORTS = {
    "desktop": {"width": 1365, "height": 900},
    "mobile": {"width": 390, "height": 844},
}
METRICS = ("navigation_ms", "fcp_ms", "lcp_ms", "cls",
           "theme_toggle_ms", "style_recalc_ms", "layout_ms", "paint_ms",
           "scroll_reveal_ms", "scroll_cls")


def trial_order(names: list[str], index: int) -> list[str]:
    if not names:
        return []
    n = index % len(names)
    return names[n:] + names[:n]


def make_fixture(css: str, *, kind: str, rows: int, sections: int,
                 deferred: bool) -> str:
    """Deterministic, external-resource-free, realistic dashboard/table DOM."""
    if kind not in ("dashboard", "long-table") or rows < 0 or sections < 0:
        raise ValueError("Unknown fixture or negative counts")

    kpis = "".join(
        f'<article class="syn-app-card"><p class="syn-caption">REVENUE {i+1:02d}</p>'
        f'<p class="syn-stat-value">{(i+1)*1642:,}</p></article>' for i in range(12)
    )
    header = (f'<header class="syn-header"><div><p class="syn-eyebrow">OPERATIONS / LIVE</p>'
              f'<h1 class="syn-heading">{kind.replace("-", " ").title()}</h1></div>'
              '<nav class="syn-nav" aria-label="Workspace">'
              '<a href="#records">Records</a><a href="#activity">Activity</a></nav></header>')
    extra = []
    if kind == "dashboard":
        top_rows = min(12, rows)
        extras = rows - top_rows
        cards = [f'<article class="syn-feature-card"><h3 class="syn-heading">Campaign {n:04d}</h3>'
                 '<p>Regional inventory, operator updates, scheduled creative and delivery.</p>'
                 '<p class="syn-status syn-status--success">Active</p></article>'
                 for n in range(extras)]
        for index in range(sections):
            card_slice = cards[index::max(sections, 1)]
            if card_slice:
                text = '<div class="syn-feature-grid">' + "".join(card_slice) + '</div>'
            else:
                text = '<p class="syn-muted">No scheduled updates.</p>'
            extra.append((index, text, "40rem"))
    else:
        top_rows = min(12, rows)
        extras = rows - top_rows
        for index in range(sections):
            count = len(range(index, extras, max(sections, 1)))
            rows_html = "".join(
                f'<tr><th scope="row">Asset {index+1:02d}-{n:04d}</th>'
                f'<td>Flight {n:04d}</td>'
                '<td><span class="syn-status syn-status--success">Active</span></td>'
                f'<td class="syn-cell--numeric">{(n+1)*184:,}</td></tr>'
                for n in range(count))
            body = ('<div class="syn-table-wrap"><table class="syn-table">'
                    '<caption class="syn-caption">Regional campaign assets</caption>'
                    '<thead><tr><th>Asset</th><th>Flight</th><th>Status</th><th>Revenue</th></tr></thead>'
                    f'<tbody>{rows_html}</tbody></table></div>')
            extra.append((index, body, f"{max(8, count)*3+6}rem"))

    first_rows = "".join(
        f'<tr><th scope="row">Customer {n:04d}</th><td>Campaign {n:04d}</td>'
        '<td><span class="syn-status syn-status--success">Active</span></td>'
        f'<td class="syn-cell--numeric">{(n+1)*184:,}</td></tr>'
        for n in range(top_rows)
    )
    main_table = ('<section id="records" class="syn-app-card"><h2 class="syn-heading">Recent records</h2>'
                  '<div class="syn-table-wrap"><table class="syn-table">'
                  '<caption>Recent active campaigns</caption>'
                  '<thead><tr><th>Customer</th><th>Campaign</th>'
                  '<th>Status</th><th>Revenue</th></tr></thead>'
                  f'<tbody>{first_rows}</tbody></table></div></section>')
    blocks = "".join(
        f'<section class="syn-app-card{" syn-defer-section" if deferred else ""}" '
        f'style="--syn-defer-size:{hint}" aria-labelledby="segment-{i}">'
        f'<h2 class="syn-heading" id="segment-{i}">Region {i+1:02d}</h2>{content}</section>'
        for i, content, hint in extra
    )
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>SYNTYR Offline Render Benchmark</title><style>{css}</style></head>'
            f'<body class="syn-root syn-page" data-syn-theme="studio" data-syn-fixture="{kind}">'
            '<main class="syn-shell">'
            f'{header}<section class="syn-kpi-grid" aria-label="Key performance indicators">{kpis}</section>'
            f'{main_table}<div id="activity" class="syn-stack">{blocks}</div></main></body></html>')


def summarize(samples: dict, *, browser: str, viewport: str, fixture: str,
              runs: int, rows: int, sections: int) -> dict:
    def median_or_none(values: list, metric: str):
        available = [record[metric] for record in values if record.get(metric) is not None]
        return round(statistics.median(available), 3) if available else None
    return {
        "browser": browser,
        "viewport": viewport,
        "fixture": {"kind": fixture, "rows": rows, "sections": sections},
        "runs": runs,
        "unit": "milliseconds except CLS",
        "results": {
            variant: {metric: median_or_none(values, metric) for metric in METRICS}
            for variant, values in samples.items()
        },
        "limitations": [
            "Synthetic local file benchmark: not field Core Web Vitals or a production LCP/INP claim.",
            "Some browsers do not expose FCP/LCP/layout-shift; missing metrics are null, never zero.",
            "CDP style and layout durations are Chromium-only; paint duration is not exposed and remains null.",
            "Navigation and theme timing may vary by hardware and thermal state; use medians.",
            "Only below-fold sections are deferred; document structure and CSS are identical.",
            "Scroll reveal is synthetic and can expose deferred-content latency; scroll CLS is non-input layout shift recorded after the jump.",
        ],
    }


INIT_JS = """(() => {
  const state = {lcp: null, cls: null};
  window.__syntyrPerf = state;
  if (!('PerformanceObserver' in window)) return;
  const supported = PerformanceObserver.supportedEntryTypes || [];
  for (const [type, callback] of [
    ['largest-contentful-paint', (list) => {
      for (const e of list.getEntries()) state.lcp = e.startTime;
    }],
    ['layout-shift', (list) => {
      for (const e of list.getEntries()) {
        if (!e.hadRecentInput) state.cls += e.value;
      }
    }],
  ]) {
    if (!supported.includes(type)) continue;
    try {
      new PerformanceObserver(callback).observe({type, buffered: true});
      if (type === 'layout-shift') state.cls = 0;
    } catch (_) { /* browser does not support this metric */ }
  }
})()"""


def cdp_snapshot(session) -> dict:
    return {item["name"]: item["value"]
            for item in session.send("Performance.getMetrics")["metrics"]}


def sample(browser, browser_name: str, path: Path, viewport_name: str) -> dict:
    context = browser.new_context(viewport=VIEWPORTS[viewport_name],
                                  device_scale_factor=1, reduced_motion="reduce")
    page = context.new_page()
    page.add_init_script(INIT_JS)
    cdpsession = None
    try:
        if browser_name == "chromium":
            cdpsession = context.new_cdp_session(page)
            cdpsession.send("Performance.enable")
        start = time.perf_counter()
        page.goto(path.as_uri(), wait_until="load", timeout=60000)
        # Force the initial layout and let first paints settle.
        page.evaluate("() => void document.body.offsetHeight")
        page.evaluate("() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
        navigation = (time.perf_counter() - start) * 1000
        if cdpsession:
            before = cdp_snapshot(cdpsession)
        else:
            before = {}
        theme = page.evaluate("""() => {
          const root = document.body, key = document.querySelector('#records');
          const start = performance.now();
          for (let i=0; i<6; i++) {
            root.dataset.synTheme = i % 2 ? 'studio' : 'noir';
            void getComputedStyle(key).color;
            void root.offsetHeight;
          }
          return (performance.now() - start) / 6;
        }""")
        page.evaluate("() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
        after = cdp_snapshot(cdpsession) if cdpsession else {}
        timings = page.evaluate("""() => {
          const nav = performance.getEntriesByType('navigation')[0] || {};
          const paint = performance.getEntriesByType('paint').find(e => e.name === 'first-contentful-paint');
          const state = window.__syntyrPerf || {};
          return {
            fcp: paint ? paint.startTime : null,
            lcp: state.lcp ?? null,
            cls: state.cls ?? null,
          };
        }""")
        def delta(name):
            if not before or name not in before or name not in after:
                return None
            return max(0, after[name] - before[name]) * 1000

        # The initial load is not the whole story: reveal a late section and
        # record the price paid when the user reaches previously skipped content.
        scroll_cls_before = page.evaluate("() => window.__syntyrPerf?.cls ?? null")
        scroll_reveal = page.evaluate("""async () => {
          const sections = document.querySelectorAll('[id^="segment-"]');
          if (!sections.length) return null;
          const last = sections[sections.length - 1];
          const started = performance.now();
          last.scrollIntoView({block: 'start'});
          await new Promise(resolve => requestAnimationFrame(() =>
            requestAnimationFrame(resolve)));
          void last.getBoundingClientRect().height;
          return performance.now() - started;
        }""")
        scroll_cls_after = page.evaluate("() => window.__syntyrPerf?.cls ?? null")
        scroll_cls = (
            max(0, scroll_cls_after - scroll_cls_before)
            if scroll_cls_before is not None and scroll_cls_after is not None
            else None
        )

        return {
            "scroll_reveal_ms": scroll_reveal,
            "scroll_cls": scroll_cls,
            "navigation_ms": navigation,
            "fcp_ms": timings["fcp"],
            "lcp_ms": timings["lcp"],
            "cls": timings["cls"],
            "theme_toggle_ms": theme,
            "style_recalc_ms": delta("RecalcStyleDuration"),
            "layout_ms": delta("LayoutDuration"),
            "paint_ms": delta("PaintDuration"),
        }
    finally:
        context.close()


def run(args) -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise RuntimeError("Playwright is optional; install in a developer venv") from error
    core = (ROOT / "dist/syntyr.core.css").read_text(encoding="utf-8")
    recipes = (ROOT / "dist/syntyr.recipes.css").read_text(encoding="utf-8")
    css = core + "\n" + recipes
    browsers = args.browsers.split(",")
    if len(set(browsers)) != len(browsers) or not set(browsers) <= set(BROWSERS):
        raise ValueError("Browser list must contain unique names from chromium,firefox,webkit")
    report = {"config": {"rows": args.rows, "sections": args.sections, "runs": args.runs,
                         "viewport_widths": {name: v["width"] for name, v in VIEWPORTS.items()},
                         "stylesheets": ["syntyr.core.css", "syntyr.recipes.css"]},
              "measurements": [], "blocked": {}}
    with tempfile.TemporaryDirectory(prefix="syntyr-bench-") as tmp:
        files = {}
        for kind in ("dashboard", "long-table"):
            for variant in ("standard", "deferred"):
                path = Path(tmp) / f"{kind}-{variant}.html"
                path.write_text(make_fixture(css, kind=kind, rows=args.rows,
                                             sections=args.sections,
                                             deferred=variant == "deferred"), encoding="utf-8")
                files[(kind, variant)] = path
        with sync_playwright() as playwright:
            for browser_name in browsers:
                try:
                    kw = {"headless": True}
                    executable = (os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
                                  or shutil.which("chromium") or shutil.which("chromium-browser"))
                    if browser_name == "chromium" and executable:
                        kw.update(executable_path=executable, args=["--no-sandbox"])
                    browser = getattr(playwright, browser_name).launch(**kw)
                except Exception as error:
                    report["blocked"][browser_name] = str(error).splitlines()[0][:300]
                    continue
                try:
                    for viewport in VIEWPORTS:
                        for kind in ("dashboard", "long-table"):
                            samples = {"standard": [], "deferred": []}
                            for round_index in range(args.runs + 1):
                                for variant in trial_order(list(samples), round_index):
                                    value = sample(browser, browser_name,
                                                   files[(kind, variant)], viewport)
                                    if round_index:
                                        samples[variant].append(value)
                            result = summarize(samples, browser=browser_name, viewport=viewport,
                                               fixture=kind, runs=args.runs,
                                               rows=args.rows, sections=args.sections)
                            result["browser_version"] = browser.version
                            report["measurements"].append(result)
                            print(f"MEASURED {browser_name} {viewport} {kind}", file=sys.stderr)
                finally:
                    browser.close()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browsers", default="chromium,firefox,webkit")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--rows", type=int, default=1200)
    parser.add_argument("--sections", type=int, default=12)
    parser.add_argument("--output", type=Path, help="write complete JSON report to this path")
    args = parser.parse_args()
    if args.runs < 1 or args.rows < 1 or args.sections < 1:
        parser.error("runs, rows, sections must be positive")
    try:
        result = run(args)
    except Exception as error:
        print(f"BENCHMARK ERROR: {error}", file=sys.stderr)
        return 2
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if not result["blocked"] else 1


if __name__ == "__main__":
    sys.exit(main())
