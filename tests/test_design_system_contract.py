"""Contracts for a framework-neutral SaaS, business and terminal design system."""
from pathlib import Path
import json
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


def palette_from_css(css, theme):
    selector = re.search(r'\[data-cy-theme="' + re.escape(theme) + r'"\][^{]*\{([^}]+)\}', css)
    if not selector:
        raise AssertionError(f'Missing {theme} CSS palette')
    return dict(re.findall(r'(--cy-[\w-]+):\s*(#[\da-fA-F]{6})\s*;', selector.group(1)))


class DesignSystemContract(unittest.TestCase):
    def test_professional_studio_theme_and_accessible_contrast_pairings(self):
        css = (ROOT / 'src/tokens.css').read_text()
        self.assertIn('[data-cy-theme="studio"]', css)
        self.assertIn('color-scheme: light', css)
        palette = palette_from_css(css, 'studio')
        for token in ('--cy-bg', '--cy-surface', '--cy-text', '--cy-muted',
                      '--cy-accent', '--cy-on-accent', '--cy-frame', '--cy-danger'):
            self.assertIn(token, palette)

    def test_opt_in_recipes_are_separate_from_lightweight_core(self):
        source = (ROOT / 'src/recipes.css').read_text()
        bundled = (ROOT / 'dist/cyberline.recipes.css').read_text()
        all_css = (ROOT / 'dist/cyberline.all.css').read_text()
        core = (ROOT / 'dist/cyberline.core.css').read_text()
        for cls in ('.cy-app-shell', '.cy-app-rail', '.cy-workspace', '.cy-site-hero',
                    '.cy-feature-grid', '.cy-terminal', '.cy-terminal-line', '.cy-frame--precision'):
            self.assertIn(cls, source)
            self.assertIn(cls, bundled)
            self.assertIn(cls, all_css)
            self.assertNotIn(cls, core)
        self.assertIn('@layer cy.recipes', source)
        self.assertNotIn('!important', source)

    def test_terminal_ansi_palette_is_synced_to_browser_themes(self):
        themes = json.loads((ROOT / 'terminal/palettes.json').read_text())['themes']
        self.assertEqual(set(themes), {'grid', 'noir', 'studio'})
        css = (ROOT / 'src/tokens.css').read_text()
        for name, theme in themes.items():
            with self.subTest(theme=name):
                css_colors = palette_from_css(css, name)
                for term_key, css_key in (('background', '--cy-bg'),
                                          ('foreground', '--cy-text'),
                                          ('accent', '--cy-accent')):
                    self.assertEqual(theme[term_key].lower(), css_colors[css_key].lower())
                self.assertEqual(len(theme['ansi']), 16)
                self.assertTrue(all(re.fullmatch(r'#[0-9a-fA-F]{6}', color)
                                    for color in theme['ansi']))

    def test_live_html_examples_cover_three_product_types_without_scripts(self):
        for path, landmark in (('examples/saas.html', 'cy-app-shell'),
                               ('examples/business.html', 'cy-site-hero'),
                               ('examples/terminal.html', 'cy-terminal')):
            with self.subTest(path=path):
                html = (ROOT / path).read_text()
                self.assertIn(landmark, html)
                self.assertIn('cyberline.recipes.css', html)
                self.assertIn('<main', html)
                self.assertIn('<h1', html)
                self.assertNotIn('<script', html.lower())
                self.assertNotIn('http://', html)
                self.assertNotIn('https://', html)

    def test_optional_cinematic_effects_are_static_and_isolated(self):
        effects = (ROOT / 'src/effects.css').read_text()
        core = (ROOT / 'dist/cyberline.core.css').read_text()
        for selector in ('.cy-horizon', '.cy-atmosphere'):
            self.assertIn(selector, effects)
            self.assertNotIn(selector, core)
        self.assertNotIn('@keyframes', effects)
        self.assertIn('forced-colors: active', effects)

    def test_studio_default_text_contrast(self):
        palette = palette_from_css((ROOT / 'src/tokens.css').read_text(), 'studio')

        def luminance(color):
            channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            channels = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
                        for v in channels]
            return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]

        def ratio(a, b):
            light, dark = sorted((luminance(a), luminance(b)), reverse=True)
            return (light + 0.05) / (dark + 0.05)

        for fg, bg in (('--cy-text', '--cy-bg'),
                       ('--cy-muted', '--cy-surface'),
                       ('--cy-accent', '--cy-surface'),
                       ('--cy-on-accent', '--cy-accent'),
                       ('--cy-danger', '--cy-surface')):
            with self.subTest(foreground=fg, background=bg):
                self.assertGreaterEqual(ratio(palette[fg], palette[bg]), 4.5)

    def test_colored_cli_spans_supply_matching_background(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("cyberline_cli", ROOT / "examples/ansi_cli.py")
        cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli)
        rendered = cli.styled("OK", "#8ce6bb", True, "#080f19")
        self.assertIn("\x1b[38;2;140;230;187m", rendered)
        self.assertIn("\x1b[48;2;8;15;25m", rendered)
        self.assertTrue(rendered.endswith("\x1b[0m"))
        self.assertEqual(cli.styled("OK", "#8ce6bb", False, "#080f19"), "OK")

    def test_cli_rejects_color_if_windows_vt_activation_fails(self):
        import importlib.util
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location("cyberline_cli", ROOT / "examples/ansi_cli.py")
        cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli)
        class FakeTTY:
            def isatty(self):
                return True
            def fileno(self):
                return 1
        with patch.object(cli.os, "name", "nt"):
            with patch.object(cli, "_enable_windows_vt", return_value=False):
                self.assertFalse(cli.should_color(FakeTTY(), {"TERM": "xterm-256color"}))
            with patch.object(cli, "_enable_windows_vt", return_value=True):
                self.assertTrue(cli.should_color(FakeTTY(), {"TERM": "xterm-256color"}))
        self.assertFalse(cli.should_color(FakeTTY(), {"NO_COLOR": "", "TERM": "xterm"}))
        self.assertFalse(cli.should_color(FakeTTY(), {"CLICOLOR": "0", "TERM": "xterm"}))

    def test_labeled_visual_groups_have_explicit_group_roles(self):
        from html.parser import HTMLParser
        class NamedGroups(HTMLParser):
            def __init__(self):
                super().__init__()
                self.seen = []
            def handle_starttag(self, tag, attrs):
                a = dict(attrs)
                classes = set(a.get("class", "").split())
                if a.get("aria-label") and classes.intersection({"cy-stats", "business-visual"}):
                    self.seen.append((a.get("class"), a.get("role")))
        for filename in ("docs/index.html", "examples/resources.html", "examples/business.html"):
            with self.subTest(filename=filename):
                doc = NamedGroups()
                doc.feed((ROOT / filename).read_text())
                self.assertTrue(doc.seen)
                self.assertTrue(all(role == "group" for _, role in doc.seen), doc.seen)

    def test_gallery_integration_guide_has_accessible_hit_area(self):
        from html.parser import HTMLParser
        class GuideLink(HTMLParser):
            def __init__(self):
                super().__init__()
                self.classes = []
            def handle_starttag(self, tag, attrs):
                attributes = dict(attrs)
                if tag == "a" and attributes.get("href") == "saas-cli-business.md":
                    self.classes.append(attributes.get("class", ""))
        parser = GuideLink()
        parser.feed((ROOT / "docs/index.html").read_text())
        self.assertEqual(len(parser.classes), 1)
        self.assertIn("cy-button", parser.classes[0])

    def test_gallery_does_not_advertise_unreleased_theme_as_tagged_release(self):
        page = (ROOT / "docs/index.html").read_text()
        self.assertIn("Studio is not included in the linked v0.3.0-alpha.1 release", page)

    def test_browser_matrix_and_axe_cover_saas_business_terminal(self):
        for path in ("tests/browser_matrix.py", "tests/axe_audit.py"):
            s = (ROOT / path).read_text()
            for name in ("examples/saas.html", "examples/business.html", "examples/terminal.html"):
                self.assertIn(name, s)

    def test_cli_example_respects_no_color_and_pipelines(self):
        cli = ROOT / 'examples/ansi_cli.py'
        run = subprocess.run([sys.executable, str(cli), '--theme', 'studio'],
                             capture_output=True, text=True, check=True)
        self.assertNotIn('\x1b[', run.stdout)
        self.assertIn('CYBERLINE', run.stdout)
        run = subprocess.run([sys.executable, str(cli), '--theme', 'grid', '--no-color'],
                             capture_output=True, text=True, check=True)
        self.assertNotIn('\x1b[', run.stdout)


if __name__ == '__main__':
    unittest.main()
