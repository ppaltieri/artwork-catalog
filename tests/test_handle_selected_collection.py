
from types import SimpleNamespace

import pytest

from artwork_catalog import handle_selected_collection


@pytest.fixture
def collection():
    return SimpleNamespace(
        name="Paintings",
        description="My paintings",
        artwork_ids=["artwork-1", "artwork-2"],
        id="collection-1",
    )


@pytest.fixture
def artworks():
    return [
        SimpleNamespace(
            id="artwork-1",
            title="Painting One",
            year=2025,
        ),
        SimpleNamespace(
            id="artwork-2",
            title="Painting Two",
            year=2026,
        ),
        SimpleNamespace(
            id="artwork-3",
            title="Painting Three",
            year=2024,
        ),
    ]


def test_handle_selected_collection_view(
    monkeypatch, capsys, collection, artworks
):
    entries = iter([1, 7])

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "load_artworks",
        lambda: artworks,
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )
    captured = capsys.readouterr()

    assert captured.out.count(collection.name) == 2
    assert collection.description in captured.out
    assert "Painting One, 2025" in captured.out
    assert "Painting Two, 2026" in captured.out
    assert "Painting Three, 2024" not in captured.out
    assert result is None


def test_handle_selected_collection_view_empty(
    monkeypatch, capsys, collection
):
    entries = iter([1, 7])
    collection.artwork_ids = []
    collection.description = None

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "load_artworks",
        lambda: [],
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )
    captured = capsys.readouterr()

    assert "Empty collection" in captured.out
    assert result is None


def test_handle_selected_collection_view_empty_description(
    monkeypatch, capsys, collection
):
    entries = iter([1, 7])
    collection.artwork_ids = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "load_artworks",
        lambda: [],
    )

    handle_selected_collection.handle_selected_collection(collection)
    captured = capsys.readouterr()

    assert collection.description in captured.out
    assert "Empty collection" in captured.out


def test_handle_selected_collection_edit_none(
    monkeypatch, collection
):
    entries = iter([2, 7])
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "edit_collection",
        lambda selected: calls.append(("edit", selected)) or None,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "update_collection",
        lambda old, new: calls.append(("update", old, new)),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )

    assert calls == [("edit", collection)]
    assert result is None


def test_handle_selected_collection_edit(
    monkeypatch, capsys, collection
):
    entries = iter([2, 7])
    edited_collection = SimpleNamespace(
        name="New Name",
        description="New description",
        artwork_ids=collection.artwork_ids.copy(),
        id=collection.id,
    )
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "edit_collection",
        lambda selected: edited_collection,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "update_collection",
        lambda old, new: calls.append((old, new)),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )
    captured = capsys.readouterr()

    assert calls == [(collection, edited_collection)]
    assert collection.name in captured.out
    assert edited_collection.name in captured.out
    assert result is None


def test_handle_selected_collection_add_no_artworks(
    monkeypatch, capsys, collection
):
    entries = iter([3, 7])
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "load_artworks",
        lambda: [],
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "select_multiple_artworks",
        lambda items: calls.append(("select", items)),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )
    captured = capsys.readouterr()

    assert "No artworks found." in captured.out
    assert calls == []
    assert result is None


def test_handle_selected_collection_add_none(
    monkeypatch, collection, artworks
):
    entries = iter([3, 7])
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "select_multiple_artworks",
        lambda items: calls.append(("select", items)) or None,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "add_multiple_artworks_to_collection",
        lambda selected, items: calls.append(("add", selected, items)),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )

    assert calls == [("select", artworks)]
    assert result is None


def test_handle_selected_collection_add_all_duplicates(
    monkeypatch, capsys, collection, artworks
):
    entries = iter([3, 7])
    selected_artworks = artworks[:2]
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "select_multiple_artworks",
        lambda items: selected_artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "add_multiple_artworks_to_collection",
        lambda selected, items: (
            calls.append((selected, items))
            or (collection, ["Painting One", "Painting Two"])
        ),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )
    captured = capsys.readouterr()

    assert calls == [(collection, selected_artworks)]
    assert "All selected artworks are already in this collection." in captured.out
    assert result is None


def test_handle_selected_collection_add_partial_duplicates(
    monkeypatch, capsys, collection, artworks
):
    entries = iter([3, 7])
    selected_artworks = [artworks[0], artworks[2]]
    edited_collection = SimpleNamespace(
        name="Updated Paintings",
        description=collection.description,
        artwork_ids=["artwork-1", "artwork-2", "artwork-3"],
        id=collection.id,
    )
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "select_multiple_artworks",
        lambda items: selected_artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "add_multiple_artworks_to_collection",
        lambda selected, items: (
            calls.append((selected, items))
            or (edited_collection, ["Painting One"])
        ),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )
    captured = capsys.readouterr()

    assert calls == [(collection, selected_artworks)]
    assert "Already in collection: Painting One" in captured.out
    assert edited_collection.name in captured.out
    assert result is None


