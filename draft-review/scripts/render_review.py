#!/usr/bin/env python3
"""Render an immutable, offline writing review using only the Python standard library."""
import argparse
import hashlib
import html
import json
import re
import shutil
import tempfile
import uuid
from datetime import datetime
from pathlib import Path

CATEGORIES = ('structure', 'ideas', 'clarity', 'voice', 'mechanics', 'strength')
PRIORITIES = ('high', 'medium', 'low')
VERSION = '1.0.0'


def esc(value):
    return html.escape(str(value), quote=True)


def validate(data, draft):
    if not isinstance(data, dict):
        raise ValueError('Feedback must be an object.')
    for field in ('title', 'essay_id', 'draft_label', 'intent', 'reader_response'):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f'{field} must be a nonempty string.')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', data['essay_id']):
        raise ValueError('essay_id must be a lowercase kebab-case slug.')
    for field in ('priorities', 'assumptions'):
        if not isinstance(data.get(field, []), list) or not all(isinstance(x, str) for x in data.get(field, [])):
            raise ValueError(f'{field} must be a list of strings.')
    if not data.get('priorities'):
        raise ValueError('Provide at least one revision priority or deliberate next step.')
    if not isinstance(data.get('notes'), list):
        raise ValueError('notes must be a list.')
    ids = set()
    for note in data['notes']:
        if not isinstance(note, dict):
            raise ValueError('Each note must be an object.')
        for field in ('id', 'category', 'priority', 'tag', 'title', 'observation', 'suggestion'):
            if not isinstance(note.get(field), str) or not note[field].strip():
                raise ValueError(f'Note field {field} must be a nonempty string.')
        if not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_-]*', note['id']) or note['id'] in ids:
            raise ValueError('Note IDs must be unique HTML-safe identifiers.')
        ids.add(note['id'])
        if note['category'] not in CATEGORIES or note['priority'] not in PRIORITIES:
            raise ValueError(f'Unknown category or priority in {note["id"]}.')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', note['tag']):
            raise ValueError('Craft tags must be kebab-case.')
        quote = note.get('quote', '')
        if not isinstance(quote, str) or not isinstance(note.get('alternative', ''), str):
            raise ValueError('quote and alternative must be strings.')
        if not quote:
            note['range'] = None
            continue
        matches = [m.start() for m in re.finditer('(?=' + re.escape(quote) + ')', draft)]
        if len(matches) > 1 and 'occurrence' not in note:
            raise ValueError(f'Ambiguous quote in {note["id"]}; supply occurrence.')
        occurrence = note.get('occurrence', 1)
        if type(occurrence) is not int or not 1 <= occurrence <= len(matches):
            raise ValueError(f'Quote occurrence not found in {note["id"]}: {quote!r}')
        start = matches[occurrence - 1]
        note['range'] = [start, start + len(quote)]
    return data


def render_draft(draft, notes):
    points = {0, len(draft)}
    for n in notes:
        if n['range']:
            points.update(n['range'])
    parts, seen = [], set()
    points = sorted(points)
    for start, end in zip(points, points[1:]):
        text = esc(draft[start:end])
        active = [n for n in notes if n['range'] and n['range'][0] <= start < n['range'][1]]
        if active:
            identifiers = ' '.join(n['id'] for n in active)
            anchors = ''.join(f'<span id="anchor-{esc(n["id"])}"></span>' for n in active if n['id'] not in seen)
            seen.update(n['id'] for n in active)
            categories = ' '.join(sorted({n['category'] for n in active}))
            title = '; '.join(n['title'] for n in active)
            parts.append(f'{anchors}<mark tabindex="0" role="button" data-notes="{identifiers}" data-categories="{categories}" aria-label="{esc(title)}" title="{esc(title)}">{text}</mark>')
        else:
            parts.append(text)
    return ''.join(parts)


def render_notes(notes):
    cards = []
    for number, n in enumerate(notes, 1):
        quote = f'<blockquote>{esc(n["quote"])}</blockquote>' if n.get('quote') else '<p class="global">Whole draft</p>'
        jump = f'<a class="jump" data-note="{n["id"]}" href="#anchor-{n["id"]}">Find in draft ↗</a>' if n['range'] else ''
        alternative = f'<div class="alternative"><b>Small wording option</b><p>{esc(n["alternative"])}</p></div>' if n.get('alternative') else ''
        cards.append(f'''<article class="note" id="note-{n['id']}" tabindex="-1" data-id="{n['id']}" data-category="{n['category']}" data-priority="{n['priority']}">
<div class="note-meta"><span class="badge {n['category']}">{n['category'].title()}</span><span>{n['priority'].title()} priority · {number:02}</span></div>
<h3>{esc(n['title'])}</h3>{quote}<p>{esc(n['observation'])}</p><div class="try"><b>{'Keep in mind' if n['category'] == 'strength' else 'Consider'}</b><p>{esc(n['suggestion'])}</p></div>{alternative}
<footer><span class="tag">{esc(n['tag'])}</span>{jump}</footer></article>''')
    return '\n'.join(cards)


