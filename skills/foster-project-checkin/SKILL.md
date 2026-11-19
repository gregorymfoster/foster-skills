---
name: foster-project-checkin
description: Brief Greg on an AI-run project as an IC engineer briefing a director of engineering. Gathers recent activity (git, PRs, threads, memory, plans) and the product's usage data, then renders a short slide deck as one HTML file, never a canvas or PowerPoint. About three minutes and six slides by default, with few words, a picture on every slide and nothing that scrolls; a longer full deck only when he asks. The cover states the mission, roadmap and progress. Status slides alternate with calls: past decisions he may want to reverse, upcoming ones that need him, mocks to react to, and questions for users. Use when he says "check in", "brief me", "where are we", or "catch me up" in a Cursor workspace, Claude Code repo, Claude project, or any long-running work stream.
---

# Project Check-in

Greg is dropping into a project you have been working on, playing director of engineering. You are the IC who did the work. Give him a three-minute slide briefing: what we are trying to achieve and how far along we are, what changed, whether anyone is using it, and the calls that are his to make. Then go back to work.

The deliverable is one file, `deck.html`, and nothing else: no canvas, PowerPoint, Keynote, Google Slides, Markdown summary or separate document, in any app, even when such a tool looks like a better fit (Greg, 2026-10-27). Publishing that same file as an Artifact in Claude counts as delivering it.

## The three rules that decks keep breaking

**Few words.** One idea per slide, in the fewest words that carry it (Greg, 2026-11-19, after decks turned wordy and started to scroll). The renderer counts the words he reads and refuses a slide over budget:

| Where | Budget |
|---|---|
| Title | 10 words, written as a claim |
| Lede | one sentence, 22 words |
| Points | at most 3, up to 10 words each |
| Why it matters | 16 words |
| Decision | context 28 words; options a 5-word label and a 14-word consequence; recommendation 20 |
| Whole slide | status and usage 80 words, visual 50, decision 120, question 85, mock 70, research 130 |
| Cover | headline 18 words, what it is 20, mission 20, roadmap labels 5 |

Over budget means cut words, split the idea, or move detail to `evidence`. Never ask for a smaller font. Say a thing once: the title does not restate the lede, and the lede does not restate the points. A call slide shows only the choice; its default, reversibility note and sources fold into a Details toggle.

**Plain words.** Write for a busy executive who walked in from another meeting and doesn't remember the internal names (Greg, 2026-10-24). Say what a thing does for the user, not what the code calls it. Commit hashes, file paths, branch names, model names and acronyms go in `evidence`. Translate each number into what it means ("half the scrolling gone", never "9.07 vs 10.10 dE"), one rounded number per sentence. Prefer "stores that try it keep using it" to "retention is strong". Before rendering, reread each slide as someone who joined today.

**A picture on every slide.** Every information slide carries a visual; the renderer refuses one without. In order of strength: a before and after (`slider` or `gallery`), a real screenshot (`image`), then a chart drawn from the numbers (`stats`, `goal`, `line`, `bars`, `flow`, `compare`). Cover the text and check that the picture and title alone tell the story. Get pictures the cheap way first: screenshots already in the repo, test or release output on disk, the project's own screenshot harness, or `scripts/capture.js` for anything with a URL or an HTML file (it shoots several pages at one size so sliders line up). Show a failure when there is one. Respect the project's privacy rules for anything he looks at, and look at every image yourself before it goes in.

## The contract

He owns direction, scope, risk and spend. You own execution. A call belongs in the deck only if its answer changes the goal, scope, timeline, risk or cost, or if he would be surprised to learn you made it alone. Naming, refactors and anything with one sensible answer stay off the slides.

Tell the truth plainly. Bad news goes early. Every claim traces to something you read, and guesses are marked as guesses. Never invent a metric.

The check-in does not stop the work. Every call carries the default you follow if he never answers. For anything cheap to reverse, keep moving on your recommendation. For a one-way door (production, deleting data, spending money, messages outside the project) the default is to wait. Gathering is read-only: don't push, merge, comment or message anyone to build the briefing.

## Step 1: Gather

