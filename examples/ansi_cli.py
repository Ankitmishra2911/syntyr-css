#!/usr/bin/env python3
"""Stdlib-only example: theme-driven ANSI CLI output (not part of Cyberline CSS)."""
from pathlib import Path
import argparse
import json
import os
import sys

PALETTES = Path(__file__).resolve().parents[1] / "terminal" / "palettes.json"


def styled(text, color, enabled):
    if not enabled:
        return text
    red, green, blue = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return f"\x1b[38;2;{red};{green};{blue}m{text}\x1b[0m"


def main():
    parser = argparse.ArgumentParser(description="Preview Cyberline ANSI palettes")
    parser.add_argument("--theme", choices=("grid", "noir", "studio"), default="grid")
    parser.add_argument("--no-color", action="store_true", help="Always output plain text")
    args = parser.parse_args()
    theme = json.loads(PALETTES.read_text(encoding="utf-8"))["themes"][args.theme]
    enabled = (sys.stdout.isatty() and not args.no_color and
               "NO_COLOR" not in os.environ and os.environ.get("CLICOLOR") != "0" and
               os.environ.get("TERM", "") != "dumb")
    print(styled("CYBERLINE / CLI STATUS", theme["accent"], enabled))
    print(f"Theme: {args.theme}")
    print(f"[{styled('OK', theme['ansi'][2], enabled)}] 6 tasks completed")
    print(f"[{styled('WARN', theme['ansi'][3], enabled)}] 1 task pending")
    print(styled("Run with --no-color for machine-readable/plain logs.", theme["foreground"], enabled))


if __name__ == "__main__":
    main()
