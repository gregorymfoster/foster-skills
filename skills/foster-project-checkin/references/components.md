# Components

Every check-in deck is built from the same small set of components, so a deck made by Claude Code, Codex, Cursor or anything else looks like every other deck. The pattern comes from Matt Pocock's teach skill: lessons there reuse one shared stylesheet and a growing library of components instead of each lesson inventing its own look. Here the library lives in this skill folder:

- `assets/components/deck.css` is the only stylesheet. Light and dark mode, phone layout and print all live in it.
- `assets/components/deck.js` is the only script: slide navigation, option picking, the before/after slider, notes, and "Copy my calls".
- `assets/deck.html` is the page skeleton. The renderer inlines the two files above, so every deck is one offline HTML file.
- `assets/starter.html` is a finished deck with every component, for building by hand (see the last section).
- `assets/sample/deck.json` is the made-up project the starter is generated from.

Agents never write HTML, CSS or inline styles for a deck. You pick components and fill them with words, numbers and pictures through the deck JSON. The renderer refuses any field it doesn't know, so a style hint or a made-up layout fails loudly instead of quietly producing a different-looking deck.

## Pick a component by its job

| The slide needs to show | Use | Notes |
|---|---|---|
| A change in what a user sees | `slider` (drag to compare) or `gallery` (side by side) | Two screenshots of the same view at the same size. The strongest slide for UI work. |
| The thing working | `image` | A real screenshot, terminal capture or SVG diagram. |
| One or two numbers that matter | `stats` | A big number, a plain label, and how it changed. |
| A trend over time | `line` | One to three series over 2 to 12 points. |
| A comparison between a few things | `bars` | Old way, new way, best possible. Highlight the one you want read. |
| How the parts connect, or a rollout order | `flow` | Two to six steps, each with a state. |
| A rule or behavior that changed, in words | `compare` | Short before and after text. |
| Real output | `code` | At most 18 lines. |
| A choice with known options | decision slide | Options, a recommendation, a default. |
| Something only the director knows | question slide | Free text with up to four quick answers. |

If nothing fits, use the closest component and say what was missing in `gaps`. A new component goes into this skill (renderer, stylesheet, this file and a test), never into one deck.

## Slides

**status**: eyebrow "Where things stand", a claim as the title, the lede, up to five points with a state chip (`done`, `moving`, `blocked`, `dropped`, `risk`), and an optional visual beside the points.

**visual**: eyebrow "What it looks like", the title, the lede, and one full-width visual.

**decision**: eyebrow "Call N", an amber left edge, two to four option cards (A, B, C, D) tagged "My rec" and "In effect now", then the recommendation, the default, how reversible it is, and a note field.

**question**: eyebrow "Question N · Only you know this", a blue left edge, the context, optional quick-answer chips, a free-text answer, and what you will assume if he doesn't answer. With a visual, the picture sits on the left and the answer on the right. Use a question when you can't honestly write the options, for example "Which customers matter most for this?" or "Does this match what you saw in the store?". When you can write the options, make it a decision.

Both kinds of ask show on the progress track (amber for calls, blue for questions) and in the closing recap, and both go into the "Copy my calls" text.

## Visuals

Every visual takes an optional `caption`.

**image**: `src`, `alt`. Local files are inlined as base64. `https://` and `data:image/` sources pass through.

**gallery**: `images`, two or three, each with `src`, `alt` and a short `label`.

**slider**: `before` and `after`, each with `src`, `alt` and `label`. Both images should be the same size and framing (same viewport, same scroll position) so the drag lines up. The after image sets the size.

**stats**: `stats`, one to four, each with `value` (a short string such as "6 s" or "87%"), `label`, optional `change` ("up from 41%") and optional `tone` (`good`, `bad`, `neutral`). Tone adds an arrow as well as a color, so it never relies on color alone.

**line**: `question` (the chart title, as a plain question), optional `unit`, `x` (2 to 12 labels), and `series`, one to three, each with `label` and `values` (one number per x label, or null for a gap). The chart starts at zero unless values go negative, labels each line at its end, puts a tooltip on every point, and carries a hidden data table for screen readers.

**bars**: `question`, optional `unit`, two to six `bars`, each with `label`, `value` and optional `highlight`.

**flow**: two to six `steps`, each with `label`, optional `detail` and `state`.

**compare**: `before` and `after`, each with `label` and `text`.

**code**: `text`, at most 18 lines.

## The palette

Colors are tokens on `:root` in the stylesheet, redefined for dark mode. Accent green marks progress and recommendations, amber marks calls, blue marks questions, and the state colors mark point and step states. Chart lines use three validated categorical slots (blue, orange, aqua) in fixed order: the first series is always blue. Don't ask for other colors. If a chart needs more than three series, it needs to be two charts.

## Two ways to build, one look

**With the renderer** (any agent that can run Python 3): write the deck JSON and run `scripts/render_deck.py`. It validates everything and inlines the images. Prefer this whenever it can run.

**By hand** (no Python, or a chat with no tools): copy `assets/starter.html` and edit it. It is the sample deck as the renderer produces it, with the stylesheet and script already inlined and a `COMPONENT` comment above every slide. The visuals the sample doesn't use (gallery, image, flow, compare, code) sit in a `<template>` at the end of the slides, ready to copy out. A note at the top of the file lists what to change. Keep the style and script blocks untouched and change only words, numbers and images. The page script reads each call from the slide's own markup and draws line charts from their `data-chart` JSON, so nothing needs computing except bar widths.

The renderer regenerates the starter with `python3 scripts/render_deck.py --starter`, and a test fails if the two drift apart, so a hand-built deck looks exactly like a rendered one. Say in `gaps` when a deck was built by hand, since nothing validated it.

`assets/sample/deck.json` uses most components on a made-up project. Render it, or open `assets/starter.html`, to see the look.
