#!/usr/bin/env node
// Take same-size screenshots for a check-in deck, so before-and-after sliders line up. Needs Node with Playwright.
//
//   node capture.js --out shots today=http://localhost:3000/search mock=./mock.html
//
// Each name=target pair becomes <out>/<name>.png. A target is a URL or a local HTML file. Options:
//   --width 1280 --height 800   viewport (every shot in one run shares it)
//   --selector "main .results"  shoot one element instead of the viewport
//   --dark                      dark color scheme
//   --wait 500                  extra milliseconds after load, for late-drawing pages
//   --full                      the whole page instead of the viewport (don't use for sliders)
// Native apps have no URL: use the project's own screenshot harness (a simulator run, a test tour) and keep the sizes equal.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const args = process.argv.slice(2);
  const opt = (name, fallback) => { const i = args.indexOf('--' + name); return i < 0 ? fallback : args[i + 1]; };
  const flag = name => args.includes('--' + name);
  const valued = ['out', 'width', 'height', 'selector', 'wait'];
  const pairs = args.filter((a, i) => !a.startsWith('--') && !valued.includes((args[i - 1] || '').slice(2)) && a.includes('='));
  if (!pairs.length) { console.error('Usage: node capture.js --out <dir> name=<url or file> [name=<url or file> ...]'); process.exit(2); }
  const out = opt('out', '.');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: Number(opt('width', 1280)), height: Number(opt('height', 800)) },
    deviceScaleFactor: 2, colorScheme: flag('dark') ? 'dark' : 'light',
  });
  let failed = false;
  for (const pair of pairs) {
    const name = pair.slice(0, pair.indexOf('=')), target = pair.slice(pair.indexOf('=') + 1);
    const url = /^https?:\/\//.test(target) ? target : 'file://' + path.resolve(target);
    const file = path.join(out, name + '.png');
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(Number(opt('wait', 0)));
      const selector = opt('selector');
      if (selector) await page.locator(selector).first().screenshot({ path: file });
      else await page.screenshot({ path: file, fullPage: flag('full') });
      console.log(file);
    } catch (error) {
      failed = true;
      console.error(`${name}: ${String(error.message).split('\n')[0]}`);
    }
  }
  await browser.close();
  process.exit(failed ? 1 : 0);
})();
