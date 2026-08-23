# psyscan-library

![logo](logo.png)

Public, versioned index of vetted task and experiment cards for both
[psychscanner](https://github.com/saurabhr/psychscanner) and
[psychscanner-primal](https://github.com/saurabhr/psychscanner-primal), the
slim Hub-optimized distribution.

This repo is not the place to write library code — it's a curated data
index. Cards live under `tasks/<distro>/` and `experiments/<distro>/`, where
`<distro>` is `psychscanner` or `primal`. **Cards are not portable between
the two** — `psychscanner` cards may use `.json`, `.tcard.psyscan`, or
`.xcard.psyscan`; `primal` cards are plain `.json` only, and primal has no
experiment cards at all. Every card has been verified to actually load and
run end-to-end against its distro's built-in mock LLM before being merged —
not just checked for valid JSON.

## Compatibility

`pyproject.toml` has an extra per distro (`psyscan-library[psychscanner]` or
`psyscan-library[primal]`) rather than a single dependency, since the two
packages install as the same `psychscanner` import name and can't be
co-installed. Cards aren't guaranteed to run against releases older than the
pinned minimum for their distro.

## Dedup

`INDEX_LEDGER.json` (repo root, derived, committed) hashes every card's
content — keyed by its `tasks/<distro>/...` or `experiments/<distro>/...`
path — so a contribution can't be added twice under different names, and
flags a filename that's already taken.

See the [Tutorial](tutorial.md) for a walkthrough plus a one-liner
run command for every card currently in this repo,
[Browsing cards](browsing.md) to pull cards from a checkout (or via
`download_lib()`) the same way your own code would, or
[Contributing a card](contributing.md) to add one.
