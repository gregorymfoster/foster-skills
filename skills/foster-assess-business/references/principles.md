# Principles

A private file where the user writes down their own judgment: rules of thumb, filters they apply to every idea, and lessons from ideas they've tried. The skill reads it on every run and turns each principle into a verdict row, so the assessment gets sharper as the file grows.

Keep it private: `principles.md` in the project, in `.agents/`, or in `~/.config/foster-assess-business/principles.md` to use it across projects. It never belongs in a public repository.

## Format

One section per principle. "Check" is what makes it testable; without one, the skill can't give a verdict. "Kind" decides how much it weighs.

```markdown
## <Short name>

- Rule: <the principle in one sentence>
- Why: <the story or evidence behind it>
- Check: <how to judge pass or fail for a given idea>
- Kind: filter | heuristic | red flag
- Added: <date>, from <idea or experience>
```

- **filter**: failing it should usually kill the idea. Shown in the verdict table.
- **heuristic**: a lean, not a rule. Shown in the verdict table, weighed in the pros and cons.
- **red flag**: a pattern that has burned the user before. Only shown when it fires, at the top of the Cons paragraph.

A principle that duplicates a built-in lens overrides that lens's rubric. Write it with the same name (for example "Free-first") and the skill uses the user's check instead.

## Lessons log

Below the principles, an optional dated log of outcomes, one line each: what was tried, what happened, what it taught. When a lesson keeps recurring, promote it to a principle.

```markdown
## Lessons

- 2026-03-04: <idea>. Ran a deposit test with 10 prospects, 0 paid. Stated interest meant nothing in this segment.
```

## Example

```markdown
## Sell to someone with a deadline

- Rule: the buyer must face a dated consequence (an audit, a renewal, a regulation) if the problem isn't solved.
- Why: our last two products stalled in "nice to have" for a year.
- Check: name the deadline and who it belongs to. No deadline is a fail.
- Kind: filter
- Added: 2026-01-10, from the reporting-tool attempt

## Beware the champion who can't buy

- Rule: enthusiastic users without budget authority are not a signal on their own.
- Why: 40 happy pilot users, zero conversions, because nobody above them cared.
- Check: does the adoption path reach the signer within the first month?
- Kind: red flag
- Added: 2026-02-02
```