def test_handle_selected_collection_add_success(
    monkeypatch, capsys, collection, artworks
):
    entries = iter([3, 7])
    selected_artworks = [artworks[2]]
    edited_collection = SimpleNamespace(
        name="Updated Paintings",
        description=collection.description,
        artwork_ids=["artwork-1", "artwork-2", "artwork-3"],
        id=collection.id,
    )
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "select_multiple_artworks",
        lambda items: selected_artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "add_multiple_artworks_to_collection",
        lambda selected, items: (
            calls.append((selected, items))
            or (edited_collection, [])
        ),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )
    captured = capsys.readouterr()

    assert calls == [(collection, selected_artworks)]
    assert "Already in collection:" not in captured.out
    assert edited_collection.name in captured.out
    assert result is None


def test_handle_selected_collection_remove_empty(
    monkeypatch, capsys, collection, artworks
):
    entries = iter([4, 7])
    collection.artwork_ids = []
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "select_multiple_artworks",
        lambda items: calls.append(("select", items)),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )
    captured = capsys.readouterr()

    assert "No artworks in this collection." in captured.out
    assert calls == []
    assert result is None


def test_handle_selected_collection_remove_none(
    monkeypatch, collection, artworks
):
    entries = iter([4, 7])
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "select_multiple_artworks",
        lambda items: calls.append(("select", items)) or None,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "remove_multiple_artworks_from_collection_confirmation",
        lambda selected: calls.append(("confirm", selected)),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )

    assert calls == [("select", artworks[:2])]
    assert result is None


def test_handle_selected_collection_remove_no(
    monkeypatch, collection, artworks
):
    entries = iter([4, 7])
    selected_artworks = [artworks[0]]
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "select_multiple_artworks",
        lambda items: selected_artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "remove_multiple_artworks_from_collection_confirmation",
        lambda selected: calls.append(("confirm", selected)) or 2,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "remove_multiple_artworks_from_collection",
        lambda selected, items: calls.append(("remove", selected, items)),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )

    assert calls == [("confirm", collection)]
    assert result is None


def test_handle_selected_collection_remove_yes(
    monkeypatch, capsys, collection, artworks
):
    entries = iter([4, 7])
    selected_artworks = [artworks[0]]
    edited_collection = SimpleNamespace(
        name="Updated Paintings",
        description=collection.description,
        artwork_ids=["artwork-2"],
        id=collection.id,
    )
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "select_multiple_artworks",
        lambda items: calls.append(("select", items))
        or selected_artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "remove_multiple_artworks_from_collection_confirmation",
        lambda selected: calls.append(("confirm", selected)) or 1,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "remove_multiple_artworks_from_collection",
        lambda selected, items: (
            calls.append(("remove", selected, items))
            or edited_collection
        ),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )
    captured = capsys.readouterr()

    assert calls == [
        ("select", artworks[:2]),
        ("confirm", collection),
        ("remove", collection, selected_artworks),
    ]
    assert edited_collection.name in captured.out
    assert result is None


def test_handle_selected_collection_export_empty(
    monkeypatch, capsys, collection, artworks
):
    entries = iter([5, 7])
    collection.artwork_ids = []
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "get_required_input",
        lambda prompt, commands: calls.append(("input",)),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "export_collection_pdf",
        lambda selected, items, path: calls.append(("export",)),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )
    captured = capsys.readouterr()

    assert "No artworks in this collection." in captured.out
    assert calls == []
    assert result is None


def test_handle_selected_collection_export(
    monkeypatch, collection, artworks
):
    entries = iter([5, 7])
    output_path = "paintings.pdf"
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "get_required_input",
        lambda prompt, commands: (
            calls.append(("input", prompt, commands))
            or output_path
        ),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "export_collection_pdf",
        lambda selected, items, path: calls.append(
            ("export", selected, items, path)
        ),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )

    assert calls == [
        ("input", "Save as: ", False),
        ("export", collection, artworks[:2], output_path),
    ]
    assert result is None


def test_handle_selected_collection_delete_yes(
    monkeypatch, capsys, collection
):
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: 6,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "delete_collection_confirmation",
        lambda: 1,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "delete_collection",
        lambda selected: calls.append(selected),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )
    captured = capsys.readouterr()

    assert captured.out.count(collection.name) == 1
    assert calls == [collection]
    assert result is None


def test_handle_selected_collection_delete_no(
    monkeypatch, capsys, collection
):
    entries = iter([6, 7])
    calls = []

    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "delete_collection_confirmation",
        lambda: 2,
    )
    monkeypatch.setattr(
        handle_selected_collection,
        "delete_collection",
        lambda selected: calls.append(selected),
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )
    captured = capsys.readouterr()

    assert captured.out.count(collection.name) == 2
    assert calls == []
    assert result is None


def test_handle_selected_collection_back(monkeypatch, collection):
    monkeypatch.setattr(
        handle_selected_collection,
        "selected_collection_menu",
        lambda: 7,
    )

    result = handle_selected_collection.handle_selected_collection(
        collection
    )

    assert result is None
