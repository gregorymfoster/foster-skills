import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('render_deck.py')
spec = importlib.util.spec_from_file_location('renderer', SCRIPT)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

PNG = bytes.fromhex('89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000d49444154789c6360000002000154a24f5d0000000049454e44ae426082')


def status(title='Search is live'):
    return dict(kind='status', title=title, lede='Internal users can search.', points=[dict(text='Index built', state='done')])


def decision(identifier='db', timing='upcoming'):
    d = dict(kind='decision', id=identifier, timing=timing, question='Which database?', context='We need one by Friday.', options=[dict(label='SQLite', consequence='Simple.'), dict(label='Postgres', consequence='Scales.')], recommended=1, recommendation='We will need concurrency.', default='I go with Postgres.', reversibility='costly')
    if timing == 'made':
        d['current'] = 0
    return d


def deck():
    return dict(project='Search', project_id='search', window='Since Oct 17', headline='Search works for staff.', next=['Ranking tweaks'], slides=[status(), decision('keep', 'made'), dict(kind='visual', title='The results page', lede='It looks like this.', visual=dict(type='flow', steps=[dict(label='Query'), dict(label='Rank', state='moving')])), decision()])


class DeckTests(unittest.TestCase):
    def test_valid_deck_passes_without_errors(self):
        data, warnings = r.validate(deck())
        self.assertFalse(any('decision' in w or 'visual slide' in w for w in warnings))
        self.assertEqual(data['seconds'], 20 + 35 + 50 + 35 + 50 + 25)

    def test_decisions_must_be_interleaved(self):
        data = deck()
        data['slides'] = [status('a'), status('b'), status('c'), decision()]
        with self.assertRaisesRegex(ValueError, 'in a row'):
            r.validate(data)
        data['slides'] = [status('a'), status('b'), decision('x'), status('c'), status('d'), decision('y')]
        r.validate(data)

    def test_deck_needs_a_decision_and_a_time_budget(self):
        data = deck()
        data['slides'] = [status('a'), status('b')]
        with self.assertRaisesRegex(ValueError, '3 to 10'):
            r.validate(data)
        data = deck()
        for slide in data['slides']:
            slide['seconds'] = 90
        data['slides'] += [status('e'), decision('z')]
        for slide in data['slides']:
            slide['seconds'] = 90
        with self.assertRaisesRegex(ValueError, 'five minutes'):
            r.validate(data)

    def test_decision_shape_is_enforced(self):
        bad = deck()
        bad['slides'][1].pop('current')
        with self.assertRaisesRegex(ValueError, 'current'):
            r.validate(bad)
        bad = deck()
        bad['slides'][3]['current'] = 0
        with self.assertRaisesRegex(ValueError, 'nothing is current'):
            r.validate(bad)
        bad = deck()
        bad['slides'][3]['recommended'] = 5
        with self.assertRaisesRegex(ValueError, 'recommended'):
            r.validate(bad)
        bad = deck()
        bad['slides'][3]['id'] = 'keep'
        with self.assertRaisesRegex(ValueError, 'unique'):
            r.validate(bad)
        bad = deck()
        bad['slides'][3]['evidence'] = [dict(label='x', url='javascript:alert(1)')]
        with self.assertRaisesRegex(ValueError, 'http'):
            r.validate(bad)

    def test_missing_timing_or_visual_only_warns(self):
        data = deck()
        data['slides'] = [status('a'), decision('x'), status('b'), decision('y')]
        _, warnings = r.validate(data)
        self.assertTrue(any('No made decision' in w for w in warnings))
        self.assertTrue(any('No visual' in w for w in warnings))

    def test_hostile_text_is_escaped_and_meta_cannot_close_script(self):
        data = deck()
        data['headline'] = '<script>alert(1)</script> @@SLIDES@@'
        data['slides'][3]['question'] = '</script><img src=x onerror=alert(1)>'
        data, _ = r.validate(data)
        data.update(deck_id='d1', created_at='2026-10-24T00:00:00')
        page = r.page(data)
        self.assertNotIn('<script>alert(1)', page)
        self.assertNotIn('<img src=x', page)
        self.assertIn('@@SLIDES@@', page)
        meta = page.split('<script type="application/json" id="meta">')[1].split('</script>')[0]
        self.assertEqual(json.loads(meta)['calls'][1]['question'], '</script><img src=x onerror=alert(1)>')

    def test_local_image_is_inlined(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'shot.png').write_bytes(PNG)
            data = deck()
            data['slides'][2]['visual'] = dict(type='image', src='shot.png', alt='Results page')
            data, _ = r.validate(data, Path(tmp))
            self.assertTrue(data['slides'][2]['visual']['src'].startswith('data:image/png;base64,'))
            data['slides'][2]['visual'] = dict(type='image', src='missing.png', alt='x')
            with self.assertRaisesRegex(ValueError, 'not found'):
                r.validate(data, Path(tmp))

    def test_gallery_bars_and_cover_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ('a.png', 'b.png'):
                (Path(tmp) / name).write_bytes(PNG)
            data = deck()
            data['what_it_is'] = 'A search box for the whole catalog.'
            data['hero'] = dict(src='a.png', alt='Search page')
            data['slides'][0]['visual'] = dict(type='bars', question='Seconds to find a product', bars=[dict(label='Old page', value=40), dict(label='Search', value=6, highlight=True)])
            data['slides'][0]['why'] = 'Staff stop asking engineers to look things up.'
            data['slides'][2] = dict(kind='visual', title='Results got clearer', lede='Before and after.', why='Fewer wrong clicks.', evidence=[dict(label='PR 41')], visual=dict(type='gallery', images=[dict(src='a.png', alt='Old', label='Before'), dict(src='b.png', alt='New', label='After')]))
            data, warnings = r.validate(data, Path(tmp))
            self.assertEqual(warnings, [])
            data.update(deck_id='d1', created_at='2026-10-24T00:00:00')
            page = r.page(data)
            self.assertIn('class="gallery"', page)
            self.assertIn('width:15.0%', page)
            self.assertIn('Why it matters', page)
            self.assertIn('A search box for the whole catalog.', page)
            self.assertIn('<details class="evidence">', page)
            bad = deck()
            bad['slides'][2]['visual'] = dict(type='gallery', images=[dict(src='a.png', alt='x', label='Only one')])
            with self.assertRaisesRegex(ValueError, '2 or 3'):
                r.validate(bad, Path(tmp))
            bad['slides'][2]['visual'] = dict(type='bars', question='q', bars=[dict(label='a', value=0), dict(label='b', value=0)])
            with self.assertRaisesRegex(ValueError, 'above zero'):
                r.validate(bad, Path(tmp))

    def test_insider_shorthand_and_missing_pictures_warn(self):
        data = deck()
        data['headline'] = 'Shipped 3d205ec with the new cull_rules in engine/src/cull.rs.'
        _, warnings = r.validate(data)
        self.assertTrue(any('commit hash' in w for w in warnings))
        data = deck()
        data['slides'] = [status('a'), decision('x'), status('b'), decision('y')]
        _, warnings = r.validate(data)
        self.assertTrue(any('have a picture' in w for w in warnings))
        self.assertTrue(any('why it matters' in w for w in warnings))

    def test_cli_archives_each_deck_and_finds_latest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'deck.json'
            source.write_text(json.dumps(deck()))
            archive = root / 'archive'
            outputs = []
            for _ in range(2):
                result = subprocess.run([sys.executable, str(SCRIPT), '--deck', str(source), '--archive', str(archive)], text=True, capture_output=True, check=True)
                outputs.append(json.loads(result.stdout))
            self.assertNotEqual(outputs[0]['deck'], outputs[1]['deck'])
            html = Path(outputs[1]['deck']).read_text()
            self.assertIn('Already made, reverse?', html)
            self.assertIn('In effect now', html)
            self.assertNotIn('@@', html)
            found = subprocess.run([sys.executable, str(SCRIPT), '--latest', 'search', '--archive', str(archive)], text=True, capture_output=True, check=True)
            self.assertEqual(found.stdout.strip(), outputs[1]['data'])

    def test_check_writes_nothing_and_repo_output_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '.git').mkdir()
            source = root / 'deck.json'
            source.write_text(json.dumps(deck()))
            checked = subprocess.run([sys.executable, str(SCRIPT), '--deck', str(source), '--check', '--archive', str(root / 'out')], text=True, capture_output=True, check=True)
            self.assertTrue(json.loads(checked.stdout)['ok'])
            refused = subprocess.run([sys.executable, str(SCRIPT), '--deck', str(source), '--archive', str(root / 'out')], text=True, capture_output=True)
            self.assertNotEqual(refused.returncode, 0)
            self.assertFalse((root / 'out').exists())


if __name__ == '__main__': unittest.main()
