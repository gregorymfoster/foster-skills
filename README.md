# skills

Personal agent skills, one directory per skill.

To activate a skill on a machine, symlink its directory into
`~/.cursor/skills/`:

```bash
ln -s "$(pwd)/research-paper" ~/.cursor/skills/research-paper
```

## Skills

- `research-paper` — pipeline from a research question to a published,
  illustrated post on the personal research site.
- `draft-review` — annotated HTML feedback on personal drafts, with the source
  left untouched and reviews archived locally for later comparison.

For Codex, symlink the desired skill directory into `~/.codex/skills/`.
