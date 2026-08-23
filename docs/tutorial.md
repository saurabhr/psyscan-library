# Tutorial: running a card from this index

Walks through loading one card and running it with `psychscanner`, from a
mock-LLM sanity check to a real model call, then gives a quick-reference for
every card currently in this repo. Uses `bfi44` (a 44-item personality
survey, `tasks/psychscanner/bfi44.json`) as the running example, but every
step works the same for any card here.

## 1. Install

```bash
git clone https://github.com/saurabhr/psyscan-library.git
cd psyscan-library
pip install -e ".[psychscanner]"   # or ".[primal]" for tasks/primal/ cards — never both
```

## 2. Find a card

```python
from psychscanner import list_task_library

list_task_library(dirs="tasks/psychscanner")
# ['bfi44', 'cognitive_rl_bandit', 'example_survey', 'pal50',
#  'prospect_theory_demo', 'vlm_shapes_demo', 'vviq16']
```

## 3. Sanity-check it against the mock LLM

No API key needed — `run_card` defaults to `psychscanner`'s built-in mock
model, the same gate every card here already passed in CI (see
[Contributing a card](contributing.md)):

```python
from psychscanner import run_card

results = run_card("bfi44", dirs="tasks/psychscanner")
```

If this raises, something's wrong with the card (open an issue) — every
card under `tasks/` and `experiments/` is expected to run.

## 4. Run it against a real model

Swap `model`/`family` for a real provider (see `psychscanner`'s
[PsychScanner Workflow guide](https://github.com/saurabhr/psychscanner/blob/main/docs/guides/psychscanner_workflow.md)
for the full list of supported families):

```python
results = run_card(
    "bfi44",
    dirs="tasks/psychscanner",
    model="gpt-4o-mini",
    family="openai",
    nsim=10,          # 10 simulated participants
)
```

## 5. Every card in this repo, one-liner run

Each card below was actually executed via `run_card()` against the mock LLM
when this tutorial was written — not just structurally validated — to
confirm the documented usage pattern really works for every one, not only
the running example above.

### `tasks/psychscanner/` (`pip install -e ".[psychscanner]"`)

| Card | What it is | Run it |
|---|---|---|
| `example_survey` | Seed/bootstrap card | `run_card("example_survey", dirs="tasks/psychscanner")` |
| `bfi44` | Big Five personality survey (44 items) | `run_card("bfi44", dirs="tasks/psychscanner")` |
| `vviq16` | Vividness of Visual Imagery Questionnaire (16 items) | `run_card("vviq16", dirs="tasks/psychscanner")` |
| `pal50` | Paired-associate learning, study + structured-recall phases | `run_card("pal50", dirs="tasks/psychscanner")` |
| `cognitive_rl_bandit` | 3-armed bandit, reward-scored | `run_card("cognitive_rl_bandit", dirs="tasks/psychscanner")` |
| `prospect_theory_demo` | Gain/loss gamble choices, ground-truth-scored | `run_card("prospect_theory_demo", dirs="tasks/psychscanner")` |
| `vlm_shapes_demo` | Multimodal shape/colour naming (6 embedded images) | `run_card("vlm_shapes_demo", dirs="tasks/psychscanner")` |

### `tasks/primal/` (`pip install -e ".[primal]"` instead — different install, not both)

| Card | What it is | Run it |
|---|---|---|
| `rm_singleturn_demo` | Seed/bootstrap card | `run_card("rm_singleturn_demo", dirs="tasks/primal")` |
| `introspection_weights_demo` | Multi-attribute 2AFC choice, decision-only subset with real per-trial ground truth | `run_card("introspection_weights_demo", dirs="tasks/primal")` |

`pal50`, `cognitive_rl_bandit`, and `vlm_shapes_demo` all use structured
per-trial parsing or multimodal content — if a future contribution of that
kind fails against the mock LLM with `NotImplementedError:
with_structured_output is not implemented for this model`, that's a
`psychscanner` mock-model gap, not your card; see the fix in
`psychscanner/src/psychscanner/memories/base/mock_llm.py` for reference.

## 6. Reading a trial

Open any card's JSON directly to see what a trial looks like before running
anything — e.g. `tasks/psychscanner/vviq16.json`'s first trial:

```json
{
  "trcode": "S1_1",
  "stimulus": "The exact contour of face, head, shoulders and body."
}
```

Multimodal cards (`vlm_shapes_demo`) embed images as base64 directly in
`stimulus` — see [Contributing a card](contributing.md#what-makes-a-good-card)
for size guidance before adding your own.