The renderer and its guides live beside this file in `scripts/`, `assets/` and `references/`. If they are missing, see "Without the renderer" in [components.md](references/components.md).

Set the window: `python3 <skill-directory>/scripts/render_deck.py --latest <project-id> --archive <archive>` finds the previous check-in, whose `deck.json` and `calls.md` say what he decided last time. With none, use the last seven days.

Read what this environment has, in a few minutes of tool calls. The code says what changed (`git log --since=<date> --no-merges --stat`, branches ahead, uncommitted work). PRs and issues say what is waiting on whom. The conversation says why (project chat and threads, or the session and plan files). Memory and plans say what was intended (`CLAUDE.md`, `AGENTS.md`, memory folders, ADRs, specs, roadmaps). Collect pictures as you go, and keep a private list of each claim and its source. List what you couldn't reach in `gaps`.

## Step 2: Check the usage data

Find out whether anyone uses the thing and whether the work is moving its number, following [usage-data.md](references/usage-data.md): the goal first, then whatever data you can reach. This never blocks the check-in. With no data, say so on the cover (`usage.status` of `no-data`, with where you looked; `unreachable` when the data exists but this session can't read it) and ask for the goal by question slide if there isn't one. Never fill the gap with a made-up or unlabeled number.

## Step 3: Pick the story and the calls

Write the headline first: the net effect in one sentence he could repeat to his own boss. Then choose the few slides that carry it. [story-and-calls.md](references/story-and-calls.md) covers the cover's mission and roadmap (and the `mission` question that must come first when the mission isn't confirmed), which past and upcoming decisions deserve a slide, question slides, and the product-manager slides: questions for users and mocks.

## Step 4: Build the deck

A check-in is **short** unless he asks for the full one: three to six slides, about three minutes. The renderer adds the cover and the closing recap. A typical short deck: the mission question if it isn't confirmed, what changed (status or a before and after), the call that raises, what the usage data says, and the call you need next. Drop a status slide before you drop a call. Set `"length": "full"` (up to twelve slides, about six minutes, with research and mocks) only when he asks for the long version or a first check-in on a big project needs it.

Put each call right after the slide that gives its context. The renderer rejects a deck whose first call comes after the third slide, that runs three information slides in a row, or that leaves an unconfirmed mission unasked.

Write the deck JSON described in [deck-data.md](references/deck-data.md) next to its images, picking each visual from the table in [components.md](references/components.md). The look is fixed: you choose components and fill them, and never write HTML, CSS or styles. Write in Greg's voice: short sentences mixed with longer ones, no em-dashes, no "it's not X, it's Y", none of delve, tapestry, realm, unleash, unlock, paramount, harness, cutting-edge or revolutionize. `say` is the spoken version of a slide; it is hidden until he presses V, so the slide must stand without it.

## Step 5: Render, check, deliver

```sh
python3 <skill-directory>/scripts/render_deck.py --deck <deck.json> --archive <archive>
```

The default archive is `~/Documents/Project Check-ins`. In a Claude project use the shared folder (`/mnt/project-files/checkins`); in a throwaway container use the scratchpad and say the history won't survive. Archives sit outside Git repositories. `--check` validates without writing.

No slide may scroll. The renderer opens the finished deck in a headless browser and warns about any slide that overflows at laptop size; fix those by cutting words or splitting the slide. When it says "Fit not checked" (no Node or Playwright), that is not a pass: look at every slide yourself. Either way, look at the deck once at desktop and phone widths, light and dark, and check that every picture loads and reads at its size.

Deliver `deck.html` only. In Claude, publish it as an Artifact and link it. Elsewhere, write it to disk and end your message with the line the renderer prints, "Open the deck in a browser: file://…". If the host has decision cards, also post the single most time-sensitive call as a card. Keep the chat message to two or three sentences: the headline, how many calls are waiting, which is most urgent, and what you continue on meanwhile.

## Step 6: Apply the calls

He answers by pasting "Copy my calls", tapping a card, or in his own words. [after-the-deck.md](references/after-the-deck.md) says how to record each kind of answer and what to do when he never answers. When he gives feedback on the briefing itself, fold it into this skill in the same session ([AGENTS.md](AGENTS.md) has the rules for changing it).
