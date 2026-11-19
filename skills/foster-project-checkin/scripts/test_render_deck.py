import copy
import html
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


STATS = dict(type='stats', stats=[dict(value='6 s', label='to find a product', change='down from 40 s', tone='good')])


def status(title='Search is live'):
    return dict(kind='status', title=title, lede='Internal users can search.', points=[dict(text='Index built', state='done')], visual=copy.deepcopy(STATS))


def decision(identifier='db', timing='upcoming'):
    d = dict(kind='decision', id=identifier, timing=timing, question='Which database?', context='We need one by Friday.', options=[dict(label='SQLite', consequence='Simple.'), dict(label='Postgres', consequence='Scales.')], recommended=1, recommendation='We will need concurrency.', default='I go with Postgres.', reversibility='costly')
    if timing == 'made':
        d['current'] = 0
    return d


MISSION = dict(statement='Staff find any product in seconds.', roadmap=[dict(label='Staff search', state='done'), dict(label='Customer search', state='next')], clarity='confirmed', source='Kickoff notes')


NO_DATA = dict(status='no-data', goal='Staff find a product in under 10 seconds', searched=['Connected analytics tools', 'Event calls in the code'])


def deck():
    return dict(project='Search', project_id='search', window='Since Oct 17', headline='Search works for staff.', next=['Ranking tweaks'], usage=copy.deepcopy(NO_DATA), mission=copy.deepcopy(MISSION), slides=[status(), decision('keep', 'made'), dict(kind='visual', title='The results page', lede='It looks like this.', visual=dict(type='flow', steps=[dict(label='Query'), dict(label='Rank', state='moving')])), decision()])


