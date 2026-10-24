# Project Check-in maintenance

Greg explicitly authorized automatic commit and push whenever this skill is updated (decided at the 2026-10-24 check-in). After running the tests below, commit only intended changes and push to `gregorymfoster/skills` without asking again. Use a rebase workflow; preserve unrelated work and never force-push. This applies to the skill and its supporting documentation, not to check-in decks, calls, or other project data.

Before every push, run the tests locally. There is no CI on this repository by design:

```sh
python3 -m unittest discover -s project-checkin/scripts -p 'test_*.py'
```

The canonical directory is `/Users/gregfoster/code/skills/project-checkin`. Installed locations should be symlinks to it. Check-in archives belong outside this repository.
