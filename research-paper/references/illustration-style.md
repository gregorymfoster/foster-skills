# Research-site illustration style

The canonical research-site images use an editorial thin-line system:

- warm off-white paper;
- fine charcoal ink with slight hand-drawn variation;
- small clean hand lettering;
- one muted ochre accent;
- flat geometry and generous whitespace;
- information carried by scale, spacing, hatching, and relationships.

Avoid generic technical-infographic styling: saturated semantic palettes,
cards, badges, title banners, stock icons, gradients, shadows, glossy objects,
and presentation-slide chrome.

## Canonical references

Inspect at least three before generating. Pass the most relevant JPEGs as
style references to the image model and state that their content must be
ignored.

- `~/code/research/assets/illustrations/bigger-problems/03-infographic-2026-numbers.jpg`
- `~/code/research/assets/illustrations/second-mountain/04-infographic-timescales.jpg`
- `~/code/research/assets/illustrations/sudden-wealth/02-comparison-folklore-vs-record.jpg`
- `~/code/research/assets/illustrations/sudden-wealth/03-framework-pause-enough-mission.jpg`

Read the prompt beside each chosen reference. Reuse its visual grammar: open
rules instead of cards, hatching instead of extra colors, labels adjacent to
marks, and empty paper instead of decorative fill.

## Inspection gate

Compare every render beside the canonical images and reject it if:

- it could pass as a corporate presentation slide;
- more than charcoal and muted ochre carry meaning;
- boxes, icons, banners, or backgrounds compete with the data;
- text is decorative, misspelled, tiny, or detached from its mark;
- whitespace and line work no longer provide the hierarchy;
- its density comes from visual containers instead of exact relationships.

Correct a failed render by editing its saved prompt and generating a new
candidate. Keep the article's exact facts and labels while changing the visual
grammar.
