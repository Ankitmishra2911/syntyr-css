"""Opt-in local automated WCAG-tagged audit, using a developer-supplied axe-core JS.

The audit script is never loaded by the site or library. Install Playwright in
a temporary test environment and supply a local axe-core script, e.g.:

  curl -fsSL https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js -o /tmp/axe.min.js
  python3 tests/axe_audit.py --axe-file /tmp/axe.min.js

Automated checks do not replace screen reader, keyboard or zoom verification.
"""
import argparse
from pathlib import Path
import os
import shutil
import sys

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "docs/index.html", "examples/console.html",
          "examples/resources.html", "examples/pricing.html", "docs/console-kit.html",
         "examples/saas.html", "examples/business.html", "examples/terminal.html",
         "examples/geometry-terminal.html",
         "examples/vertigo-admin.html")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--axe-file", type=Path, required=True)
    args = parser.parse_args()
    if not args.axe_file.is_file():
        parser.error(f"Missing local axe-core script: {args.axe_file}")
    exe = (os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
           or shutil.which("chromium") or shutil.which("chromium-browser"))
    kwargs = {"headless": True}
    if exe:
        kwargs.update(executable_path=exe, args=["--no-sandbox"])
    violations = 0
    manual_review = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(**kwargs)
        for path in PAGES:
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.goto((ROOT / path).as_uri())
            page.add_script_tag(path=str(args.axe_file.resolve()))
            result = page.evaluate("""async () => axe.run(document, {
                runOnly: { type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa'] }
            })""")
            count = len(result["violations"])
            incomplete = len(result["incomplete"])
            violations += count
            manual_review += incomplete
            print(f"{path}: {count} automated violations, {incomplete} incomplete checks")
            for item in result["violations"]:
                print(f"  {item['impact']} {item['id']}: " +
                      ", ".join(str(n["target"]) for n in item["nodes"][:4]))
            page.close()
        browser.close()
    print(f"TOTAL: {violations} violations, {manual_review} incomplete checks requiring review")
    return int(bool(violations))


if __name__ == "__main__":
    sys.exit(main())
