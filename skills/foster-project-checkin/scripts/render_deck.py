#!/usr/bin/env python3
"""Render a five-minute project check-in deck as one offline HTML file, using only the Python standard library."""
import argparse
import base64
import html
import json
import math
import re
import shutil
import sys
import tempfile
import uuid
from datetime import datetime
from pathlib import Path

VERSION = '2.0.0'
KINDS = ('status', 'visual', 'decision', 'question')
TIMINGS = ('made', 'upcoming')
REVERSIBILITY = ('cheap', 'costly', 'one-way')
STATES = ('done', 'moving', 'blocked', 'dropped', 'risk')
VISUALS = ('image', 'gallery', 'slider', 'bars', 'line', 'stats', 'flow', 'compare', 'code')
TONES = ('good', 'bad', 'neutral')
SECONDS = {'cover': 20, 'status': 35, 'visual': 35, 'decision': 50, 'question': 40, 'close': 25}
MAX_DECISIONS = 5
MAX_QUESTIONS = 3
SOFT_LIMIT = 330
HARD_LIMIT = 420
MAX_INFO_RUN = 2
IMAGE_TYPES = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp', '.svg': 'image/svg+xml'}
SLUG = r'[a-z0-9]+(?:-[a-z0-9]+)*'
# Every field the renderer reads. Anything else is refused, so no agent can smuggle in its own styling or layout,
# and a misspelled field fails loudly instead of silently vanishing from the deck.
INFO_FIELDS = {'kind', 'title', 'lede', 'body', 'why', 'say', 'evidence', 'seconds', 'visual'}
FIELDS = {
    'deck': {'project', 'project_id', 'window', 'what_it_is', 'headline', 'hero', 'metrics', 'gaps', 'slides', 'next',
             'schema_version', 'deck_id', 'created_at', 'skill_version', 'seconds'},
    'status': INFO_FIELDS | {'points'},
    'visual': INFO_FIELDS,
    'decision': {'kind', 'id', 'timing', 'question', 'context', 'options', 'current', 'recommended', 'recommendation', 'default',
                 'reversibility', 'reversibility_note', 'needed_by', 'evidence', 'say', 'seconds'},
    'question': {'kind', 'id', 'question', 'context', 'suggestions', 'default', 'needed_by', 'visual', 'evidence', 'say', 'seconds'},
    'image': {'type', 'src', 'alt', 'caption'},
    'gallery': {'type', 'images', 'caption'},
    'slider': {'type', 'before', 'after', 'caption'},
    'bars': {'type', 'question', 'unit', 'bars', 'caption'},
    'line': {'type', 'question', 'unit', 'x', 'series', 'caption'},
    'stats': {'type', 'stats', 'caption'},
    'flow': {'type', 'steps', 'caption'},
    'compare': {'type', 'before', 'after', 'caption'},
    'code': {'type', 'text', 'caption'},
    'picture': {'src', 'alt', 'label'},
    'bar': {'label', 'value', 'highlight'},
    'series': {'label', 'values'},
    'stat': {'value', 'label', 'change', 'tone'},
    'step': {'label', 'detail', 'state'},
    'side': {'label', 'text'},
    'point': {'text', 'state', 'url'},
    'option': {'label', 'consequence'},
    'metric': {'value', 'label'},
    'link': {'label', 'url'},
}
# Insider shorthand that a director without the context would have to ask about. Warn, don't fail.
JARGON = [
    (re.compile(r'\b(?=[0-9a-f]*[a-f])(?=[0-9a-f]*[0-9])[0-9a-f]{7,40}\b'), 'a commit hash'),
    (re.compile(r'`[^`]+`'), 'code in backticks'),
    (re.compile(r'(?<![\w/:.])(?:[\w.-]+/)+[\w.-]+\.\w{1,5}\b'), 'a file path'),
    (re.compile(r'\b[a-z]+(?:_[a-z0-9]+)+\b'), 'a code identifier'),
]


def esc(value):
    return html.escape(str(value), quote=True)


def text(obj, field, label, required=True):
    value = obj.get(field, '')
    if not isinstance(value, str) or (required and not value.strip()):
        raise ValueError(f'{label} needs {field} as a nonempty string.' if required else f'{label} {field} must be a string.')
    return value


def known(obj, shape, label):
    extra = sorted(set(obj) - FIELDS[shape])
    if extra:
        raise ValueError(f'{label} has fields the renderer does not know: {", ".join(extra)}. The look is fixed; see references/components.md for what each component takes.')


def number(value):
    return type(value) in (int, float)


def check_url(url, label):
    if not re.match(r'https?://', url):
        raise ValueError(f'{label} link must be an http(s) URL.')


