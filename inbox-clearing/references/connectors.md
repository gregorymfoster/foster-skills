# Gmail and Superhuman verification

Discover callable tools and read their current schemas. Tool names and sync behavior may change; use this reference for the verification criteria.

## Inventory

- Gmail's INBOX label exposes message, thread, and unread counts. These are different totals; name the one being reported.
- Fully paginate the chosen inbox search and deduplicate by thread ID. A count alone does not establish review coverage.
- Superhuman list results can include mixed conversations whose latest message is SENT or DRAFT. Earlier incoming messages may still have INBOX in Gmail even when Superhuman's summary omits it.
- For a Gmail account, Gmail's per-message labels are the authority for whether an archive removed the conversation from the inbox. Inspect all relevant messages, with adequate pagination or message limits.

## Read efficiently

Use search results to identify threads, then read only the needed conversations. For batch reads, inspect the returned schema before extracting fields. Return sender, date, subject, labels, and relevant plain text to the model; omit transport headers, tracking links, and duplicate HTML. Retain the raw response only where further inspection is needed. Read attachments when the obligation lives there.

## Archive

1. Recheck the current thread and the applicable approval.
2. Prefer Gmail's thread archive when it explicitly removes INBOX from every message. If using Superhuman's thread update, supply the current last-message ID and the documented mark-done operation.
3. Inspect each result for success or failure.
4. Read the affected thread and verify that every message lacks INBOX. A stale latest-message summary or successful request alone does not prove the whole thread is archived.

If a sync delay is plausible, make a bounded follow-up read. If the expected state still cannot be verified, record the discrepancy and leave the action unconfirmed. Preserve drafts and other labels unless their change was authorized.

## Snooze

Confirm the tool's reminder operation and whether it also marks the thread done. Verify the active reminder's thread ID, date, and timezone, then verify the intended inbox state. If the reminder list is temporarily stale, make a bounded follow-up query. A successful creation response does not establish that both states are correct.

When a reminder triggers, update its existing ledger item. Retain the email while its task is due; reassess the underlying obligation before archiving or moving the date.

## Send and external outcomes

Before sending, inspect the actual draft, recipients, attachment contents, and the latest thread. After an authorized send, verify a sent message containing the intended text and files. Check for independent user sends before retrying an uncertain result.

For bank, insurance, subscription, and medical tasks, record the account's exact status and the time checked. Separate request received, submitted, processing, sent, posted, settled, recipient received, and completed. Use the state that answers the email's actual question; keep any remaining obligation tracked.
