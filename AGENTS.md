# Working in this repository

Greg wants changes published right away (2026-10-24). Commit and push straight to `main`; don't open pull requests. Before every push, run all tests and stop if any fail:

```sh
(for d in scripts skills/*/scripts; do python3 -m unittest discover -s "$d" -p 'test_*.py' || exit 1; done)
```

Check the exit status, not the printed output. There is no CI. Never force-push `main`, and preserve unrelated work. After changing `plugin.json`, run `python3 scripts/sync_plugin.py`, and bump its `version` when skills change so plugin installs pick up the update. Personal drafts, reviews, and check-in archives never go into this repository.
