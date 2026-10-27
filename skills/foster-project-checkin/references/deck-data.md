# Deck data

The renderer takes one JSON object and produces a single offline HTML deck. It adds a cover slide built from the top-level fields and a closing "Your calls" slide built from the decisions, so `slides` holds only the middle of the talk. All text renders as escaped plain text. There is no Markdown and no HTML, and no field for styling: the look comes from the shared components in [components.md](components.md), and the renderer refuses any field it doesn't know. `assets/sample/deck.json` is a full worked example.

```json
{
  "project": "Search service",
  "project_id": "search-service",
  "window": "Since Oct 17 (last check-in)",
  "what_it_is": "A search box that lets staff find any product in the catalog.",
  "headline": "Staff can search the whole catalog now, but results are still sorted by date and two old apps still use the old search.",
  "hero": {"src": "screens/search.png", "alt": "The new search page", "caption": "The staging build."},
  "metrics": [
    {"value": "14", "label": "PRs merged"},
    {"value": "180 ms", "label": "p95 query time"}
  ],
  "usage": {
    "status": "at-risk",
    "goal": "150 of our 200 stores searching every week by Dec 1",
    "sources": [{"name": "Search event log", "as_of": "Oct 26"}]
  },
  "gaps": ["Cursor chat history (not readable from this session)"],
  "slides": [
    {
      "kind": "status",
      "title": "Search is live for internal users",
      "lede": "Anyone on staff can search the full catalog. Customers still see the old page.",
      "body": "Optional extra paragraph. Keep it short.",
      "points": [
        {"text": "Index rebuilt nightly", "state": "done", "url": "https://github.com/org/repo/pull/41"},
        {"text": "Typo tolerance", "state": "moving"},
        {"text": "Faceted filters", "state": "dropped"}
      ],
      "visual": {"type": "bars", "question": "Seconds for staff to find a product", "unit": "s", "bars": [{"label": "Old catalog page", "value": 40}, {"label": "New search", "value": 6, "highlight": true}]},
      "why": "Support stops asking engineers to look products up.",
      "say": "One to three sentences, the way you would say it out loud.",
      "evidence": [{"label": "PR #41", "url": "https://github.com/org/repo/pull/41"}],
      "seconds": 35
    },
    {
      "kind": "decision",
      "id": "sqlite-index",
      "timing": "made",
      "question": "Keep the index in SQLite, or move to Postgres now?",
      "context": "I picked SQLite in week one to ship fast. It works, but writes lock the whole file and the nightly rebuild now takes 40 minutes.",
      "options": [
        {"label": "Keep SQLite", "consequence": "No migration. Rebuild time keeps growing with the catalog."},
        {"label": "Move to Postgres", "consequence": "About two days. Removes the lock and the rebuild window."}
      ],
      "current": 0,
      "recommended": 1,
      "recommendation": "The migration is two days today and gets worse with every table we add.",
      "default": "Keep SQLite and revisit at the next check-in.",
      "reversibility": "costly",
      "reversibility_note": "Cheap until the ranking tables land next week.",
      "needed_by": "Before ranking work starts",
      "evidence": [{"label": "PR #38", "url": "https://github.com/org/repo/pull/38"}]
    },
    {
      "kind": "usage",
      "data_from": "search event log, Sep 22 to Oct 26",
      "title": "112 of 200 stores search every week, behind the pace for December",
      "lede": "Use grew fast after launch, then flattened. At this rate about 130 stores search weekly by Dec 1.",
      "points": [
        {"text": "9 in 10 stores that try it come back the next week", "state": "up"},
        {"text": "Night shifts search three times as often as day shifts", "state": "surprise"},
        {"text": "Two stores' scanners never report searches", "state": "data-gap"}
      ],
      "visual": {"type": "goal", "metric": "Stores searching every week", "current": 112, "target": 150, "projected": 130, "by": "Dec 1", "status": "at-risk"},
      "why": "Stores that start keep going, so the gap is the stores that haven't tried it.",
      "evidence": [{"label": "Event log: distinct stores with a staff search, per week, test accounts excluded"}]
    },
    {
      "kind": "visual",
      "title": "What a staff search looks like today",
      "lede": "Results are correct but sorted by date, not relevance.",
      "visual": {"type": "gallery", "images": [{"src": "screens/before.png", "alt": "Old results page", "label": "Before"}, {"src": "screens/after.png", "alt": "New results page", "label": "After"}], "caption": "The same query, Oct 10 and today."},
      "why": "Staff find the right product on the first screen."
    }
  ],
  "next": ["Typo tolerance behind a flag", "Move the two old clients"]
}
```

## Top level

`project` is the display name. `what_it_is` is optional but strongly encouraged: one plain sentence (240 characters or fewer) on what the project is and who it's for, shown above the headline, for a director who has forgotten or never knew. `hero` is an optional image (`src`, `alt`, `caption`) shown on the cover. `project_id` is a stable kebab-case slug; the archive groups decks by it, and `--latest <project_id>` finds the previous check-in. `window` names the period covered in words. `headline` is the net effect in one plain sentence of 180 characters or fewer. `metrics` is optional, at most four, and every number in it must come from a source you checked. `usage` is required on every deck: the result of the usage data step in [usage-data.md](usage-data.md), shown on the cover as one line. It has a `status` of `on-track`, `at-risk`, `off-track` or `too-early` (data and a goal), `no-goal` (data but no agreed target) or `no-data` (nothing measures the project); a `goal` in plain words, required for the first four and refused for `no-goal`; `sources`, each with a `name`, an optional `as_of` saying how fresh it is and an optional `url`, required unless the status is `no-data`; and `searched`, the places you looked, required when the status is `no-data` (which takes no sources). `gaps` lists sources you could not read so the director knows what the briefing is blind to. `next` is required: what you keep working on while the calls are open.

