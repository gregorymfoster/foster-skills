# foster-skills

Personal agent skills, one directory per skill under `skills/`. The repository is also a plugin, so Claude Code, Codex, ChatGPT, and Cursor can each install all of them at once with their scripts included.

## Skills

- `foster-research-paper`: pipeline from a research question to a published,
  illustrated post on the personal research site.
- `foster-draft-review`: annotated HTML feedback on personal drafts, with the source
  left untouched and reviews archived locally for later comparison.
- `foster-project-checkin`: a five-minute slide briefing on an AI-run project, with
  status slides and decision slides interleaved so you can make the calls
  while the agent keeps working.
- `foster-fuzz`: drives an app's real UI like a crowd of realistic users,
  through every flow and state it can reach, and reports the bugs and UI/UX
  problems it finds with screenshots and repro steps.

## Install

**Claude Code**

```
/plugin marketplace add gregorymfoster/foster-skills
/plugin install foster-skills@foster-skills
```

Pull changes later with `/plugin marketplace update foster-skills`.

**Codex and ChatGPT**

```bash
codex plugin marketplace add gregorymfoster/foster-skills
codex plugin add foster-skills@foster-skills
```

Once the marketplace is added, the ChatGPT desktop app lists the plugin in its Plugins directory. OpenAI notes that repo marketplaces aren't on every ChatGPT surface yet.

**Cursor**

```bash
mkdir -p ~/.cursor/plugins/local
ln -s "$(pwd)" ~/.cursor/plugins/local/foster-skills
```

Then run **Developer: Reload Window**. You can also symlink one skill at a time into `~/.cursor/skills/` or `~/.codex/skills/`:

```bash
ln -s "$(pwd)/skills/foster-research-paper" ~/.cursor/skills/foster-research-paper
```

**claude.ai**

claude.ai doesn't install plugins. Add skills one at a time, from a skill card in a chat or by uploading a zipped skill folder in Settings.

## Plugin files

`plugin.json` at the root is the single source of truth: name, version, description, author. Codex, ChatGPT, and Cursor read it directly, and Claude Code reads it too. Two marketplace files are generated from it, `.claude-plugin/marketplace.json` for Claude Code and `.agents/plugins/marketplace.json` for Codex and ChatGPT. Don't edit them by hand. After changing `plugin.json` (bump `version` when skills change), run:

```bash
python3 scripts/sync_plugin.py
```

## Tests

There is no CI. Run every test locally before pushing:

```bash
(for d in scripts skills/*/scripts; do python3 -m unittest discover -s "$d" -p 'test_*.py' || exit 1; done)
```

The test in `scripts/` fails if the generated marketplace files have drifted from `plugin.json`.
