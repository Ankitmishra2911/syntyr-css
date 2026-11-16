"""Portable static-site deployment adapters: deterministic and fail-closed."""
from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from static_deploy import (  # noqa: E402
    DeploymentError,
    CloudflareDirectoryProvider,
    NulangCloudBundleProvider,
    StaticSite,
    validate_site_url,
)


class StaticDeployTests(unittest.TestCase):
    def sample(self, root: Path) -> Path:
        site = root / "site"
        (site / "css").mkdir(parents=True)
        (site / "index.html").write_bytes(b"<h1>Syntyr</h1>")
        (site / "css/site.css").write_bytes(b"body{}")
        return site

    def test_cloudflare_adapter_stages_exact_site_without_mutating_source(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            site = self.sample(root)
            (site / "_headers").write_text("/*\n  X-Content-Type-Options: nosniff\n")
            source = StaticSite.load(site)
            target = root / "published"
            receipt = CloudflareDirectoryProvider().prepare(source, target, "https://example.com")
            self.assertEqual(receipt["provider"], "cloudflare")
            self.assertEqual((target / "css/site.css").read_bytes(), b"body{}")
            self.assertEqual((target / "_headers").read_bytes(), (site / "_headers").read_bytes())
            self.assertFalse((target / "syntyr-deploy.json").exists())

    def test_nulang_bundle_is_deterministic_and_records_content_hashes(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            site = StaticSite.load(self.sample(root))
            a, b = root / "one.zip", root / "two.zip"
            provider = NulangCloudBundleProvider()
            receipt = provider.prepare(site, a, "https://demo.example")
            provider.prepare(site, b, "https://demo.example")
            self.assertEqual(a.read_bytes(), b.read_bytes())
            self.assertEqual(receipt["status"], "prepared_only")
            with ZipFile(a) as archive:
                manifest = json.loads(archive.read("syntyr-deploy.json"))
                self.assertEqual(manifest["schema"], "syntyr.static-site.bundle/v1")
                self.assertEqual(manifest["origin"], "https://demo.example")
                self.assertEqual(manifest["files"][0]["path"], "css/site.css")
                self.assertEqual(len(manifest["files"][0]["sha256"]), 64)
                self.assertEqual(archive.read("site/index.html"), b"<h1>Syntyr</h1>")

    def test_nulang_refuses_cloudflare_specific_headers(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            site = self.sample(root)
            (site / "_headers").write_text("/*\n  X-Frame-Options: DENY\n")
            with self.assertRaisesRegex(DeploymentError, "Cloudflare"):
                NulangCloudBundleProvider().prepare(StaticSite.load(site), root / "site.zip", "https://example.com")

    def test_rejects_symlinks_and_secret_files_before_staging(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            site = self.sample(root)
            (site / ".env").write_text("SECRET=example")
            with self.assertRaisesRegex(DeploymentError, "disallowed"):
                StaticSite.load(site)
            (site / ".env").unlink()
            (site / "css/leak.css").symlink_to(site / "index.html")
            with self.assertRaisesRegex(DeploymentError, "symlink"):
                StaticSite.load(site)

    def test_refuses_repository_root_and_overwriting_targets(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaises(DeploymentError):
                StaticSite.load(ROOT)
            site = StaticSite.load(self.sample(root))
            target = root / "published"
            target.mkdir()
            with self.assertRaisesRegex(DeploymentError, "exists"):
                CloudflareDirectoryProvider().prepare(site, target, "https://example.com")

    def test_rejects_output_path_that_resolves_inside_source(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            site = StaticSite.load(self.sample(root))
            (root / "alternate").mkdir()
            # A lexical prefix check is insufficient when an existing directory
            # component and .. resolve back inside the source tree.
            disguised = root / "alternate" / ".." / "site" / "nested-output"
            with self.assertRaisesRegex(DeploymentError, "outside"):
                CloudflareDirectoryProvider().prepare(site, disguised, "https://example.com")
            self.assertFalse((site.source / "nested-output").exists())

    def test_url_validation_rejects_paths_and_non_https(self):
        for url in ("http://example.com", "https://example.com/path", "https://user:pass@example.com",
                    "https://example.com/?q=1", "https://example.com/#anchor", "file:///tmp/site"):
            with self.subTest(url=url), self.assertRaises(DeploymentError):
                validate_site_url(url)
        self.assertEqual(validate_site_url("https://demo.example/"), "https://demo.example")

    def test_cli_is_experimental_and_refuses_live_publish(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            site = self.sample(root)
            command = [sys.executable, str(ROOT / "scripts/static_deploy.py"),
                       "--provider", "nulang-cloud", "--site-dir", str(site),
                       "--site-url", "https://demo.example",
                       "--output", str(root / "site.zip")]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("experimental", result.stderr.lower())
            result = subprocess.run(command + ["--experimental-nulang-cloud", "--publish"],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not supported", result.stderr.lower())
            self.assertFalse((root / "site.zip").exists())
            result = subprocess.run(command + ["--experimental-nulang-cloud"],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "site.zip").is_file())


class PortableBuildTests(unittest.TestCase):
    def test_site_export_supports_custom_origin_without_cloudflare_headers(self):
        from build_cloudflare_site import source_files
        files = source_files(site_url="https://demo.example", include_cloudflare_headers=False)
        self.assertNotIn("_headers", files)
        self.assertIn(b"https://demo.example/sitemap.xml", files["robots.txt"])
        self.assertIn(b"https://demo.example", files["sitemap.xml"])
        self.assertNotIn(b"https://syntyr-css.pages.dev", files["sitemap.xml"])
        self.assertIn(b'https://demo.example/', files["index.html"])


if __name__ == "__main__":
    unittest.main()