## Slides

There are five kinds. Every slide takes an optional `say` (the voiceover line, shown under the slide and toggled with V) and an optional `seconds` (defaults: status 35, visual 35, usage 40, decision 50, question 40). The cover adds 20 seconds and the close adds 25.

Every information slide (status, visual or usage) also takes `why`, one sentence on why it matters to the user or the goal, shown under the content, and `evidence`, a list of `label` with optional `url`, shown as a collapsed Sources list. Put commit hashes, file paths, branch names and metric names there, not in the slide text.

A **status** slide needs `title` and `lede`, takes up to five `points`, and takes an optional `visual` of any type, shown beside the points. A point has `text`, an optional `url`, and a `state` of `done`, `moving`, `blocked`, `dropped`, or `risk`. Write the title as a claim ("Search is live for internal users"), not a topic ("Search update"). The lede is the so-what.

A **usage** slide shows what the usage data says. It takes the same fields as a status slide plus a required `data_from`, the source and the dates it covers in plain words ("search event log, Sep 22 to Oct 26"), shown in the eyebrow. Its points are findings whose `state` is `up`, `down` or `flat` (a metric that moved or didn't), `surprise`, `data-gap` (a hole or flaw in the data) or `blocked` (something stops you measuring). Give it a `goal` visual when there is a goal, or a `line` for the trend. Put the queries, tables and event names in `evidence`.

A **visual** slide needs `title`, `lede`, and a `visual` of one of ten types. [components.md](components.md) has a table for picking one by the job the slide does. `gallery` takes two or three `images`, each with `src`, `alt` and a short `label` ("Before", "After", "Your own edit"); it is the best way to show anything that changes what a user sees. `slider` takes `before` and `after`, each with `src`, `alt` and `label`, and lets the director drag a handle across two same-size screenshots of the same view. `goal` takes a plain `metric` label, numeric `current` and `target`, optional numeric `baseline` (default 0) and `projected`, optional `unit` and `by`, and a `status` of `on-track`, `at-risk`, `off-track` or `too-early`. `stats` takes one to four `stats`, each with a short `value` string, a `label`, an optional `change` ("up from 41%") and an optional `tone` of `good`, `bad` or `neutral`. `line` takes a plain-language `question`, an optional `unit`, `x` (2 to 12 labels such as dates) and one to three `series`, each with a `label` and one number (or null) per x label. `bars` takes a plain-language `question`, an optional `unit`, and two to six `bars`, each with `label`, a numeric `value`, and optional `highlight`; use it for one comparison that matters (old way, new way, best possible). `image` takes `src` and `alt`; a local path (relative to the deck JSON) is inlined as base64 so the deck stays one file, and `https://` and `data:image/` sources pass through. SVG diagrams go here too, as image files, so nothing in them can run. `flow` takes two to six `steps`, each with `label`, optional `detail`, and a `state`; use it for a pipeline, an architecture path, or a rollout sequence. `compare` takes `before` and `after`, each with `label` and `text`. `code` takes `text` of at most 18 lines for real output: a CLI run, an API response, a log line. Every type takes an optional `caption`.

A **decision** slide needs `id` (unique, lowercase), `timing` (`made` or `upcoming`), `question`, `context`, two to four `options` (each with `label` and `consequence`), `recommended` (the zero-based index of your pick), `recommendation` (why, in a sentence), `default` (what you do if the director never answers), and `reversibility` (`cheap`, `costly`, or `one-way`). A `made` decision also needs `current`, the index of the option in effect now; an `upcoming` one must not have it. Optional fields are `reversibility_note`, `needed_by`, and `evidence` (a list of `label` with optional `url`).

A **question** slide asks for something only the director knows, answered in words. It needs `id` (unique across decisions and questions), `question`, `context`, and `default` (what you will assume if there is no answer). It takes optional `suggestions` (up to four quick answers of 60 characters or less, shown as chips), `needed_by`, `evidence`, and a `visual` of any type shown beside the answer box. If you can write the options and a recommendation, make it a decision instead.

## Rules the renderer enforces

Unknown fields anywhere are an error. The deck holds 3 to 10 content slides. The first decision or question appears within the first three, and no more than two information slides run in a row. There are at most five decisions and at most three questions, with at least one of either. Every deck needs `usage`. With any status but `no-data` the deck needs at least one usage slide; with `no-data` it may not have one. With no goal, it needs a question slide asking for one. It warns when usage is tracked against a goal but no slide carries a `goal` visual. The estimated runtime must stay at or under 420 seconds; past 330 it warns. It warns, without failing, when there is no `made` decision, no `upcoming` decision, or no visual slide, because sometimes the evidence has none and inventing one is worse. It also warns when fewer than half the information slides carry a picture, when an information slide has no `why`, and when text the director reads holds insider shorthand: a commit hash, code in backticks, a file path, or a snake_case identifier. Links must be http(s). The archive must sit outside any Git repository.

## Archive layout

Each run writes `<archive>/<project_id>/<deck_id>/deck.html` and `deck.json`. `deck.json` is the validated input plus `deck_id`, `created_at`, total `seconds`, and the skill version. After the director answers, write their calls to `calls.md` in the same folder. The next check-in reads both to open with follow-through.
