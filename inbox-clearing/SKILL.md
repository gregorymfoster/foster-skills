---
name: inbox-clearing
description: Work collaboratively through an email inbox until every thread has a verified action, archive, reply, or intentional hold. Use for inbox sweeps and clearing an email backlog; use narrower skills for a single email or a briefing alone.
---

# Inbox Clearing

Help the user close open loops with as little repeated decision work as possible. Completion means every thread in the agreed scope has a disposition and a next step where needed. An empty inbox is optional.

## Establish the sweep

Use answers already in the conversation. Ask only for missing choices that change execution:

- Which account and scope: the whole inbox, unread mail, or a date range?
- What would make the sweep feel done, and which deadlines or concerns matter most?
- Which routine categories may be archived after review? May waiting threads receive dated snoozes? Should replies use email alone or another named source?

For a broad request, propose clearing everything by acting, archiving, replying, or holding appropriately. A useful archive rule covers reviewed promotions, expired invitations, and settled or superseded confirmations. Obtain authorization for the rule, then apply it without asking again for each matching batch. Keep invitations and introductions requiring a personal preference pending until the user decides. Prioritize active money, security, health, legal, and deadline matters.

Record the scope, timezone, permissions, and exceptions. Authorization persists within the conversation; a saved skill or an old sweep log does not grant authorization for a new sweep. Sending, subscription changes, payments, uploads, and account changes each need their own applicable authorization. Follow the current tool and browser policies.

## Inventory and reconcile

Prefer connected email tools. Read [references/connectors.md](references/connectors.md) when using Gmail or Superhuman, reconciling counts, or verifying an archive or snooze.

Paginate the full agreed scope, deduplicate by thread ID, and record the provider and scan time. Include older unresolved mail and mixed threads containing drafts or sent messages. For a large backlog, review in manageable batches with urgent items first; preserve the unreviewed remainder in the inventory.

Read the conversation before choosing an action. Fetch enough history to establish the current request; follow older messages or attachments when they contain the unresolved obligation. Summaries and snippets locate candidates but may omit decisive facts.

Reconcile each candidate against later replies, related threads, current Sent Mail, and the user's answers. If the user says an item was handled, treat that as evidence of the stated action and inspect only the remaining uncertainty. Recheck for new activity immediately before a mutation. A sent reply can resolve the need to respond while leaving a separate outcome pending.

Use a private, durable tracker when the sweep spans batches or turns. Read [references/sweep-state.md](references/sweep-state.md) for its fields and resumption rules. Reuse an existing tracker if available; keep personal contents outside skill files and public repositories.

## Decide and act

Assign each reviewed thread one current disposition:

| Disposition | Required evidence or next step |
| --- | --- |
| Archive | The thread matches an approved routine rule, is confirmed resolved, or is clearly superseded. Verify removal from the inbox. |
| Act | Name and perform the authorized task. Record the actual confirmation, or keep the unfinished step pending. |
| Reply | Prepare a source-grounded reply, identify its recipient and purpose, and obtain explicit send authorization. Verify delivery after sending. A draft remains pending. |
| Wait | Record what was sent or submitted, who owes the response, and when or why to check again. Use an authorized snooze when useful. |
| Hold | Record the user's intentional choice to defer or keep a reference, with a date or trigger when one applies. |
| Decision needed | State the unresolved fact or preference and ask the smallest useful question. This is not a completed hold. |

### Ask concrete questions

Group related decisions into short rounds the user can answer easily. Include the sender or subject, amount or deadline when relevant, and the practical choice. Examples: “Has this payment settled?”, “Both of these sign-ins yours?”, “Accept, decline, or hold this invitation?”

Avoid a long queue of overlapping unanswered questions. Keep pending questions in the tracker; reuse answers and continue independent work while awaiting them. Separate factual confirmation from permission: recognizing a charge does not authorize a payment, and wanting a referral does not authorize sending private information.

If a user flags a possible omission, check the evidence and fix it. “Didn't we already email them?” calls for a Sent Mail and draft check before another message. Preserve ambiguity when the user is unsure; investigate through authorized sources or keep the uncertainty visible.

### Prepare replies

Use the agreed context sources and the user's tone. Draft only claims supported by the threads or the user's answers. Preserve useful existing drafts, checking whether newer messages made them obsolete. Present concrete recipients, text, and attachments before requesting send approval. Authorization to draft is distinct from authorization to send.

Apply the humanizer skill in embedded mode as the final editorial pass for substantive emails and other shareable prose when available. Preserve factual, clinical, financial, and legal distinctions. Short transactional acknowledgments do not need an editorial workflow.

### Resolve tasks behind the email

Inspect another account or portal when needed to answer a specific open question and access is authorized. Use read-only checks to establish amounts, deadlines, payment status, subscriptions, or claim status. Prepare consequential changes for review and follow the required user handoff or approval at execution.

Match evidence to the precise obligation. A sent wire still may await recipient receipt. A submitted claim can fail or remain in processing. A refund can settle while a subscription remains active. A past meeting can still contain a survey or other task. A recognized reset request does not establish that every later credential change was intended.

Keep financial and clinical details sourced. For a medical attachment, preserve the clinician's content, verify readability and visit details, and confirm permission for the specific file and destination before uploading. Let the user complete authentication challenges requiring their participation. Record access limits explicitly.

### Keep actionable to-dos in Reminders

When the sweep identifies an actionable to-do for the user, create or update it in Apple Reminders when available. Use the user's existing to-do list and relevant section. Search first and update an existing matching reminder rather than creating duplicates. Include the concrete action, source email link, and relevant deadline or next-check date in the user's timezone. Set priority from urgency and explicit user instructions; a high-priority request should use High priority and the established high-priority section when possible.

Do not leave user tasks only in chat or the sweep tracker. Verify the saved reminder's title, notes, due date, and priority. If Reminders is unavailable, record the task in the tracker and explain the access limit. A waiting item may receive a reminder to check for a response; creating the reminder does not authorize a send, payment, account change, or email snooze. Keep uncertainty visible, including contradictory invoice markings, until payment or other completion evidence resolves it.

### Handle waiting items

Choose a return date based on the actual deadline, expected response time, delivery date, or payment date. Record the timezone and the check to perform. Verify both the reminder and the intended inbox state. An unanswered decision stays pending unless the user chooses a hold; elapsed time is not consent.

Snoozing an email is separate from creating a scheduled agent follow-up. Create automations only when requested. Permanent filters, unsubscribes, trash, and bulk deletion require separate authorization from routine archiving.

## Verify and finish

After each batch, record successful changes and failures by thread. Reconcile new messages and triggered reminders against the existing tracker, updating the thread's state rather than counting every reminder as a new obligation. Check the affected threads through the provider that exposes the required state. Report counts with their source and timestamp when providers disagree.

Before calling the sweep complete, check that every thread in scope is reviewed and has either a verified completed action, an authorized archive, a sent reply with any follow-up tracked, or an intentional hold/wait with its next check recorded. Outstanding drafts, unanswered decisions, failed actions, and inaccessible evidence remain incomplete. Coverage limits belong in the report.

Continue useful authorized work until only user decisions or external blockers remain. Then give a concise handoff with the highest-priority decisions, verified results, and the tracker link. Resume from that state when answers arrive. Avoid repeated scans or status-only turns when nothing actionable has changed. Goal and automation status follow their tool-specific rules; this skill does not create them automatically.

Keep the final update brief: what was cleared, what is waiting, what still needs the user, and the next real deadline. Provide the exact archive list in the private tracker, with a short category summary in chat unless the user asks for the full list.
