#!/usr/bin/env node
// Does every slide fit its box without scrolling? Opens a rendered deck.html in headless Chromium (needs Playwright)
// and reports, per viewport, the slides that overflow before the page shrinks them and the shrink each one needed.
// Usage: node check_fit.js <deck.html> [--shots <dir>]   Exit code 1 when a slide overflows at the laptop size (1280x720).
const path = require('path');
const { chromium } = require('playwright');

const VIEWPORTS = [[1440, 900], [1280, 720], [1024, 640]];
const LAPTOP = '1280x720';

(async () => {
  const args = process.argv.slice(2);
  const file = args.find(a => !a.startsWith('--'));
  const shots = args.includes('--shots') ? args[args.indexOf('--shots') + 1] : null;
  if (!file) { console.error('Usage: node check_fit.js <deck.html> [--shots <dir>]'); process.exit(2); }
  const browser = await chromium.launch();
  let failed = false;
  for (const [w, h] of VIEWPORTS) {
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await page.goto('file://' + path.resolve(file));
    const n = await page.evaluate(() => document.querySelectorAll('.slide').length);
    const said = await page.evaluate(() => [...document.querySelectorAll('.say')].some(e => getComputedStyle(e).display !== 'none'));
    if (said && !failed) { console.log('voiceover: showing on load; it should start hidden'); failed = true; }
    const rows = [];
    for (let i = 0; i < n; i++) {
      await page.evaluate(i => location.hash = '#' + (i + 1), i);
      await page.keyboard.press('End'); await page.keyboard.press('Home');
      for (let k = 0; k < i; k++) await page.keyboard.press('ArrowRight');
      const r = await page.evaluate(() => {
        const s = document.querySelector('.slide.active');
        const fit = s.style.getPropertyValue('--fit');
        s.style.removeProperty('--fit');
        const over = s.scrollHeight - s.clientHeight;
        if (fit) s.style.setProperty('--fit', fit);
        return { kind: s.dataset.kind, over, fit: fit || '1' };
      });
      rows.push(r);
      if (shots && `${w}x${h}` === LAPTOP) await page.screenshot({ path: path.join(shots, `slide-${i + 1}-${r.kind}.png`) });
    }
    const bad = rows.map((r, i) => r.over > 1 ? `${i + 1} ${r.kind} (+${r.over}px, shrunk to ${Math.round(r.fit * 100)}%)` : null).filter(Boolean);
    console.log(`${w}x${h}: ${bad.length ? 'overflow on slide ' + bad.join(', ') : 'every slide fits'}`);
    if (`${w}x${h}` === LAPTOP && bad.length) failed = true;
    await page.close();
  }
  await browser.close();
  process.exit(failed ? 1 : 0);
})();
