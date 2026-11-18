"""Contracts for the optional OOH operations workspace GET-server example."""
from html.parser import HTMLParser
from pathlib import Path
import sys
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))
import geo_operations_server as app


class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.fragments, self.scripts = set(), [], []
        self.mains = self.h1s = 0

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get("id"):
            self.ids.add(data["id"])
        if tag == "a" and data.get("href", "").startswith("#"):
            self.fragments.append(data["href"][1:])
        if tag == "script":
            self.scripts.append(tag)
        self.mains += tag == "main"
        self.h1s += tag == "h1"


class GeoOperationsServerTests(unittest.TestCase):
    def test_filters_combine_query_status_and_type(self):
        rows = app.filter_assets(query="east", status="available", kind="static")
        self.assertTrue(rows)
        self.assertTrue(all("east" in f"{a.name} {a.district} {a.code}".lower() for a in rows))
        self.assertTrue(all(a.status == "available" and a.kind == "static" for a in rows))
        self.assertEqual(app.filter_assets("nonexistent", "all", "all"), [])

    def test_search_selection_and_native_get_form(self):
        page = app.render_dashboard("query=east&status=available&type=static&selected=ES-024")
        self.assertIn("East Junction", page)
        self.assertNotIn("Central Loop", page)
        self.assertIn('name="query" type="search" value="east"', page)
        self.assertIn('<option value="available" selected>', page)
        self.assertIn('<option value="static" selected>', page)
        self.assertIn('data-syn-selected="true"', page)
        self.assertEqual(page.count('aria-current="location"'), 1)
        self.assertIn('tabindex="-1"', page)
        self.assertIn("selected=ES-024", page)
        self.assertIn('href="/dist/syntyr.geo.css"', page)
        self.assertIn('class="syn-geo-shell"', page)
        self.assertIn('class="syn-geo-marker-layer"', page)
        self.assertIn('style="--syn-geo-x:', page)
        self.assertNotIn('syn-ops-', page)
        self.assertNotIn('syntyr.workspaces.css', page)
        self.assertIn('method="get"', page)
        self.assertNotIn("<script", page.lower())

    def test_invalid_selection_falls_back_to_visible_record(self):
        rows = app.filter_assets("east", "all", "all")
        page = app.render_dashboard("query=east&selected=invalid")
        self.assertIn(f"SELECTED / {rows[0].code}", page)
        self.assertNotIn("selected=invalid", page)

    def test_empty_search_has_no_stale_selection(self):
        page = app.render_dashboard("query=nonexistent&status=booked")
        self.assertIn("No assets match your filters", page)
        self.assertIn("0 of ", page)
        self.assertNotIn('id="selection"', page)
        self.assertNotIn('data-syn-selected="true"', page)

    def test_untrusted_query_is_escaped_and_bounded(self):
        page = app.render_dashboard("query=%3Cscript%3Ealert%281%29%3C%2Fscript%3E")
        self.assertIn("&lt;script&gt;", page)
        self.assertNotIn("<script>", page)
        self.assertLess(len(app.render_dashboard("query=" + "x" * 10000)), 15000)

    def test_semantics_and_fragment_targets(self):
        page = app.render_dashboard("")
        audit = Audit()
        audit.feed(page)
        self.assertEqual((audit.mains, audit.h1s), (1, 1))
        self.assertEqual(audit.scripts, [])
        self.assertFalse(set(audit.fragments) - audit.ids)
        self.assertIn('aria-label="Illustrative sample asset map"', page)
        self.assertIn("Sample data", page)
        self.assertIn('id="filter-query"', page)
        self.assertIn('for="filter-query"', page)

    @classmethod
    def setUpClass(cls):
        cls.server = app.create_server(port=0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=5)
        cls.server.server_close()

    def test_repo_only_geo_demo_does_not_duplicate_public_css_api(self):
        page = app.render_dashboard("")
        self.assertEqual(set(app.CSS_FILES), {
            "/dist/syntyr.core.css", "/dist/syntyr.recipes.css", "/dist/syntyr.geo.css"
        })
        self.assertNotIn("syn-ops-", page)
        self.assertNotIn("workspaces.css", page)
        self.assertIn("geo_operations_server.py", (ROOT / "docs/geo.md").read_text())
        self.assertIn("standard-library GET-filtering demo", (ROOT / "llms.txt").read_text())

    def test_http_allowlist_and_filtering(self):
        with urlopen(self.base + "/?status=booked") as r:
            body = r.read().decode()
            self.assertEqual(r.status, 200)
            self.assertIn("Central Loop", body)
            self.assertNotIn("East Junction", body)
            self.assertEqual(r.headers["Content-Type"], "text/html; charset=utf-8")
            self.assertIn("default-src 'none'", r.headers["Content-Security-Policy"])
        with urlopen(self.base + "/dist/syntyr.geo.css") as r:
            self.assertIn("text/css", r.headers["Content-Type"])
            self.assertIn(b".syn-geo-workspace", r.read())
        for path in ("/.env", "/README.md", "/dist/../.git/config", "/unknown"):
            with self.subTest(path=path), self.assertRaises(HTTPError) as ctx:
                urlopen(self.base + path)
            self.assertEqual(ctx.exception.code, 404)
            ctx.exception.close()


if __name__ == "__main__":
    unittest.main()
