---
name: foster-fuzz
description: Fuzz-test the app, project or site at hand by driving its real UI like a crowd of realistic users. Maps every screen, flow and state, seeds a throwaway sandbox with believable and nasty data, then clicks, types, interrupts and resizes its way through looking for bugs, broken states and UI/UX problems. Produces a ranked findings report with screenshots and repro steps, and turns confirmed bugs into failing tests. Use when Greg says "fuzz", "fuzz test", "bash on it", "try to break it", "test-drive", "QA pass", or "find bugs in" an app, in Cursor, Claude Code, Codex or a cloud session.
---

# Fuzz

Greg wants you to use the thing the way a few dozen real people would, all at once, and find what breaks before they do. Unit tests prove the code does what its author meant. This skill hunts for what nobody meant: the screen that says "No matches" for half a second while results load, the menu item that fires twice, the title that runs off its card, the error that shows a stack trace, the button Return doesn't press.

You are a tester, not a fixer, until the report is done. Explore widely first, write everything down, and only then fix (or hand back) what you found.

## 1. Learn the project's own rules first

Read before you click. The project's own docs tell you what "correct" means, and most of the best findings are violations of rules the project already wrote down.

- `CLAUDE.md`, `AGENTS.md`, `README`, any glossary, `docs/testing.md`, ADRs. Note every rule a person could see break: "every write is undoable", "no spinners", "errors are sentences, never raw exceptions", "file names have no spaces", "the original is never modified", "no em-dashes in UI copy".
- The route table, command table or API surface. That is the list of things a user can do.
- The existing end-to-end tests, screenshot scripts and tours (`just shots`, `just tour`, `e2e/`, `cypress/`, `playwright.config.*`). Reuse their setup: how they start the server, seed data and reset state. Don't build a second harness when one exists.
- Recent commits titled "fixes from test-driving" or similar. They show which kinds of bugs this app tends to have, so look for more of the same.

Write the result down as a **map**: every screen or view, every flow (a sequence a person does to get something done), every state each screen can be in, and the invariants. Save it with the report. It doubles as your coverage checklist.

## 2. Build a sandbox you can wreck

Never fuzz against real data, production, or anything that sends messages to the outside world.

- Run against a throwaway home, database or library folder (`mktemp -d`). Delete and recreate it between runs.
- Find the project's test switches for side effects and use them. Magpie, for example, has `MAGPIE_HOME`, `MAGPIE_VOLUMES` (fake mounted e-readers) and `MAGPIE_OPENED` (logs the email it would have opened instead of opening Mail). If a flow would send an email, charge a card, post somewhere or touch a real device and there is no fake, stop at the last screen before the send and note it as untested.
- Use the project's dev server or a production build served locally. Prefer the build: some bugs only show up in it.
- If the app is native (a Tauri, Electron or Mac app), drive the web layer headlessly for breadth, then do a short pass in the real app shell with computer use for what only the shell does: menus, keyboard shortcuts, window dragging, file dialogs, system sheets. Magpie's Mac test-drive found five bugs the headless runs couldn't.

## 3. Seed it like real life, then like a bad day