def check_links(items, label):
    if not isinstance(items, list):
        raise ValueError(f'{label} evidence must be a list.')
    for item in items:
        if not isinstance(item, dict):
            raise ValueError(f'{label} evidence entries must be objects.')
        known(item, 'link', f'{label} evidence')
        text(item, 'label', f'{label} evidence')
        if item.get('url'):
            check_url(item['url'], label)


def inline_image(src, base):
    if src.startswith('data:image/') or src.startswith('https://'):
        return src
    path = Path(src).expanduser()
    path = path if path.is_absolute() else (base / path).resolve()
    kind = IMAGE_TYPES.get(path.suffix.lower())
    if not kind or not path.is_file():
        raise ValueError(f'Image not found or not a supported type: {src}')
    return f'data:{kind};base64,' + base64.b64encode(path.read_bytes()).decode()


def picture(image, label, base):
    if not isinstance(image, dict):
        raise ValueError(f'{label} images must be objects.')
    known(image, 'picture', label)
    image['src'] = inline_image(text(image, 'src', label), base)
    text(image, 'alt', label)
    text(image, 'label', label)


def validate_visual(visual, label, base):
    if not isinstance(visual, dict) or visual.get('type') not in VISUALS:
        raise ValueError(f'{label} needs a visual with type in {VISUALS}.')
    kind = visual['type']
    known(visual, kind, f'{label} {kind}')
    if kind == 'image':
        visual['src'] = inline_image(text(visual, 'src', label), base)
        text(visual, 'alt', label)
    elif kind == 'gallery':
        images = visual.get('images')
        if not isinstance(images, list) or not 2 <= len(images) <= 3:
            raise ValueError(f'{label} gallery needs 2 or 3 images, for example before and after.')
        for image in images:
            picture(image, f'{label} gallery image', base)
    elif kind == 'slider':
        for side in ('before', 'after'):
            picture(visual.get(side), f'{label} slider {side}', base)
    elif kind == 'bars':
        text(visual, 'question', label)
        text(visual, 'unit', label, required=False)
        bars = visual.get('bars')
        if not isinstance(bars, list) or not 2 <= len(bars) <= 6:
            raise ValueError(f'{label} bars needs 2 to 6 bars.')
        for bar in bars:
            if not isinstance(bar, dict):
                raise ValueError(f'{label} bars must be objects.')
            known(bar, 'bar', f'{label} bar')
            text(bar, 'label', f'{label} bar')
            if not number(bar.get('value')) or bar['value'] < 0:
                raise ValueError(f'{label} bar value must be a number of zero or more.')
        if not any(b['value'] > 0 for b in bars):
            raise ValueError(f'{label} bars need at least one value above zero.')
    elif kind == 'line':
        text(visual, 'question', label)
        text(visual, 'unit', label, required=False)
        xs = visual.get('x')
        if not isinstance(xs, list) or not 2 <= len(xs) <= 12 or not all(isinstance(x, str) and x.strip() for x in xs):
            raise ValueError(f'{label} line needs x as 2 to 12 labels, such as dates or week names.')
        series = visual.get('series')
        if not isinstance(series, list) or not 1 <= len(series) <= 3:
            raise ValueError(f'{label} line needs 1 to 3 series; more than three lines is unreadable on a slide.')
        for line in series:
            if not isinstance(line, dict):
                raise ValueError(f'{label} line series must be objects.')
            known(line, 'series', f'{label} line series')
            text(line, 'label', f'{label} line series')
            values = line.get('values')
            if not isinstance(values, list) or len(values) != len(xs) or not all(v is None or number(v) for v in values):
                raise ValueError(f'{label} line series values must be one number (or null for a gap) per x label.')
            if all(v is None for v in values):
                raise ValueError(f'{label} line series needs at least one value.')
    elif kind == 'stats':
        stats = visual.get('stats')
        if not isinstance(stats, list) or not 1 <= len(stats) <= 4:
            raise ValueError(f'{label} stats needs 1 to 4 numbers.')
        for stat in stats:
            if not isinstance(stat, dict):
                raise ValueError(f'{label} stats must be objects.')
            known(stat, 'stat', f'{label} stat')
            text(stat, 'value', f'{label} stat')
            text(stat, 'label', f'{label} stat')
            text(stat, 'change', f'{label} stat', required=False)
            if stat.get('tone', 'neutral') not in TONES:
                raise ValueError(f'{label} stat tone must be one of {TONES}.')
    elif kind == 'flow':
        steps = visual.get('steps')
        if not isinstance(steps, list) or not 2 <= len(steps) <= 6:
            raise ValueError(f'{label} flow needs 2 to 6 steps.')
        for step in steps:
            if not isinstance(step, dict):
                raise ValueError(f'{label} flow steps must be objects.')
            known(step, 'step', f'{label} step')
            text(step, 'label', f'{label} step')
            text(step, 'detail', f'{label} step', required=False)
            if step.get('state', 'done') not in STATES:
                raise ValueError(f'{label} step state must be one of {STATES}.')
    elif kind == 'compare':
        for side in ('before', 'after'):
            if not isinstance(visual.get(side), dict):
                raise ValueError(f'{label} compare needs {side}.')
            known(visual[side], 'side', f'{label} {side}')
            text(visual[side], 'label', f'{label} {side}')
            text(visual[side], 'text', f'{label} {side}')
    else:
        text(visual, 'text', label)
        if len(visual['text'].splitlines()) > 18:
            raise ValueError(f'{label} code is too long for a slide; trim it to 18 lines.')
    text(visual, 'caption', label, required=False)


