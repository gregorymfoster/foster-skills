# Founders and team lenses

## Founder fit

One verdict row per founder. Name the role they would own and which strengths it uses. Pass when each founder has a real, ownable side of the business in their strength. Partial pass when their craft carries over but their domain expertise doesn't, or their role is thin. Fail when the idea needs skills nobody on the team has and can't hire cheaply. Ask: would a competitor with these founders' exact advantages do it better? If not, that's fit.

For the scorecard, give team-level fit as High, Medium or Low, noting who leads.

## Constraints

From the profile: non-competes and what they cover, dates they lift, employer outside-activity approvals, conflicts of interest, no-go areas. Verdicts: Pass, Pass with disclosure, Parked until a date, or Fail. Skip the row when the profile lists none. In anything shared beyond the founders, describe constraints in general terms ("clear of the founder's non-compete") and never quote the agreements.

## The founder profile

A private file the skill reads before judging: `founders.md` in the project, in `.agents/`, or in `~/.config/foster-assess-business/founders.md`. Profiles hold sensitive details, so keep them out of public repositories. Blank fields are fine; the matching verdicts are marked provisional and asked about at the end of the report.

```markdown
## <Name>

- Role in the company: <what they would own>
- Strengths: <domains, skills, networks, track record>
- Can skill up in: <areas they're willing to learn>
- Weak spots: <what they'd need a partner or hire for>
- Constraints: <non-competes, approvals, conflicts, dates they lift>
- No-go areas: <markets or kinds of work they won't do>

## Team

- Time commitment: <side project, part-time, full-time, and from when>
- Funding preference: <venture, self-funded, undecided>
- Preferred buyer and sales motion: <developers, small firms, enterprise; product-led or sales-led>
- Markets to avoid: <for example, markets with small budgets>
- Lenses: <keep all, or list lenses to drop, such as free-first>
- Every founder should own a side of the business: <yes or no>
```

## Example

```markdown
## Alex

- Role in the company: product and engineering
- Strengths: developer tools, infrastructure, ten years building internal platforms at a large company
- Can skill up in: security
- Constraints: non-compete on code-review tools until March 2028

## Sam

- Role in the company: operations and sales
- Strengths: built and ran a 60-person remote services team, enterprise sales into mid-size firms
- No-go areas: anything that needs a hardware supply chain

## Team

- Time commitment: side project for a year, then full-time if it works
- Funding preference: undecided
- Markets to avoid: education, consumer apps
- Every founder should own a side of the business: yes
```
