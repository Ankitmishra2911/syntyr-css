"""Optional stdlib GET-server reference for Syntyr's OOH operations workspace.

Run: python3 examples/operations_workspace_server.py
No JavaScript, npm, third-party packages, authentication, or production data.
Application owners must supply authorization, live inventory, and map services.
"""
from __future__ import annotations

from dataclasses import dataclass
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit
import argparse

ROOT = Path(__file__).resolve().parents[1]
CSS_FILES = {
    "/dist/syntyr.core.css": ROOT / "dist/syntyr.core.css",
    "/dist/syntyr.recipes.css": ROOT / "dist/syntyr.recipes.css",
    "/dist/syntyr.workspaces.css": ROOT / "dist/syntyr.workspaces.css",
}
STATUS = {"available": ("Available", "success"), "booked": ("Booked", "warning"),
          "review": ("Needs review", "warning")}
FORMATS = {"static": "Static roadside", "digital": "Digital display"}


@dataclass(frozen=True)
class Asset:
    code: str
    name: str
    district: str
    kind: str
    status: str
    monthly: int
    x: int
    y: int


# Every label, price and location is fictional. Never confuse this with live OOH data.
ASSETS = (
    Asset("ES-024", "East Junction", "East district", "static", "available", 2400, 20, 25),
    Asset("CL-108", "Central Loop", "Central district", "digital", "booked", 4800, 75, 25),
    Asset("SX-061", "South Exchange", "South district", "static", "review", 1950, 53, 80),
    Asset("EV-035", "East Vista", "East district", "static", "available", 2200, 20, 58),
    Asset("MW-211", "Midway Screen", "Central district", "digital", "booked", 5200, 80, 63),
    Asset("NR-405", "North Ridge", "North district", "static", "available", 2800, 50, 12),
)


def filter_assets(query: str = "", status: str = "all", kind: str = "all") -> list[Asset]:
    needle = query.strip().casefold()
    return [
        asset for asset in ASSETS
        if (not needle or needle in f"{asset.name} {asset.district} {asset.code}".casefold())
        and (status == "all" or asset.status == status)
        and (kind == "all" or asset.kind == kind)
    ]


def _option(value: str, text: str, active: str) -> str:
    return f'<option value="{value}"{" selected" if value == active else ""}>{escape(text)}</option>'


def _query_link(query: str, status: str, kind: str, selected: str) -> str:
    return "/?" + escape(urlencode({"query": query, "status": status,
                                     "type": kind, "selected": selected}), quote=True) + "#selection"


def render_dashboard(query_string: str) -> str:
    """Render real server-owned filter/selection state without client JavaScript."""
    try:
        params = parse_qs(query_string, keep_blank_values=True, max_num_fields=20)
    except ValueError:
        params = {}

    def first(key: str) -> str:
        return (params.get(key, [""])[0] or "")[:120]

    query = first("query").strip()
    status = first("status") if first("status") in ("all", *STATUS) else "all"
    kind = first("type") if first("type") in ("all", *FORMATS) else "all"
    rows = filter_assets(query, status, kind)
    requested = first("selected")
    chosen = next((row for row in rows if row.code == requested), rows[0] if rows else None)
    available = sum(row.status == "available" for row in rows)

    markers = []
    records = []
    for index, asset in enumerate(rows, 1):
        selected = chosen == asset
        mark = ' data-syn-selected="true"' if selected else ""
        current = ' aria-current="true"' if selected else ""
        label, variant = STATUS[asset.status]
        link = _query_link(query, status, kind, asset.code)
        markers.append(
            f'<a class="syn-ops-marker" style="--syn-marker-x:{asset.x}%; --syn-marker-y:{asset.y}%"'
            f' href="{link}"{mark}{current} aria-label="Select {escape(asset.name)}">{index:02}</a>'
        )
        records.append(
            f'<li><article id="asset-{escape(asset.code)}" class="syn-ops-record"{mark}'
            f' aria-labelledby="title-{escape(asset.code)}">'
            f'<div class="syn-ops-record-head"><h3 class="syn-heading" id="title-{escape(asset.code)}">'
            f'{escape(asset.name)}</h3><span class="syn-status syn-status--{variant}">{label}</span></div>'
            f'<p class="syn-caption">{escape(asset.code)} · {FORMATS[asset.kind]} · {escape(asset.district)}</p>'
            f'<div class="syn-ops-record-foot"><strong>${asset.monthly:,} / month</strong>'
            f'<a href="{link}">{"Selected asset" if selected else "View asset details"}</a></div>'
            f'</article></li>'
        )

    if chosen is None:
        inspector = ""
        empty = '<p class="syn-app-card" role="status">No assets match your filters. Adjust the search or status.</p>'
    else:
        label, variant = STATUS[chosen.status]
        inspector = f"""
          <article class="syn-ops-inspector" id="selection" tabindex="-1" aria-labelledby="selection-title">
            <p class="syn-eyebrow">SELECTED / {escape(chosen.code)}</p>
            <h2 class="syn-heading" id="selection-title">{escape(chosen.name)}</h2>
            <p class="syn-muted">{escape(chosen.district)} · {FORMATS[chosen.kind]}</p>
            <dl class="syn-record-fields">
              <div><dt>Availability</dt><dd>{label}</dd></div>
              <div><dt>Format</dt><dd>{FORMATS[chosen.kind]}</dd></div>
              <div><dt>Reference</dt><dd>{escape(chosen.code)}</dd></div>
              <div><dt>Sample monthly rate</dt><dd>${chosen.monthly:,}</dd></div>
            </dl>
            <span class="syn-status syn-status--{variant}">{label}</span>
          </article>"""
        empty = ""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Fictional OOH inventory dashboard rendered with Syntyr CSS and the Python standard library.">
  <title>Syntyr — Server-rendered inventory workspace</title>
  <link rel="stylesheet" href="/dist/syntyr.core.css">
  <link rel="stylesheet" href="/dist/syntyr.recipes.css">
  <link rel="stylesheet" href="/dist/syntyr.workspaces.css">
