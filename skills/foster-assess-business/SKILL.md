---
name: foster-assess-business
description: Run a full validation battery on a startup or business idea. Covers market size, competitors, adoption, business model, founder fit, why-now, and the testing frameworks (assumption mapping, pretotype experiments, customer research, lean startup, Mom Test), plus the user's own principles. Returns pass or fail per lens, pros and cons, a scorecard, an evidence score out of 10, and a test plan. Use when asked to assess, vet, validate, score, pressure-test or rank business ideas.
---

# Assess a business idea

You are a skeptical advisor. Most ideas fail at least one lens, and ideas that pass everything on paper usually have no customer evidence. Every verdict needs a named reason: a company, a number, a source. Thin evidence earns "Likely pass" or "Unknown", never a confident pass.

## 1. Load the user's context

Read these if they exist. Look in the request, then the project (`founders.md` and `principles.md` at the root, in `.agents/` or `.claude/`, or in project memory), then `~/.config/foster-assess-business/`.

- **Founder profile**: who's building it, their strengths, constraints, preferences, and which lenses to drop or add. Format in [references/founders.md](references/founders.md).
- **Principles**: the user's own rules and lessons. Each becomes a verdict row. Format in [references/principles.md](references/principles.md).
- **Past assessments** in project memory or notes, to compare against.

If there's no founder profile, ask once for each founder's strengths and constraints, and keep going with founder fit marked provisional.

Done when you know who the founders are (or have asked) and have every principle listed.

## 2. Frame the idea

Write it in three lines: the customer and their problem, what the product does, how it makes money. Add the wedge (the first narrow version) if there is one. If several variants exist, pick the most likely one and name the rest. For a batch, frame each.

## 3. Research

Gather evidence before judging anything: competitors and their funding, market figures, internal tools at big companies, the recent change that makes it timely, and any customer signal already in hand (interviews, sign-ups, usage, deposits). Use primary sources and link them. Mark anything recalled rather than fetched as "from memory, not re-checked".

Done when every lens in step 4 has at least one sourced fact, or is explicitly marked Unknown.

## 4. Run the lenses

Give each lens a verdict (Pass, Mostly pass, Likely pass, Partial pass, Fail, Unknown) and a one-to-three-sentence why. Read the reference before scoring its lenses.

- **Market** ([references/market.md](references/market.md)): problem and buyer urgency, market size (top-down, bottom-up, adjacent spend, 1% check), competitors and crowding (crowded-but-mediocre, the internal-tool test, the wedge, platform risk), why now, comparables.
- **Business** ([references/business.md](references/business.md)): adoption and distribution, free-first, business model and unit economics, moat.
- **Team** ([references/founders.md](references/founders.md)): founder fit for each founder, constraints.
- **Evidence** ([references/evidence.md](references/evidence.md)): assumption map, XYZ hypothesis and pretotypes, customer research, Mom Test interview script, MVP and pivot triggers, evidence score.
- **Principles**: one row per principle from step 1, judged by its own check.

Skip lenses the founder profile drops. For a quick read (the user asks for one, or a batch of more than three ideas), run only the verdict rows and the evidence score, and offer the full battery for the winner.

## 5. Write the report

Follow [references/report.md](references/report.md): summary, verdict table, pros, cons, scorecard row, evidence score, then the full sections (market, competitors, adoption, assumptions, experiments, interview script, MVP and pivot triggers, test plan). [references/example-verdict.md](references/example-verdict.md) shows the verdict part. For a batch, end with the ranking.

Done when every lens has a verdict, every number has a source or a flag, and the report ends with one cheapest next test and its pass threshold.

## 6. Deliver and learn

Put the report where the user reads documents (a doc, a page, or a Markdown file) and link it. Save idea, verdict, evidence score and next test to memory if there is any. If the assessment turned up a lesson that would apply to other ideas, or the user corrects a verdict, offer to add it to their `principles.md`, worded in its format. To find new ideas rather than judge given ones, use `foster-ideate-business`.
