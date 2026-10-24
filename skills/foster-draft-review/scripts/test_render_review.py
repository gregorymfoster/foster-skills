import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

SCRIPT = Path(__file__).with_name('render_review.py')
spec = importlib.util.spec_from_file_location('renderer', SCRIPT)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


def feedback():
    return dict(title='An essay', essay_id='an-essay', draft_label='Draft 1', intent='Explore a question.', reader_response='A tension remains.', priorities=['Explore the tension.'], notes=[dict(id='n1', category='ideas', priority='high', tag='stakes', quote='same', occurrence=2, title='The return', observation='This repeats.', suggestion='What changes?')])


def structure_feedback():
    data = feedback()
    data.update(
        stage='structure',
        reverse_outline=[
            dict(label='Opening', job='Asks why.', diagnosis='Needs a scene.', quote='First thought.'),
            dict(label='Turn', job='Tests the idea.', diagnosis='Changes the question.', quote='Second thought.'),
        ],
        through_lines=[dict(title='Follow the question', question='Why?', use='The opening.', set_aside='The detour.', needs='An example.', recommended=True, selected=True)],
        patterns=[dict(title='A repeated move', evidence=['First thought.', 'Second thought.'], why='The reader waits for a new move.', practice='Give each paragraph a job.')],
        notes=[],
    )
    return data


class ReviewTests(unittest.TestCase):
    def test_ambiguous_and_missing_anchors_fail(self):
        data = feedback()
        del data['notes'][0]['occurrence']
        with self.assertRaisesRegex(ValueError, 'Ambiguous'):
            r.validate(data, 'same same')
        with self.assertRaisesRegex(ValueError, 'not found'):
            r.validate(feedback(), 'different')

    def test_overlapping_quotes_and_hostile_text_preserved(self):
        draft = 'same same <script>alert(1)</script> & @@TITLE@@\n\n雪'
        data = feedback()
        second = copy.deepcopy(data['notes'][0])
        second.update(id='n2', quote='same same', occurrence=1)
        data['notes'].append(second)
        r.validate(data, draft)
        self.assertEqual(data['notes'][0]['range'], [5, 9])
        rendered = r.render_draft(draft, data['notes'])
        class Text(HTMLParser):
            def __init__(self):
                super().__init__(); self.parts=[]
            def handle_data(self, value): self.parts.append(value)
        p = Text(); p.feed(rendered)
        self.assertEqual(''.join(p.parts), draft)
        self.assertIn('data-notes="n1 n2"', rendered)
        self.assertNotIn('<script>', rendered)

    def test_archive_is_immutable_and_source_bytes_survive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); source=root/'draft.txt'; data=root/'input.json'; archive=root/'archive'
            raw=b'same\r\nsame <script>bad</script> @@TITLE@@'
            source.write_bytes(raw); data.write_text(json.dumps(feedback()))
            results=[]
            for _ in range(2):
                result=subprocess.run([sys.executable,str(SCRIPT),'--draft',str(source),'--feedback',str(data),'--archive',str(archive)],text=True,capture_output=True,check=True)
                results.append(json.loads(result.stdout))
            self.assertNotEqual(results[0]['review'],results[1]['review'])
            self.assertEqual(source.read_bytes(),raw)
            for result in results:
                output=Path(result['review'])
                self.assertEqual((output.parent/'draft.txt').read_bytes(),raw)
                self.assertIn('@@TITLE@@',output.read_text())
                self.assertIn('&lt;script&gt;bad&lt;/script&gt;',output.read_text())
            self.assertEqual((archive/'index.html').read_text().count('/review.html'),2)

    def test_repository_output_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'.git').mkdir()
            result=subprocess.run([sys.executable,str(SCRIPT),'--init','--archive',str(root/'private')],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse((root/'private').exists())

    def test_structure_map_renders_and_keeps_draft_text(self):
        draft = 'First thought.\n\nSecond thought.\n\nThird thought.'
        data = structure_feedback()
        r.validate(data, draft)
        data.update(created_at='2026-09-28T00:00:00', source_sha256='a' * 64)
        html = r.page(data, draft)
        self.assertIn('Reverse outline', html)
        self.assertIn('Through-lines to test', html)
        self.assertIn('Patterns to watch', html)
        self.assertIn('Why it matters', html)
        self.assertIn('Your choice', html)
        self.assertIn('href="#outline-2"', html)
        self.assertIn('id="outline-2"', html)
        self.assertIn('No margin notes for this pass.', html)
        self.assertNotIn('@@OUTLINE@@', html)
        rendered = r.render_draft(draft, data['notes'], data['reverse_outline'])
        class Text(HTMLParser):
            def __init__(self):
                super().__init__(); self.parts = []
            def handle_data(self, value): self.parts.append(value)
        parsed = Text(); parsed.feed(rendered)
        self.assertEqual(''.join(parsed.parts), draft)

    def test_structure_map_rejects_unanchored_or_reordered_feedback(self):
        draft = 'First thought.\n\nSecond thought.'
        data = structure_feedback()
        data['reverse_outline'].reverse()
        with self.assertRaisesRegex(ValueError, 'draft order'):
            r.validate(data, draft)
        data = structure_feedback()
        data['patterns'][0]['evidence'] = ['invented detail']
        with self.assertRaisesRegex(ValueError, 'exact evidence'):
            r.validate(data, draft)
        data = structure_feedback()
        data['reverse_outline'] = []
        with self.assertRaisesRegex(ValueError, 'needs a reverse_outline'):
            r.validate(data, draft)
        data = structure_feedback()
        data['notes'] = [dict(id='n1', category='structure', priority='high', tag='sequence', quote='First thought.', title='The start', observation='It begins here.', suggestion='Test the order.', alternative='A rewritten opening.')]
        with self.assertRaisesRegex(ValueError, 'do not include wording alternatives'):
            r.validate(data, draft)

    def test_legacy_feedback_still_renders_without_structure_sections(self):
        data = feedback()
        r.validate(data, 'same same')
        data.update(created_at='2026-09-28T00:00:00', source_sha256='a' * 64)
        html = r.page(data, 'same same')
        self.assertIn('Development pass', html)
        self.assertNotIn('Reverse outline', html)
        self.assertNotIn('Review the shape', html)

    def test_structure_review_archives_with_author_choice(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'draft.txt'
            raw = 'First thought.\r\n\r\nSecond thought.\r\n\r\nThird thought.'.encode()
            source.write_bytes(raw)
            input_file = root / 'feedback.json'
            input_file.write_text(json.dumps(structure_feedback()))
            result = subprocess.run([sys.executable, str(SCRIPT), '--draft', str(source), '--feedback', str(input_file), '--archive', str(root / 'archive')], text=True, capture_output=True, check=True)
            paths = json.loads(result.stdout)
            output = Path(paths['review'])
            review = json.loads(Path(paths['data']).read_text())
            self.assertEqual((output.parent / 'draft.txt').read_bytes(), raw)
            self.assertEqual(review['schema_version'], 2)
            self.assertEqual(review['stage'], 'structure')
            self.assertTrue(review['through_lines'][0]['selected'])
            self.assertIn('href="#outline-2"', output.read_text())


if __name__ == '__main__': unittest.main()
