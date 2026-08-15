# Humanize checklist

Condensed from the humanizer skill (Wikipedia's "Signs of AI writing").
Run as a loop: edit the draft, audit it, fix what the audit finds.

## Register

Research notes are reference prose: neutral and plain is the correct human
voice. Keep the human signals already present (first-person uncertainty,
mixed verdicts, specific hard-to-fabricate detail) and skip injected
personality.

## Edit pass

Rewrite, never just delete; the rewrite covers everything the original
covers.

- Punctuate with commas, periods, colons, and parentheses. Em and en
  dashes are the strongest single tell: zero in the final text.
- Straight quotes only.
- Sentence-case headings.
- Bold only where it carries meaning; a run of bolded labels (case names,
  numbered principles, list headers) is mechanical, so let headings and
  sentence structure carry navigation.
- Plain copulas: "is", "has". Rewrite "serves as", "stands as", "boasts".
- Cut significance inflation ("pivotal", "testament", "underscores",
  "reflects broader trends") and AI vocabulary ("delve", "tapestry",
  "landscape", "vibrant", "crucial", "showcase").
- Cut stock transitions ("ultimately", "in conclusion") and signposting
  ("let's dive in").
- Break formulaic rule-of-three cadences; keep a triple only when the
  content genuinely has three parts.
- Rewrite "from X to Y" ranges that are not a real scale.
- Limit "not X, but Y" constructions to ones making a genuine distinction.
- Attribute opinions to named sources; "experts argue" is a weasel.
- State what is unknown plainly instead of filling gaps with plausible
  guesses ("likely grew up...", "maintains a low profile").

## Audit pass

Scan the final text and treat any hit as unfinished work:

- `rg -c '—|–'` for dashes; `rg -n "’|‘|“|”"` for curly quotes.
- `rg -n '^#+ '` and check headings for Title Case (a lone pronoun "I" is
  fine).
- `rg -c '\*\*'` and justify each remaining bold.
- Read for clusters: one tell in isolation is often legitimate; several
  together are a confession.
- Check counts against lists ("two numbers" followed by three items).
