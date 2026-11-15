"""Optional, dependency-free static HTML checks against the Syntyr CSS contract.

This is a development tool, not a CSS preprocessor or application dependency.
It validates only literal HTML attributes. Dynamic templates need their own
language-aware integration; false claims about rendered state are avoided.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "metadata" / "syntyr-contract.json"


def _stylesheet_name(href: str, names: set[str]) -> str | None:
    """Match a published Syntyr entrypoint, not an unrelated stylesheet."""
    path = urlsplit(href).path.replace("\\", "/")
    for name in sorted(names, key=len, reverse=True):
        if path == name or path.endswith("/" + name):
            return name
    return None


def _is_dynamic(value: str) -> bool:
    return any(char in value for char in "{}$<>")  # conservative template escape


class _SyntyrParser(HTMLParser):
    def __init__(self, contract: dict):
        super().__init__(convert_charrefs=True)
        self.classes = {c["name"]: c for c in contract["classes"]}
        self.attribute_values = contract["attributes"]
        self.stylesheet_names = set(contract["stylesheets"])
        self.linked_stylesheets: set[str] = set()
        self.used_classes: list[tuple[int, int, str]] = []
        self.diagnostics: list[dict] = []

    def _error(self, code: str, message: str, line: int, column: int):
        self.diagnostics.append({
            "line": line, "column": column + 1,
            "severity": "error", "code": code, "message": message,
        })

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        line, col = self.getpos()
        if tag.lower() == "link" and "stylesheet" in (data.get("rel") or "").split():
            name = _stylesheet_name(data.get("href") or "", self.stylesheet_names)
            if name:
                self.linked_stylesheets.add(name)
        for class_attr in ("class", "classname"):
            class_value = data.get(class_attr) or ""
            if _is_dynamic(class_value):
                continue  # template output cannot be resolved safely without its renderer
            for name in class_value.split():
                if not name.startswith("syn-"):
                    continue
                if name not in self.classes:
                    self._error("unknown-class", f"Unknown Syntyr class '{name}'.",
                                line, col)
                else:
                    self.used_classes.append((line, col, name))
        for name, allowed in self.attribute_values.items():
            value = data.get(name)
            if value is not None and not _is_dynamic(value) and allowed and value not in allowed:
                self._error("invalid-attribute-value",
                            f"Invalid {name}='{value}'; expected one of: {', '.join(allowed)}.",
                            line, col)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def validate_html(html: str, contract: dict, *, stylesheets: set[str] | None = None) -> list[dict]:
    """Return deterministic diagnostics for literal HTML.

    When no Syntyr stylesheet is linked and none is explicitly provided,
    treat input as a partial HTML fragment and skip module presence checks.
    """
    parser = _SyntyrParser(contract)
    parser.feed(html)
    parser.close()
    loaded = parser.linked_stylesheets if stylesheets is None else stylesheets
    if loaded:
        for line, col, name in parser.used_classes:
            expected = set(parser.classes[name]["stylesheets"])
            if not expected.intersection(loaded):
                hint = ", ".join(sorted(expected, key=lambda n: (n.count("/"), len(n)))[:3])
                parser._error("missing-stylesheet",
                              f"'{name}' is not in the loaded Syntyr CSS; add {hint}.",
                              line, col)
    return sorted(parser.diagnostics, key=lambda d: (d["line"], d["column"],
                                                    d["code"] == "missing-stylesheet"))


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Validate literal Syntyr classes and states in HTML.")
    p.add_argument("files", nargs="+", type=Path, help="Static HTML files to check.")
    p.add_argument("--format", choices=("text", "json"), default="text")
    p.add_argument("--stylesheets", action="append", default=None,
                   help="Known loaded Syntyr stylesheets, comma-separated; overrides HTML links.")
    p.add_argument("--contract", type=Path, default=CONTRACT)
    args = p.parse_args(argv)
    try:
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
        configured = None
        if args.stylesheets is not None:
            configured = set()
            for value in args.stylesheets:
                for item in value.split(","):
                    found = _stylesheet_name(item.strip(), set(contract["stylesheets"]))
                    if found is None:
                        p.error(f"Unrecognized Syntyr stylesheet: {item}")
                    configured.add(found)
        results = []
        for file in args.files:
            diagnostics = validate_html(file.read_text(encoding="utf-8"), contract,
                                        stylesheets=configured)
            results += [{"file": str(file), **diag} for diag in diagnostics]
    except (OSError, UnicodeError, ValueError, KeyError) as exc:
        print(f"syntyr check: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        for diag in results:
            print(f"{diag['file']}:{diag['line']}:{diag['column']}: "
                  f"{diag['severity']} [{diag['code']}]: {diag['message']}")
        if not results:
            print(f"OK: {len(args.files)} file(s) checked")
    return 1 if results else 0


if __name__ == "__main__":
    sys.exit(main())
