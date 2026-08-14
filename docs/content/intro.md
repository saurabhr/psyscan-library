# psyscan-library

![logo](../logo.png)

Public, versioned index of vetted task and experiment cards for
[psychscanner](https://github.com/saurabhr/psychscanner).

This repo is not the place to write library code — it's a curated data
index. Every card under `tasks/` and `experiments/` is a plain psychscanner
task/experiment card (`.json`, `.tcard.psyscan`, `.xcard.psyscan`), and every
card has been verified to actually load and run end-to-end against
psychscanner's built-in mock LLM before being merged — not just checked for
valid JSON.

## Compatibility

`pyproject.toml` pins the `psychscanner` version this index was validated
against (`psychscanner>=0.5.0`). Cards aren't guaranteed to run against
older releases.

## Dedup

`INDEX_LEDGER.json` (repo root, derived, committed) hashes every card's
content so a contribution can't be added twice under different names, and
flags a filename that's already taken.

See [Browse the index](browsing.py) to pull cards from a checkout the same
way your own code would, or [Contributing a card](contributing.md) to add
one.