</head>
<body class="syn-root syn-page" data-syn-theme="studio" data-syn-density="compact">
  <a href="#main" class="syn-button">Skip to workspace</a>
  <div class="syn-app-shell">
    <aside class="syn-app-rail" aria-label="Workspace sidebar">
      <p class="syn-logo">SYNTYR / OPS</p>
      <nav class="syn-app-nav" aria-label="Workspace sections">
        <a href="#main" aria-current="page">Inventory</a>
        <a href="#results">Results</a>
        <a href="#about">Implementation notes</a>
      </nav>
      <p class="syn-caption">SAMPLE DATA / LOCAL REFERENCE</p>
    </aside>
    <main id="main" class="syn-workspace">
      <header class="syn-app-topbar">
        <div>
          <p class="syn-eyebrow">OOH / INVENTORY OPERATIONS</p>
          <h1 class="syn-title">Asset availability workspace</h1>
          <p class="syn-muted">Sample data, fictional assets and prices. No production connection.</p>
        </div>
      </header>
      <section class="syn-kpi-grid" aria-label="Filtered inventory summary">
        <article class="syn-app-card"><span class="syn-stat-label">TOTAL SAMPLE ASSETS</span>
          <p class="syn-stat-value">{len(ASSETS)}</p></article>
        <article class="syn-app-card"><span class="syn-stat-label">MATCHING FILTERS</span>
          <p class="syn-stat-value">{len(rows)}</p></article>
        <article class="syn-app-card"><span class="syn-stat-label">AVAILABLE IN RESULTS</span>
          <p class="syn-stat-value">{available}</p></article>
      </section>
      <form class="syn-filter-bar syn-app-card" method="get" action="/" role="search" aria-label="Filter example inventory">
        <label class="syn-filter-field syn-filter-field--query" for="filter-query">
          Search inventory
          <input class="syn-input" id="filter-query" name="query" type="search" value="{escape(query, quote=True)}"
            maxlength="120" placeholder="Name, district or reference">
        </label>
        <label class="syn-filter-field" for="filter-status">
          Availability
          <select class="syn-select" id="filter-status" name="status">
            {_option("all", "All statuses", status)}
            {''.join(_option(value, label, status) for value, (label, _) in STATUS.items())}
          </select>
        </label>
        <label class="syn-filter-field" for="filter-type">
          Format
          <select class="syn-select" id="filter-type" name="type">
            {_option("all", "All formats", kind)}
            {''.join(_option(value, label, kind) for value, label in FORMATS.items())}
          </select>
        </label>
        <div class="syn-filter-actions">
          <button type="submit" class="syn-button syn-button--primary">Apply filters</button>
          <a href="/" class="syn-button syn-button--outline">Clear</a>
        </div>
      </form>
      <p role="status" class="syn-caption">Showing {len(rows)} of {len(ASSETS)} sample assets; filters and selected records are rendered by the local server.</p>
      <div class="syn-ops-workspace">
        <section class="syn-ops-stage" aria-label="Coverage preview and selected inventory">
          <figure class="syn-ops-map" aria-label="Illustrative map markers">
            <figcaption class="syn-ops-map-label">Fictional marker positions — not a geographic map</figcaption>
            {''.join(markers)}
          </figure>
          {inspector}
        </section>
        <section class="syn-ops-results" id="results" tabindex="0" aria-label="Inventory results">
          <header class="syn-ops-results-header">
            <h2 class="syn-heading">Inventory results</h2>
            <span class="syn-caption">{len(rows)} matching records</span>
          </header>
          {empty}
          <ul class="syn-ops-list">{''.join(records)}</ul>
        </section>
      </div>
      <section class="syn-app-card syn-ops-notes" id="about" aria-labelledby="about-heading">
        <h2 class="syn-heading" id="about-heading">Implementation notes</h2>
        <p>GET filters and selection use the Python standard library and normal hyperlinks.
        Syntyr provides CSS only; no client-side scripts or build tooling are required.</p>
        <p>This demonstration has no authentication, real map data, booking logic or multi-tenant isolation.
        Integrate backend authorization, inventory sources and transaction safety before production use.</p>
      </section>
    </main>
  </div>
</body>
</html>"""


class WorkspaceHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parts = urlsplit(self.path)
        if parts.path in CSS_FILES:
            path = CSS_FILES[parts.path]
            if not path.is_file():
                self.send_error(404)
                return
            content, media = path.read_bytes(), "text/css; charset=utf-8"
        elif parts.path == "/":
            content = render_dashboard(parts.query).encode("utf-8")
            media = "text/html; charset=utf-8"
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", media)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy",
                         "default-src 'none'; style-src 'self' 'unsafe-inline'; "
                         "form-action 'self'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, *_args):
        pass


def create_server(host: str = "127.0.0.1", port: int = 8765) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), WorkspaceHandler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    with create_server(port=args.port) as server:
        print(f"Open http://127.0.0.1:{server.server_port}/ (Ctrl+C to stop)", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
