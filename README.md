# psyscan-library

![logo](docs/logo.png)

Public, versioned index of vetted task and experiment cards for
[psychscanner](https://github.com/saurabhr/psychscanner).

This repo is not the place to write library code — it's a curated data index.
Every card under `tasks/` and `experiments/` is a plain `psychscanner` task
card / experiment card (`.json`, `.tcard.psyscan`, `.xcard.psyscan`), and every
card here has been verified to actually load and run end-to-end against
`psychscanner`'s built-in mock LLM before being merged.

## Using a card

```python
from psychscanner import task_library, experiment_library

card = task_library("my_task", dirs="path/to/psyscan-library/tasks")
```

Point `dirs=` (or `PSYCHSCANNER_TASK_LIBRARY_DIRS` /
`PSYCHSCANNER_EXPERIMENT_LIBRARY_DIRS`) at a checkout of this repo's `tasks/`
or `experiments/` folder.

## Compatibility

`pyproject.toml` pins the `psychscanner` version this index was validated
against (`psychscanner>=0.5.0`). Cards aren't guaranteed to run against older
releases.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
