# Contributing a task or experiment card

1. Add your card as a single file:
   - task card → `tasks/<name>.json` (or `.tcard.psyscan`)
   - experiment card → `experiments/<name>.json` (or `.xcard.psyscan`)
2. Validate it locally:
   ```bash
   pip install -e .  # installs the pinned psychscanner version
   python scripts/validate_contribution.py tasks/<name>.json
   ```
   This checks, in order: required fields are present, the filename/content
   isn't a duplicate of an existing card, and — the hard requirement — **the
   card actually runs end-to-end** against `psychscanner`'s built-in mock LLM.
   A card that raises during a real run will not be merged.
3. Regenerate the ledger and commit it:
   ```bash
   python scripts/index_ledger.py build
   ```
4. Open a PR. CI re-runs the same two checks on every changed card.

## Existing seed cards

`tasks/example_survey.json` was copied in from `psychscanner`'s own
`examples/tasks/` to bootstrap this index — it's not auto-synced. This repo
is now the source of truth for it going forward; if `psychscanner`'s copy
ever changes, treat that as the one that drifted, not this one.

## What makes a good card

- `taskname` and `items` (task cards) or `task_file` (experiment cards) —
  see `psychscanner`'s [task_library guide](https://github.com/saurabhr/psychscanner/blob/main/docs/guides/task_library.md)
  for the full schema.
- Every trial needs a `trcode` and a `stimulus` (or pre-built `hmsg`).
- Keep names filesystem-safe and unique — the ledger rejects both filename
  collisions and byte-identical content under a different name.
