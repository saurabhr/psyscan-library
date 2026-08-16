# Contributing a task or experiment card

1. Pick your distro and add your card as a single file:
   - `psychscanner` task card → `tasks/psychscanner/<name>.json` (or `.tcard.psyscan`)
   - `psychscanner` experiment card → `experiments/psychscanner/<name>.json` (or `.xcard.psyscan`)
   - `primal` task card → `tasks/primal/<name>.json` (plain JSON only — primal has
     no experiment cards)
2. Validate it locally, with the matching package installed:
   ```bash
   pip install -e ".[psychscanner]"  # or ".[primal]" — never both, same import name
   python scripts/validate_contribution.py tasks/psychscanner/<name>.json
   ```
   This checks, in order: required fields are present, the filename/content
   isn't a duplicate of an existing card, and — the hard requirement — **the
   card actually runs end-to-end** against that distro's built-in mock LLM.
   A card that raises during a real run will not be merged. If the installed
   package doesn't match the card's distro subfolder, validation reports
   `SKIP` rather than pass/fail — CI validates each distro in its own job.
   On a full `PASS` it also regenerates `INDEX_LEDGER.json` — commit that
   change along with your card. (`python scripts/index_ledger.py build`
   still exists for a manual rebuild, e.g. after deleting a card by hand.)
3. Open a PR. CI re-runs the same checks, per distro, on every changed card.

## Existing seed cards

`tasks/psychscanner/example_survey.json` was copied in from `psychscanner`'s
own `examples/tasks/` to bootstrap this index — it's not auto-synced. This
repo is now the source of truth for it going forward; if `psychscanner`'s
copy ever changes, treat that as the one that drifted, not this one.
Likewise `tasks/primal/rm_singleturn_demo.json` was seeded from
`psychscanner-primal`'s examples.

## What makes a good card

- `taskname` and `items` (task cards) or `task_file` (experiment cards) —
  see `psychscanner`'s [task_library guide](https://github.com/saurabhr/psychscanner/blob/main/docs/guides/task_library.md)
  for the full schema.
- Every trial needs a `trcode` and a `stimulus` (or pre-built `hmsg`).
- Keep names filesystem-safe and unique — the ledger rejects both filename
  collisions and byte-identical content under a different name.
