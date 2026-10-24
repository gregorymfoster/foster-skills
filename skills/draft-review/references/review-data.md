# Review data

The renderer takes a UTF-8 draft and a JSON object. The draft is copied byte for byte; its exact text is displayed with original whitespace. Markdown syntax stays visible, like a plain-text manuscript. This avoids silently changing the author's text through formatting.

The default first pass has `stage: "structure"`. Write actual editorial feedback rather than generic placeholders. IDs should describe the piece and stay stable across drafts. `previous_review_id` is optional. `assumptions`, `through_lines`, `patterns`, and `notes` can be empty when the draft does not warrant them. A structure pass requires a reverse outline; the other two stage-specific sections should earn their space. The example shows the shape, not a target number of cards.

```json
{
  "title": "The essay's title",
  "essay_id": "stable-essay-slug",
  "draft_label": "Draft 1",
  "stage": "structure",
  "intent": "Audience, purpose, and stage, with assumptions identified.",
  "reader_response": "What you understood, felt, expected, or found unresolved on first reading.",
  "assumptions": [],
  "priorities": ["A concrete revision task with a reason."],
  "reverse_outline": [
    {
      "label": "Opening puzzle",
      "job": "What this contiguous block currently does for the reader.",
      "diagnosis": "What the block earns, repeats, delays, or leaves unresolved.",
      "quote": "An exact quote at the start of this block.",
      "occurrence": 1
    }
  ],
  "through_lines": [
    {
      "title": "A possible center of gravity",
      "question": "The inquiry this version would pursue.",
      "use": "Existing material this version would keep central.",
      "set_aside": "Material to shorten or save for another piece.",
      "needs": "A missing observation, counterexample, or structural move.",
      "recommended": true,
      "selected": false
    }
  ],
  "patterns": [
    {
      "title": "A tendency visible in this draft",
      "evidence": ["One exact excerpt", "Another exact excerpt"],
      "why": "What this pattern does to the reader and the craft principle behind it.",
      "practice": "A reusable revision exercise."
    }
  ],
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

`stage` is `structure` or `development`. Only an explicit user request advances to `development`; old archived reviews without a stage still render as development reviews. For a structure pass, `reverse_outline` contains the current draft's contiguous blocks in reading order. Each `quote` locates the start of a block; its displayed size runs until the next block. Start at the first substantive prose, cover the whole draft, and avoid splitting every paragraph into a card unless that helps reveal its job. `job` describes the current function, while `diagnosis` explains the reader effect. The HTML gives each block a proportional bar and a jump to the draft. Repeated or ambiguous quotes need a one-based `occurrence`; out-of-order block starts are rejected.

`through_lines` names genuinely distinct ways the existing material could become a focused essay. Recommend at most one and explain its tradeoff through `use`, `set_aside`, and `needs`. Mark `selected: true` only after the author chooses that direction; the page labels it “Your choice.” Describe structural directions, not replacement paragraphs, invented scenes, or ready-made conclusions. `patterns` are observations supported by two distinct exact excerpts from the draft, an explanation of their effect on the reader, and a practice the writer can reuse. In a single-draft review, label them as patterns **in this draft** rather than trends across the writer's work. Both sections are optional; omit empty speculation.

Categories: `structure`, `ideas`, `clarity`, `voice`, `mechanics`, `strength`. Priorities: `high`, `medium`, `low`. Priority is revision impact, not a judgment of the author. Keep the overview to a manageable set of tasks, usually three. In the structure stage, notes should illuminate architectural choices not already clear in the reverse outline; detailed notes wait for an explicitly requested development pass.

Use concise, stable kebab-case craft tags, for example `focus`, `opening`, `ending`, `sequence`, `pacing`, `stakes`, `specificity`, `evidence`, `counterargument`, `transition`, `repetition`, `sentence-load`, `diction`, `rhythm`, `punctuation`. Reuse the nearest established tag before inventing a synonym. Categories support navigation; tags support longitudinal analysis.

Anchor with `quote` and a one-based `occurrence`. Repeated quotes require an explicit occurrence; the renderer rejects ambiguous or missing anchors. Multiple notes can overlap the same text. An empty quote means whole-draft feedback. Keep quotes short enough to locate the issue, long enough to be unambiguous. Quotes and all commentary are rendered as escaped text, never executable HTML.

`alternative` exists for backward compatibility and an explicitly requested local wording example. Leave it empty in structure passes. Use `suggestion` for structural operations and idea prompts. There is deliberately no revised-draft field.

The archived JSON adds `schema_version`, `review_id`, local creation timestamp, source SHA-256, source filename, skill version, and resolved character ranges. Preserve the original inputs in the archive; this data makes later comparisons possible without scraping the HTML. Dates and hashes identify versions, not quality scores.
