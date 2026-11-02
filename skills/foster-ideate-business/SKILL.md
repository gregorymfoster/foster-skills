---
name: foster-ideate-business
description: Generate new startup or business ideas that fit a specific founding team. Mines the team's unfair advantages and runs idea lenses (internal tools nobody has made generic, crowded fields of mediocre tools, free-first products that grow a paid tier, regional versions, why-now shifts, services that should be software), screens the raw list, and hands the best ideas to foster-assess-business. Reads the same private founders.md and principles.md. Use when asked to brainstorm, generate, find or suggest business ideas.
---

# Generate business ideas

You are a well-read scout working for one specific team. Volume first, judgment second: write many concrete ideas, then kill most of them with a named reason. A good idea names a buyer, a painful job and a company or tool that proves the need. "AI for X" is not an idea.

## 1. Load the user's context

Read the same private files `foster-assess-business` reads, from the same places: the request, then the project (`founders.md` and `principles.md` at the root, in `.agents/` or `.claude/`, or in project memory), then `~/.config/foster-assess-business/`. Also read any past idea lists or assessments, so you don't repeat ideas already tried or dropped. Formats are in that skill's `references/founders.md` and `references/principles.md`.

If there's no founder profile, ask once for each founder's strengths, networks and constraints, and keep going with fit marked provisional.

Done when you can list each founder's edges and constraints, every principle, and every idea already on the table.

## 2. Find the seeds

Turn the context into seeds, the raw material the lenses work on. Follow [references/seeds.md](references/seeds.md): each founder's unfair advantages, the problems they've seen up close, the user's principles and filters, and the brief (markets to aim at or avoid, time commitment, funding preference).

Done when you have five to ten seeds, each one line, and a written list of no-go areas.

## 3. Generate

Run every lens in [references/lenses.md](references/lenses.md) against the seeds. Aim for 20 to 40 raw ideas, one line each in the form "for <buyer>, <what it does>, because <proof of need>". Search the web as you go: engineering blogs, open-sourced internal tools, review sites, forums and job posts are where ideas hide. Don't judge yet, but drop anything in a no-go area or inside a founder's constraint.

Done when each lens has produced at least two ideas or a note saying why it produced none, and every idea names a buyer.

## 4. Screen

Apply the quick screen in [references/screen.md](references/screen.md) to every raw idea: keep or kill, with a one-line reason. Merge near-duplicates. Keep five to eight.

Done when every raw idea has a keep or kill and a reason, and the shortlist is at most eight.

## 5. Shape the shortlist

For each kept idea, write the three-line frame `foster-assess-business` expects (the customer and their problem, what the product does, how it makes money), the wedge, the lens that produced it, the strongest proof with a link, and the biggest open question. Mark anything recalled rather than fetched as "from memory, not re-checked".

Done when every shortlisted idea has a frame, a wedge and at least one sourced fact.

## 6. Rank and hand off

Write the slate as described in [references/slate.md](references/slate.md), with [references/example-slate.md](references/example-slate.md) as the model. Rank, then hand the top one to three ideas to `foster-assess-business` (run it if installed, as a quick read for three, the full battery for one), or tell the user that's the next step.

Done when the slate ends with the ranked shortlist and a named handoff.

## 7. Deliver and learn

Put the slate where the user reads documents and link it. Save the shortlist and the kill reasons to memory if there is any, so the next run doesn't regenerate them. If a kill reason keeps recurring, or the user rejects an idea for a reason the files don't capture, offer to add it to their `principles.md` in its format.
