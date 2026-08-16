# psyscan-library

[![Docs](https://readthedocs.org/projects/psyscan-library/badge/?version=latest)](https://psyscan-library.readthedocs.io/en/latest/?badge=latest)

![logo](docs/logo.png)

Public, versioned index of vetted task and experiment cards for both
[psychscanner](https://github.com/saurabhr/psychscanner) and
[psychscanner-primal](https://github.com/saurabhr/psychscanner-primal), the
slim Hub-optimized distribution.

This repo is not the place to write library code — it's a curated data index.
Cards live under `tasks/<distro>/` and `experiments/<distro>/`, where
`<distro>` is `psychscanner` or `primal` — **cards are not portable between
the two.** `psychscanner` cards may use `.json`, `.tcard.psyscan`, or
`.xcard.psyscan`; `primal` cards are plain `.json` only, and primal has no
experiment cards at all (no `experiment_library` there). Every card has been
verified to actually load and run end-to-end against its distro's built-in
mock LLM before being merged — see [CONTRIBUTING.md](CONTRIBUTING.md).

## Using a card

```python
from psychscanner import task_library, experiment_library

card = task_library("my_task", dirs="path/to/psyscan-library/tasks/psychscanner")
```

Point `dirs=` (or `PSYCHSCANNER_TASK_LIBRARY_DIRS` /
`PSYCHSCANNER_EXPERIMENT_LIBRARY_DIRS`) at the `tasks/<distro>/` or
`experiments/<distro>/` subfolder matching your installed package.

Or let `psychscanner.download_lib()` fetch and point at the right subfolder
for you — see that function's docstring for the `library=`/`kind=` options.
It refuses to hand you cards for a distro you don't have installed unless you
pass `library="all"` explicitly.

## Compatibility

`pyproject.toml` has an extra per distro (`psyscan-library[psychscanner]` or
`psyscan-library[primal]`) rather than a single dependency — the two packages
install as the same `psychscanner` import name, so they can't be
co-installed. Cards aren't guaranteed to run against older releases than the
pinned minimum for their distro.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