def validate(data, base=Path('.')):
    if not isinstance(data, dict):
        raise ValueError('Deck must be an object.')
    known(data, 'deck', 'Deck')
    for field in ('project', 'project_id', 'window', 'headline'):
        text(data, field, 'Deck')
    if len(data['headline']) > 180:
        raise ValueError('headline must fit on a cover slide; keep it under 180 characters.')
    text(data, 'what_it_is', 'Deck', required=False)
    if len(data.get('what_it_is', '')) > 240:
        raise ValueError('what_it_is is one sentence on what the project is; keep it under 240 characters.')
    if data.get('hero') is not None:
        hero = data['hero']
        if not isinstance(hero, dict) or hero.get('type', 'image') != 'image':
            raise ValueError('hero must be an image visual.')
        hero.setdefault('type', 'image')
        validate_visual(hero, 'Cover hero', base)
    if not re.fullmatch(SLUG, data['project_id']):
        raise ValueError('project_id must be a lowercase kebab-case slug.')
    for field in ('gaps', 'next'):
        values = data.get(field, [])
        if not isinstance(values, list) or not all(isinstance(x, str) and x.strip() for x in values):
            raise ValueError(f'{field} must be a list of nonempty strings.')
    if not data.get('next'):
        raise ValueError('next must say what you keep working on while the calls are open.')
    metrics = data.get('metrics', [])
    if not isinstance(metrics, list) or len(metrics) > 4:
        raise ValueError('metrics must be a list of at most four entries.')
    for metric in metrics:
        if not isinstance(metric, dict):
            raise ValueError('Each metric must be an object.')
        known(metric, 'metric', 'Metric')
        text(metric, 'value', 'Metric')
        text(metric, 'label', 'Metric')
    slides = data.get('slides')
    if not isinstance(slides, list) or not 3 <= len(slides) <= 10:
        raise ValueError('slides must be a list of 3 to 10 content slides.')
    ids, warnings, run, first_call = set(), [], 0, None
    total = SECONDS['cover'] + SECONDS['close']
    for number, slide in enumerate(slides, 1):
        label = f'Slide {number}'
        if not isinstance(slide, dict) or slide.get('kind') not in KINDS:
            raise ValueError(f'{label} needs kind in {KINDS}.')
        kind = slide['kind']
        known(slide, kind, label)
        seconds = slide.setdefault('seconds', SECONDS[kind])
        if type(seconds) is not int or not 10 <= seconds <= 90:
            raise ValueError(f'{label} seconds must be a whole number from 10 to 90.')
        total += seconds
        text(slide, 'say', label, required=False)
        if kind in ('decision', 'question'):
            (validate_decision if kind == 'decision' else validate_question)(slide, label, ids, base)
            first_call = first_call or number
            run = 0
            continue
        run += 1
        if run > MAX_INFO_RUN:
            raise ValueError(f'{label} makes {run} information slides in a row; interleave a decision so the director can weigh in.')
        text(slide, 'title', label)
        text(slide, 'lede', label)
        text(slide, 'body', label, required=False)
        text(slide, 'why', label, required=False)
        check_links(slide.get('evidence', []), label)
        if kind == 'status':
            points = slide.get('points', [])
            if not isinstance(points, list) or len(points) > 5:
                raise ValueError(f'{label} points must be a list of at most five.')
            for point in points:
                if not isinstance(point, dict):
                    raise ValueError(f'{label} points must be objects.')
                known(point, 'point', f'{label} point')
                text(point, 'text', f'{label} point')
                if point.get('state', 'done') not in STATES:
                    raise ValueError(f'{label} point state must be one of {STATES}.')
                if point.get('url'):
                    check_url(point['url'], label)
            if slide.get('visual') is not None:
                validate_visual(slide['visual'], label, base)
        else:
            validate_visual(slide.get('visual'), label, base)
    decisions = sum(s['kind'] == 'decision' for s in slides)
    questions = sum(s['kind'] == 'question' for s in slides)
    if first_call is None:
        raise ValueError('A check-in needs at least one decision or question slide.')
    if first_call > 3:
        raise ValueError('Put the first decision or question within the first three slides.')
    if decisions > MAX_DECISIONS:
        raise ValueError(f'Keep a check-in to at most {MAX_DECISIONS} decisions.')
    if questions > MAX_QUESTIONS:
        raise ValueError(f'Keep a check-in to at most {MAX_QUESTIONS} open questions; turn the rest into decisions with options.')
    if total > HARD_LIMIT:
        raise ValueError(f'The deck runs about {total} seconds; cut it to fit five minutes.')
    if total > SOFT_LIMIT:
        warnings.append(f'The deck runs about {total} seconds, past the five-minute target.')
    timings = {s['timing'] for s in slides if s['kind'] == 'decision'}
    for timing in TIMINGS:
        if timing not in timings:
            warnings.append(f'No {timing} decision. Fine if the evidence has none; do not invent one.')
    if not any(s['kind'] == 'visual' for s in slides):
        warnings.append('No visual slide shows what the work looks like.')
    info = [s for s in slides if s['kind'] in ('status', 'visual')]
    pictured = sum(1 for s in info if s.get('visual'))
    if info and pictured * 2 < len(info):
        warnings.append(f'Only {pictured} of {len(info)} information slides have a picture. Show features with screenshots, before-and-afters or a chart.')
    without_why = [i for i, s in enumerate(slides, 1) if s['kind'] in ('status', 'visual') and not s.get('why')]
    if without_why:
        warnings.append('Slides ' + ', '.join(map(str, without_why)) + ' do not say why it matters (add why).')
    warnings.extend(plain_language(data))
    data['seconds'] = total
    return data, warnings


