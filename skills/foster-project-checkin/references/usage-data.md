# Usage data

Greg wants every check-in to answer the questions a data scientist would ask before the meeting: is anyone using this, how much, what in the numbers is surprising, what is wrong with the numbers themselves, and are we on pace for the goal. (Greg, 2026-10-27.) This step runs in every check-in. When nothing measures the project, the deck says so plainly and asks for the goal. It never guesses.

Budget it like the rest of gathering: ten to fifteen tool calls, read-only. Don't add tracking, run writes, or install anything in order to brief him. If instrumentation is missing, propose it as a decision instead.

## 1. Pin down the goal

Look for the number this work is supposed to move before looking at any data, so the data answers a question instead of suggesting one. Check the last deck's `calls.md` and `deck.json` (a goal he set last time wins), project memory and rules files, specs and PRDs, roadmaps or OKRs, the README, the PR that launched the feature, and the project chat.

A usable goal has a metric, a target, and ideally a baseline and a date: "150 of 200 stores searching every week by Dec 1". If you find a direction without a number ("more stores using search"), treat it as no goal. If you find nothing, the deck gets a question slide that asks which number would tell him this is working. Offer two to four candidate metrics as quick answers and say which one you will track if he doesn't answer.

## 2. Find the data, cheapest first

Every harness exposes data differently. Check what this one actually has instead of assuming.

**Connected tools.** Look at your own tool list first. In Claude, scan the available and deferred tools (ToolSearch for "analytics", "query", "sql", "events", "metrics" helps), and the connector list if there is one. In Claude Code, also check `.mcp.json` and `claude mcp list`. In Cursor, check `.cursor/mcp.json` and the global MCP settings. In Codex, check `mcp_servers` in `~/.codex/config.toml`. The families worth trying, roughly in order of how directly they measure use:

- Product analytics: Amplitude, Mixpanel, PostHog, Pendo, Heap, Google Analytics, Segment.
- Warehouses and databases: BigQuery, Snowflake, Databricks, Redshift, a Postgres or MySQL replica.
- Notebooks and BI: Hex, Mode, Looker, Metabase, Definite. Existing dashboards here often already compute the metric, so read them before writing a query.
- Operations: Datadog, Sentry, Grafana, PagerDuty. These give request volume, error rates and incidents, which count as usage signals and as blockers.
- Money and distribution: Stripe, app store consoles, package registries.

A connector that is configured but fails to connect, or needs a sign-in, is a blocker worth naming. Put it in `gaps` and, if it holds the main metric, on the usage slide as a `blocked` finding.

**Command-line tools that are already signed in:** `bq`, `snowsql`, `psql` with a read-only URL already in the environment, `gcloud`, `datadog-ci`, `sentry-cli`, `stripe`. Never paste or hunt for credentials.

**The repository.** Search the code for tracking calls (`track(`, `capture(`, `logEvent`, `analytics.`, `posthog`, `amplitude`, `mixpanel`, `segment`) to learn the event names, and check `git log -S` for when each one was added. An event added halfway through the window is a data issue to report, not a trend. Saved queries, notebooks and dashboard definitions in folders like `sql/`, `analytics/` or `notebooks/` tell you how the team already measures things. Local SQLite files, log files and CSV exports can hold real use. Test fixtures and seed data don't.

**Proxy signals when there is no telemetry.** Tools, libraries, skills and internal scripts often have no analytics. Use what exists and label it as a proxy: package downloads (npm, PyPI), release download counts and repository traffic or clones from GitHub, issues and PRs from people other than the author, archived outputs (for a skill like this one, how many check-in decks exist and how often), support tickets, app store reviews. A proxy can carry the slide if you say on it that it is a proxy and what it misses.

## 3. Read it like a data scientist

Answer these, in this order, for the check-in window and the window before it:

1. **Adoption.** How many distinct people or accounts used the feature, out of how many could have. Reach as a share beats a raw count.
2. **Frequency and retention.** How often they come back. Share of week-one users still active in week two is the single most useful retention number for a young feature.
3. **Depth.** Do they finish the thing it is for? One funnel step from start to the key action is enough.
4. **Trend.** Weekly points across the window, plus the level before launch when there was one. Mark launches and releases on the timeline in your notes, so you can tell a release bump from steady growth.
5. **Progress toward the goal.** Current value, target, baseline, deadline. Project the pace by extending the last three or four weekly points in a straight line, and say that is how you projected it. Call it on track when the projection meets the target, at risk when it lands within about 80 percent of the gap, off track below that, and too early when there are fewer than two weeks of data or too few users for the number to mean anything.

Then look for the one or two findings that would change a decision. Segment by the splits the business cares about (platform, plan, store or team, new versus existing users) and look for outliers and surprises. Say "these move together", never "this caused that", unless an experiment says so.

Before any number goes on a slide, check it:

- Cross-check one headline number a second way (a different table, the dashboard, a raw count).
- Compare it to the previous deck. A number that more than doubled or halved needs a reason on the slide.
- Exclude internal, test and bot traffic, or say you couldn't.
- Watch for renamed or newly added events, timezone cutoffs, sampling, late-arriving data, and double counting across devices.
- Treat small numbers as small. Under about 30 users, give counts, not percentages.

Each problem you find is a data issue. Note it as a `data-gap` finding when it limits what the numbers can say, or as `blocked` when it stops you measuring at all. Blockers outside the data (an access request, a broken event, a feature flag stuck off) go there too.

## 4. Put it in the deck

Every deck carries a `usage` summary, which the cover shows as one line: where things stand against the goal, the goal in words, and which data says so with how fresh it is. With data, the deck also gets a usage slide. [deck-data.md](deck-data.md) has the fields and [components.md](components.md) has the components.

A good usage slide has a claim title with the headline number ("112 of 200 stores search every week, behind the pace for December"), a lede that says what the trend means, and three or four findings with states: `up`, `down` or `flat` for the metrics that moved, `surprise` for the thing nobody expected, `data-gap` for a hole in the data, `blocked` for what stops you. Pair it with a `goal` visual when there is a goal, or a `line` for the adoption trend when there isn't one yet. A second usage slide is fine when the data has two stories, as long as the deck stays inside its time budget.

Follow the usage slide with the call it raises: is this the right goal, should we instrument the missing step, do we chase the stores that never tried it. Put each query in plain words in `evidence` (the table and event names belong there too), so the next check-in can rerun it.

Keep it aggregate. No individual user names, emails or account IDs on slides, and no raw rows in the archive. Project privacy rules apply to data the same way they apply to screenshots.

## When there is no data

Set `usage.status` to `no-data`, list every place you looked in `usage.searched`, and leave out the usage slide (the renderer refuses one without data). The cover then reads "No usage data · Nothing measures this yet. Looked in: …". If there is no goal either, ask for it with a question slide; the renderer requires one. Then make a decision slide for how to start measuring when that is a real choice (add one event for the key action, connect the analytics tool, or keep running on judgment), with your recommendation and what it costs.

## Save the recipe

When the data step works, save what it took to project memory: the goal and where it came from, the sources and how to reach them, and the queries in plain words with their table or event names. The next check-in should be able to rerun it in two or three calls. When it fails, save where you looked so the next one doesn't search the same empty places.
