"""Contract tests for Syntyr's opt-in Expo native integration smoke fixture."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples/expo-native-smoke"


class ExpoNativeSmokeTest(unittest.TestCase):
    def test_fixture_uses_official_expo_sdk_with_no_native_core_dependency(self):
        package = json.loads((FIXTURE / "package.json").read_text())
        self.assertTrue(package["private"])
        self.assertTrue(package["dependencies"]["expo"].startswith("~58."))
        self.assertTrue(package["dependencies"]["react-native"].startswith("0.88."))
        for name in ("sync", "typecheck", "test", "export:android", "export:ios"):
            self.assertIn(name, package["scripts"])
        core = json.loads((ROOT / "package.json").read_text())
        self.assertNotIn("expo", core.get("dependencies", {}))
        self.assertNotIn("react-native", core.get("dependencies", {}))
        self.assertNotIn("jest", core.get("devDependencies", {}))

    def test_source_sync_reuses_exact_canonical_adapter(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run(
                ["node", str(FIXTURE / "scripts/sync-adapter.mjs"), "--output", temp],
                cwd=FIXTURE, capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            target = Path(temp)
            for file in ("tokens.ts", "styles.ts"):
                self.assertEqual(
                    (target / file).read_bytes(),
                    (ROOT / "integrations/react-native" / file).read_bytes(),
                )
            source = (ROOT / "examples/react-native/App.tsx").read_text()
            rewritten = source.replace("../../integrations/react-native/", "./")
            self.assertEqual((target / "App.tsx").read_text(), rewritten)

    def test_fixture_has_native_interaction_tests_and_platform_exports(self):
        test = (FIXTURE / "App.test.tsx").read_text()
        for fragment in ("fireEvent.press", "fireEvent.changeText", "getByLabelText",
                         "getByRole", "Submitted 1 time(s)"):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, test)
        package = json.loads((FIXTURE / "package.json").read_text())
        self.assertIn("--platform android", package["scripts"]["export:android"])
        self.assertIn("--platform ios", package["scripts"]["export:ios"])
        self.assertTrue((FIXTURE / "package-lock.json").is_file())
        if (ROOT / ".git").exists():
            tracked_lock = subprocess.run(
                ["git", "ls-files", "--error-unmatch", "examples/expo-native-smoke/package-lock.json"],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(tracked_lock.returncode, 0, "npm ci requires the lockfile to be committed")
        self.assertTrue((FIXTURE / "tsconfig.json").is_file())
        self.assertTrue((FIXTURE / "index.ts").is_file())
        self.assertTrue((FIXTURE / "README.md").is_file())
        self.assertTrue((FIXTURE / ".gitignore").is_file())


if __name__ == "__main__":
    unittest.main()