class DeckTests(unittest.TestCase):
    def test_valid_deck_passes_without_errors(self):
        data, warnings = r.validate(deck())
        self.assertFalse(any('decision' in w or 'visual slide' in w for w in warnings))
        self.assertEqual(data['seconds'], 20 + 25 + 40 + 25 + 40 + 20)

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
        with self.assertRaisesRegex(ValueError, '3 to 6'):
            r.validate(data)
        data['length'] = 'full'
        with self.assertRaisesRegex(ValueError, '3 to 12'):
            r.validate(data)
        data = deck()
        data['slides'] += [status('e'), decision('z')]
        for slide in data['slides']:
            slide['seconds'] = 90
        with self.assertRaisesRegex(ValueError, 'a short check-in fits in 250'):
            r.validate(data)

    def test_a_check_in_is_short_unless_asked_for_the_full_one(self):
        data = deck()
        data['slides'] = [status('a'), decision('x'), status('b'), decision('y'), status('c'), decision('z'), status('d')]
        with self.assertRaisesRegex(ValueError, 'set length to full'):
            r.validate(data)
        data['length'] = 'full'
        validated, warnings = r.validate(data)
        self.assertTrue(any('No mock' in w for w in warnings))
        data['length'] = 'long'
        with self.assertRaisesRegex(ValueError, 'length must be'):
            r.validate(data)
        # A short deck picks its slides, so it is not nagged to include every kind.
        validated, warnings = r.validate(deck())
        self.assertEqual(validated['length'], 'short')
        self.assertFalse(any(w.startswith('No ') for w in warnings))

    def test_call_small_print_folds_into_details(self):
        data, _ = r.validate(deck())
        data.update(deck_id='d1', created_at='2026-10-24T00:00:00')
        page = r.page(data)
        call = page.split('data-id="keep"')[1].split('</section>')[0]
        shown, folded = call.split('<details class="more">')
        self.assertIn("Why I'd pick B", shown)
        self.assertIn('Gets costly to change', shown)
        self.assertNotIn('I go with Postgres.</dd>', shown)
        self.assertIn('weigh in</dt><dd>I go with Postgres.', folded)

    def test_renderer_version_matches_the_plugin(self):
        plugin = json.loads((SCRIPT.parents[3] / 'plugin.json').read_text())
        self.assertEqual(r.VERSION, plugin['version'], 'Bump VERSION in render_deck.py with plugin.json.')

    def test_skipped_fit_check_says_so(self):
        import shutil
        original = shutil.which
        try:
            r.shutil.which = lambda name: None
            lines, note = r.fit_check(Path('deck.html'))
        finally:
            r.shutil.which = original
        self.assertIsNone(lines)
        self.assertIn('Fit not checked', note)

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
        data['length'] = 'full'
        data['slides'] = [status('a'), decision('x'), status('b'), decision('y')]
        _, warnings = r.validate(data)
        self.assertTrue(any('No made decision' in w for w in warnings))
        self.assertTrue(any('No visual' in w for w in warnings))

    def test_every_information_slide_needs_a_picture(self):
        data = deck()
        data['slides'][0].pop('visual')
        with self.assertRaisesRegex(ValueError, 'no picture'):
            r.validate(data)

    def test_words_are_capped_per_field_and_per_slide(self):
        data = deck()
        data['slides'][0]['lede'] = ' '.join(['word'] * 23)
        with self.assertRaisesRegex(ValueError, 'lede is 23 words; keep it to 22'):
            r.validate(data)
        data = deck()
        data['headline'] = ' '.join(['word'] * 19)
        with self.assertRaisesRegex(ValueError, 'headline is 19 words'):
            r.validate(data)
        data = deck()
        data['slides'][1]['options'][0]['consequence'] = ' '.join(['word'] * 15)
        with self.assertRaisesRegex(ValueError, 'option consequence is 15 words'):
            r.validate(data)
        data = deck()
        data['slides'][2]['visual']['steps'][0]['detail'] = ' '.join(['word'] * 9)
        with self.assertRaisesRegex(ValueError, 'step detail is 9 words'):
            r.validate(data)
        # Each field fits, but together they put too much in front of the director.
        data = deck()
        full = data['slides'][1]
        full['options'] = [dict(label=' '.join(['opt'] * 5), consequence=' '.join(['word'] * 14)) for _ in range(4)]
        full['context'] = ' '.join(['word'] * 28)
        full['recommendation'] = ' '.join(['word'] * 20)
        with self.assertRaisesRegex(ValueError, 'Slide 2 puts .* words in front of the director; a decision slide holds 120'):
            r.validate(data)
        data = deck()
        data['slides'][0]['points'] = [dict(text='x')] * 4
        with self.assertRaisesRegex(ValueError, 'at most 3'):
            r.validate(data)
        data = deck()
        data['next'] = ['a'] * 5
        with self.assertRaisesRegex(ValueError, 'four items'):
            r.validate(data)
        for field in ('body', 'progress'):
            data = deck()
            (data['slides'][0] if field == 'body' else data['mission'])[field] = 'An extra paragraph.'
            with self.assertRaisesRegex(ValueError, 'does not know'):
                r.validate(data)

    def test_slide_labels_live_in_the_bar_and_gaps_on_the_close(self):
        data = deck()
        data['gaps'] = ['Support tickets']
        data, _ = r.validate(data)
        data.update(deck_id='d1', created_at='2026-10-24T00:00:00')
        page = r.page(data)
        self.assertNotIn('<div class="eyebrow">Where things stand', page)
        self.assertIn('data-label="Where things stand"', page)
        self.assertIn('data-label="Call 1 · Already made, reverse?"', page)
        self.assertIn('<span class="label" id="label"></span>', page)
        self.assertIn('2 things need you, 1 of them about reversing something already in place. About 3 minutes.', page)
        cover, close = page.split('<section class="slide close')
        self.assertNotIn('Not checked', cover)
        self.assertIn('Not checked: Support tickets', close)
        self.assertIn('zoom:var(--fit,1)', page)

    def test_sample_deck_fits_every_slide_in_a_browser(self):
        # Needs Node with Playwright and its Chromium; otherwise the word caps are the only guard and this is skipped.
        probe = subprocess.run(['node', '-e', "require('playwright')"], capture_output=True)
        if probe.returncode != 0:
            self.skipTest('Playwright is not installed for Node.')
        sample = SCRIPT.parent.parent / 'assets' / 'sample' / 'deck.json'
        with tempfile.TemporaryDirectory() as tmp:
            run = subprocess.run([sys.executable, str(SCRIPT), '--deck', str(sample), '--archive', tmp], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            deck = json.loads(run.stdout)['deck']
            fit = subprocess.run(['node', str(SCRIPT.with_name('check_fit.js')), deck], capture_output=True, text=True, timeout=120)
            self.assertEqual(fit.returncode, 0, fit.stdout + fit.stderr)
            self.assertIn('1280x720: every slide fits', fit.stdout)

    def test_hostile_text_is_escaped_and_meta_cannot_close_script(self):
        data = deck()
        data['headline'] = '<script>alert(1)</script> @@SLIDES@@'
        data['slides'][3]['question'] = '</script><img src=x onerror=alert(1)>'
        data['project'] = '</script><img src=x onerror=alert(1)>'
        data, _ = r.validate(data)
        data.update(deck_id='d1', created_at='2026-10-24T00:00:00')
        page = r.page(data)
        self.assertNotIn('<script>alert(1)', page)
        self.assertNotIn('<img src=x', page)
        self.assertIn('@@SLIDES@@', page)
        meta = page.split('<script type="application/json" id="meta">')[1].split('</script>')[0]
        self.assertEqual(json.loads(meta)['project'], '</script><img src=x onerror=alert(1)>')
        self.assertIn('<h2>&lt;/script&gt;&lt;img src=x onerror=alert(1)&gt;</h2>', page)

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
            self.assertEqual([w for w in warnings if not w.startswith(('No mock', 'No research'))], [])
            data.update(deck_id='d1', created_at='2026-10-24T00:00:00')
            page = r.page(data)
            self.assertIn('class="gallery"', page)
            self.assertIn('width:15.0%', page)
            self.assertIn('Why it matters', page)
            self.assertIn('A search box for the whole catalog.', page)
            self.assertIn('2 things need you', page)
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
        self.assertTrue(any('why it matters' in w for w in warnings))

    def test_unknown_fields_are_refused(self):
        for mutate in (lambda d: d.update(style='dark'), lambda d: d['slides'][0].update(html='<b>x</b>'),
                       lambda d: d['slides'][2]['visual'].update(color='red'), lambda d: d['slides'][1]['options'][0].update(icon='x')):
            data = deck()
            mutate(data)
            with self.assertRaisesRegex(ValueError, 'does not know'):
                r.validate(data)

    def test_archived_deck_still_validates(self):
        data, _ = r.validate(deck())
        data.update(schema_version=1, deck_id='d1', created_at='2026-10-24T00:00:00', skill_version='1.1.0')
        r.validate(json.loads(json.dumps(data)))

    def test_question_slides_count_as_weighing_in(self):
        question = dict(kind='question', id='who', question='Which store matters most?', context='Two stores asked.', suggestions=['North', 'South'], default='I treat them the same.')
        data = deck()
        data['slides'] = [status('a'), status('b'), question, status('c'), decision()]
        data, _ = r.validate(data)
        self.assertEqual(data['seconds'], 20 + 25 + 25 + 30 + 25 + 40 + 20)
        data.update(deck_id='d1', created_at='2026-10-24T00:00:00')
        page = r.page(data)
        self.assertIn('Question 1', page)
        self.assertIn('class="chip"', page)
        self.assertIn('2 things need you. About 3 minutes.', page)
        # The page script reads calls from the markup, so the markup must carry them.
        self.assertIn('data-kind="question" data-label="Question 1 · Only you know this" data-id="who" data-default="I treat them the same."', page)
        self.assertIn('data-kind="decision" data-label="Call 1 · Coming up, your call" data-id="db" data-timing="upcoming" data-recommended="1" data-default="I go with Postgres."', page)
        self.assertNotIn('calls', page.split('<script type="application/json" id="meta">')[1].split('</script>')[0])
        data = deck()
        data['slides'] = [status('a'), question, status('b')]
        r.validate(data)
        data['slides'] = [status('a'), dict(question, id='a'), dict(question, id='b'), dict(question, id='c'), dict(question, id='d')]
        with self.assertRaisesRegex(ValueError, 'at most 3 open questions'):
            r.validate(data)
        data['slides'] = [status('a'), dict(question, suggestions=['x' * 61]), status('b')]
        with self.assertRaisesRegex(ValueError, 'suggestions'):
            r.validate(data)
        data['slides'] = [status('a'), dict(question, id='db'), decision('db')]
        with self.assertRaisesRegex(ValueError, 'unique'):
            r.validate(data)

    def test_line_stats_and_slider_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ('a.png', 'b.png'):
                (Path(tmp) / name).write_bytes(PNG)
            data = deck()
            data['slides'][0]['visual'] = dict(type='stats', stats=[dict(value='6 s', label='to find a product', change='down from 40 s', tone='good')])
            data['slides'][2]['visual'] = dict(type='line', question='Seconds to find a product', unit='s', x=['W1', 'W2', 'W3'], series=[dict(label='New', values=[30, None, 6]), dict(label='Old', values=[40, 41, 40])])
            data['slides'].append(dict(kind='visual', title='Before and after', lede='Drag to compare.', visual=dict(type='slider', before=dict(src='a.png', alt='Old', label='Before'), after=dict(src='b.png', alt='New', label='After'))))
            data, _ = r.validate(data, Path(tmp))
            data.update(deck_id='d1', created_at='2026-10-24T00:00:00')
            page = r.page(data)
            self.assertIn('class="stat tone-good"', page)
            chart = html.unescape(page.split('data-chart="')[1].split('"')[0])
            self.assertEqual(json.loads(chart)['series'][0], {'label': 'New', 'values': [30, None, 6]})
            self.assertIn('class="slider"', page)
            self.assertIn('data:image/png;base64,', page)
            bad = deck()
            bad['slides'][2]['visual'] = dict(type='line', question='q', x=['a', 'b'], series=[dict(label='x', values=[1])])
            with self.assertRaisesRegex(ValueError, 'one number'):
                r.validate(bad)
            bad['slides'][2]['visual'] = dict(type='line', question='q', x=['a', 'b'], series=[dict(label=str(i), values=[1, 2]) for i in range(4)])
            with self.assertRaisesRegex(ValueError, '1 to 3 series'):
                r.validate(bad)
            bad['slides'][2]['visual'] = dict(type='stats', stats=[dict(value='1', label='x', tone='great')])
            with self.assertRaisesRegex(ValueError, 'tone'):
                r.validate(bad)

    def usage_deck(self):
        data = deck()
        data['usage'] = dict(status='at-risk', goal='150 stores searching weekly by Dec 1', sources=[dict(name='Search event log', as_of='Oct 26')])
        data['slides'][2] = dict(kind='usage', data_from='search event log, Oct 1 to 26', title='112 stores search every week', lede='Growth flattened.', why='The gap is stores that never tried it.',
                                 points=[dict(text='Most stores come back', state='up'), dict(text='Two stores never report', state='data-gap')],
                                 visual=dict(type='goal', metric='Stores searching weekly', current=112, target=150, projected=130, by='Dec 1', status='at-risk'))
        return data

    def test_usage_slide_goal_and_cover_line_render(self):
        data, warnings = r.validate(self.usage_deck())
        self.assertFalse(any('goal' in w or 'usage' in w for w in warnings))
        self.assertEqual(data['seconds'], 20 + 25 + 40 + 30 + 40 + 20)
        data.update(deck_id='d1', created_at='2026-10-24T00:00:00')
        page = r.page(data)
        self.assertIn('data-label="What the usage data says · search event log, Oct 1 to 26"', page)
        self.assertIn('<i>data gap</i>', page)
        self.assertIn('class="goal goal-at-risk"', page)
        self.assertIn('width:74.7%', page)
        self.assertIn('left:86.7%', page)
        self.assertIn('112 of 150 by Dec 1, heading for 130', page)
        self.assertIn('<p class="usage-line usage-line-at-risk"><i>At risk</i><span>Goal: 150 stores searching weekly by Dec 1</span>', page)
        self.assertIn('Search event log (through Oct 26)', page)

    def test_goal_shape_is_enforced(self):
        for change, message in ((dict(status='fine'), 'status'), (dict(target=0), 'differ'), (dict(current='112'), 'current'), (dict(projected='x'), 'projected')):
            data = self.usage_deck()
            data['slides'][2]['visual'].update(change)
            with self.assertRaisesRegex(ValueError, message):
                r.validate(data)
        data = self.usage_deck()
        data['slides'][2]['visual'].update(current=5, target=1, baseline=10, unit='%')
        data, _ = r.validate(data)
        self.assertIn('5% of 1%', r.render_goal(data['slides'][2]['visual']))
        self.assertEqual(r.num(1250000), '1,250,000')
        self.assertEqual(r.num(0.125), '0.12')

    def test_usage_step_cannot_be_skipped_or_faked(self):
        data = deck()
        data.pop('usage')
        with self.assertRaisesRegex(ValueError, 'usage data step'):
            r.validate(data)
        data = self.usage_deck()
        data['slides'][2]['kind'] = 'status'
        data['slides'][2].pop('data_from')
        data['slides'][2]['points'] = []
        data['slides'][2]['visual'] = copy.deepcopy(STATS)
        with self.assertRaisesRegex(ValueError, 'give it a usage slide'):
            r.validate(data)
        data = self.usage_deck()
        data['usage'] = copy.deepcopy(NO_DATA)
        with self.assertRaisesRegex(ValueError, 'needs usage data'):
            r.validate(data)
        for usage, message in ((dict(NO_DATA, searched=[]), 'where you looked'), (dict(NO_DATA, sources=[dict(name='x')]), 'no sources'),
                               (dict(status='on-track', sources=[dict(name='Log')]), 'goal in words'), (dict(status='on-track', goal='g'), 'needs sources'),
                               (dict(status='booming', goal='g'), 'status must be'), (dict(NO_DATA, sources=[dict(name='x', rows=3)]), 'does not know')):
            data = deck()
            data['usage'] = usage
            with self.assertRaisesRegex(ValueError, message):
                r.validate(data)
        data = self.usage_deck()
        data['slides'][2]['points'][0]['state'] = 'done'
        with self.assertRaisesRegex(ValueError, 'point state'):
            r.validate(data)

    def test_data_that_exists_but_cannot_be_read_is_not_no_data(self):
        out_of_reach = dict(status='unreachable', goal='Staff find a product in under 10 seconds', searched=['Analytics dashboard (not connected to this session)'])
        data = deck()
        data['usage'] = copy.deepcopy(out_of_reach)
        data, _ = r.validate(data)
        data.update(deck_id='d1', created_at='2026-10-24T00:00:00')
        self.assertIn('<i>Usage not read</i>', r.page(data))
        self.assertIn('The data exists, but I could not read it: Analytics dashboard (not connected to this session)', r.page(data))
        for usage, message in ((dict(out_of_reach, searched=[]), 'out of reach'), (dict(out_of_reach, sources=[dict(name='x')]), 'out of reach')):
            data = deck()
            data['usage'] = usage
            with self.assertRaisesRegex(ValueError, message):
                r.validate(data)
        data = self.usage_deck()
        data['usage'] = copy.deepcopy(out_of_reach)
        with self.assertRaisesRegex(ValueError, 'needs usage data'):
            r.validate(data)

    def test_no_goal_means_asking_for_one(self):
        question = dict(kind='question', id='goal', question='Which number tells you this works?', context='Nothing sets a target yet.', suggestions=['Weekly stores', 'Time to find'], default='I track weekly stores.')
        data = deck()
        data['usage'] = dict(status='no-data', searched=['Connected tools'])
        with self.assertRaisesRegex(ValueError, 'no goal yet'):
            r.validate(data)
        data['slides'][3] = question
        data, _ = r.validate(data)
        data.update(deck_id='d1', created_at='2026-10-24T00:00:00')
        self.assertIn('<i>No usage data</i><span class="src">Nothing measures this yet. Looked in: Connected tools</span>', r.page(data))
        data = self.usage_deck()
        data['usage'] = dict(status='no-goal', sources=[dict(name='Log')])
        data['slides'][2]['visual'] = dict(type='bars', question='Stores per week', bars=[dict(label='Oct', value=112), dict(label='Sep', value=80)])
        data['slides'][3] = question
        _, warnings = r.validate(data)
        self.assertFalse(any('goal' in w for w in warnings))
        data['usage']['goal'] = 'g'
        with self.assertRaisesRegex(ValueError, 'no goal is agreed'):
            r.validate(data)
        data = self.usage_deck()
        data['slides'][2]['visual'] = dict(type='stats', stats=[dict(value='112', label='stores')])
        _, warnings = r.validate(data)
        self.assertTrue(any('goal visual' in w for w in warnings))

    def test_mission_is_on_every_cover_and_an_unsure_one_is_asked_first(self):
        data = deck()
        data.pop('mission')
        with self.assertRaisesRegex(ValueError, 'mission'):
            r.validate(data)
        data = deck()
        data['mission'].pop('source')
        with self.assertRaisesRegex(ValueError, 'source'):
            r.validate(data)
        data = deck()
        data['mission']['roadmap'][0]['state'] = 'soon'
        with self.assertRaisesRegex(ValueError, 'state'):
            r.validate(data)
        data = deck()
        data['mission']['clarity'] = 'inferred'
        with self.assertRaisesRegex(ValueError, 'id mission'):
            r.validate(data)
        ask = dict(kind='question', id='mission', question='Is this the goal?', context='I guessed it.', default='Keep it.')
        data['slides'].insert(0, ask)
        validated, _ = r.validate(data)
        validated.update(deck_id='d1', created_at='2026-10-27T00:00:00')
        page = r.page(validated)
        self.assertIn('class="mission mission-inferred"', page)
        self.assertIn('My reading. Confirm?', page)
        self.assertIn('class="road-done"', page)

    def test_mocks_and_user_research_render_as_calls(self):
        data = deck()
        mock = dict(kind='mock', id='lookalikes', title='Show in-stock lookalikes', lede='Sold-out items stop topping the list.', cost='Three days.', default='Park it.', visual=dict(type='image', src='data:image/png;base64,AA', alt='Mock'))
        research = dict(kind='research', id='users', title='Ask stores two things', lede='Each answer changes the plan.', default='Send the first.', asks=[dict(who='Managers', question='Why did you stop?', learn='Training or search.', how='Email'), dict(who='Night shift', question='What do you look up?', learn='A shortcut.', how='Poll')])
        data['slides'] = [status('a'), mock, status('b'), status('c'), research, decision()]
        validated, warnings = r.validate(data)
        self.assertFalse(any('No mock' in w or 'No research' in w for w in warnings))
        validated.update(deck_id='d1', created_at='2026-10-27T00:00:00')
        page = r.page(validated)
        self.assertIn('data-kind="mock"', page)
        self.assertIn('Build it', page)
        self.assertIn('class="ask-item" data-research="users"', page)
        self.assertIn('3 things need you', page)
        bad = copy.deepcopy(data)
        bad['slides'][1]['visual'] = dict(type='stats', stats=[dict(value='1', label='x')])
        with self.assertRaisesRegex(ValueError, 'picture of the idea'):
            r.validate(bad)
        bad = copy.deepcopy(data)
        bad['slides'][4]['asks'] = bad['slides'][4]['asks'][:1]
        with self.assertRaisesRegex(ValueError, '2 to 3 asks'):
            r.validate(bad)
        bad = copy.deepcopy(data)
        bad['slides'][4]['asks'][0]['extra'] = 1
        with self.assertRaisesRegex(ValueError, 'does not know'):
            r.validate(bad)
        bad = copy.deepcopy(data)
        bad['slides'] = [status('a'), mock, dict(mock, id='m2'), dict(mock, id='m3'), decision()]
        with self.assertRaisesRegex(ValueError, 'at most 2 mocks'):
            r.validate(bad)
        _, warnings = r.validate(dict(deck(), length='full'))
        self.assertTrue(any('No mock' in w for w in warnings))
        self.assertTrue(any('No research' in w for w in warnings))

    def test_sample_deck_renders_clean_with_shared_components(self):
        sample = SCRIPT.parent.parent / 'assets' / 'sample' / 'deck.json'
        data, warnings = r.validate(json.loads(sample.read_text()), sample.parent)
        self.assertEqual(warnings, [])
        data.update(deck_id='d1', created_at='2026-10-24T00:00:00')
        page = r.page(data)
        css = (SCRIPT.parent.parent / 'assets' / 'components' / 'deck.css').read_text()
        self.assertIn(css, page)
        self.assertNotIn('@@', page)


    def test_starter_deck_matches_the_renderer(self):
        starter = SCRIPT.parent.parent / 'assets' / 'starter.html'
        self.assertEqual(starter.read_text(), r.starter(), 'assets/starter.html is stale; run render_deck.py --starter')
        text = starter.read_text()
        for kind in r.VISUALS:
            self.assertIn(f'with a {kind} visual', text)
        for kind in ('decision slide (made)', 'decision slide (upcoming)', 'question slide', 'mock slide', 'research slide'):
            self.assertIn(kind, text)

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
            self.assertTrue(outputs[1]['open'].startswith('file://'))
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
