#!/usr/bin/env python3
"""Validate a contributed task or experiment card before it's merged.

Three gates, in order — first failure wins:
  1. structure  — required keys are present and well-typed
  2. dedup      — not a filename/content duplicate of an existing card (index_ledger)
  3. executes   — the card actually runs end-to-end against psychscanner's built-in
                  mock LLM (no API key needed). This is the "only take tasks that
                  will run" gate — a card that raises here does not get merged.

Usage:
    python scripts/validate_contribution.py tasks/my_task.json
    python scripts/validate_contribution.py experiments/my_experiment.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from index_ledger import _load_ledger, find_duplicates  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent


def validate_task_structure(card: dict) -> list[str]:
    errors = []
    if not card.get("taskname"):
        errors.append("missing required key: 'taskname'")
    items = card.get("items")
    if not isinstance(items, dict) or not items:
        errors.append("missing/empty required key: 'items' (must be a non-empty dict)")
        return errors
    for group, trials in items.items():
        trial_list = trials if isinstance(trials, list) else [trials]
        for trial in trial_list:
            if not isinstance(trial, dict):
                errors.append(f"items['{group}']: trial is not an object")
                continue
            if "trcode" not in trial:
                errors.append(f"items['{group}']: trial missing 'trcode'")
            if "stimulus" not in trial and "hmsg" not in trial:
                errors.append(f"items['{group}']: trial missing 'stimulus' (or 'hmsg')")
    return errors


def validate_experiment_structure(card: dict) -> list[str]:
    errors = []
    if not card.get("task_file"):
        errors.append("missing required key: 'task_file' (embedded task card dict)")
    return errors


def validate_runs(path: Path, card: dict) -> list[str]:
    """Actually execute the card end-to-end against the mock LLM. Import is lazy so
    structural/dedup checks still work without psychscanner installed."""
    try:
        from psychscanner import ExpCard, ExpCardInit, ScannerModel
    except ImportError as exc:
        return [f"could not import psychscanner to execute the card: {exc}"]

    is_experiment = path.resolve().relative_to(REPO_ROOT).parts[0] == "experiments"
    task_file = card.get("task_file") if is_experiment else card

    try:
        card_in = ExpCardInit(
            task_file=task_file,
            cogtype="no",
            nsim=1,
            model="mock-chat-model",
            family="mock-llm",
        )
        exp = ExpCard(card_in)
        scanner = ScannerModel(expcard=exp)
        scanner.run()
    except Exception as exc:  # noqa: BLE001 - any failure here means "does not run"
        return [f"card did not run against the mock LLM: {type(exc).__name__}: {exc}"]
    return []


def validate_contribution(path: Path) -> list[str]:
    errors = []

    try:
        card = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]

    is_experiment = path.resolve().relative_to(REPO_ROOT).parts[0] == "experiments"
    errors += validate_experiment_structure(card) if is_experiment else validate_task_structure(card)
    if errors:
        return errors  # don't bother running/deduping a structurally broken card

    errors += find_duplicates(path, _load_ledger())
    if errors:
        return errors  # don't execute a duplicate

    errors += validate_runs(path, card)
    return errors


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print(__doc__)
        return 2

    overall_ok = True
    for arg in argv:
        path = Path(arg)
        errors = validate_contribution(path)
        if errors:
            overall_ok = False
            print(f"FAIL: {path}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"PASS: {path}")

    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
