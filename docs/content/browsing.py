import marimo

__generated_with = "0.23.2"
app = marimo.App()


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Browse the index

        Every card in this repo is discoverable by `psychscanner.task_library()`
        / `experiment_library()` — point `dirs=` at a checkout of `tasks/` or
        `experiments/`. This page runs for real at build time against the
        built-in `mock-llm` (no API key, no network).
        """
    )
    return


@app.cell
def _():
    from pathlib import Path

    from psychscanner import list_task_library

    tasks_dir = Path(__file__).resolve().parents[2] / "tasks"
    names = list_task_library(dirs=str(tasks_dir))
    names
    return Path, list_task_library, names, tasks_dir


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Run one card end-to-end""")
    return


@app.cell
def _(Path, names, tasks_dir):
    import tempfile

    from psychscanner import ExpCard, ExpCardInit, ScannerModel, task_library

    first_card = names[0]
    task_path = task_library(first_card, format="path", dirs=str(tasks_dir))

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
    first_card, results
    return (
        ExpCard,
        ExpCardInit,
        ScannerModel,
        card,
        first_card,
        proj_dir,
        results,
        scanner,
        task_path,
        tempfile,
    )


if __name__ == "__main__":
    app.run()
