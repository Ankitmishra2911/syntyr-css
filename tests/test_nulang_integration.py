"""Optional Nulang UI protocol rendering contract; no runtime JS."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "integrations/nulang"))
from render import ProtocolError, render_document  # noqa: E402

CONTRACT = json.loads((ROOT / "metadata/syntyr-contract.json").read_text())

def sample():
    return {
        "protocol": "nulang-ui/1", "document_id": "demo", "revision": "1", "root": "root",
        "nodes": [
            {"id": "root", "kind": "column", "children": ["head", "card"]},
            {"id": "head", "kind": "heading", "properties": {
                "text": {"type": "string", "value": "Operations"},
                "level": {"type": "i64", "value": "1"}}},
            {"id": "card", "kind": "panel", "children": ["label", "stat", "link"]},
            {"id": "label", "kind": "text", "properties": {
                "text": {"type": "string", "value": "System healthy"}}},
            {"id": "stat", "kind": "metric", "properties": {
                "label": {"type": "string", "value": "Jobs"},
                "value": {"type": "string", "value": "42"}}},
            {"id": "link", "kind": "link", "properties": {
                "text": {"type": "string", "value": "Documentation"},
                "href": {"type": "string", "value": "/docs"}}},
        ],
    }


class AdapterTests(unittest.TestCase):
    def test_semantic_protocol_renders_accessible_syntyr_html(self):
        html = render_document(sample(), CONTRACT)
        self.assertIn('class="syn-root syn-page"', html)
        self.assertIn('data-syn-theme="studio"', html)
        self.assertIn('href="../dist/syntyr.core.css"', html)
        self.assertIn('<h1 class="syn-heading">Operations</h1>', html)
        self.assertIn('<section class="syn-panel">', html)
        self.assertIn('<strong class="syn-stat-value">42</strong>', html)
        self.assertIn('href="/docs"', html)
        self.assertNotIn('<script', html)
        self.assertNotIn('onclick', html)

    def test_string_properties_escape_markup_and_attributes(self):
        doc = sample()
        doc["nodes"][1]["properties"]["text"]["value"] = '<img src=x onerror="alert(1)">'
        doc["nodes"][5]["properties"]["text"]["value"] = 'A "quote" & <B>'
        html = render_document(doc, CONTRACT)
        self.assertIn('&lt;img src=x onerror=', html)
        self.assertNotIn('<img src=x', html)
        self.assertIn('A &quot;quote&quot; &amp; &lt;B&gt;', html)

    def test_invalid_href_is_rejected(self):
        for href in ("javascript:alert(1)", "//external.com", "data:text/html,a", "https://x.com\n"):
            with self.subTest(href=href):
                doc = sample()
                doc["nodes"][5]["properties"]["href"]["value"] = href
                with self.assertRaises(ProtocolError):
                    render_document(doc, CONTRACT)

    def test_interaction_graph_not_confused_with_renderable_html(self):
        doc = sample()
        doc["nodes"][1]["kind"] = "signal"
        with self.assertRaisesRegex(ProtocolError, "unsupported node kind"):
            render_document(doc, CONTRACT)

    def test_action_bindings_not_silently_broken(self):
        doc = sample()
        doc["nodes"][5]["actions"] = [{"event": "activate", "action_id": "save", "placement": "server"}]
        with self.assertRaisesRegex(ProtocolError, "action"):
            render_document(doc, CONTRACT)

    def test_protocol_structure_validation(self):
        invalids = []
        x = sample(); x["protocol"] = "nulang-ui/2"; invalids.append(x)
        x = sample(); x["revision"] = 2; invalids.append(x)
        x = sample(); x["revision"] = str(1 << 64); invalids.append(x)
        x = sample(); x["nodes"][1]["actions"] = {}; invalids.append(x)
        x = sample(); x["nodes"][2]["children"].append("missing"); invalids.append(x)
        x = sample(); x["nodes"][2]["children"].append("head"); invalids.append(x)
        x = sample(); x["nodes"][2]["children"].append("root"); invalids.append(x)
        x = sample(); x["nodes"].append(copy.deepcopy(x["nodes"][0])); invalids.append(x)
        x = sample(); x["nodes"][2]["children"].append("label"); invalids.append(x)
        x = sample(); x["nodes"][1]["properties"]["text"] = "<unsafe>"; invalids.append(x)
        x = sample(); x["nodes"][1]["properties"]["level"]["value"] = "7"; invalids.append(x)
        x = sample(); x["nodes"][4]["children"] = ["label"]; invalids.append(x)
        for doc in invalids:
            with self.subTest(doc=doc):
                with self.assertRaises(ProtocolError):
                    render_document(doc, CONTRACT)

    def test_only_defined_core_classes_and_known_theme(self):
        doc = sample()
        bad = copy.deepcopy(CONTRACT)
        bad["classes"] = [c for c in bad["classes"] if c["name"] != "syn-panel"]
        with self.assertRaisesRegex(ProtocolError, "contract"):
            render_document(doc, bad)
        with self.assertRaisesRegex(ProtocolError, "theme"):
            render_document(doc, CONTRACT, theme="hacked")

    def test_committed_preview_is_reproducible_and_validates(self):
        cmd = [sys.executable, "integrations/nulang/render.py",
               "--input", "integrations/nulang/sample-ui.json",
               "--output", "examples/nulang-ui.html"]
        result = subprocess.run(cmd + ["--check"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        check = subprocess.run(
            [sys.executable, "scripts/syntyr_check.py", "examples/nulang-ui.html"],
            cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_real_nulang_example_uses_server_rendered_html(self):
        path = ROOT / "integrations/nulang/web-example/src/main.nula"
        source = path.read_text()
        self.assertIn('import stdlib::web::html', source)
        self.assertIn('app "syntyr-demo"', source)
        self.assertIn('data-syn-theme', source)
        self.assertIn('syn-root', source)
        self.assertNotIn('<script', source)


if __name__ == "__main__":
    unittest.main()
