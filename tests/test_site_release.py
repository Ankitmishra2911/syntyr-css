"""Static-site and release distribution contracts; no third-party packages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class LinkedAssets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag in ("a", "link", "img", "script"):
            url = attrs.get("href") or attrs.get("src")
            if url:
                self.paths.append(url)


class SiteReleaseTests(unittest.TestCase):
    def test_pages_entry_and_gallery_navigation(self):
        self.assertTrue((ROOT / ".nojekyll").exists(), "disable implicit Jekyll processing")
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        gallery = (ROOT / "docs/index.html").read_text(encoding="utf-8")
        self.assertIn('href="docs/"', home)
        self.assertIn('id="install"', gallery)
        self.assertIn('href="../LICENSE"', gallery)
        self.assertNotIn("<script", home.lower())
        self.assertNotIn("<script", gallery.lower())

    def test_site_links_resolve_on_pages_subpath(self):
        for source in (ROOT / "index.html", ROOT / "docs/index.html",
                       ROOT / "examples/console.html", ROOT / "examples/landing.html",
                       ROOT / "examples/pricing.html", ROOT / "examples/resources.html",
                       ROOT / "docs/console-kit.html",
                       ROOT / "examples/saas.html", ROOT / "examples/business.html",
                       ROOT / "examples/terminal.html",
                       ROOT / "examples/vertigo-admin.html"):
            with self.subTest(page=source.relative_to(ROOT)):
                parser = LinkedAssets()
                parser.feed(source.read_text(encoding="utf-8"))
                for href in parser.paths:
                    parsed = urlsplit(href)
                    if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
                        continue
                    destination = (source.parent / unquote(parsed.path)).resolve()
                    self.assertTrue(destination.is_relative_to(ROOT))
                    self.assertTrue(destination.exists(), f"{source.name}: missing {href}")

    def test_versioned_distribution_is_reproducible(self):
        self.assertEqual((ROOT / "VERSION").read_text().strip(), "0.3.0-alpha.4")
        with tempfile.TemporaryDirectory() as tmp:
            paths = [Path(tmp) / n for n in ("one.zip", "two.zip")]
            for target in paths:
                result = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/package_release.py"), str(target)],
                    cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(paths[0].read_bytes(), paths[1].read_bytes())
            with zipfile.ZipFile(paths[0]) as archive:
                names = set(archive.namelist())
                prefix = "syntyr-css-0.3.0-alpha.4/"
                for filename in ("LICENSE", "README.md", "dist/syntyr.core.css",
                                 "dist/syntyr.css", "dist/syntyr.semantic.css",
                                 "dist/syntyr.effects.css", "dist/syntyr.all.css",
                                 "dist/syntyr.recipes.css", "dist/syntyr.utilities.css",
                                 "dist/cyberline.utilities.css", "terminal/palettes.json",
                                 "docs/distribution.md"):
                    self.assertIn(prefix + filename, names)
                self.assertFalse(any("business/" in entry for entry in names))


if __name__ == "__main__":
    unittest.main()