Set up state through the API or core directly (Magpie's `call(page, "books.import", …)`), not by clicking, so you spend your clicks on exploring.

Start with a **believable** world: real-looking names and content in realistic amounts (a shelf of fifteen classics, not "Test Book 1"). Then add the **nasty** cases a real user eventually brings:

- Empty, exactly one, and a lot (hundreds or thousands of items).
- Very long text with no spaces, very short text, emoji, accents, CJK, right-to-left text, leading and trailing whitespace.
- Markup and code in text fields: `<b>`, `&amp;`, `"; DROP TABLE`, `{{name}}`, a pasted URL, a pasted paragraph.
- Missing values ("Unknown", blank, null), duplicates, near-duplicates differing only in case or accents.
- Wrong file types, zero-byte files, huge files, files with spaces and unicode in their names, damaged files.
- Dates at edges: today, the year 1900, the far future, time zones, daylight saving changes.

Pick three to five **personas** from what the app is for and give each a goal: the first-time user with nothing yet, the power user with a big messy library who lives on keyboard shortcuts, the impatient one who double-clicks everything and hits Escape halfway, the careful one who reads every message and tries undo after each step.

## 4. Explore in passes

Drive the UI with whatever browser tool you have: Playwright (preinstalled in cloud sessions), Cursor's or Claude's built-in browser, or computer use for native windows. Work through these passes in order, ticking off the map as you go. Take a screenshot at every new screen and every state change, light and dark if the app has both.

1. **Happy paths per persona.** Do each persona's goal start to finish, the obvious way. Anything that fails here is the most important finding.
2. **Every state of every screen.** Empty, one, many, loading, error, offline or server down, permission denied, locked or read-only, mid-job. Many apps take URL parameters for screens and sheets (Magpie's `?sheet=review&theme=dark`); use them to jump straight to a state.
3. **Inputs.** Put the nasty data from step 3 into every field, search box and file picker. Submit empty forms. Paste instead of type. Check what comes back out matches what went in.
4. **Interruptions and timing.** Double-click and triple-click buttons. Press Escape, Back, Cmd+Z and Reload in the middle of a flow and in the middle of a background job. Type faster than search can answer. Open the same thing in two tabs and change it in both. Cut the network mid-request.
5. **Keyboard and layout.** Do a whole flow with only the keyboard: Tab order, focus rings, Return on the primary button, Escape to close, the documented shortcuts. Resize to a narrow window, a tall one, and 200% zoom. Look for clipped, overlapping or overflowing text.
6. **Recovery.** After every write, try to undo it, then redo it. Delete something and look for it in the trash, removed view or history. Check that a failed action leaves things as they were.
7. **Free play.** Spend the last stretch wandering: follow whatever looked odd, combine features nobody would test together, and repeat the flow that broke with small changes to find the edges of the bug.

Timebox it. Without a budget from Greg, spend about an hour of driving, and say in the report which parts of the map you didn't reach.

## 5. Know a bug when you see one

Watch these on every step, automatically where you can. [references/oracles.md](references/oracles.md) has a Playwright snippet that collects most of them.

- Console errors and warnings, uncaught exceptions, failed or 4xx/5xx network requests, requests that never finish.
- Text a person shouldn't see: stack traces, `undefined`, `NaN`, `[object Object]`, raw error codes, file paths from the machine, unescaped HTML, template placeholders.
- Layout: elements wider than their container, text cut off without an ellipsis, overlapping elements, controls under 24 px, content hidden behind sticky headers.
- Accessibility basics: buttons and fields without names, images without alt text, focus lost after closing a dialog. Run axe if it's installed.
- State that lies: a count that doesn't match the list, "No results" while still loading, a toast saying it worked when it didn't, a stale screen after a change elsewhere.
- The project's own rules from step 1, checked through the API or file system as well as the screen (was the original file modified? did the write record history?).
- UX, judged with fresh eyes on the screenshots: confusing or inconsistent words, an action with no feedback, a destructive action with no confirmation or undo, a dead end with no way back, placeholder text that looks like a typed value, a flow that takes more steps than it should.

Look at the screenshots yourself, one at a time, as someone who has never seen the app. Many of the best findings are visible in a still and invisible to every assertion.

## 6. Write each finding so someone else can fix it

Before a finding goes in the report, reproduce it a second time from a clean sandbox. If it only happens sometimes, say how often. For each one record:

- A one-line title in plain words ("Search shows No matches for a moment while results load").
- Severity: **broken** (data loss, crash, a flow that can't be finished, a broken project rule), **wrong** (incorrect result or misleading state, with a workaround), or **rough** (UX or visual problem, works but feels bad).
- Steps to reproduce from the sandbox, the expected result and the actual result.
- A screenshot or short video, plus console or network output when it helps.
- Where in the code it probably lives, if you can tell quickly. Mark it as a guess.

Merge duplicates (one root cause, many symptoms is one finding). Keep a separate short list of things you couldn't test and why.

## 7. Report, then fix

Write the report to a gitignored folder in the project, such as `fuzz/<YYYY-MM-DD>/` (add it to `.gitignore` if needed): `report.md`, `map.md`, and a `shots/` folder. Open the report with three lines: how many findings at each severity, the single worst one, and how much of the map you covered. Then the findings, worst first. In a Claude project, also publish the report so Greg can read it on his phone.

Then, unless Greg said report only:

- For each **broken** or **wrong** finding, write a failing end-to-end test that reproduces it, in the project's existing test style, then fix it and watch the test pass. One commit per fix.
- Fix **rough** findings that have one obvious answer. Leave the ones that are a design call (wording, layout, whether a confirmation belongs there) in the report as questions for Greg, each with your recommendation.
- Run the project's full check (`just check`, `npm test`, whatever the docs say) before pushing, and follow the project's rules for where to push.

Finally, leave the fuzzing behind in a form you can run again. If the project has no tour or screenshot script, offer to turn your seed data and walk-through into one (Magpie's `just tour` came out of exactly this), so the next pass starts from a richer place.
