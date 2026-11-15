"""Optional static HTML renderer for a constrained nulang-ui/1 semantic subset.

Nulang's real compiler signal graph is *not* an HTML tree and is deliberately
unsupported. These semantic node kinds are this Syntyr adapter's opt-in
conventions, not guaranteed Nulang renderer behavior.
"""
from __future__ import annotations
import argparse
from html import escape
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "metadata/syntyr-contract.json"
MAX_NODES, MAX_DEPTH = 512, 64
CLASS_BY_KIND = {
    "column": "syn-stack", "row": "syn-actions", "panel": "syn-panel",
    "heading": "syn-heading", "text": None, "badge": "syn-badge",
    "metric": "syn-stat", "link": "syn-button",
}
EXTRA_CLASSES = {"syn-root", "syn-page", "syn-shell", "syn-stat-label", "syn-stat-value"}
LEAF_PROPERTIES = {
    "heading": {"text", "level"}, "text": {"text"}, "badge": {"text"},
    "metric": {"label", "value"}, "link": {"text", "href"},
}


class ProtocolError(ValueError):
    """Input is outside the supported static rendering protocol."""


def require(valid: bool, reason: str):
    if not valid:
        raise ProtocolError(reason)


def typed_property(node: dict, key: str, *, numeric: bool = False) -> str:
    value = node["properties"].get(key)
    require(isinstance(value, dict), f"{node['id']}: missing typed property '{key}'")
    wire_type, raw = value.get("type"), value.get("value")
    if wire_type == "string":
        require(isinstance(raw, str), f"{node['id']}: {key} must be a string")
        return raw
    if numeric and wire_type == "i64":
        require(isinstance(raw, str) and bool(re.fullmatch(r"-?(?:0|[1-9][0-9]*)", raw))
                and -(1 << 63) <= int(raw) < (1 << 63),
                f"{node['id']}: invalid lossless i64 for {key}")
        return raw
    raise ProtocolError(f"{node['id']}: unsupported wire value for {key}")


def safe_href(href: str, *, stylesheet: bool = False) -> bool:
    if not isinstance(href, str) or not href or href.strip() != href:
        return False
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in href) or "\\" in href or href.startswith("//"):
        return False
    try:
        parts = urlsplit(href)
    except ValueError:
        return False
    if parts.scheme or parts.netloc:
        if stylesheet or parts.scheme.lower() != "https" or not parts.netloc:
            return False
        return bool(re.fullmatch(r"[A-Za-z0-9.-]+(?::[0-9]{1,5})?", parts.netloc))
    return ":" not in href.split("/", 1)[0]


def validate_document(doc: dict) -> tuple[dict[str, dict], str]:
    require(isinstance(doc, dict), "expected an object")
    require(doc.get("protocol") == "nulang-ui/1", "unsupported protocol: expected nulang-ui/1")
    revision = doc.get("revision")
    require(isinstance(revision, str) and 1 <= len(revision) <= 20
            and bool(re.fullmatch("[0-9]+", revision)) and int(revision) < (1 << 64),
            "revision must be a decimal u64 string")
    require(isinstance(doc.get("document_id"), str) and bool(doc["document_id"].strip()),
            "missing document_id")
    root = doc.get("root")
    require(isinstance(root, str) and bool(root.strip()), "missing root id")
    nodes = doc.get("nodes")
    require(isinstance(nodes, list) and 0 < len(nodes) <= MAX_NODES,
            f"node list must contain 1..{MAX_NODES} items")
    by_id: dict[str, dict] = {}
    parents: dict[str, int] = {}
    for node in nodes:
        require(isinstance(node, dict), "node must be an object")
        nid, kind = node.get("id"), node.get("kind")
        require(isinstance(nid, str) and bool(nid.strip()), "empty node id")
        require(nid not in by_id, f"duplicate node id: {nid}")
        require(isinstance(kind, str) and kind in CLASS_BY_KIND,
                f"{nid}: unsupported node kind '{kind}' (interaction graphs are not HTML)")
        actions = node.get("actions", [])
        require(isinstance(actions, list), f"{nid}: actions must be a list")
        require(not actions, f"{nid}: action bindings require a real Nulang host")
        props, children = node.get("properties", {}), node.get("children", [])
        require(isinstance(props, dict), f"{nid}: properties must be an object")
        require(isinstance(children, list), f"{nid}: children must be an array")
        expected_props = LEAF_PROPERTIES.get(kind, set())
        require(set(props) == expected_props,
                f"{nid}: expected properties {sorted(expected_props)}, got {sorted(props)}")
        if kind in LEAF_PROPERTIES:
            require(not children, f"{nid}: leaf {kind} cannot have children")
        by_id[nid] = {"id": nid, "kind": kind, "properties": props, "children": children}
    require(root in by_id, f"missing root node {root}")
    for node in by_id.values():
        seen: set[str] = set()
        for child in node["children"]:
            require(isinstance(child, str) and child in by_id,
                    f"{node['id']}: dangling child {child!r}")
            require(child not in seen, f"{node['id']}: duplicate child {child}")
            seen.add(child)
            parents[child] = parents.get(child, 0) + 1
            require(parents[child] <= 1, f"{child}: multiple parents")
    require(root not in parents, "root cannot have a parent")
    visited: set[str] = set()
    stack = [(root, 0)]
    while stack:
        nid, depth = stack.pop()
        require(depth <= MAX_DEPTH, f"tree too deep (max {MAX_DEPTH})")
        require(nid not in visited, f"cycle or repeated node: {nid}")
        visited.add(nid)
        stack.extend((child, depth + 1) for child in by_id[nid]["children"])
    require(len(visited) == len(by_id), "orphan/unreachable nodes")
    return by_id, root


