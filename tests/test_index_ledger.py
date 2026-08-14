"""Regression test: the dedup gate must catch duplicates within the same
batch/PR, not just against the already-committed INDEX_LEDGER.json.

_load_ledger() previously preferred the committed ledger snapshot over a
fresh scan, so two new, not-yet-ledgered cards with identical content (or
a filename collision) were each checked only against pre-existing entries
-- neither saw the other, so both passed.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import index_ledger  # noqa: E402


def _make_repo(tmp_path: Path, monkeypatch) -> Path:
    (tmp_path / "tasks").mkdir()
    (tmp_path / "experiments").mkdir()
    monkeypatch.setattr(index_ledger, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(index_ledger, "LEDGER_PATH", tmp_path / "INDEX_LEDGER.json")
    return tmp_path


def test_load_ledger_sees_new_sibling_files_not_yet_committed(tmp_path, monkeypatch):
    repo = _make_repo(tmp_path, monkeypatch)
    # Simulate a stale committed ledger with zero entries (as if these two
    # cards were both just added in the same PR, before `build` ran).
    (repo / "INDEX_LEDGER.json").write_text("{}", encoding="utf-8")

    card_a = repo / "tasks" / "a.json"
    card_b = repo / "tasks" / "b.json"
    card_a.write_text('{"taskname": "dup"}', encoding="utf-8")
    card_b.write_text('{"taskname": "dup"}', encoding="utf-8")  # byte-identical to a.json

    ledger = index_ledger._load_ledger()
    warnings_for_b = index_ledger.find_duplicates(card_b, ledger)

    assert any("byte-identical" in w for w in warnings_for_b), warnings_for_b


def test_load_ledger_still_catches_duplicates_against_committed_entries(tmp_path, monkeypatch):
    repo = _make_repo(tmp_path, monkeypatch)
    existing = repo / "tasks" / "existing.json"
    existing.write_text('{"taskname": "old"}', encoding="utf-8")
    index_ledger.LEDGER_PATH.write_text(
        '{"tasks/existing.json": {"kind": "task", "content_hash": "%s"}}'
        % index_ledger._content_hash(existing),
        encoding="utf-8",
    )

    new_card = repo / "tasks" / "new.json"
    new_card.write_text('{"taskname": "old"}', encoding="utf-8")  # same content as existing.json

    ledger = index_ledger._load_ledger()
    warnings = index_ledger.find_duplicates(new_card, ledger)
    assert any("byte-identical" in w for w in warnings), warnings


if __name__ == "__main__":
    import tempfile
    from types import SimpleNamespace

    class _MP:
        def setattr(self, obj, name, value):
            setattr(obj, name, value)

    with tempfile.TemporaryDirectory() as d:
        test_load_ledger_sees_new_sibling_files_not_yet_committed(Path(d), _MP())
    print("demo() OK")


def test_malformed_committed_ledger_does_not_crash(tmp_path, monkeypatch):
    """A hand-edited or corrupted INDEX_LEDGER.json used to crash with a raw
    JSONDecodeError/KeyError -- _load_ledger() no longer reads that file at
    all (see above), so a malformed one on disk can't affect the check."""
    repo = _make_repo(tmp_path, monkeypatch)
    (repo / "INDEX_LEDGER.json").write_text("{not valid json", encoding="utf-8")

    card = repo / "tasks" / "a.json"
    card.write_text('{"taskname": "x"}', encoding="utf-8")

    ledger = index_ledger._load_ledger()
    warnings = index_ledger.find_duplicates(card, ledger)
    assert warnings == []
