"""Developer-only Hugo documentation proof verification.

Requires Hugo v0.170.0 on PATH or --hugo /path/to/pinned/hugo.
Does not change the live site and needs no runtime dependencies.
"""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "experiments/hugo"
PREFIX = "/cyberline-hugo-preview/"
REQUIRED = (
    "index.html",
    "guide/index.html",
    "guide/components/index.html",
    "guide/recipes/index.html",
    "guide/theme-customization/index.html",
    "guide/vertigo-integration/index.html",
    "examples/console.html",
    "dist/cyberline.core.css",
    "terminal/palettes.json",
)


class References(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ("a", "link", "img"):
            value = d.get("href") or d.get("src")
            if value:
                self.urls.append(value)


def verify(hugo: str) -> tuple[int, int]:
    with tempfile.TemporaryDirectory(prefix="cyberline-hugo-") as target:
        destination = Path(target)
        result = subprocess.run(
            [
                hugo, "--source", str(PROJECT), "--destination",
                str(destination), "--minify",
            ],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        if result.returncode:
            raise AssertionError(f"Hugo build failed:\n{result.stdout}\n{result.stderr}")
        if "WARN" in result.stderr:
            raise AssertionError(f"Unexpected Hugo warning:\n{result.stderr}")
        for path in REQUIRED:
            if not (destination / path).is_file():
                raise AssertionError(f"Missing output: {path}")
        forbidden = [
            p.relative_to(destination).as_posix() for p in destination.rglob("*")
            if p.is_file() and (p.suffix in (".py", ".pyc") or "__pycache__" in p.parts)
        ]
        if forbidden:
            raise AssertionError(f"Non-public source copied into generated site: {forbidden}")
        html_files = [destination / "index.html"] + sorted((destination / "guide").rglob("*.html"))
        if len(html_files) < 10:
            raise AssertionError(f"Expected the canonical Markdown guides, got {len(html_files)} pages")
        total_links = 0
        for page in html_files:
            content = page.read_text(encoding="utf-8")
            if "<script" in content.lower():
                raise AssertionError(f"Unexpected client-side JavaScript: {page}")
            parser = References()
            parser.feed(content)
            for url in parser.urls:
                uri = urlsplit(url)
                if uri.scheme or uri.netloc or not uri.path:
                    continue
                path = unquote(uri.path)
                if path.startswith(PREFIX):
                    path = path.removeprefix(PREFIX)
                    resolved = destination / path
                elif path.startswith("/"):
                    raise AssertionError(f"Unscoped root link in {page}: {url}")
                else:
                    resolved = (page.parent / path).resolve()
                    if not resolved.is_relative_to(destination):
                        raise AssertionError(f"Link escapes preview root in {page}: {url}")
                if path.endswith("/"):
                    resolved /= "index.html"
                if not resolved.exists():
                    raise AssertionError(f"Broken generated link in {page.relative_to(destination)}: {url}")
                total_links += 1
        print(f"PASS Hugo preview: {len(html_files)} HTML pages, {total_links} local links, no JS or Python assets.")
        return len(html_files), total_links


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hugo", default="hugo", help="Path to pinned Hugo executable")
    args = parser.parse_args()
    verify(args.hugo)
