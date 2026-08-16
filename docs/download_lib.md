# `download_lib()`

Both `psychscanner` and `psychscanner-primal` ship `download_lib()`, which
clones (or updates) this repo into a shared cache directory
(`~/.cache/psychscanner/psyscan-library` by default) and returns paths ready
to pass straight to `task_library(dirs=...)` / `experiment_library(dirs=...)`.

```python
from psychscanner import download_lib, task_library

paths = download_lib()               # library="psychscanner", kind="both"
# {"tasks": PosixPath(".../tasks/psychscanner"),
#  "experiments": PosixPath(".../experiments/psychscanner")}

card = task_library("example_survey", dirs=paths["tasks"])
```

## Parameters

- **`library`** — `"psychscanner"` (default on the full package), `"primal"`
  (default on `psychscanner-primal`), or `"all"`.
- **`kind`** — `"tasks"`, `"experiments"`, or `"both"` (default). Full
  `psychscanner` only — `psychscanner-primal`'s `download_lib()` has no
  `kind` parameter, since primal has no experiment cards at all.
- **`dest`** — override the cache directory.
- **`ref`** — branch/tag to check out (default `"main"`).

## The distro check

Cards aren't portable between `psychscanner` and `primal` — see
[the index page](index.md#compatibility). `download_lib()` checks which
package is actually installed (via `importlib.metadata`) and refuses a
mismatched `library=` request:

```python
>>> download_lib(library="primal")  # psychscanner installed, not primal
RuntimeError: library='primal' but the installed package is 'psychscanner' --
'primal' cards aren't guaranteed to run here. Install the matching package,
or pass library='all' to fetch both anyway.
```

Pass `library="all"` to opt out of that check — useful for browsing both
distros' cards, or a CI job that validates both. `primal`'s `download_lib()`
also lets you fetch the other distro's cards with `library="psychscanner"`
for inspection/porting, even though it can't run them locally.

## Caching

Repeat calls reuse the cache directory and just `git fetch` + `reset --hard`
rather than re-cloning. If you need an isolated checkout (e.g. pinned to a
specific `ref` per test run), pass `dest=` explicitly.
