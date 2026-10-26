# Oracles: catching bugs automatically while you drive

Attach this to every page before you start a pass. It records console errors, uncaught exceptions, failed requests and slow requests, and gives you two checks to run after each step: one for text a person shouldn't see and one for layout overflow. It needs only Playwright, which is preinstalled in cloud sessions (`require('playwright')`).

```js
// fuzz-oracles.js: watch a Playwright page and collect anything suspicious.
export function watch(page, findings, label = () => page.url()) {
  const add = (kind, detail) => findings.push({ kind, detail, where: label(), at: new Date().toISOString() });
  page.on("console", (m) => (m.type() === "error" || m.type() === "warning") && add(`console.${m.type()}`, m.text()));
  page.on("pageerror", (e) => add("uncaught", `${e.message}\n${e.stack ?? ""}`));
  page.on("requestfailed", (r) => add("request-failed", `${r.method()} ${r.url()} ${r.failure()?.errorText ?? ""}`));
  page.on("response", (r) => r.status() >= 400 && add(`http-${r.status()}`, `${r.request().method()} ${r.url()}`));
  const started = new Map();
  page.on("request", (r) => started.set(r, Date.now()));
  page.on("requestfinished", (r) => {
    const ms = Date.now() - (started.get(r) ?? Date.now());
    if (ms > 3000) add("slow-request", `${ms} ms ${r.method()} ${r.url()}`);
  });
}

// Text that should never reach a person.
const LEAKS = /\bundefined\b|\bNaN\b|\[object Object\]|\bnull\b|Error:|at \S+ \(|Traceback|\{\{.*?\}\}|&amp;|&lt;|<\/?[a-z]+>|\/(tmp|Users|home|var)\//;

export async function leakedText(page) {
  return page.evaluate((src) => {
    const re = new RegExp(src);
    const out = [];
    const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let n = walk.nextNode(); n; n = walk.nextNode()) {
      const t = n.textContent.trim();
      if (t && re.test(t) && n.parentElement.closest("script,style,code,pre") === null) out.push(t.slice(0, 160));
    }
    for (const el of document.querySelectorAll("input,textarea")) if (el.placeholder && re.test(el.placeholder)) out.push(`placeholder: ${el.placeholder}`);
    return out;
  }, LEAKS.source);
}

// Visible elements whose content spills out of them without an ellipsis, and tiny targets.
export async function layoutProblems(page) {
  return page.evaluate(() => {
    const out = [];
    const vw = document.documentElement.clientWidth;
    if (document.documentElement.scrollWidth > vw + 1) out.push(`page scrolls sideways (${document.documentElement.scrollWidth}px > ${vw}px)`);
    for (const el of document.querySelectorAll("body *")) {
      const s = getComputedStyle(el);
      if (s.display === "none" || s.visibility === "hidden" || el.getClientRects().length === 0) continue;
      const clipped = el.scrollWidth > el.clientWidth + 1 && s.overflowX !== "auto" && s.overflowX !== "scroll" && s.textOverflow !== "ellipsis";
      if (clipped && el.children.length === 0 && el.textContent.trim()) out.push(`text spills out: "${el.textContent.trim().slice(0, 60)}"`);
      if (el.matches("button,a[href],[role=button],input,select")) {
        const r = el.getBoundingClientRect();
        if (r.width > 0 && (r.width < 24 || r.height < 24)) out.push(`small target ${Math.round(r.width)}x${Math.round(r.height)}: ${el.getAttribute("aria-label") || el.textContent.trim().slice(0, 40)}`);
        if (!el.getAttribute("aria-label") && !el.textContent.trim() && !el.labels?.length && !el.title) out.push(`control with no name: <${el.tagName.toLowerCase()} class="${el.className}">`);
      }
    }
    return [...new Set(out)];
  });
}
```

A pass then looks like this. Keep the step label meaningful, because it becomes the "where" in each finding.

```js
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)("playwright"); // works in projects and with a global install
import { watch, leakedText, layoutProblems } from "./fuzz-oracles.js";

const findings = [];
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
let step = "start";
watch(page, findings, () => step);

async function check(name) {
  step = name;
  await page.waitForTimeout(300);
  for (const t of await leakedText(page)) findings.push({ kind: "leaked-text", detail: t, where: name });
  for (const p of await layoutProblems(page)) findings.push({ kind: "layout", detail: p, where: name });
  await page.screenshot({ path: `fuzz/shots/${String(findings.length).padStart(3, "0")}-${name}.png` });
}

await page.goto("http://127.0.0.1:4319/");
await check("first-launch");
// ...drive a flow, calling check() after every step...
```

These are leads, not findings. The regexes are blunt on purpose and will flag real words like "null" in a book title, so look at each hit before it goes in the report. If axe is in the project (`@axe-core/playwright`), run it on each screen as well.

## Interruptions worth scripting

Some timing bugs are hard to hit by hand. These one-liners make them easy:

```js
await page.getByRole("button", { name: "Save" }).dblclick();             // does it save twice?
await page.route("**/api/**", (r) => setTimeout(() => r.continue(), 2000)); // slow server: what shows while waiting?
await page.context().setOffline(true);                                   // offline mid-flow
await page.keyboard.type("austen", { delay: 10 });                        // typing faster than search answers
await page.setViewportSize({ width: 600, height: 800 });                  // narrow window
await page.emulateMedia({ colorScheme: "dark" });                         // dark mode
const second = await page.context().newPage(); await second.goto(page.url()); // same thing in two tabs
```