def plain_language(data):
    """Warn about insider shorthand on anything the director reads. Evidence and captions are exempt."""
    found = []
    fields = [('Cover', data.get('headline', '')), ('Cover', data.get('what_it_is', ''))]
    for number, slide in enumerate(data['slides'], 1):
        label = f'Slide {number}'
        for field in ('title', 'lede', 'body', 'why', 'say', 'question', 'context', 'recommendation', 'default'):
            fields.append((label, slide.get(field, '')))
        fields += [(label, p['text']) for p in slide.get('points', [])]
        fields += [(label, o['label'] + ' ' + o['consequence']) for o in slide.get('options', [])]
        fields += [(label, s) for s in slide.get('suggestions', [])]
    for label, value in fields:
        for pattern, kind in JARGON:
            match = pattern.search(value or '')
            if match:
                found.append(f'{label} has {kind} ("{match.group(0)}"). Say it plainly, or move it to evidence.')
                break
    return found


def claim_id(slide, label, ids):
    identifier = text(slide, 'id', label)
    if not re.fullmatch(r'[a-z][a-z0-9-]*', identifier) or identifier in ids:
        raise ValueError(f'{label} {slide["kind"]} id must be a unique lowercase identifier.')
    ids.add(identifier)


def validate_question(slide, label, ids, base):
    """An open question: something only the director knows, answered in words rather than by picking an option."""
    claim_id(slide, label, ids)
    for field in ('question', 'context', 'default'):
        text(slide, field, label)
    text(slide, 'needed_by', label, required=False)
    suggestions = slide.get('suggestions', [])
    if not isinstance(suggestions, list) or len(suggestions) > 4 or not all(isinstance(x, str) and x.strip() and len(x) <= 60 for x in suggestions):
        raise ValueError(f'{label} suggestions must be at most four short answers (60 characters each).')
    if slide.get('visual') is not None:
        validate_visual(slide['visual'], label, base)
    check_links(slide.get('evidence', []), label)


def validate_decision(slide, label, ids, base=None):
    claim_id(slide, label, ids)
    if slide.get('timing') not in TIMINGS:
        raise ValueError(f'{label} timing must be made or upcoming.')
    for field in ('question', 'context', 'recommendation', 'default'):
        text(slide, field, label)
    options = slide.get('options')
    if not isinstance(options, list) or not 2 <= len(options) <= 4:
        raise ValueError(f'{label} needs 2 to 4 options.')
    for option in options:
        if not isinstance(option, dict):
            raise ValueError(f'{label} options must be objects.')
        known(option, 'option', f'{label} option')
        text(option, 'label', f'{label} option')
        text(option, 'consequence', f'{label} option')
    for field in ('recommended', 'current'):
        value = slide.get(field)
        if field == 'current' and slide['timing'] == 'upcoming':
            if value is not None:
                raise ValueError(f'{label} is upcoming, so nothing is current yet.')
            continue
        if type(value) is not int or not 0 <= value < len(options):
            raise ValueError(f'{label} {field} must index one of its options.')
    if slide.get('reversibility') not in REVERSIBILITY:
        raise ValueError(f'{label} reversibility must be one of {REVERSIBILITY}.')
    for field in ('reversibility_note', 'needed_by'):
        text(slide, field, label, required=False)
    check_links(slide.get('evidence', []), label)


