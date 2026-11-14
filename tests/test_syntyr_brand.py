"""SYNTYR packaging, branding and stable source API contract."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
MODULES = ('core','semantic','effects','recipes','all')

class SyntyrBrandTests(unittest.TestCase):
    def test_public_site_and_package_use_current_brand(self):
        for rel in ('index.html','docs/index.html','docs/console-kit.html'):
            with self.subTest(page=rel):
                text = (ROOT/rel).read_text()
                self.assertIn('SYNTYR', text)
                self.assertIn('syn-', text)

    def test_current_stylesheet_paths_are_built_and_tracked(self):
        tracked = subprocess.check_output(
            ['git','ls-files','--','dist/'], cwd=ROOT, text=True).splitlines()
        expected = {f'dist/syntyr{suffix}.css'
                    for suffix in ('','.core','.semantic','.effects','.recipes','.geometry','.all')}
        self.assertTrue(expected <= set(tracked), f'Git is missing {expected-set(tracked)}')
        self.assertEqual({p.as_posix().split('/')[-1]
                          for p in (ROOT/'dist').glob('*.css')},
                         {path.split('/')[-1] for path in expected})
        result = subprocess.run([sys.executable,'scripts/build.py','--check'],
                                cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_release_zip_is_syntyr_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp)/'release.zip'
            result = subprocess.run([sys.executable,'scripts/package_release.py',str(archive)],
                                    cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            with ZipFile(archive) as zip_file:
                names = zip_file.namelist()
                prefix = 'syntyr-css-0.3.0-alpha.4/'
                self.assertEqual(len(names),11)
                self.assertIn(prefix+'README.md',names)
                for suffix in ('','.core','.semantic','.effects','.recipes','.geometry','.all'):
                    self.assertIn(prefix+f'dist/syntyr{suffix}.css',names)

    def test_readme_explains_syn_namespace(self):
        readme=(ROOT/'README.md').read_text()
        self.assertTrue(readme.startswith('# SYNTYR CSS'))
        self.assertIn('syn-root',readme)
        self.assertIn('syntyr.core.css',readme)
        self.assertIn('dporkka/syntyr-css',readme)

if __name__ == '__main__':unittest.main()
