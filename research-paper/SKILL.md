---
name: research-paper
description: Pipeline from a research question to a published post on the personal research site (github.com/gregorymfoster/research). Researches primary sources, writes a cited writeup, humanizes it, audits links, adds minimal editorial illustrations, and publishes to GitHub Pages. Use when asked to "research and publish" or "write a research post".
---

# Research paper

Run the steps in order; a step starts only after the previous one meets its
done criterion.

## Step 1: Research

- Fix the bounded question in one sentence before searching.
- Search and fetch primary sources: the original paper, the author's own
  essay or interview, the official text. When a secondary write-up cites
  something, fetch the original before using it; the secondary's paraphrase
  is never the claim.
- Label every finding as empirical, first-person testimony, or traditional
  wisdom. Trace famous statistics to their provenance and flag the shaky
  ones as shaky.
- Done when new sources repeat what you already hold. Expect on the order
  of 25 to 50 fetches for a full post.

## Step 2: Write

- One Markdown file, roughly 3,000 to 6,000 words, structured for a reader:
  what the evidence says, named cases, principles each tied to its sources,
  a further-reading list, and a closing section listing claims you could
  not verify and how they are labeled in the text.
- Every substantive claim carries a markdown link to the source that owns it.
- Natural paragraphs with varied sentence length, sentence-case headings,
  punctuation from commas, periods, colons, and parentheses.
- Done when the draft answers the question and every claim is labeled
  (empirical / testimony / wisdom) and linked or flagged.

## Step 3: Humanize

- Run the full pass in [references/humanize-checklist.md](references/humanize-checklist.md):
  edit, then audit, then fix what the audit finds.
- Done when the checklist's scans come back clean.

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
  (`~/.cursor/skills/baoyu-article-illustrator/`). House defaults live in
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
  (`https://gregorymfoster.github.io/research/assets/...`) so the markdown
  renders anywhere it is copied.
- Open the post with a short italic provenance note: which model and agent
  wrote it, the date, and the human's role.
- Commit and push `main`; Pages rebuilds on push.
- Done when the live post URL returns 200, the new content is visible in
  the served HTML, and every image URL returns 200. A first build on a new
  site can wedge in "building"; re-trigger with
  `gh api -X POST repos/gregorymfoster/research/pages/builds`.
