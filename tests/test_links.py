import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_links.py"
spec = importlib.util.spec_from_file_location("link_checks", SCRIPT)
links = importlib.util.module_from_spec(spec)
spec.loader.exec_module(links)

class Links(unittest.TestCase):
    def test_current_entry_points_have_existing_local_file_targets(self):
        for name in links.CURRENT:
            self.assertEqual(links.check_file(links.ROOT / name, links.ROOT), [])

    def test_missing_and_outside_targets_fail_while_remote_urls_are_ignored(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "good.md").write_text("good")
            doc = root / "README.md"
            doc.write_text("[good](good.md) [missing](missing.md) [outside](../outside.md) [remote](https://example.org)")
            result = links.check_file(doc, root)
            self.assertEqual(len(result), 2)
            self.assertTrue(any("missing.md" in problem for problem in result))
            self.assertTrue(any("outside" in problem for problem in result))