def say(slide):
    return f'<p class="say"><span>Voiceover</span>{esc(slide["say"])}</p>' if slide.get('say') else ''


def link(label, url):
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>' if url else esc(label)


def nice_step(span):
    raw = span / 4 or 1
    power = 10 ** math.floor(math.log10(raw))
    return next(m * power for m in (1, 2, 2.5, 5, 10) if m * power >= raw)


def fmt(value):
    return format(round(value, 2), 'g')


def render_line(v):
    """A small inline SVG line chart. Colors come from the stylesheet so it follows light and dark mode."""
    width, height, left, right, top, bottom = 680, 240, 44, 150, 14, 30
    values = [x for line in v['series'] for x in line['values'] if x is not None]
    low, high = min(0, min(values)), max(values)
    step = nice_step(high - low)
    low, high = math.floor(low / step) * step, math.ceil(high / step) * step
    if high == low:
        high = low + step
    plot_w, plot_h = width - left - right, height - top - bottom
    count = len(v['x'])
    unit = f' {v["unit"]}' if v.get('unit') else ''
    px = lambda i: left + plot_w * i / (count - 1)
    py = lambda val: top + plot_h * (1 - (val - low) / (high - low))
    parts = []
    tick = low
    while tick <= high + step / 2:
        y = py(tick)
        parts.append(f'<line class="grid" x1="{left}" x2="{left + plot_w}" y1="{y:.1f}" y2="{y:.1f}"/><text class="tick" x="{left - 8}" y="{y + 4:.1f}" text-anchor="end">{esc(fmt(tick))}</text>')
        tick += step
    every = max(1, math.ceil(count / 6))
    for i, label in enumerate(v['x']):
        if i % every == 0 or i == count - 1:
            parts.append(f'<text class="tick" x="{px(i):.1f}" y="{height - 8}" text-anchor="middle">{esc(label)}</text>')
    ends = []
    for n, line in enumerate(v['series'], 1):
        segments, current = [], []
        for i, val in enumerate(line['values']):
            if val is None:
                segments, current = segments + [current] if current else segments, []
            else:
                current.append(f'{px(i):.1f},{py(val):.1f}')
        segments += [current] if current else []
        for seg in segments:
            if len(seg) > 1:
                parts.append(f'<polyline class="series s{n}" points="{" ".join(seg)}"/>')
        for i, val in enumerate(line['values']):
            if val is not None:
                parts.append(f'<g class="pt s{n}"><circle class="hit" cx="{px(i):.1f}" cy="{py(val):.1f}" r="11"/><circle class="dot" cx="{px(i):.1f}" cy="{py(val):.1f}" r="4"/><title>{esc(line["label"])}, {esc(v["x"][i])}: {esc(fmt(val))}{esc(unit)}</title></g>')
        last = max(i for i, val in enumerate(line['values']) if val is not None)
        ends.append([py(line['values'][last]), n, line, line['values'][last]])
    # Direct labels at the right edge, nudged apart so they never overlap.
    ends.sort()
    for i in range(1, len(ends)):
        ends[i][0] = max(ends[i][0], ends[i - 1][0] + 30)
    for y, n, line, val in ends:
        parts.append(f'<g class="end s{n}"><rect x="{left + plot_w + 10}" y="{y - 11:.1f}" width="10" height="3" rx="1.5"/><text x="{left + plot_w + 26}" y="{y - 5:.1f}">{esc(line["label"])}</text><text class="val" x="{left + plot_w + 26}" y="{y + 11:.1f}">{esc(fmt(val))}{esc(unit)}</text></g>')
    head = ''.join(f'<th scope="col">{esc(x)}</th>' for x in v['x'])
    rows = ''.join(f'<tr><th scope="row">{esc(line["label"])}</th>' + ''.join(f'<td>{"" if val is None else esc(fmt(val))}</td>' for val in line['values']) + '</tr>' for line in v['series'])
    table = f'<div class="sr-only"><table><caption>{esc(v["question"])}{esc(unit and " (" + v["unit"] + ")")}</caption><tr><td></td>{head}</tr>{rows}</table></div>'
    legend = '<p class="legend">' + ''.join(f'<span class="s{n}"><i></i>{esc(line["label"])}</span>' for n, line in enumerate(v['series'], 1)) + '</p>' if len(v['series']) > 1 else ''
    svg = f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{esc(v["question"])}">{"".join(parts)}</svg>'
    return f'<div class="chart line-chart"><p class="question">{esc(v["question"])}</p>{legend}{svg}{table}</div>'


