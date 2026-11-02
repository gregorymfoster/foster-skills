---
name: foster-assess-business
description: Run a battery of validation assessments on a startup or business idea. Scores it against shape filters (free-first, the internal-tool test, crowded-but-mediocre, big-money market, founder fit, why-now, constraints) and the testing frameworks (assumption mapping, lean experiments, customer research, lean startup, Mom Test). Produces a verdict table with pass or fail per filter, pros and cons, an evidence score out of 10, and the cheapest next test. Founder profiles and the filter set are configurable. Use when asked to "assess", "judge", "score", "vet", "validate", "pressure-test", or give a "verdict on" a business idea, or to rank several ideas.
---

# Assess a business idea

The goal is an honest verdict on an idea in a fixed shape: a table that says pass or fail on each filter and each testing framework, a paragraph of pros, a paragraph of cons, and a number that says how much real evidence exists. Ideas that pass every filter on paper and have zero customer evidence are common. Say so plainly; that gap is usually the most useful thing in the report.

You are an advisor, not a cheerleader. Most ideas should fail at least one filter. A "pass" needs a named reason: a company, a number, a source, a person. "Likely pass" and "partial pass" are fine verdicts when the evidence is thin, as long as the why says what is missing.

## 1. Load the founders, the filters, and the idea

Founder fit and constraints depend on who is building it, so read the founder profile before judging anything. Look, in this order, for:

