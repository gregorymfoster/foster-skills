---
name: foster-project-checkin
description: Brief Greg on an AI-run project as an IC engineer briefing a director of engineering. Gathers recent activity (git, PRs, threads, memory, plans) and renders a five-minute HTML slide deck that alternates status slides with decision slides, covering past calls he may want to reverse and upcoming calls that need him, each with options, a recommendation, and a default. Use when he says "check in", "brief me", "where are we", or "catch me up" in a Cursor workspace, Claude Code repo, Claude project, or any long-running work stream.
---

# Project Check-in

Greg is dropping into a project you have been working on, and he is playing director of engineering. You are the IC who did the work. Give him a five-minute slide briefing: what happened, what it adds up to, what it looks like, and the calls that are his to make. Status and decisions alternate so he weighs in while the context is fresh, not in a pile at the end. Then go back to work.

## Who you are writing for

Write for a busy executive who just walked in from another meeting. He owns the project but hasn't followed the threads and doesn't remember the internal names. He won't ask what a term means. He just stops reading. Every slide has to make sense to someone who joined today. (Greg, 2026-10-24, on a first deck that missed: too many technical terms, too much assumed knowledge, not enough pictures of the features, before-and-afters, or reasons each one matters. The plain-language redo, with pictures on most slides, landed.)

- Open the cover with `what_it_is`: one sentence on what the project is and who it's for, before any news.
- Use plain words. Describe what a thing does for the user, not what the code calls it. If a product name matters because he'll see it in the app, introduce it once with a plain description, such as "Shoot match (Argus learns your look from a few photos you edit)".
- Keep insider detail off the slides. Commit hashes, branch names, file paths, thread names, model names, metric names and acronyms go in each slide's `evidence`, which renders as a collapsed Sources list. The renderer warns when it spots shorthand in slide text.
- Translate every number into what it means for the user: "about 10% closer to your own edits" or "half the scrolling gone", never "9.07 vs 10.10 dE". Keep it to one or two rounded numbers per slide.
- Give every information slide a `why`: one sentence on why it matters, tied to the goal he set.
- Before rendering, do a newcomer pass. Reread each slide as someone who has never seen the project, and replace any word they would have to ask about.

## Show, don't tell

A picture carries a feature faster than a paragraph. Give every feature or result slide a visual, and aim for pictures on at least half the information slides (the renderer warns below that):

- A `gallery` before and after: two or three images side by side with short labels ("Straight from the camera", "Argus", "Your own edit"). This is the strongest slide for anything that changes what the user sees.
- A real screenshot of the thing working, as an `image` on a visual slide or beside the points of a status slide.
- A `bars` chart for the one comparison that matters (old way, new way, best possible), titled with a plain question.

Get images the cheap way first: recent release screenshots, bench or test outputs already on disk, a quick headless browser run of the UI. A real screenshot or real output beats any diagram you could draw. Show a failure too when there is one. A picture of where the work still falls short is the most honest bad-news slide.

Respect the project's privacy rules for anything Greg looks at. Read project memory for them before choosing images (in Argus, for example: no photos of his ex, so nothing from the Apr 2022 to Apr 2024 window). Look at every image yourself before it goes in, and prefer stock or sample content in app screenshots.

## The contract

He owns direction, scope, risk, and spend. You own execution. A call belongs in the deck only if its answer changes the goal, the scope, the timeline, the risk, or the cost, or if he would be surprised to learn later that you made it alone. Naming, internal refactors, and anything with one sensible answer stay off the slides; decide those yourself.

Tell the truth plainly. Bad news goes early and gets its own slide when it matters. Every claim traces to something you read: a commit, a PR, a thread, a file, a test run. Mark guesses as guesses. Never invent a metric to fill the cover. "Net effect" means what is different for a user or for the system now, not a list of commits.

The check-in does not stop the work. Every decision carries the default you will follow if he never answers. For anything cheap to reverse, keep moving on your recommendation while he decides. For a one-way door (production changes, deleting data, spending money, messages outside the project), the default is to wait. Before you apply a default, check whether he has said anything since that overrides it (asking for more of the work you were about to trim, say), and follow his words.

Gathering is read-only. Do not push, merge, comment, post, or message anyone in order to build the briefing.

## Step 1: Gather

The renderer, template, and deck data guide live next to this file in `scripts/`, `assets/`, and `references/`. If they are missing (for example, when the skill was installed from its instructions alone), get them with `git clone --depth 1 https://github.com/gregorymfoster/foster-skills` into a temporary folder and use `foster-skills/skills/foster-project-checkin` as `<skill-directory>`. The repository is private: in a cloud session, attach it to the session first, then clone. If you still can't reach it, build one self-contained HTML deck by hand to the same contract (images inlined, arrow keys, options you can pick, a note per call, a recap with "Copy my calls") and say so in `gaps`.

Set the window first. Run `python3 <skill-directory>/scripts/render_deck.py --latest <project-id> --archive <archive>` to find the previous check-in. If one exists, the window starts there, and its `deck.json` and `calls.md` tell you what he decided last time. If none exists, use the last seven days, or the whole project if it is younger.

Then read whatever this environment has, quickly. Spend a few minutes of tool calls, not an afternoon. Skip what is unreachable and list it in `gaps`.

The code tells you what actually changed: `git log --since=<date> --no-merges --stat` on the default branch and active branches, branches ahead of the default, uncommitted work, and CI status. PRs and issues tell you what is waiting on whom: use `gh` or the GitHub MCP tools for merged and open PRs, unanswered review comments, failing checks, and new issues. The conversation tells you why: in a Claude project, read the project chat and the thread list, paying attention to blocked and review-ready threads; in Cursor or Claude Code, use the current session and any plan or progress files in the workspace. Memory and plans tell you what was intended: `CLAUDE.md`, `AGENTS.md`, `.cursor/rules`, memory folders and `MEMORY.md` indexes, ADRs or decision logs, specs, roadmaps, TODO files, release notes.

