"""Smoke test for the validator itself — structure and dedup gates, no psychscanner needed."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from validate_contribution import validate_task_structure, validate_experiment_structure  # noqa: E402


def test_task_structure_requires_taskname_and_items():
    errors = validate_task_structure({})
    assert any("taskname" in e for e in errors)
    assert any("items" in e for e in errors)


def test_task_structure_requires_trcode_and_stimulus_per_trial():
    card = {"taskname": "t", "items": {"g1": [{}]}}
    errors = validate_task_structure(card)
    assert any("trcode" in e for e in errors)
    assert any("stimulus" in e for e in errors)


def test_task_structure_passes_on_valid_card():
    card = {"taskname": "t", "items": {"g1": [{"trcode": "g1_1", "stimulus": "hi"}]}}
    assert validate_task_structure(card) == []


def test_experiment_structure_requires_task_file():
    assert validate_experiment_structure({}) != []
    assert validate_experiment_structure({"task_file": {"taskname": "t", "items": {}}}) == []


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok  {name}")
