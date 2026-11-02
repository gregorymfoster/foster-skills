# The shape filters, in detail

Each filter gets a verdict and a short why. Use the full scale: Pass, Mostly pass, Likely pass, Partial pass, Fail, Unknown. "Likely" means the logic holds but the evidence is thin; "Partial" and "Mostly" mean some parts pass and others don't. The why should say which.

## 1. Free-first

The free-first filter favors products the team can build and give away for a while to earn trust and a foot in the door, then layer paid services on later. Free users "pay" in the Mom Test sense: with time, feedback and usage.

Free-first only works when five things hold. Score each yes, weak, or no:

1. **Adopt without buying.** An individual can start using it without a purchase decision, a procurement review, or IT approval. Hardware and anything that needs an admin to install fails here.
2. **Near-zero cost to serve.** Free users cost almost nothing: it runs on their machine, or the hosted part is cheap per user. Heavy model inference on the company's bill fails unless it can be capped.
3. **Usage compounds.** Free use builds something that gets more valuable over time: accumulated data, team habits, templates, network effects, a public reputation.
4. **A natural paid layer, bought by someone else.** The team, firm or company pays for admin, policy, audit, hosting, retention, support or scale. If the only buyer is the same individual who got it free, the paid layer is weak.
5. **Beats the free options already out there.** The free version has to be clearly better than what's already free. This test knocks out more ideas than you'd expect: many fields are full of free extensions, scripts and open-source projects.

Pass needs all five, or four with a clear plan for the fifth. Watch for buyers who don't adopt bottoms-up (lawyers, clinicians, anyone whose laptop IT locks down); there the free tier becomes a free firm pilot, which is still free-first but slower. Say so.

Always pair a pass with a dated money test, around month 4: put a paid plan in front of the most active free users so free usage can't quietly become the whole strategy. Usage counts as payment only with numbers attached: installs still active in week 4, feedback calls taken, introductions to the person who signs.

## 2. The internal-tool test

The best tools often already exist, hacked together inside some top company, and haven't been made generic and easy to adopt. Many durable companies are one firm's in-house system repackaged for everyone else.

Pass when you can name a specific internal tool at a well-known company, with a source: an engineering blog post, a talk, an open-sourced repo, press coverage with usage numbers. Examples of internal tools: JPMorgan's LLM Suite and McKinsey's Lilli (in-house AI platforms only the largest firms could afford), Dropbox's Securitybot, Stripe's Smokescreen.

Check whether it has already been productized, often by the people who built it (Airbnb's StreamAlert became Panther, Uber's Michelangelo became Tecton, Facebook's osquery led to Kolide and Fleet; from memory, not re-checked). If a polished product already exists, the test still passes on the first half but the next filter will likely fail. The richest seam right now is the AI-era generation of internal tools built since 2023 that nobody has packaged for smaller companies.

## 3. Crowded but mediocre

Split "crowded" into two kinds:

- **Crowded with weak, unbacked tools: open.** Dozens of one-person repos, half-finished extensions, tools with no polish or long-term backing. This is often the best opening: the need is proven and nobody has done it well.
- **Crowded with polished, well-funded leaders: closed.** A leader with real revenue, a big round, or a platform owner bundling it in.

Name the leaders you found, with funding or revenue where you can, and name the long tail. If the field is split (polished at the enterprise end, nothing for small companies), say which slice the idea targets and whether that slice is open. Flag the risk of being filed as "a cheaper <leader>".

## 4. Big-money market

Favor markets where it's possible to build large, lucrative businesses. Look for proof that buyers already spend on this layer: a competitor's ARR, category spend, prices people pay today, or budgets the buyer already controls. Pass with a number and a source. "Likely pass" when adjacent spend is proven but this segment's willingness to pay isn't. Low-budget markets (consumer hobby tools, many education markets, anything the founder profile lists under markets to avoid) fail unless the idea sells to a different buyer.

Note monetization traps: open-source infrastructure that is hard to charge for, services that don't scale past headcount, buyers who expect it free forever.

## 5. Founder fit

Read the founder profile (see `founders.md`). For each founder, name the role they would own and which strengths it uses. Pass when every founder has a real, ownable side of the business in their strength. Partial pass when a founder's craft carries over but their domain expertise doesn't, or when one founder's role is thin. Fail when the idea needs skills nobody on the team has and can't hire for cheaply.

Ask: could a competitor with these exact founders' advantages do it better? If not, that's a fit.

## 6. Why now

Name the specific change, with a date and a source: a platform shift (AI in every tool), a vendor tightening API terms or hoarding data, a new regulation, a collapse in some cost, a big acquisition that leaves customers stranded. Pass when the change is recent, concrete, and makes the idea possible or necessary today. Fail when the honest answer is "it was always a good idea". Also note when the window might close, for example when incumbents are visibly converging.

## 7. Constraints

From the founder profile: non-competes and the areas they cover, dates they lift, employer outside-activity approvals, conflicts of interest with current employers or investors, no-go areas. Verdicts: Pass, Pass with disclosure (fine but needs an approval or disclosure), Parked until <date>, or Fail. In anything published, describe constraints generally and never quote the agreements.
