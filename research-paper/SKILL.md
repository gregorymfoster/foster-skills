---
name: research-paper
description: Pipeline from a research question to a published post on the personal research site (github.com/gregorymfoster/research). Researches primary sources, writes a cited writeup, humanizes it, audits links, adds minimal editorial illustrations, and publishes to GitHub Pages. Use when asked to "research and publish" or "write a research post".
---

# Research paper

Run the steps in order; a step starts only after the previous one meets its
done criterion. The lead agent owns the pipeline and the published result; it
delegates the two phases marked below to subagents and inspects what they
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
- Label every finding as empirical, first-person testimony, or traditional
  wisdom. Trace famous statistics to their provenance and flag the shaky
  ones as shaky.
- The subagent stops when new sources repeat what it already holds, and
  reports back the file path, its strongest findings, and the claims it
  could not verify.
- Done when the lead has read the draft and spot-checked a sample of its
  citations against the linked sources.

## Step 2: Write

The draft is the research subagent's deliverable, so these requirements go
into its dispatch prompt alongside Step 1's sourcing rules.

- One Markdown file, roughly 3,000 to 6,000 words, structured for a reader:
  what the evidence says, named cases, principles each tied to its sources,
  a further-reading list, and a closing section listing claims you could
  not verify and how they are labeled in the text.
- Every substantive claim carries a markdown link to the source that owns it.
- Natural paragraphs with varied sentence length, sentence-case headings,
  punctuation from commas, periods, colons, and parentheses.
- Done when the draft answers the question and every claim is labeled
  (empirical / testimony / wisdom) and linked or flagged.

## Step 3: Humanize (audit subagent)

- The writer cannot see the slop it just wrote, so the audit runs in a
  fresh subagent: give it the draft path and the path to
  [references/humanize-checklist.md](references/humanize-checklist.md),
  which it reads in full (a paraphrased rubric loses the standards it
  encodes). Withhold the lead's own opinion of the prose.
- The lead applies the fixes the audit finds, then sends the result to a
  new delegate for re-audit; a resumed auditor carries its first pass into
  the second.
- Done when a fresh audit comes back clean.

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
- Minimal density, 3 to 5 images. Favor charts of the piece's own
  numerical results, plus at most one scene; every label carries the
  article's actual numbers or terms.
- Save the outline and one prompt file per image before generating, and
  commit them beside the images so any image can be regenerated later.
- Convert images to JPEG before committing; aim under 300 KB each.
- Done when every image serves with its labels spelled correctly. A flawed
  image is regenerated from an edited prompt file, never patched over.

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
