"""The optional docs editor browser runner supports an existing local browser."""
from pathlib import Path
from unittest.mock import patch
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('theme_editor_runner', ROOT / 'tests/theme_editor_browser.py')
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class ThemeEditorRunnerContract(unittest.TestCase):
    def test_respects_explicit_chromium_binary(self):
        with patch.dict('os.environ', {'PLAYWRIGHT_CHROMIUM_EXECUTABLE': '/usr/bin/custom-chrome'}):
            opts = RUNNER.chromium_launch_options()
        self.assertEqual(opts['executable_path'], '/usr/bin/custom-chrome')
        self.assertTrue(opts['headless'])


if __name__ == '__main__':
    unittest.main()