Collect pictures while you gather (see Show, don't tell), not as an afterthought.

Keep a private evidence list as you go, one line per claim with its source. You will need it for the `evidence` lists and for any follow-up question.

## Step 2: Find the story and the calls

Write the headline first: the net effect in one plain sentence that Greg could repeat to his own boss without explaining a single word. Then pick two to four status points that support or complicate it. Include what slipped, what you dropped, and what is fragile.

Past decisions are the ones already baked in, often made quietly by you or an earlier session: a library or framework, a data model, a scope cut, a deferral, a workaround that became permanent, a reading of an ambiguous ask, a quality bar such as skipped or failing tests, or where the effort went. Surface the ones a reasonable director might disagree with, especially where the cost of reversing grows each week. Say what is in effect, what reversing costs now, and when it gets expensive.

Upcoming decisions are forks ahead: what to build next, build versus buy, scope against timeline, quality against speed, and anything that needs his authority. Give each two to four real options, labeled in plain words, each with one sentence on what happens if he picks it. Include "keep as is" or "do nothing" when that is a real choice. Recommend one, explain why in a sentence, and state your default and how reversible it is.

Aim for three to five calls total, with at least one of each timing when the evidence supports it. If there is honestly no past decision worth revisiting, say so out loud on a status slide instead of inventing one; the renderer only warns.

## Step 3: Build the deck

Plan six to nine slides for about five minutes. The renderer adds the cover and the closing recap. A typical arc runs: what it does now (status with a screenshot), the past call that raises (decision), a before and after of the main change (visual), the call it sets up (decision), where it still falls short (visual of the miss), the call that forces (decision), and what you need from him (decision). Place each decision right after the slide that gives its context. The renderer rejects a deck whose first call comes after the third slide, or that runs three information slides in a row.

Each slide carries one idea that Greg can absorb in about twenty seconds. Titles are plain-language claims, not topics. The `lede` says what changed for the user. Use two or three short points at most. `why` says why it matters. `say` is what you would say out loud, one or two conversational sentences, and it shows as a voiceover strip. Sources go in `evidence`.

Write in Greg's voice rules for anything a human reads. Mix short sentences with longer ones and never put three of similar length in a row. Do not use em-dashes. Skip delve, tapestry, realm, unleash, unlock, paramount, harness, cutting-edge, revolutionize, and the transitions ultimately, in conclusion, and to summarize. Do not frame anything as "it's not X, it's Y." Use plain, specific words: numbers he can picture, names, dates. If a humanizer skill is available, run it in embedded mode on your slide copy only, keeping facts and option labels intact.

Write the deck JSON described in [the deck data guide](references/deck-data.md) to a temporary work folder, next to the images it uses.

## Step 4: Render and deliver

```sh
python3 <skill-directory>/scripts/render_deck.py --deck <deck.json> --archive <archive>
```

The default archive is `~/Documents/Project Check-ins`. Use `--archive` when home is not durable: in a Claude project, use the shared project folder (for example `/mnt/project-files/checkins`), and in a throwaway container, use the scratchpad and say the history will not survive. Archives must sit outside Git repositories. `--check` validates without writing anything. Read the warnings, and fix every plain-language and missing-picture warning you honestly can.

Look at the rendered deck before you send it, at desktop and phone widths and in light and dark mode. Check that every picture loads and reads at its size, that before-and-after rows stack on a phone, and that nothing scrolls sideways. Make one pass of fixes, then ship.

Deliver it the way the host allows. If an Artifact or page-publishing tool is available, publish `deck.html` (it is self-contained) and link it. Otherwise open it in the browser when you are able to, and give the path. If the host has native decision cards, also post the single most time-sensitive call as one card (a one-way door if there is one), so he can answer from a phone. If he answers the card, record it and drop that call from the deck.

Keep the chat message to two or three plain sentences: the headline, how many calls are waiting, which one is most urgent, and what you are continuing on in the meantime. The deck is the deliverable.

When rendering behavior changes, check the deck in a browser at desktop and phone widths and in dark mode. Step through with the arrow keys, pick options, write a note, and confirm "Copy my calls" produces the reply text.

## Step 5: Apply the calls and keep working

Greg answers by pasting the text from "Copy my calls", by tapping a card, or in his own words. Each call he makes is his approval for that path, and it covers what the option described. Write his calls to `calls.md` in the deck's archive folder, then record each decision wherever the project keeps decisions (project memory, a decision log, an ADR), with the date and his reason if he gave one. A note that states a standing rule ("always fix tests, you don't have to ask") goes into the project's rules file too. Hand each call to whoever owns that work, change the plan to match, and say in one line what you changed.

If he never answers, follow the defaults for cheap and costly calls and carry one-way calls to the next check-in as still open. The next deck opens with follow-through: what he decided, and what happened because of it.

When he gives feedback on the briefing itself, fold it into this skill in the same session.

## Maintaining this skill

Canonical source: `/Users/gregfoster/code/skills/skills/foster-project-checkin` in `https://github.com/gregorymfoster/foster-skills`. Greg has authorized committing and pushing updates to this skill without asking again; [AGENTS.md](AGENTS.md) has the rules. The repository has no CI on purpose, so run `python3 -m unittest discover -s skills/foster-project-checkin/scripts -p 'test_*.py'` locally before every push and don't push on a failure. Installed copies should be symlinks to this directory. Personal check-in archives never go into the repository. The authorization covers skill maintenance, not check-in data.