def render_visual(v):
    if v['type'] == 'image':
        body = f'<img src="{esc(v["src"])}" alt="{esc(v["alt"])}">'
    elif v['type'] == 'gallery':
        body = f'<div class="gallery" style="--n:{len(v["images"])}">' + ''.join(f'<figure><img src="{esc(i["src"])}" alt="{esc(i["alt"])}"><b>{esc(i["label"])}</b></figure>' for i in v['images']) + '</div>'
    elif v['type'] == 'slider':
        before, after = v['before'], v['after']
        body = f'''<div class="slider" style="--pos:50%"><img src="{esc(after['src'])}" alt="{esc(after['alt'])}"><div class="slider-before"><img src="{esc(before['src'])}" alt="{esc(before['alt'])}"></div><span class="slider-handle" aria-hidden="true"></span><b class="slider-label before">{esc(before['label'])}</b><b class="slider-label after">{esc(after['label'])}</b><input type="range" min="0" max="100" value="50" aria-label="Drag to compare {esc(before['label'])} with {esc(after['label'])}"></div>'''
    elif v['type'] == 'line':
        body = render_line(v)
    elif v['type'] == 'stats':
        arrow = {'good': '▲', 'bad': '▼', 'neutral': '●'}
        body = f'<div class="stats" style="--n:{len(v["stats"])}">' + ''.join(f'<div class="stat tone-{esc(st.get("tone", "neutral"))}"><b>{esc(st["value"])}</b><span>{esc(st["label"])}</span>' + (f'<em><i aria-hidden="true">{arrow[st.get("tone", "neutral")]}</i>{esc(st["change"])}</em>' if st.get('change') else '') + '</div>' for st in v['stats']) + '</div>'
    elif v['type'] == 'bars':
        top = max(b['value'] for b in v['bars'])
        unit = f' {esc(v["unit"])}' if v.get('unit') else ''
        rows = ''.join(f'<div class="row{" hi" if b.get("highlight") else ""}"><span>{esc(b["label"])}</span><span class="track2"><span class="fill" style="width:{b["value"] / top * 100:.1f}%"></span></span><b>{esc(format(b["value"], "g"))}{unit}</b></div>' for b in v['bars'])
        body = f'<div class="bars"><p class="question">{esc(v["question"])}</p>{rows}</div>'
    elif v['type'] == 'flow':
        body = '<ol class="flow">' + ''.join(f'<li class="state-{esc(s.get("state", "done"))}"><strong>{esc(s["label"])}</strong><span>{esc(s.get("detail", ""))}</span></li>' for s in v['steps']) + '</ol>'
    elif v['type'] == 'compare':
        body = '<div class="compare">' + ''.join(f'<div class="{side}"><b>{esc(v[side]["label"])}</b><p>{esc(v[side]["text"])}</p></div>' for side in ('before', 'after')) + '</div>'
    else:
        body = f'<pre><code>{esc(v["text"])}</code></pre>'
    caption = f'<figcaption>{esc(v["caption"])}</figcaption>' if v.get('caption') else ''
    return f'<figure class="figure figure-{v["type"]}">{body}{caption}</figure>'


def render_info(slide, number):
    eyebrow = 'What it looks like' if slide['kind'] == 'visual' else 'Where things stand'
    body = f'<p class="body">{esc(slide["body"])}</p>' if slide.get('body') else ''
    extra = ''
    if slide['kind'] == 'status' and slide.get('points'):
        extra = '<ul class="points">' + ''.join(f'<li class="state-{esc(p.get("state", "done"))}"><i>{esc(p.get("state", "done"))}</i><span>{link(p["text"], p.get("url"))}</span></li>' for p in slide['points']) + '</ul>'
    if slide.get('visual'):
        figure = render_visual(slide['visual'])
        # A status picture sits beside its points so the slide fits without scrolling.
        extra = f'<div class="split">{extra}{figure}</div>' if extra else figure
    why = f'<p class="why"><b>Why it matters</b>{esc(slide["why"])}</p>' if slide.get('why') else ''
    evidence = slide.get('evidence', [])
    sources = '<details class="evidence"><summary>Sources</summary>' + ', '.join(link(e['label'], e.get('url')) for e in evidence) + '</details>' if evidence else ''
    return f'''<section class="slide info {slide['kind']}" data-kind="{slide['kind']}" data-seconds="{slide['seconds']}" aria-label="Slide {number}">
<div class="eyebrow">{eyebrow}</div><h2>{esc(slide['title'])}</h2><p class="lede">{esc(slide['lede'])}</p>{body}{extra}{why}{sources}{say(slide)}</section>'''


