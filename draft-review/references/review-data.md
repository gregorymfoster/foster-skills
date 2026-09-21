# Review data

The renderer takes a UTF-8 draft and a JSON object. The draft is copied byte for byte; its exact text is displayed with original whitespace. Markdown syntax stays visible, like a plain-text manuscript. This avoids silently changing the author's text through formatting.

Required fields are shown below. Write actual editorial feedback rather than generic placeholders. IDs should describe the piece and stay stable across drafts. `previous_review_id` is optional. `assumptions` can be empty.

```json
{
  "title": "The essay's title",
  "essay_id": "stable-essay-slug",
  "draft_label": "Draft 1",
  "intent": "Audience, purpose, and stage, with assumptions identified.",
  "reader_response": "What you understood, felt, expected, or found unresolved on first reading.",
  "assumptions": [],
  "priorities": ["A concrete revision task with a reason."],
  "notes": [
    {
      "id": "n1",
      "category": "structure",
      "priority": "high",
      "tag": "ending",
      "quote": "An exact passage from the draft.",
      "occurrence": 1,
      "title": "Short editorial observation",
      "observation": "What happens at this passage, and its effect on the reader.",
      "suggestion": "A revision operation, diagnostic question, or optional idea to explore.",
      "alternative": ""
    }
  ]
}
```

Categories: `structure`, `ideas`, `clarity`, `voice`, `mechanics`, `strength`. Priorities: `high`, `medium`, `low`. Priority is revision impact, not a judgment of the author. Keep the overview to a manageable set of tasks, usually three; detailed notes remain available in the margin.

Use concise, stable kebab-case craft tags, for example `focus`, `opening`, `ending`, `sequence`, `pacing`, `stakes`, `specificity`, `evidence`, `counterargument`, `transition`, `repetition`, `sentence-load`, `diction`, `rhythm`, `punctuation`. Reuse the nearest established tag before inventing a synonym. Categories support navigation; tags support longitudinal analysis.

Anchor with `quote` and a one-based `occurrence`. Repeated quotes require an explicit occurrence; the renderer rejects ambiguous or missing anchors. Multiple notes can overlap the same text. An empty quote means whole-draft feedback. Keep quotes short enough to locate the issue, long enough to be unambiguous. Quotes and all commentary are rendered as escaped text, never executable HTML.

`alternative` is optional and is only for an isolated local wording suggestion, as permitted by the editorial contract. Most notes should leave it empty. Use `suggestion` for structural operations and idea prompts. There is deliberately no revised-draft field.

The archived JSON adds `schema_version`, `review_id`, local creation timestamp, source SHA-256, source filename, skill version, and resolved character ranges. Preserve the original inputs in the archive; this data makes later comparisons possible without scraping the HTML. Dates and hashes identify versions, not quality scores.
