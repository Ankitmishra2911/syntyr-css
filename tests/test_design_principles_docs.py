"""Published design guidance must remain discoverable and copyable."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs/design-principles.md"


class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.referenced_ids = set()
        self.classes = set()
        self.labels = []
        self.tags = set()

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        self.tags.add(tag)
        if "id" in data:
            self.ids.add(data["id"])
        if data.get("for"):
            self.referenced_ids.add(data["for"])
            self.labels.append(data["for"])
        for key in ("aria-describedby", "aria-labelledby"):
            self.referenced_ids.update(data.get(key, "").split())
        self.classes.update(data.get("class", "").split())


class DesignPrinciplesDocs(unittest.TestCase):
    def test_principles_guide_is_linked_and_published_explicitly(self):
        self.assertTrue(GUIDE.is_file())
        for path in ("README.md", "DESIGN.md", "llms.txt"):
            self.assertIn("design-principles.md", (ROOT / path).read_text(), path)
        site = (ROOT / "scripts/build_cloudflare_site.py").read_text()
        reference = (ROOT / "scripts/build_agent_docs.py").read_text()
        self.assertIn('"design-principles.md"', site)
        self.assertIn('"docs/design-principles.md"', reference)
        self.assertIn("scripts/design_conformance.py",
                      (ROOT / "CONTRIBUTING.md").read_text())

    def test_guidance_distinguishes_required_behavior_from_visual_choices(self):
        guide = GUIDE.read_text()
        for section in ("## Universal defaults", "## Component state contract",
                        "## Composition examples", "## Deliberate non-defaults",
                        "## What automated checks do not prove"):
            self.assertIn(section, guide)
        for term in ("WCAG 2.2 AA", "progressive disclosure", "feedback",
                     "semantic HTML", "reduced motion", "contrast", "focus-visible"):
            self.assertIn(term.lower(), guide.lower())

    def test_html_recipes_use_referentially_sound_semantic_markup_and_real_hooks(self):
        guide = GUIDE.read_text()
        snippets = re.findall(r"```html\n(.*?)\n```", guide, re.DOTALL)
        self.assertGreaterEqual(len(snippets), 3)
        css = "\n".join(path.read_text() for path in (ROOT / "src").rglob("*.css"))
        found_tags = set()
        for snippet in snippets:
            parser = Markup()
            parser.feed(snippet)
            found_tags.update(parser.tags)
            self.assertTrue(parser.referenced_ids <= parser.ids,
                            parser.referenced_ids - parser.ids)
            for klass in parser.classes:
                if klass.startswith("syn-"):
                    self.assertIn("." + klass, css, klass)
        self.assertTrue({"main", "form", "table", "caption", "label"} <= found_tags)
        self.assertIn('scope="col"', guide)
        self.assertIn('method="get"', guide)


if __name__ == "__main__":
    unittest.main()
