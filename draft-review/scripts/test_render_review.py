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


if __name__ == '__main__': unittest.main()
