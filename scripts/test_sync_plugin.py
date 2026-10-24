import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class PluginTests(unittest.TestCase):
    def test_generated_files_match_plugin_json(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'sync_plugin.py'), '--check'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_every_skill_is_discoverable(self):
        for skill in (ROOT / 'skills').iterdir():
            if not skill.is_dir():
                continue
            text = (skill / 'SKILL.md').read_text(encoding='utf-8')
            self.assertTrue(text.startswith('---\n'), skill.name)
            front = text.split('---\n')[1]
            self.assertIn(f'name: {skill.name}\n', front)
            self.assertIn('description: ', front)

    def test_plugin_json_has_shared_fields(self):
        plugin = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
        for field in ('name', 'displayName', 'version', 'description', 'author'):
            self.assertIn(field, plugin)


if __name__ == '__main__': unittest.main()
