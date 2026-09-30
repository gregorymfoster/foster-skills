# Durable sweep state

Use one current ledger and a concise action log. Reuse an existing private tracker rather than creating several competing summaries. Keep synced reference sources read-only.

## Sweep header

Record:

- Account, scope, timezone, and the user's definition of done.
- Approved rules and specific actions, including exceptions and whether permission applies only to this sweep.
- Context sources allowed for replies and portal checks.
- Last complete inventory time, provider, unique thread count, unread count if useful, and any coverage gaps.

## Current thread ledger

| Field | Content |
| --- | --- |
| Identity | Stable thread ID and an email link; subject or sender for recognition. |
| Current obligation | One sentence describing what still needs to happen. |
| Evidence | Relevant user answer, latest message, portal status, or confirmed action, with its date. |
| Disposition | Archive, act, reply, wait, hold, or decision needed. |
| Next step | Concrete action and owner; include a date, timezone, or trigger where applicable. |
| Permission | Approved, awaiting the specific approval, or read-only check allowed. |
| Verification | What actually succeeded, how it was checked, and any remaining uncertainty. |

Group related threads under one obligation while retaining every thread ID and its disposition. Separate distinct obligations within a conversation, such as a settled payment and an uncompleted funding request.

## Action log

Append or prepend brief dated entries containing affected thread IDs, the approved reason for each change, verification, and failures. Keep the exact archive list here. Update the current ledger so obsolete questions no longer appear pending. Newer verified evidence supersedes older uncertainty; retain historical entries as dated history.

## Resume

Read the current header, pending decisions, and latest action entries. Incorporate the user's new answers, check the relevant live threads, and continue from the unfinished step. Check Sent Mail before reviving an old draft. Inspect only the evidence needed for a remaining uncertainty; avoid redoing completed checks merely because the conversation was compacted.

## Handoff

Report the verified batch results, intentional waiting items, and the few decisions with the nearest deadlines. Link the ledger for the rest. State coverage and access limits plainly. A pending decision is not an intentional hold, and a tracker entry alone does not complete an external action.