def page(data, draft):
    template = (Path(__file__).resolve().parent.parent / 'assets' / 'review.html').read_text()
    replacements = {
        'TITLE': esc(data['title']), 'LABEL': esc(data['draft_label']),
        'DATE': esc(data['created_at'][:10]), 'COUNT': str(len(data['notes'])),
        'WORDS': str(len(draft.split())), 'INTENT': esc(data['intent']),
        'RESPONSE': esc(data['reader_response']),
        'PRIORITIES': ''.join('<li>' + esc(x) + '</li>' for x in data['priorities']),
        'ASSUMPTIONS': ('<p class="assumptions"><b>Assumptions:</b> ' + esc(' '.join(data['assumptions'])) + '</p>') if data.get('assumptions') else '',
        'DRAFT': render_draft(draft, data['notes']), 'NOTES': render_notes(data['notes']),
        'FILTERS': ''.join(f'<button type="button" data-filter="{c}" aria-pressed="false">{c.title()} <span>{sum(n["category"] == c for n in data["notes"])}</span></button>' for c in CATEGORIES),
        'HASH': data['source_sha256'][:12],
    }
    # One pass: literal template-like strings in a user's draft must stay literal.
    return re.sub(r'@@([A-Z]+)@@', lambda m: replacements[m.group(1)], template)


def rebuild_index(root):
    reviews = []
    for file in root.glob('*/review.json'):
        try:
            d = json.loads(file.read_text())
            reviews.append((d['created_at'], file.parent.name, d))
        except (ValueError, KeyError, OSError):
            continue
    reviews.sort(reverse=True)
    rows = ''.join(f'<li><a href="{esc(folder)}/review.html">{esc(d["title"])}</a><p>{esc(d["draft_label"])} · {esc(d["created_at"][:10])} · {len(d["notes"])} notes</p></li>' for _, folder, d in reviews)
    content = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Writing Feedback</title><style>body{max-width:820px;margin:70px auto;padding:0 24px;background:#f6f4ef;color:#273832;font:17px/1.6 system-ui}h1{font:48px Georgia}a{color:#276852}ul{padding:0;list-style:none}li{padding:20px 0;border-bottom:1px solid #d6dbd5}li a{font-size:24px}li p{margin:5px 0;color:#626e68}</style><p>YOUR WRITING / REVIEW ARCHIVE</p><h1>Writing Feedback</h1><p>Read, reflect, then revise in your own words.</p><ul>' + (rows or '<li>Your first review will appear here.</li>') + '</ul></html>'
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=root, delete=False, suffix='.tmp') as f:
        f.write(content)
        temp = Path(f.name)
    temp.replace(root / 'index.html')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--draft', type=Path)
    parser.add_argument('--feedback', type=Path)
    parser.add_argument('--archive', type=Path, default=Path.home() / 'Documents' / 'Writing Feedback')
    parser.add_argument('--init', action='store_true', help='Create/rebuild the archive index only.')
    args = parser.parse_args()
    root = args.archive.expanduser().resolve()
    if any((p / '.git').exists() for p in [root, *root.parents]):
        parser.error('Keep personal feedback outside Git repositories.')
    root.mkdir(parents=True, exist_ok=True)
    if args.init:
        rebuild_index(root)
        print(root / 'index.html')
        return
    if not args.draft or not args.feedback:
        parser.error('--draft and --feedback are required unless --init is used.')
    raw = args.draft.read_bytes()
    draft = raw.decode('utf-8')
    if not draft.strip():
        parser.error('Draft is empty.')
    try:
        data = validate(json.loads(args.feedback.read_text(encoding='utf-8')), draft)
    except ValueError as error:
        parser.error(str(error))
    now = datetime.now().astimezone()
    review_id = now.strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:10]
    data.update(schema_version=1, review_id=review_id, created_at=now.isoformat(), source_sha256=hashlib.sha256(raw).hexdigest(), source_filename=args.draft.name, skill_version=VERSION)
    rendered = page(data, draft)
    target = root / (review_id + '-' + data['essay_id'][:80])
    staging = Path(tempfile.mkdtemp(prefix='.pending-', dir=root))
    try:
        (staging / 'draft.txt').write_bytes(raw)
        (staging / 'review.json').write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        (staging / 'review.html').write_text(rendered, encoding='utf-8')
        staging.rename(target)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    rebuild_index(root)
    print(json.dumps({'review': str(target / 'review.html'), 'archive': str(root / 'index.html'), 'data': str(target / 'review.json')}, indent=2))


if __name__ == '__main__':
    main()
