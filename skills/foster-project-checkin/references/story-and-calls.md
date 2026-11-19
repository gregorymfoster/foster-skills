# The mission, the story and the calls

Read this while deciding what goes in the deck. It covers the cover's mission block, which decisions and questions belong on slides, and the product-manager slides (research and mocks). In a short check-in you will use only part of it: pick the slides whose answers matter most.

## The mission and the roadmap

Every deck opens on the same three things: the mission, the roadmap toward it, and how far along we are. Greg should never have to reconstruct what the project is for from the status slides.

Look for the mission in what Greg actually said: the kickoff message, the project's instructions, a goal he named at an earlier check-in (the last `calls.md`), project memory, a roadmap or spec file. Write it as one outcome sentence for a person ("Every store's staff can find any product in seconds"), not a feature list. Lay out the roadmap as two to six milestones of a few words each, marked `done`, `now`, `next` or `later`, with a date when there is one. The roadmap strip is the progress report; the headline and the usage line carry the numbers.

Then be honest about how sure you are. Mark it `confirmed` only when Greg said or approved it, and name where (`source`). If you assembled it from scattered evidence, it is `inferred`. If the evidence disagrees with itself (the code is heading one way, his last message another) or there is nothing to go on, it is `unclear`. Either way, the first call in the deck is a question slide with id `mission` asking him to confirm or correct it, with the roadmap as a `flow` beside it and quick answers such as "Yes, that's it". A mission that was confirmed weeks ago but that the work has drifted from deserves the same question. Once he answers, the mission goes into project memory, and later decks mark it `confirmed`.

## The story and the calls

Write the headline first: the net effect in one plain sentence that Greg could repeat to his own boss without explaining a single word. Then pick two to four status points that support or complicate it. Include what slipped, what you dropped, and what is fragile.

Past decisions are the ones already baked in, often made quietly by you or an earlier session: a library or framework, a data model, a scope cut, a deferral, a workaround that became permanent, a reading of an ambiguous ask, a quality bar such as skipped or failing tests, or where the effort went. Surface the ones a reasonable director might disagree with, especially where the cost of reversing grows each week. Say what is in effect, what reversing costs now, and when it gets expensive.

Upcoming decisions are forks ahead: what to build next, build versus buy, scope against timeline, quality against speed, and anything that needs his authority. Give each two to four real options, labeled in plain words, each with one sentence on what happens if he picks it. Include "keep as is" or "do nothing" when that is a real choice. Recommend one, explain why in a sentence, and state your default and how reversible it is.

Some things you need from him have no options you can write: which customers matter most, whether a screenshot matches what he saw, what a vague ask meant. Make those question slides, at most three, each with what you will assume if he doesn't answer. Don't turn a real decision into a question to dodge making a recommendation.

In a full check-in, aim for three to five decisions and questions, with at least one of each timing when the evidence supports it. If there is honestly no past decision worth revisiting, say so out loud on a status slide instead of inventing one; the renderer only warns.

In a short check-in, aim for two or three calls in total. The full check-in is where three to five fit.

## Think like a PM

A short check-in carries at most one of these slides, and only when the evidence earns it. The full check-in is where a research slide and one or two mocks belong.

Spend a few minutes as the project's product manager before you build the deck. The status slides say what happened. This step asks what we should learn and build next, and gets Greg's reaction while it is still cheap to change course. Start from the mission and the usage findings: where is the gap between what the product does and what the mission needs, and which unknown, if answered, would most change what we build?

**Questions that steer.** List the questions whose answers would move the plan the most, then keep the best two to four. A good question has answers that point in different directions ("What made you go back to the old way?" splits training from product fixes). A weak one gets the same answer from everyone, or one we would ignore. Each question goes to whoever can actually answer it. Questions only Greg can answer (who the product is really for, what success looks like, which user he cares about most) become question slides. Questions for users go on one research slide: who to ask, the exact wording, what each likely answer would change, and the cheapest way to ask (a one-tap poll, a two-line email, a text to three friends who use it). Greg ticks the ones worth sending. Nothing goes to users unless he ticks it.

**Mocks to react to.** Pick one or two ideas worth showing: a new feature, or a change to the UI or flow, that the evidence points to (a usage finding, a complaint, a roadmap step, a rough edge you saw while screenshotting). Show it as a picture, never a paragraph. Build the mock outside the product: a static HTML page that reuses the app's real stylesheet and components, rendered with a headless browser to a PNG the same size as a real screenshot of today's screen, or an SVG drawn over that screenshot. Put it beside today's screen with a `slider` or `gallery` so the change is obvious. Don't build the feature, push a branch, or touch the product to make a mock. Use stock or sample content, and respect the project's privacy rules as for any screenshot. Each mock slide says what the user gets (title), the problem it fixes (lede), why this idea over others (`why`), a rough cost, and your default, usually "park it". Greg answers with Build it, Change it or Not now, plus a note.

Keep this step proportionate. In a full deck, one research slide and one or two mocks fit in about a minute and a half. If the project is a weekend toy or the evidence gives you nothing worth mocking, skip the mock and say why in `gaps`; the renderer only warns.