def render_document(
    doc: dict, contract: dict, *, theme: str = "studio",
    title: str = "Nulang UI — Syntyr", css_href: str = "../dist/syntyr.core.css",
) -> str:
    """Render semantic nodes as inert Syntyr-styled HTML; never execute actions."""
    by_id, root = validate_document(doc)
    require(theme in contract.get("themes", []), f"invalid Syntyr theme: {theme}")
    require(safe_href(css_href, stylesheet=True), "CSS stylesheet URL must be local and safe")
    available = {item["name"]: item for item in contract["classes"]}
    for name in EXTRA_CLASSES | set(filter(None, CLASS_BY_KIND.values())):
        item = available.get(name)
        require(item is not None and "syntyr.core.css" in item.get("stylesheets", []),
                f"required Syntyr class missing from contract: {name}")

    def node_html(nid: str) -> str:
        node = by_id[nid]
        kind = node["kind"]
        content = "".join(node_html(child) for child in node["children"])
        if kind == "column":
            return f'<div class="syn-stack">{content}</div>'
        if kind == "row":
            return f'<div class="syn-actions">{content}</div>'
        if kind == "panel":
            return f'<section class="syn-panel">{content}</section>'
        if kind == "heading":
            level = typed_property(node, "level", numeric=True)
            require(level in ("1", "2", "3"), f"{nid}: heading level must be 1..3")
            return f'<h{level} class="syn-heading">{escape(typed_property(node, "text"))}</h{level}>'
        if kind == "text":
            return f'<p>{escape(typed_property(node, "text"))}</p>'
        if kind == "badge":
            return f'<span class="syn-badge">{escape(typed_property(node, "text"))}</span>'
        if kind == "metric":
            label = escape(typed_property(node, "label"))
            value = escape(typed_property(node, "value", numeric=True))
            return (f'<section class="syn-stat" aria-label="{label}">'
                    f'<span class="syn-stat-label">{label}</span>'
                    f'<strong class="syn-stat-value">{value}</strong></section>')
        if kind == "link":
            href = typed_property(node, "href")
            require(safe_href(href), f"{nid}: unsafe link href")
            return f'<a class="syn-button" href="{escape(href, quote=True)}">{escape(typed_property(node, "text"))}</a>'
        raise ProtocolError(f"{nid}: unsupported node kind '{kind}'")

    content = node_html(root)
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'  <title>{escape(title)}</title>\n'
        f'  <link rel="stylesheet" href="{escape(css_href, quote=True)}">\n'
        '</head>\n'
        f'<body class="syn-root syn-page" data-syn-theme="{escape(theme, quote=True)}">\n'
        f'  <main class="syn-shell" aria-label="{escape(title, quote=True)}">{content}</main>\n'
        '</body>\n</html>\n'
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Optional Syntyr static renderer for a nulang-ui/1 document")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--contract", type=Path, default=CONTRACT)
    parser.add_argument("--theme", default="studio")
    parser.add_argument("--css", default="../dist/syntyr.core.css")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        document = json.loads(args.input.read_text(encoding="utf-8"))
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
        html = render_document(document, contract, theme=args.theme, css_href=args.css)
        if args.check:
            if not args.output.exists() or args.output.read_text(encoding="utf-8") != html:
                print(f"STALE: {args.output}", file=sys.stderr)
                return 1
            print(f"OK: {args.output}")
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(html, encoding="utf-8")
            print(f"WROTE: {args.output}")
        return 0
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as error:
        print(f"Nulang/Syntyr adapter: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