1. A founders file named in the request.
2. `founders.md` in the current project or workspace (`.agents/founders.md`, `.claude/founders.md`, or the project's shared files folder).
3. Project memory or notes that describe the founders, their strengths, their preferences, and any legal or employer constraints.

[references/founders.md](references/founders.md) has the format. If no profile exists, ask once for each founder's strengths, constraints and preferences, and meanwhile judge with what you have, marking founder fit and constraints as provisional. Never invent anyone's background.

The profile can also change the filter set: drop a filter the team doesn't care about (a team happy to sell enterprise contracts from day one can drop free-first), add one of their own, or name markets to avoid. Use the default seven filters below unless the profile says otherwise.

Then pin down the idea in two sentences: who it is for, what it does, and how it makes money. If several variants are floating around, pick the one most likely meant and name the others in a line. For a batch of ideas, run the steps on each and finish with a ranking (step 6).

## 2. Gather evidence before scoring

Spend real effort here. A verdict with no citations is an opinion, and opinions score 1 on the validation ladder.

- **Market and competitors.** Who sells this today, how big they are, what they charge, who funded them. Look for revenue or ARR figures, funding rounds, and acquisitions. Note both polished leaders and the long tail of weak tools.
- **Internal versions.** Search for big companies that built this for themselves: engineering blogs, conference talks, open-sourced internal tools, press about in-house platforms. This feeds the internal-tool test.
- **Why now.** What changed in the last 12 to 24 months that makes this possible or necessary: a platform shift, a pricing or API-terms change, a regulation, a cost curve.
- **Customer signal already in hand.** Interviews, sign-ups, usage, pre-orders, letters of intent. Check the project's notes and memory. If none exists, the evidence score will be low, and that's the right answer.

Prefer primary sources and link each claim you rely on. Mark anything from memory rather than a fetched source as "from memory, not re-checked".

## 3. Run the shape filters

Judge each filter with a verdict (Pass, Likely pass, Mostly pass, Partial pass, Fail, or Unknown) and a one-to-three-sentence why. [references/filters.md](references/filters.md) has the full rubric for each; read it before scoring. In short:

1. **Free-first.** Can it be given away to earn trust and usage, with users paying in time, feedback and usage before money? Score the five sub-tests: adopt without a purchase decision, near-zero cost to serve free users, free usage compounds, a natural paid layer bought by someone else (the team or firm), and the free version beats the free options already out there.
2. **The internal-tool test.** Does a version already exist as an internal hack inside a top company that nobody has made generic and easy to adopt? Many durable tools started as one company's in-house system, repackaged for everyone else.
3. **Crowded but mediocre.** A crowded field of weak, unbacked, unpolished tools counts as open. A field with a polished, well-funded leader counts as closed.
4. **Big-money market.** Is there evidence buyers already spend real money on this layer, in a market where large, lucrative businesses get built? Low-budget markets fail unless the idea sells to a different buyer.
5. **Founder fit.** Does each founder have a real, ownable role that uses their strengths, per the founder profile? Check every founder, not just the lead.
6. **Why now.** A concrete change that opens the window today and wasn't true three years ago.
7. **Constraints.** Non-competes, employer outside-activity rules, conflicts of interest, or no-go areas listed in the founder profile. Skip the row if the profile lists none. Keep the specifics of anyone's legal agreements out of anything that will be shared beyond the founders.

## 4. Run the testing frameworks

These measure how much is known, not how good the idea sounds. Use the matching skills when they're installed (`identify-assumptions-new`, `brainstorm-experiments-new`, `customer-research`, `lean-startup`, `mom-test`); [references/evidence.md](references/evidence.md) summarizes each one well enough to run without them.

- **Assumption mapping** (identify-assumptions-new). Name the riskiest assumptions across value, usability, viability, feasibility, ethics, go-to-market, strategy and team. Give each a confidence (low, medium, high) and say whether it has been tested.
- **Lean experiment** (brainstorm-experiments-new). Write one XYZ hypothesis ("At least X% of Y will do Z") and the cheapest pretotype that tests it, with a metric and a success threshold. Favor tests where people put skin in the game: an install, a deposit, an intro to the person who signs.
- **Customer research** (customer-research). Say where unprompted customer signal lives (forums, reviews, support threads, job posts) and what it shows so far, or that nobody has looked yet.
- **Lean startup** (lean-startup). Score the plan out of 10 on the five diagnostic rows, and define the MVP plus a persevere or pivot rule set before building.
- **Mom Test** (mom-test). Write three to five past-tense questions about the customer's life, never the idea, and the commitment to ask for at the end. The verdict is "Ready to run", "Run, n conversations", or a score out of 7 if conversations already happened.

## 5. Score the evidence

Give one **evidence score out of 10**, defined in [references/evidence.md](references/evidence.md). It is the lean-startup diagnostic score, where a row earns its second point only with evidence at level 3 or higher on the validation ladder (sign-ups, deposits, active use). Also state the highest ladder level reached so far. An idea with every assumption named and a planned MVP but nothing run scores about 4. Don't round up for enthusiasm.

## 6. Write the verdict

Use this shape, which matches the worked example in [references/example-verdict.md](references/example-verdict.md):

1. **Heading**: "<Idea name>: verdict".
2. **Summary**: two to four sentences. What the idea is, how it does on the filters, how it does on evidence, and its single biggest risk.
3. **Verdict table** with three columns, Framework, Verdict, Why. Rows: the shape filters (one founder-fit row per founder), then Assumption mapping, Lean startup (with the score), Mom Test, plus Lean experiment and Customer research when they add something. Each "why" is specific: names, numbers, the source.
4. **Pros.** One paragraph, opening with the bolded word "Pros." The forces it rides, why it would be sticky, why these founders.
5. **Cons.** One paragraph, opening with "Cons." Who can kill it, who is converging on it, what makes it hard to adopt or sell, what could go badly wrong.
6. **Evidence score** line: "Evidence: n/10 (highest rung: level k, <what that was>)." Then the single cheapest next test, with its success threshold and a date or week to check it.

For several ideas, add a ranking table at the end: idea, filters passed out of the total, evidence score, and the one-line reason for its position. Rank on filters first and use evidence to break ties, unless one idea has real customer evidence, which outranks paper passes.

Write in plain prose with varied sentence length. No em-dashes, no hype words, and no "it's not X, it's Y" framing. Keep the table cells short enough to read on a phone.

## 7. Deliver

Put the verdict in a shareable document if the environment has one (a doc, a page, or a section of an existing ideas doc) and link it rather than pasting a long table into chat. Otherwise write it to a Markdown file and give the path. If the environment has persistent memory, save the outcome (idea, verdict, evidence score, next test) so the next assessment can compare against it.

If the founder profile was missing details you had to guess, list them at the end as questions, each with your best guess, so the next run is sharper.
