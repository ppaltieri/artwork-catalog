import pytest

from artwork_catalog import edit_collection
from artwork_catalog.collection import Collection


@pytest.fixture
def collection():
    return Collection(
        "Paintings",
        ["artwork-1", "artwork-2"],
        "Landscape study",
        "collection-1",
    )

def test_edit_collection_then_save(monkeypatch, collection):
    entries = iter([1, 3])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))
    monkeypatch.setattr(
        edit_collection,
        "get_required_input",
        lambda _, commands=False: "New Paintings",
    )

    result = edit_collection.edit_collection(collection)

    assert collection.name == "Paintings"
    assert collection.description == "Landscape study"

    assert result is not None
    assert result.name == "New Paintings"
    assert result.description == "Landscape study"


def test_edit_collection_empty_description_then_save(
        monkeypatch,
        collection,
    ):
    entries = iter([2, 3])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))
    monkeypatch.setattr(
        edit_collection,
        "get_input",
        lambda _, commands=False: "",
    )

    result = edit_collection.edit_collection(collection)

    assert result is not None
    assert result.description is None


def test_edit_collection_then_cancel(monkeypatch, collection):
    entries = iter([2, 4])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))
    monkeypatch.setattr(
        edit_collection,
        "get_input",
        lambda _, commands=False: "New landscape study",
    )

    result = edit_collection.edit_collection(collection)

    assert result is None
    assert collection.description == "Landscape study"


def test_edit_collection_bad_entries_then_cancel(monkeypatch, capsys, collection):
    entries = iter([0, 5, "abc", 4])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    result = edit_collection.edit_collection(collection)
    captured = capsys.readouterr()

    assert result is None
    assert captured.out.count("Invalid option.") == 3


