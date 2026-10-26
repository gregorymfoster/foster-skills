(() => {
  const meta = JSON.parse(document.getElementById('meta').textContent);
  const slides = [...document.querySelectorAll('.slide')];
  const track = document.getElementById('track');
  const key = 'checkin:' + meta.deck;
  // Every call is read from its slide's markup, so a hand-built deck needs no separate list to keep in sync.
  const calls = slides.filter(s => s.dataset.kind === 'decision' || s.dataset.kind === 'question').map(s => ({
    kind: s.dataset.kind, id: s.dataset.id, question: s.querySelector('h2').textContent, timing: s.dataset.timing,
    options: [...s.querySelectorAll(s.dataset.kind === 'decision' ? '.option strong' : '.chip')].map(o => o.textContent),
    recommended: Number(s.dataset.recommended), current: s.dataset.current === undefined ? undefined : Number(s.dataset.current),
    default: s.dataset.default
  }));
  let state = {picks: {}, notes: {}, quiet: false};
  try { state = Object.assign(state, JSON.parse(localStorage.getItem(key)) || {}); } catch (e) {}
  const save = () => { try { localStorage.setItem(key, JSON.stringify(state)); } catch (e) {} };
  const budget = slides.reduce((t, s) => t + Number(s.dataset.seconds || 0), 0);
  const fmt = s => Math.floor(s / 60) + ':' + String(Math.floor(s % 60)).padStart(2, '0');
  let current = 0, started = null;
  const seen = new Set();

  slides.forEach((s, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = s.dataset.kind === 'decision' ? 'call' : s.dataset.kind === 'question' ? 'ask' : '';
    b.setAttribute('aria-label', 'Slide ' + (i + 1) + (s.dataset.kind === 'decision' ? ', a call for you' : s.dataset.kind === 'question' ? ', a question for you' : ''));
    b.addEventListener('click', () => show(i));
    track.appendChild(b);
  });

  function show(i) {
    current = Math.max(0, Math.min(slides.length - 1, i));
    if (current > 0 && started === null) started = Date.now();
    seen.add(current);
    slides.forEach((s, n) => s.classList.toggle('active', n === current));
    [...track.children].forEach((b, n) => { b.classList.toggle('seen', seen.has(n)); b.setAttribute('aria-current', n === current); });
    document.getElementById('pos').textContent = (current + 1) + ' / ' + slides.length;
    if (slides[current].dataset.kind === 'close') recap();
    history.replaceState(null, '', '#' + (current + 1));
  }

  function pickText(c) {
    const i = state.picks[c.id];
    if (c.kind === 'question') {
      const parts = [i === undefined ? '' : c.options[i], state.notes[c.id] || ''].filter(Boolean);
      return parts.length ? parts.join('. ') : null;
    }
    if (i === undefined) return null;
    let why = i === c.recommended ? 'matches the recommendation' : 'against the recommendation';
    if (c.timing === 'made') why += i === c.current ? ', keeps what is in place' : ', reverses what is in place';
    return c.options[i] + ' (' + why + ')';
  }

  function recap() {
    const list = document.getElementById('recap');
    list.innerHTML = '';
    calls.forEach(c => {
      const li = document.createElement('li');
      const q = document.createElement('span'); q.className = 'q'; q.textContent = c.question;
      const p = document.createElement('span');
      const pick = pickText(c);
      p.className = pick ? 'pick' : 'none';
      p.textContent = pick || (c.kind === 'question' ? 'No answer yet, so I assume: ' : 'No call yet, so I go with: ') + c.default;
      li.append(q, p);
      if (state.notes[c.id] && c.kind !== 'question') { const n = document.createElement('span'); n.className = 'q'; n.textContent = 'Note: ' + state.notes[c.id]; li.append(n); }
      list.appendChild(li);
    });
  }

  function reply() {
    const lines = ['Check-in calls for ' + meta.project + ' (' + meta.date + ', deck ' + meta.deck + ')'];
    calls.forEach((c, n) => {
      lines.push((n + 1) + '. ' + c.question);
      if (c.kind === 'question') lines.push('   Answer: ' + (pickText(c) || 'no answer, assume: ' + c.default));
      else lines.push('   Call: ' + (pickText(c) || 'no call, go with your default: ' + c.default));
      if (state.notes[c.id] && c.kind !== 'question') lines.push('   Note: ' + state.notes[c.id]);
    });
    if (state.notes._general) lines.push('Also: ' + state.notes._general);
    return lines.join('\n');
  }

  // Decision options and question quick answers share one behavior: click to pick, click again to clear.
  document.querySelectorAll('.option,.chip').forEach(b => {
    const id = b.dataset.decision || b.dataset.question, opt = Number(b.dataset.option);
    const group = '[data-' + (b.dataset.decision ? 'decision' : 'question') + '="' + id + '"]';
    b.setAttribute('aria-pressed', state.picks[id] === opt);
    b.addEventListener('click', () => {
      if (state.picks[id] === opt) delete state.picks[id]; else state.picks[id] = opt;
      document.querySelectorAll(group).forEach(o => o.setAttribute('aria-pressed', state.picks[id] === Number(o.dataset.option)));
      save();
    });
  });
  document.querySelectorAll('.slider input').forEach(r => {
    r.addEventListener('input', () => r.parentElement.style.setProperty('--pos', r.value + '%'));
  });
  document.querySelectorAll('textarea[data-note]').forEach(t => {
    t.value = state.notes[t.dataset.note] || '';
    t.addEventListener('input', () => { state.notes[t.dataset.note] = t.value.trim(); save(); recap(); });
  });

  document.getElementById('copy').addEventListener('click', async () => {
    const text = reply(), done = document.getElementById('copied');
    try { await navigator.clipboard.writeText(text); done.textContent = 'Copied. Paste it back to me.'; }
    catch (e) {
      const t = document.createElement('textarea'); t.value = text; document.body.appendChild(t); t.select();
      try { document.execCommand('copy'); done.textContent = 'Copied. Paste it back to me.'; } catch (err) { done.textContent = 'Copy failed. Select the recap and copy it by hand.'; }
      t.remove();
    }
  });

  const voice = document.getElementById('voice');
  const setQuiet = q => { state.quiet = q; document.body.classList.toggle('quiet', q); voice.setAttribute('aria-pressed', !q); save(); };
  voice.addEventListener('click', () => setQuiet(!state.quiet));
  setQuiet(!!state.quiet);

  document.getElementById('prev').addEventListener('click', () => show(current - 1));
  document.getElementById('next').addEventListener('click', () => show(current + 1));
  document.addEventListener('keydown', e => {
    if (e.target.closest('textarea,input') || e.metaKey || e.ctrlKey || e.altKey) return;
    if (['ArrowRight', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); show(current + 1); }
    else if (['ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); show(current - 1); }
    else if (e.key === 'Home') show(0);
    else if (e.key === 'End') show(slides.length - 1);
    else if (e.key === 'v' || e.key === 'V') setQuiet(!state.quiet);
  });
  let touch = null;
  document.getElementById('stage').addEventListener('touchstart', e => { touch = e.touches[0]; }, {passive: true});
  document.getElementById('stage').addEventListener('touchend', e => {
    if (!touch || e.target.closest('textarea,.option,.chip,.slider')) return;
    const dx = e.changedTouches[0].clientX - touch.clientX, dy = e.changedTouches[0].clientY - touch.clientY;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) show(current + (dx < 0 ? 1 : -1));
    touch = null;
  });
  setInterval(() => {
    const s = started === null ? 0 : (Date.now() - started) / 1000;
    document.getElementById('clock').textContent = fmt(s) + ' / ' + fmt(budget);
  }, 1000);

  document.querySelectorAll('.line-chart[data-chart]').forEach(drawLine);

  const start = parseInt(location.hash.slice(1), 10);
  show(Number.isFinite(start) ? start - 1 : 0);

  // A line chart drawn from its data attribute: hairline grid, 2px lines, a label at each line's end,
  // a tooltip on every point, a legend, and a hidden table for screen readers.
  function drawLine(box) {
    const v = JSON.parse(box.dataset.chart), NS = 'http://www.w3.org/2000/svg';
    const W = 680, H = 240, L = 44, R = 150, T = 14, B = 30, pw = W - L - R, ph = H - T - B, n = v.x.length;
    const unit = v.unit ? ' ' + v.unit : '';
    const vals = v.series.flatMap(s => s.values).filter(x => x !== null);
    let low = Math.min(0, ...vals), high = Math.max(...vals);
    const raw = (high - low) / 4 || 1, pow = Math.pow(10, Math.floor(Math.log10(raw)));
    const step = [1, 2, 2.5, 5, 10].map(m => m * pow).find(x => x >= raw);
    low = Math.floor(low / step) * step; high = Math.ceil(high / step) * step;
    if (high === low) high = low + step;
    const fmt = x => String(Math.round(x * 100) / 100);
    const px = i => L + pw * i / (n - 1), py = x => T + ph * (1 - (x - low) / (high - low));
    const el = (tag, attrs, text, parent) => {
      const e = document.createElementNS(NS, tag);
      Object.entries(attrs).forEach(([k, val]) => e.setAttribute(k, val));
      if (text !== undefined) e.textContent = text;
      (parent || svg).appendChild(e);
      return e;
    };
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', v.question);
    for (let t = low; t <= high + step / 2; t += step) {
      el('line', {class: 'grid', x1: L, x2: L + pw, y1: py(t), y2: py(t)});
      el('text', {class: 'tick', x: L - 8, y: py(t) + 4, 'text-anchor': 'end'}, fmt(t));
    }
    const every = Math.max(1, Math.ceil(n / 6));
    v.x.forEach((label, i) => { if (i % every === 0 || i === n - 1) el('text', {class: 'tick', x: px(i), y: H - 8, 'text-anchor': 'middle'}, label); });
    const ends = [];
    v.series.forEach((line, k) => {
      const cls = 's' + (k + 1);
      let run = [];
      const flush = () => { if (run.length > 1) el('polyline', {class: 'series ' + cls, points: run.join(' ')}); run = []; };
      line.values.forEach((x, i) => { if (x === null) flush(); else run.push(px(i).toFixed(1) + ',' + py(x).toFixed(1)); });
      flush();
      line.values.forEach((x, i) => {
        if (x === null) return;
        const g = el('g', {class: 'pt ' + cls});
        el('circle', {class: 'hit', cx: px(i), cy: py(x), r: 11}, undefined, g);
        el('circle', {class: 'dot', cx: px(i), cy: py(x), r: 4}, undefined, g);
        el('title', {}, line.label + ', ' + v.x[i] + ': ' + fmt(x) + unit, g);
      });
      const last = line.values.map((x, i) => x === null ? -1 : i).reduce((a, b) => Math.max(a, b));
      ends.push({y: py(line.values[last]), cls, label: line.label, value: line.values[last]});
    });
    // Labels sit at the right edge, nudged apart so they never overlap.
    ends.sort((a, b) => a.y - b.y).forEach((e, i) => { if (i) e.y = Math.max(e.y, ends[i - 1].y + 30); });
    ends.forEach(e => {
      const g = el('g', {class: 'end ' + e.cls});
      el('rect', {x: L + pw + 10, y: e.y - 11, width: 10, height: 3, rx: 1.5}, undefined, g);
      el('text', {x: L + pw + 26, y: e.y - 5}, e.label, g);
      el('text', {class: 'val', x: L + pw + 26, y: e.y + 11}, fmt(e.value) + unit, g);
    });
    if (v.series.length > 1) {
      const legend = document.createElement('p');
      legend.className = 'legend';
      v.series.forEach((line, k) => {
        const item = document.createElement('span'); item.className = 's' + (k + 1);
        item.append(document.createElement('i'), line.label);
        legend.append(item);
      });
      box.append(legend);
    }
    box.append(svg);
    const wrap = document.createElement('div'), table = document.createElement('table');
    wrap.className = 'sr-only';
    table.createCaption().textContent = v.question + (v.unit ? ' (' + v.unit + ')' : '');
    const head = table.insertRow(); head.insertCell();
    v.x.forEach(x => { const th = document.createElement('th'); th.textContent = x; head.append(th); });
    v.series.forEach(line => {
      const row = table.insertRow(), th = document.createElement('th');
      th.textContent = line.label; row.append(th);
      line.values.forEach(x => { row.insertCell().textContent = x === null ? '' : fmt(x); });
    });
    wrap.append(table);
    box.append(wrap);
  }
})();
