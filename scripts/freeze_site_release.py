"""Freeze a new SYNTYR CDN release once; never overwrite published assets."""
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
manifest_path = ROOT / "site-releases/manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
target = manifest_path.parent / version
if not version or "/" in version or "\\" in version or version in {".", ".."}:
    sys.exit("Invalid version")
if version in manifest or target.exists():
    sys.exit(f"Release {version} already frozen; bump VERSION for a new release")
assets = sorted((ROOT / "dist").glob("syntyr*.css"))
if not assets:
    sys.exit("No CSS distributions to freeze")
target.mkdir(parents=True, exist_ok=False)
manifest[version] = {}
for path in assets:
    data = path.read_bytes()
    (target / path.name).write_bytes(data)
    manifest[version][path.name] = hashlib.sha256(data).hexdigest()
manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
print(f"Frozen {len(assets)} CSS files for {version}")
