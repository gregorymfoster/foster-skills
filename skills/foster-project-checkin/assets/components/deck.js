(() => {
  const meta = JSON.parse(document.getElementById('meta').textContent);
  const slides = [...document.querySelectorAll('.slide')];
  const track = document.getElementById('track');
  const key = 'checkin:' + meta.deck;
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
    meta.calls.forEach(c => {
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
    meta.calls.forEach((c, n) => {
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

  const start = parseInt(location.hash.slice(1), 10);
  show(Number.isFinite(start) ? start - 1 : 0);
})();
