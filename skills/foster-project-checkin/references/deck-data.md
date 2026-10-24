# Deck data

The renderer takes one JSON object and produces a single offline HTML deck. It adds a cover slide built from the top-level fields and a closing "Your calls" slide built from the decisions, so `slides` holds only the middle of the talk. All text renders as escaped plain text. There is no Markdown and no HTML.

```json
{
  "project": "Search service",
  "project_id": "search-service",
  "window": "Since Oct 17 (last check-in)",
  "headline": "Staff can search the whole catalog now, but ranking is still naive and two clients are hitting the old endpoint.",
  "metrics": [
    {"value": "14", "label": "PRs merged"},
    {"value": "180 ms", "label": "p95 query time"}
  ],
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
      "say": "One to three sentences, the way you would say it out loud.",
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
      "kind": "visual",
      "title": "What a staff search looks like today",
      "lede": "Results are correct but sorted by date, not relevance.",
      "visual": {"type": "image", "src": "screens/results.png", "alt": "Search results page showing 20 results sorted by date", "caption": "Captured from the staging build."}
    }
  ],
  "next": ["Typo tolerance behind a flag", "Move the two old clients"]
}
```

## Top level

`project` is the display name. `project_id` is a stable kebab-case slug; the archive groups decks by it, and `--latest <project_id>` finds the previous check-in. `window` names the period covered in words. `headline` is the net effect in one sentence of 180 characters or fewer, and it sits alone on the cover. `metrics` is optional, at most four, and every number in it must come from a source you checked. `gaps` lists sources you could not read so the director knows what the briefing is blind to. `next` is required: what you keep working on while the calls are open.

## Slides

There are three kinds. Every slide takes an optional `say` (the voiceover line, shown under the slide and toggled with V) and an optional `seconds` (defaults: status 35, visual 35, decision 50). The cover adds 20 seconds and the close adds 25.

A **status** slide needs `title` and `lede`, and takes up to five `points`. A point has `text`, an optional `url`, and a `state` of `done`, `moving`, `blocked`, `dropped`, or `risk`. Write the title as a claim ("Search is live for internal users"), not a topic ("Search update"). The lede is the so-what.

A **visual** slide needs `title`, `lede`, and a `visual` of one of four types. `image` takes `src` and `alt`; a local path (relative to the deck JSON) is inlined as base64 so the deck stays one file, and `https://` and `data:image/` sources pass through. SVG diagrams go here too, as image files, so nothing in them can run. `flow` takes two to six `steps`, each with `label`, optional `detail`, and a `state`; use it for a pipeline, an architecture path, or a rollout sequence. `compare` takes `before` and `after`, each with `label` and `text`. `code` takes `text` of at most 18 lines for real output: a CLI run, an API response, a log line. Every type takes an optional `caption`.

A **decision** slide needs `id` (unique, lowercase), `timing` (`made` or `upcoming`), `question`, `context`, two to four `options` (each with `label` and `consequence`), `recommended` (the zero-based index of your pick), `recommendation` (why, in a sentence), `default` (what you do if the director never answers), and `reversibility` (`cheap`, `costly`, or `one-way`). A `made` decision also needs `current`, the index of the option in effect now; an `upcoming` one must not have it. Optional fields are `reversibility_note`, `needed_by`, and `evidence` (a list of `label` with optional `url`).

## Rules the renderer enforces

The deck holds 3 to 10 content slides. The first decision appears within the first three, and no more than two information slides run in a row. There are one to five decisions in total. The estimated runtime must stay at or under 420 seconds; past 330 it warns. It warns, without failing, when there is no `made` decision, no `upcoming` decision, or no visual slide, because sometimes the evidence has none and inventing one is worse. Links must be http(s). The archive must sit outside any Git repository.

## Archive layout

Each run writes `<archive>/<project_id>/<deck_id>/deck.html` and `deck.json`. `deck.json` is the validated input plus `deck_id`, `created_at`, total `seconds`, and the skill version. After the director answers, write their calls to `calls.md` in the same folder. The next check-in reads both to open with follow-through.