def render_decision(slide, number, index):
    made = slide['timing'] == 'made'
    eyebrow = f'Call {index} · {"Already made, reverse?" if made else "Coming up, your call"}'
    cards = []
    for i, option in enumerate(slide['options']):
        tags = ''
        if made and i == slide['current']:
            tags += '<span class="tag current">In effect now</span>'
        if i == slide['recommended']:
            tags += '<span class="tag rec">My rec</span>'
        cards.append(f'''<button type="button" class="option" data-decision="{esc(slide['id'])}" data-option="{i}" aria-pressed="false"><span class="option-head"><b>{chr(65 + i)}</b>{tags}</span><strong>{esc(option['label'])}</strong><span>{esc(option['consequence'])}</span></button>''')
    rev = {'cheap': 'Cheap to change later', 'costly': 'Gets costly to change', 'one-way': 'One-way door'}[slide['reversibility']]
    rev_note = f' {esc(slide["reversibility_note"])}' if slide.get('reversibility_note') else ''
    needed = f'<div><dt>Need it by</dt><dd>{esc(slide["needed_by"])}</dd></div>' if slide.get('needed_by') else ''
    evidence = slide.get('evidence', [])
    sources = '<p class="evidence">Sources: ' + ', '.join(link(e['label'], e.get('url')) for e in evidence) + '</p>' if evidence else ''
    return f'''<section class="slide decision {slide['timing']}" data-kind="decision" data-seconds="{slide['seconds']}" aria-label="Slide {number}">
<div class="eyebrow">{eyebrow}</div><h2>{esc(slide['question'])}</h2><p class="lede">{esc(slide['context'])}</p>
<div class="options" style="--count:{len(slide['options'])}">{''.join(cards)}</div>
<dl class="terms"><div class="rec-why"><dt>Why I'd pick {chr(65 + slide['recommended'])}</dt><dd>{esc(slide['recommendation'])}</dd></div><div><dt>If you don't weigh in</dt><dd>{esc(slide['default'])}</dd></div><div><dt>{rev}</dt><dd class="rev-{slide['reversibility']}">{rev_note or '&nbsp;'}</dd></div>{needed}</dl>
<label class="note-field">Your note <textarea data-note="{esc(slide['id'])}" rows="1" placeholder="Optional. Context, a constraint, or a different option."></textarea></label>{sources}{say(slide)}</section>'''


def render_question(slide, number, index):
    chips = ''
    if slide.get('suggestions'):
        chips = '<div class="chips" role="group" aria-label="Quick answers">' + ''.join(f'<button type="button" class="chip" data-question="{esc(slide["id"])}" data-option="{i}" aria-pressed="false">{esc(x)}</button>' for i, x in enumerate(slide['suggestions'])) + '</div>'
    figure = render_visual(slide['visual']) if slide.get('visual') else ''
    needed = f'<div><dt>Need it by</dt><dd>{esc(slide["needed_by"])}</dd></div>' if slide.get('needed_by') else ''
    evidence = slide.get('evidence', [])
    sources = '<p class="evidence">Sources: ' + ', '.join(link(e['label'], e.get('url')) for e in evidence) + '</p>' if evidence else ''
    return f'''<section class="slide question" data-kind="question" data-seconds="{slide['seconds']}" aria-label="Slide {number}">
<div class="eyebrow">Question {index} · Only you know this</div><h2>{esc(slide['question'])}</h2><p class="lede">{esc(slide['context'])}</p>{f'<div class="ask-split">{figure}<div>' if figure else ''}{chips}
<label class="note-field answer">Your answer <textarea data-note="{esc(slide['id'])}" rows="2" placeholder="A sentence is plenty."></textarea></label>
<dl class="terms"><div><dt>If you don't answer</dt><dd>{esc(slide['default'])}</dd></div>{needed}</dl>{'</div></div>' if figure else ''}{sources}{say(slide)}</section>'''


def render_slides(data):
    decisions = [s for s in data['slides'] if s['kind'] == 'decision']
    questions = [s for s in data['slides'] if s['kind'] == 'question']
    metrics = ''.join(f'<div class="metric"><b>{esc(m["value"])}</b><span>{esc(m["label"])}</span></div>' for m in data.get('metrics', []))
    gaps = f'<p class="gaps">Not checked: {esc("; ".join(data["gaps"]))}</p>' if data.get('gaps') else ''
    made = sum(s['timing'] == 'made' for s in decisions)
    asks = [f'{len(decisions)} call{"s" if len(decisions) != 1 else ""}'] if decisions else []
    asks += [f'{len(questions)} question{"s" if len(questions) != 1 else ""}'] if questions else []
    count = ' and '.join(asks) + ' for you' + (f', {made} of them about reversing something already in place' if made else '')
    what = f'<p class="what">{esc(data["what_it_is"])}</p>' if data.get('what_it_is') else ''
    hero = render_visual(data['hero']).replace('class="figure', 'class="hero figure', 1) if data.get('hero') else ''
    parts = [f'''<section class="slide cover{' has-hero' if hero else ''}" data-kind="cover" data-seconds="{SECONDS['cover']}" aria-label="Slide 1">
<div class="eyebrow">Check-in · {esc(data['project'])} · {esc(data['window'])}</div>{what}<h1>{esc(data['headline'])}</h1>{hero}
<div class="metrics">{metrics}</div><p class="count">{count}. About {round(data['seconds'] / 60)} minutes. Arrow keys or swipe to move; pick an option on any call slide.</p>{gaps}</section>''']
    number, call, asked = 1, 0, 0
    for slide in data['slides']:
        number += 1
        if slide['kind'] == 'decision':
            call += 1
            parts.append(render_decision(slide, number, call))
        elif slide['kind'] == 'question':
            asked += 1
            parts.append(render_question(slide, number, asked))
        else:
            parts.append(render_info(slide, number))
    nexts = ''.join(f'<li>{esc(x)}</li>' for x in data['next'])
    parts.append(f'''<section class="slide close" data-kind="close" data-seconds="{SECONDS['close']}" aria-label="Slide {number + 1}">
<div class="eyebrow">Wrap-up</div><h2>Your calls</h2><ol class="recap" id="recap"></ol>
<label class="note-field">Anything else <textarea data-note="_general" rows="2" placeholder="Optional. Priorities, worries, or a question for me."></textarea></label>
<div class="actions"><button type="button" id="copy">Copy my calls</button><span id="copied" role="status"></span></div>
<div class="cooking"><b>While you decide, I keep going on</b><ul>{nexts}</ul></div></section>''')
    return '\n'.join(parts)


