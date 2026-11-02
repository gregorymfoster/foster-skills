# Worked example: a slate for Alex and Sam

A hypothetical slate showing the shape of the output. The founders are Alex and Sam from the example in `foster-assess-business`'s `references/founders.md` (Alex: developer tools and internal platforms, non-compete on code-review tools; Sam: runs a remote services team and sells to mid-size firms; the team avoids education and consumer apps). Company names and figures are from memory and not re-checked; a real run fetches and links them.

---

## Idea slate: Alex and Sam, side project

Twenty-six raw ideas, five kept. The top pick is a booking and cleanup service for shared staging environments, because Alex built one at a past job, the field is full of Slack bots and spreadsheets, and it starts free with one team. The contractor onboarding desk comes second and gives Sam a real side of the business. Both go to `foster-assess-business` for a quick read.

| Rank | Idea | Buyer | Lens | Proof of need | Biggest open question |
|---|---|---|---|---|---|
| 1 | Staging environment booking | Platform lead, 50 to 300 engineers | Mediocre field, workaround | Shared booking sheets and homegrown Slack bots | Will they pay once it works? |
| 2 | Contractor onboarding desk | Engineering ops at mid-size firms | Services to software, fit | Weeks lost per contractor to access and laptops | Is the buyer IT or engineering? |
| 3 | Test-data snapshots for small teams | Backend leads | Internal tool | Large companies run in-house masked-snapshot tools | Do small teams feel the pain? |
| 4 | Agency time tracking for Latin America | Dev agency owners | Regional | US tools miss local invoicing rules | Are budgets big enough? |
| 5 | Feature-flag cleanup | Staff engineers | Change that just happened | Flag debt after the flag-vendor price rises | Platform risk from flag vendors |

### 1. Staging environment booking

For platform teams at companies with 50 to 300 engineers, shared staging environments get double-booked and left broken. The product books, resets and expires environments from chat and CI, free for one team, paid per organization for policy, audit and cost reports. Wedge: a free bot that replaces the booking sheet. Alex leads, having run the internal version at a past job. Open question: whether a free bot this good leaves anything worth paying for.

(Ideas 2 to 5 follow the same shape in a real slate.)

### Killed ideas

| Idea | Kill reason |
|---|---|
| Pull request summarizer | Out of bounds: inside Alex's non-compete |
| Developer portal for small teams | Taken: polished, funded portals already serve them |
| Coding tutor for bootcamps | Out of bounds: education is on the avoid list |
| On-prem build cache appliance | Out of bounds: Sam's no-go on hardware |
| AI incident summaries | Platform will eat it: incident tools are shipping it |

### Handoff

Run `foster-assess-business` as a quick read on ideas 1 and 2, using the frames above, then the full battery on the winner.
