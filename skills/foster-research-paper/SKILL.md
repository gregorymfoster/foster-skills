---
name: foster-research-paper
description: Pipeline from a research question to a published post on the personal research site (github.com/gregorymfoster/research). Researches primary sources, writes a cited writeup, humanizes it, audits links, adds minimal editorial illustrations, and publishes to GitHub Pages. Use when asked to "research and publish" or "write a research post".
---

# Research paper

Run the steps in order; a step starts only after the previous one meets its
done criterion. The lead agent owns the argument, prose, and published result.
It delegates the two phases marked below to subagents and inspects what they
return rather than trusting their confidence.

## Step 1: Research (subagent)

- Fix the bounded question in one sentence, then dispatch one background
  research subagent so the 25-to-50-fetch investigation floods its context,
  not the lead's. Its prompt carries: the question, the deliverable file
  path, the effort budget, and the sourcing and labeling rules below.
- Primary sources only: the original paper, the author's own essay or
  interview, the official text. When a secondary write-up cites something,
  fetch the original before using it; the secondary's paraphrase is never
  the claim.
- In the research dossier, label every finding as empirical, first-person
  testimony, traditional wisdom, or the researcher's inference. Trace famous
  statistics to their provenance and flag the shaky ones as shaky. These are
  dossier fields, not paragraph prefixes for the published essay.
- The subagent stops when new sources repeat what it already holds, and
  reports back the dossier path, its strongest findings, and the claims it
  could not verify. The dossier groups evidence by question and records exact
  source ownership; it does not attempt the final article's voice or shape.
- Done when the lead has read the dossier and spot-checked a sample of its
  citations against the linked sources.

## Step 2: Calibrate and write (lead)

- Before drafting, read [references/editorial-style.md](references/editorial-style.md)
  in full and complete its house-voice calibration against the existing site.
  The closest canonical post is the prose authority; the dossier supplies
  facts, not structure.
- Write from a blank-page outline built around the reader's question and the
  strongest answer. Establish the stakes or central tension in the first two
  paragraphs. Put the material that motivated the request near the front,
  then earn qualifications through the argument rather than leading with a
  wall of caveats.
- Integrate evidence classes locally: name the source, add a short
  parenthetical such as `(empirical)`, or state the researcher's uncertainty
  in first person. Epistemic labels must not become repeated paragraph
  prefixes. Link the sentence that owns a claim instead of appending a bundle
  of sources after a source-summary paragraph.
- Use first person for research judgment when it clarifies who is making an
  inference: "I found," "my interpretation," and "I would define" are natural
  in this publication. Uneven emphasis, specific cases, useful quotations,
  and mixed verdicts are part of the house voice.

- One Markdown file, roughly 3,000 to 6,000 words, structured for a reader:
  what the evidence says, named cases, principles each tied to its sources,
  a further-reading list, and a closing section listing claims you could
  not verify and how they are labeled in the text.
- Every substantive claim carries a markdown link to the source that owns it.
- Natural paragraphs with varied sentence length, sentence-case headings,
  punctuation from commas, periods, colons, and parentheses.
- Done when the draft answers the question, sounds continuous with the
  canonical posts, and every claim's evidence class is clear from nearby prose
  while its source is linked or the claim is flagged.

## Step 3: Humanize (audit subagent)

- The writer cannot see the slop it just wrote, so the audit runs in a
  fresh subagent: give it the draft path and the path to
  [references/humanize-checklist.md](references/humanize-checklist.md),
  which it reads in full (a paraphrased rubric loses the standards it
  encodes). Also give it the closest canonical post selected during Step 2.
  Withhold the lead's own opinion of the prose.
- The lead applies the fixes the audit finds, then sends the result to a
  new delegate for re-audit; a resumed auditor carries its first pass into
  the second.
- "Clean" means both surfaces and voice: no generic AI patterns, no visible
  evidence scaffolding, no source-dump cadence, and no sectioning that reads
  like a reference manual. The opening must give a non-specialist a reason to
  continue, and the prose must plausibly belong beside the canonical post.
- Done when a fresh audit comes back clean on those criteria and the lead has
  read the full draft aloud or linearly rather than relying on grep checks.

## Step 4: Link audit

- Sweep the draft for substantive claims that still lack links, find their
  primary sources, and verify each URL resolves before adding it (a 403
  from a bot-blocking publisher counts as live when a search result
  confirms the page's content).
- A citation must contain the claim it backs. When no verifiable source
  exists, label the claim unverified in the text; that beats decorating it
  with a link that does not hold it.
- Done when every substantive claim links to a verified primary source or
  is explicitly labeled unverified.

## Step 5: Illustrate

- Run the `baoyu-article-illustrator` skill
  (`~/.cursor/skills/baoyu-article-illustrator/`) in the lead: it is a
  generate-inspect-regenerate loop, and that skill's own policy reserves
  subagents for creative exploration, never for parallelizing renders.
  House defaults live in
  `~/.baoyu-skills/baoyu-article-illustrator/EXTEND.md`; state the settings
  you are using up front instead of blocking on its interactive
  confirmation.
- Before choosing a style or writing prompts, read
  [references/illustration-style.md](references/illustration-style.md) in
  full. Its research-site house style overrides generic illustrator presets,
  saved preferences such as `scientific`, and the image model's default idea
  of a technical infographic.
- Inspect the canonical images and prompt files named in that reference, then
  pass the relevant canonical JPEGs as style references to every render. Keep
  information density in exact labels, spacing, and relationships rather than
  color-coded cards or stock icons.
- Plan the figures as a visual sequence, not as repeated variants of one
  infographic. Use at least two visual grammars when the subject permits:
  precise charts for the article's own numerical results, and one scene or
  conceptual illustration that makes the stakes tangible. A house style is
  not a license to turn every figure into a handwritten worksheet.
- Default to 3 to 5 images, or 4 to 6 when the user explicitly asks for many.
  Every label carries the article's actual numbers or terms. Beauty, visual
  hierarchy, and reader interest are part of the inspection gate alongside
  factual accuracy and information density.
- Save the outline and one prompt file per image before generating, and
  commit them beside the images so any image can be regenerated later.
- Convert images to JPEG before committing; aim under 300 KB each.
- Done when every image serves with its labels spelled correctly and a
  side-by-side inspection against at least three canonical site images passes
  every check in the house-style reference. Regenerate a failed image from an
  edited prompt file; never patch over it.

## Step 6: Publish

- Repo: `~/code/research` (github.com/gregorymfoster/research). Post format:
  the repo README. Images go in `assets/illustrations/{slug}/` and are
  referenced by absolute URL
  (`https://research.gmfoster.com/assets/...`) so the markdown
  renders anywhere it is copied.
- Open the post with a short italic provenance note: which model and agent
  wrote it, the date, and the human's role.
- Commit and push `main`; Pages rebuilds on push.
- Done when the live post URL returns 200, the new content is visible in
  the served HTML, and every image URL returns 200. A first build on a new
  site can wedge in "building"; re-trigger with
  `gh api -X POST repos/gregorymfoster/research/pages/builds`.
