"""Browser-owned HTML disclosure and form-control compositions."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ExampleStructure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.details = []
        self.ids = set()
        self.controls = {}
        self.options = []
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "details":
            self.details.append(attrs)
        if tag in ("input", "select"):
            self.controls[attrs.get("id")] = attrs
        if tag == "optgroup":
            self.options.append(attrs)
        if tag == "script":
            self.scripts += 1


class NativeHTMLWorkflowTests(unittest.TestCase):
    def test_named_disclosures_and_form_controls_remain_native(self):
        html = (ROOT / "examples/native-elements.html").read_text()
        doc = ExampleStructure()
        doc.feed(html)
        group = [d for d in doc.details if d.get("name") == "native-review-sections"]
        self.assertGreaterEqual(len(group), 2)
        self.assertTrue(all("open" not in item for item in group))
        self.assertIn("native-location-list", doc.ids)
        self.assertEqual(doc.controls["native-location"]["list"], "native-location-list")
        self.assertTrue(doc.controls["native-location"].get("name"))
        self.assertTrue(doc.controls["native-service"].get("name"))
        self.assertGreaterEqual(len(doc.options), 2)
        self.assertIn("<output", html)
        self.assertEqual(doc.scripts, 0)

    def test_semantic_open_state_preserves_browser_marker(self):
        css = (ROOT / "src/semantic.css").read_text()
        self.assertIn("details:not([class])[open]", css)
        self.assertIn("summary:not([class])", css)
        self.assertNotIn("list-style: none", css)
        self.assertNotIn("summary::marker", css)

    def test_native_workflows_are_discoverable(self):
        docs = (ROOT / "docs/components.md").read_text()
        self.assertIn("details name", docs)
        self.assertIn("datalist", docs)
        self.assertIn("optgroup", docs)
        self.assertIn("examples/native-elements.html", (ROOT / "README.md").read_text())


if __name__ == "__main__":
    unittest.main()
