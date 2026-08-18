# Humanize checklist

Condensed from the humanizer skill (Wikipedia's "Signs of AI writing").
Run as a loop: edit the draft, audit it, fix what the audit finds.

## Register

These are research essays, not reference notes. Plain language is the base,
but a particular researcher should be audible in the choices: first-person
uncertainty, mixed verdicts, specific hard-to-fabricate detail, surprise, and
uneven emphasis. The closest canonical post selected through
`editorial-style.md` outranks generic notions of neutral prose.

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
- Remove visible evidence scaffolding. Fold paragraph prefixes such as
  "Empirical finding:" and "Empirical inference:" into the sentence or a
  nearby parenthetical, while preserving the epistemic distinction.
- Break source-dump cadence: repeated same-length paragraphs that announce a
  category, summarize several facts, and end in a citation bundle. Rebuild the
  passage around the argument, attaching each important link to its claim.
- Move the requester's motivating question and the essay's strongest tension
  ahead of definitions and taxonomy. Technical setup earns space only when the
  reader knows why it matters.
- Treat repeated caveats as a structural defect. State each uncertainty where
  it changes the conclusion, then let the conclusion move.

## Audit pass

Scan the final text and treat any hit as unfinished work:

- `rg -c '—|–'` for dashes; `rg -n "’|‘|“|”"` for curly quotes.
- `rg -n '^#+ '` and check headings for Title Case (a lone pronoun "I" is
  fine).
- `rg -c '\*\*'` and justify each remaining bold.
- Read for clusters: one tell in isolation is often legitimate; several
  together are a confession.
- Check counts against lists ("two numbers" followed by three items).
- Compare the first 500 words, one middle section, and the ending beside the
  canonical post. Flag a mismatch in stance, cadence, evidence integration, or
  section scale even when the ordinary AI-pattern scan is clean.
- Search `rg -n '^(Empirical|Traditional wisdom|First-person testimony|Calculation)[,:]'`.
  Any repeated paragraph-prefix pattern is unfinished prose.
- Ask three editorial questions: Why would the intended reader continue after
  the opening page? Where is the writer's own judgment? Which section would a
  human editor merge or move because the research outline is showing through?
