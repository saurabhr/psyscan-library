#!/usr/bin/env python3
"""Index ledger: tracks every tasks/ and experiments/ card and flags duplicates.

INDEX_LEDGER.json is derived, not hand-edited. Regenerate it after adding or
removing a card, and commit the update as part of the PR:

    python scripts/index_ledger.py build

Check a candidate card against the ledger before opening a PR — flags a
filename already taken, or content byte-identical to an existing card under a
different name:

    python scripts/index_ledger.py check tasks/my_new_task.json
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = REPO_ROOT / "INDEX_LEDGER.json"
CARD_GLOBS = ["tasks/*.json", "tasks/*.tcard.psyscan", "experiments/*.json", "experiments/*.xcard.psyscan"]


def _content_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _all_cards() -> list[Path]:
    cards: list[Path] = []
    for pattern in CARD_GLOBS:
        cards.extend(REPO_ROOT.glob(pattern))
    return sorted(set(cards))


def build_ledger() -> dict[str, dict]:
    """Scan tasks/ and experiments/ and return {relative_path: {kind, content_hash}}."""
    ledger = {}
    for card in _all_cards():
        rel = str(card.relative_to(REPO_ROOT))
        ledger[rel] = {
            "kind": "task" if rel.startswith("tasks/") else "experiment",
            "content_hash": _content_hash(card),
        }
    return ledger


def find_duplicates(candidate: Path, ledger: dict[str, dict]) -> list[str]:
    """Return warnings if `candidate` collides by filename or content with a ledger entry."""
    warnings = []
    candidate_rel = str(candidate.resolve().relative_to(REPO_ROOT))
    candidate_hash = _content_hash(candidate)

    for existing_rel, entry in ledger.items():
        if existing_rel == candidate_rel:
            continue  # candidate is this ledger entry itself
        if Path(existing_rel).name == candidate.name:
            warnings.append(f"filename '{candidate.name}' is already used by {existing_rel}")
        if candidate_hash == entry["content_hash"]:
            warnings.append(f"content is byte-identical to existing card {existing_rel}")

    return warnings


def _load_ledger() -> dict[str, dict]:
    # Always rebuild from the current tasks/+experiments/ contents rather
    # than reading the committed INDEX_LEDGER.json snapshot. A PR can add
    # two new, not-yet-ledgered cards in the same commit; a duplicate
    # between them is invisible to a check that only looks at the
    # committed ledger, since neither candidate is in it yet. A fresh scan
    # sees both, whether they're being checked in one invocation or two.
    return build_ledger()


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print(__doc__)
        return 2

    cmd, *rest = argv

    if cmd == "build":
        ledger = build_ledger()
        LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Wrote {len(ledger)} entries to {LEDGER_PATH}")
        return 0

    if cmd == "check":
        if not rest:
            print("usage: index_ledger.py check <card-file>")
            return 2
        candidate = Path(rest[0])
        warnings = find_duplicates(candidate, _load_ledger())
        if warnings:
            print(f"DUPLICATE: {candidate} conflicts with existing card(s):")
            for w in warnings:
                print(f"  - {w}")
            return 1
        print(f"OK: {candidate} is not a duplicate of any ledgered card.")
        return 0

    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
