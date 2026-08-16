# Browsing cards

Every card in this repo is discoverable by `psychscanner.task_library()` /
`experiment_library()` — point `dirs=` at a checkout of `tasks/<distro>/` or
`experiments/<distro>/`.

## From a manual checkout

```bash
git clone https://github.com/saurabhr/psyscan-library.git
```

```python
from psychscanner import list_task_library, task_library

names = list_task_library(dirs="psyscan-library/tasks/psychscanner")
# ['example_survey']

card = task_library("example_survey", dirs="psyscan-library/tasks/psychscanner")
path = task_library("example_survey", format="path", dirs="psyscan-library/tasks/psychscanner")
```

For `primal` cards, point at `tasks/primal/` instead — and use the `primal`
distribution's `task_library()` (it has no `experiment_library`).

## Without a manual checkout: `download_lib()`

`psychscanner.download_lib()` clones/updates this repo into a shared cache
directory and hands back the paths above directly — see
[`download_lib()`](download_lib.md).

```python
from psychscanner import download_lib, task_library

paths = download_lib()  # library="psychscanner" (whichever distro you have installed)
card = task_library("example_survey", dirs=paths["tasks"])
```

## Run a card end-to-end

```python
from pathlib import Path
import tempfile

from psychscanner import ExpCard, ExpCardInit, ScannerModel, task_library

task_path = task_library("example_survey", format="path", dirs="psyscan-library/tasks/psychscanner")

proj_dir = Path(tempfile.mkdtemp(prefix="psyscan_library_docs_"))
card = ExpCardInit(
    model="mock-chat-model",
    family="mock-llm",
    projectname="psyscan_library_docs",
    proj_dir=proj_dir,
    cogtype="no",
    nsim=1,
    memory="SingleTurn",
    task_file=task_path,
)
scanner = ScannerModel(expcard=ExpCard(card))
results = scanner.run()
```

`mock-llm`/`mock-chat-model` need no API key and make no network calls —
this is exactly what `scripts/validate_contribution.py` runs against every
card before it's merged (see [Contributing a card](contributing.md)).