def page(data):
    assets = Path(__file__).resolve().parent.parent / 'assets'
    template = (assets / 'deck.html').read_text(encoding='utf-8')
    calls = []
    for s in data['slides']:
        if s['kind'] == 'decision':
            calls.append({'kind': 'decision', 'id': s['id'], 'question': s['question'], 'timing': s['timing'], 'options': [o['label'] for o in s['options']], 'recommended': s['recommended'], 'current': s.get('current'), 'default': s['default']})
        elif s['kind'] == 'question':
            calls.append({'kind': 'question', 'id': s['id'], 'question': s['question'], 'options': s.get('suggestions', []), 'default': s['default']})
    meta = {'deck': data['deck_id'], 'project': data['project'], 'date': data['created_at'][:10], 'calls': calls}
    replacements = {
        'TITLE': esc(data['project']),
        'SLIDES': render_slides(data),
        'CSS': (assets / 'components' / 'deck.css').read_text(encoding='utf-8'),
        'JS': (assets / 'components' / 'deck.js').read_text(encoding='utf-8'),
        'META': json.dumps(meta, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026'),
    }
    # One pass, so template-like text inside the deck stays literal.
    return re.sub(r'@@([A-Z]+)@@', lambda m: replacements[m.group(1)], template)


def latest(root, project_id):
    decks = []
    for file in (root / project_id).glob('*/deck.json'):
        try:
            decks.append((json.loads(file.read_text(encoding='utf-8'))['created_at'], file))
        except (ValueError, KeyError, OSError):
            continue
    # Folder names only resolve to the second, so order by the full timestamp.
    return max(decks)[1] if decks else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--deck', type=Path, help='Deck JSON to validate and render.')
    parser.add_argument('--archive', type=Path, default=Path.home() / 'Documents' / 'Project Check-ins')
    parser.add_argument('--latest', metavar='PROJECT_ID', help='Print the most recent archived deck.json for a project, then exit.')
    parser.add_argument('--check', action='store_true', help='Validate only; write nothing.')
    args = parser.parse_args()
    root = args.archive.expanduser().resolve()
    if args.latest:
        found = latest(root, args.latest)
        print(found or '')
        return
    if not args.deck:
        parser.error('--deck is required unless --latest is used.')
    try:
        data, warnings = validate(json.loads(args.deck.read_text(encoding='utf-8')), args.deck.resolve().parent)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    for warning in warnings:
        print('warning: ' + warning, file=sys.stderr)
    if args.check:
        print(json.dumps({'ok': True, 'seconds': data['seconds'], 'warnings': warnings}, indent=2))
        return
    if any((p / '.git').exists() for p in [root, *root.parents]):
        parser.error('Keep check-in archives outside Git repositories so they are not committed by accident.')
    now = datetime.now().astimezone()
    data.update(schema_version=1, deck_id=now.strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:8], created_at=now.isoformat(), skill_version=VERSION)
    rendered = page(data)
    project_root = root / data['project_id']
    project_root.mkdir(parents=True, exist_ok=True)
    target = project_root / data['deck_id']
    staging = Path(tempfile.mkdtemp(prefix='.pending-', dir=project_root))
    try:
        (staging / 'deck.json').write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        (staging / 'deck.html').write_text(rendered, encoding='utf-8')
        staging.rename(target)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    print(json.dumps({'deck': str(target / 'deck.html'), 'data': str(target / 'deck.json'), 'seconds': data['seconds'], 'warnings': warnings}, indent=2))


if __name__ == '__main__':
    main()
