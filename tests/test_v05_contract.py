"""Theme and utility contracts for Cyberline's framework-neutral v0.5 foundations."""
from pathlib import Path
from html.parser import HTMLParser
import re
import unittest

from test_contract import contrast

ROOT = Path(__file__).resolve().parents[1]
THEMES = ("grid", "noir", "industrial", "terminal", "corporate", "minimal")
REQUIRED_TOKENS = (
    "--cy-bg", "--cy-surface", "--cy-surface-hi", "--cy-text",
    "--cy-muted", "--cy-accent", "--cy-on-accent", "--cy-frame",
    "--cy-danger", "--cy-success", "--cy-warning", "--cy-accent-soft",
)


def theme_rules(source, theme):
    selector = f'.cy-root[data-cy-theme="{theme}"]'
    start = source.find(selector)
    if start < 0:
        return None
    start = source.find("{", start)
    end = source.find("}", start)
    if start < 0 or end < 0:
        return None
    declarations = source[start + 1:end]
    return dict(re.findall(r'(--cy-[\w-]+|color-scheme):\s*([^;]+);', declarations))


class ThemeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.themes = set()
        self.scripts = 0
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "data-cy-theme" in values:
            self.themes.add(values["data-cy-theme"])
        if tag == "script":
            self.scripts += 1


class ThemeAndUtilitiesContract(unittest.TestCase):
    def test_six_palettes_define_complete_accessible_tokens(self):
        source = (ROOT / "src/tokens.css").read_text()
        for name in THEMES:
            with self.subTest(theme=name):
                tokens = theme_rules(source, name)
                self.assertIsNotNone(tokens, f"missing theme: {name}")
                for token in REQUIRED_TOKENS:
                    self.assertIn(token, tokens)
                for foreground, background in (
                    ("--cy-text", "--cy-bg"),
                    ("--cy-text", "--cy-surface"),
                    ("--cy-muted", "--cy-surface"),
                    ("--cy-on-accent", "--cy-accent"),
                ):
                    self.assertGreaterEqual(
                        contrast(tokens[foreground], tokens[background]), 4.5,
                        f"{name}: {foreground} contrast against {background}",
                    )

    def test_themes_are_nested_and_native_controls_get_correct_color_scheme(self):
        source = (ROOT / "src/tokens.css").read_text()
        geometry = {
            "grid": (".25rem", ".9rem"),
            "noir": (".25rem", ".9rem"),
            "industrial": (".15rem", ".45rem"),
            "terminal": ("0", "0"),
            "corporate": (".5rem", "0"),
            "minimal": (".375rem", "0"),
        }
        for name in THEMES:
            with self.subTest(theme=name):
                self.assertIn(f'.cy-root [data-cy-theme="{name}"]', source)
                tokens = theme_rules(source, name)
                self.assertEqual(tokens.get("color-scheme"),
                                 "light" if name in ("corporate", "minimal") else "dark")
                self.assertEqual(tokens.get("--cy-radius"), geometry[name][0])
                self.assertEqual(tokens.get("--cy-cut"), geometry[name][1])

    def test_utilities_are_opt_in_and_built_deterministically(self):
        utilities = (ROOT / "src/utilities.css").read_text()
        self.assertIn("@layer cy.components", utilities)
        self.assertIn(".cy-root", utilities)
        for cls in ("cy-u-flex", "cy-u-grid", "cy-u-gap-2",
                    "cy-u-p-2", "cy-u-mt-2", "cy-u-sr-only"):
            with self.subTest(cls=cls):
                self.assertIn("." + cls, utilities)
                self.assertIn("." + cls, (ROOT / "dist/cyberline.utilities.css").read_text())
                self.assertIn("." + cls, (ROOT / "dist/cyberline.all.css").read_text())
                self.assertNotIn("." + cls, (ROOT / "dist/cyberline.core.css").read_text())
        self.assertNotIn("@import", utilities)
        self.assertNotIn("javascript", utilities.lower())
        self.assertIn("'cyberline.utilities.css'", (ROOT / "scripts/build.py").read_text())
        self.assertLess(utilities.index(".cy-u-center"), utilities.index(".cy-u-between"),
                        "between must win over centered justification when both are present")

    def test_release_includes_optional_utility_distribution(self):
        from scripts.package_release import FILES
        self.assertIn("dist/cyberline.utilities.css", FILES)

    def test_six_theme_gallery_is_static_accessible_and_discoverable(self):
        demo = (ROOT / "examples/themes.html").read_text()
        parser = ThemeParser()
        parser.feed(demo)
        self.assertTrue(set(THEMES) <= parser.themes)
        self.assertEqual(parser.scripts, 0)
        self.assertIn("cyberline.utilities.css", demo)
        self.assertNotIn('class="cy-grid" aria-label=', demo, "unroled div should not have an aria-label")
        self.assertNotIn('<button type="button"', demo, "gallery controls must perform navigation")
        self.assertEqual(demo.count('href="../docs/#components"'), 6)
        self.assertIn('href="../examples/themes.html"', (ROOT / "docs/index.html").read_text())
        guide = (ROOT / "docs/theme-customization.md").read_text()
        for theme in THEMES:
            self.assertIn("data-cy-theme=\"" + theme + "\"", guide)
        self.assertIn("cyberline.utilities.css", guide)


if __name__ == "__main__":
    unittest.main()
