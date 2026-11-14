"""Report CSS transfer sizes without coupling releases to arbitrary byte ceilings.

Usage:
  python3 scripts/asset_report.py
  python3 scripts/asset_report.py --json > /tmp/syntyr-css-sizes.json
  python3 scripts/asset_report.py --baseline /tmp/previous-syntyr-css-sizes.json

No third-party packages, network requests, or build-time CSS transforms.
"""
from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

if __package__:
    from .build import DIST, distributions
else:
    from build import DIST, distributions


def measure_distributions(dist: Path = DIST) -> dict[str, dict]:
    """Measure the exact checked-in CSS files produced by build.py."""
    report = {}
    for filename, sources in sorted(distributions().items()):
        data = (dist / filename).read_bytes()
        report[filename] = {
            "raw_bytes": len(data),
            "gzip_bytes": len(gzip.compress(data, mtime=0)),
            "sources": list(sources),
        }
    return report


def compare_reports(current: dict, baseline: dict) -> dict[str, dict[str, int]]:
    """Return only comparable entries; reporting never fails on growth."""
    changes = {}
    for filename, current_entry in current.items():
        old = baseline.get(filename)
        if not isinstance(old, dict) or not all(
                isinstance(old.get(metric), int) for metric in ("raw_bytes", "gzip_bytes")):
            continue
        changes[filename] = {
            "raw_bytes_delta": current_entry["raw_bytes"] - old["raw_bytes"],
            "gzip_bytes_delta": current_entry["gzip_bytes"] - old["gzip_bytes"],
        }
    return changes


def render_report(current: dict, *, as_json: bool = False, baseline: dict | None = None) -> str:
    """Stable JSON for CI artifacts; readable console table for local feedback."""
    compared = compare_reports(current, baseline) if baseline is not None else None
    if as_json:
        document = {"distributions": current}
        if compared is not None:
            document["comparison"] = compared
        return json.dumps(document, indent=2, sort_keys=True) + "\n"

    lines = ["Syntyr CSS asset sizes (gzip uses deterministic stdlib compression)",
             "File                           Raw bytes    Gzip bytes   vs baseline"]
    for filename, entry in current.items():
        change = compared.get(filename) if compared is not None else None
        difference = f'{change["gzip_bytes_delta"]:+d}' if change is not None else "—"
        lines.append(f'{filename:<30} {entry["raw_bytes"]:>9} {entry["gzip_bytes"]:>13} {difference:>13}')
    lines.append("Informational measurements; no hard gzip cutoff or bundler required.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="write deterministic JSON to stdout")
    parser.add_argument("--baseline", type=Path, help="optional prior JSON report for size deltas")
    args = parser.parse_args()
    baseline = None
    if args.baseline:
        previous = json.loads(args.baseline.read_text(encoding="utf-8"))
        baseline = previous["distributions"]
        if not isinstance(baseline, dict):
            parser.error("baseline distributions must be an object")
    print(render_report(measure_distributions(), as_json=args.json, baseline=baseline), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
