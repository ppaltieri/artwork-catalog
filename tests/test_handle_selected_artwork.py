from copy import deepcopy
import pytest

from artwork_catalog.artwork import Artwork
from artwork_catalog.dimensions import Dimensions
from artwork_catalog import handle_selected_artwork


@pytest.fixture
def artwork():
    dimensions = Dimensions(
        21,
        29,
        None,
        "cm",
    )
    
    return Artwork(
        "painting.jpg",
        "Test",
        2026,
        "Watercolor on paper",
        "wet-on-wet",
        "paint, paper",
        dimensions,
        None,
        id="artwork-1"
    )


def test_handle_selected_artwork_view_details(monkeypatch, capsys, artwork):
    entries = iter([1, 7])
    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )

    handle_selected_artwork.handle_selected_artwork(artwork)
    captured = capsys.readouterr()

    assert captured.out.count(f"{artwork.title}, {artwork.year}") == 2
    assert artwork.details() in captured.out


def test_handle_selected_artwork_edit_none(monkeypatch, artwork):
    entries = iter([2, 7])
    seen_by_edit = []
    updated = []

    def fake_edit_artwork(selected):
        seen_by_edit.append(selected)
        return None

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "edit_artwork",
        fake_edit_artwork,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "update_artwork",
        lambda old, new: updated.append((old, new)),
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)

    assert seen_by_edit == [artwork]
    assert updated == []
    assert result is None


def test_handle_selected_artwork_edit(monkeypatch, capsys, artwork):
    entries = iter([2, 7])
    edited_artwork = deepcopy(artwork)
    edited_artwork.title = "New Title"
    updated = []

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "edit_artwork",
        lambda _: edited_artwork,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "update_artwork",
        lambda old, new: updated.append((old, new)),
    )

    handle_selected_artwork.handle_selected_artwork(artwork)
    captured = capsys.readouterr()

    assert updated == [(artwork, edited_artwork)]
    assert f"{artwork.title}, {artwork.year}" in captured.out
    assert f"{edited_artwork.title}, {edited_artwork.year}" in captured.out


def test_handle_selected_artwork_delete_yes(monkeypatch, capsys, artwork):
    calls = []

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: 6,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "delete_artwork_confirmation",
        lambda: 1,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "remove_artwork_from_all_collections",
        lambda selected: calls.append(("remove", selected)),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "delete_artwork",
        lambda selected: calls.append(("delete", selected)),
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)
    captured = capsys.readouterr()

    assert captured.out.count(f"{artwork.title}, {artwork.year}") == 1
    assert calls == [
        ("remove", artwork),
        ("delete", artwork),
    ]
    assert result is None


def test_handle_selected_artwork_delete_no(monkeypatch, capsys, artwork):
    entries = iter([6, 7])
    calls = []

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "delete_artwork_confirmation",
        lambda: 2,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "remove_artwork_from_all_collections",
        lambda selected: calls.append(("remove", selected)),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "delete_artwork",
        lambda selected: calls.append(("delete", selected)),
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)
    captured = capsys.readouterr()

    assert captured.out.count(f"{artwork.title}, {artwork.year}") == 2
    assert calls == []
    assert result is None


def test_handle_selected_artwork_add_no_collections_create(
    monkeypatch, artwork
):
    entries = iter([3, 7])
    new_collection = object()
    calls = []

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "load_collections",
        lambda: [],
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "add_to_collection_menu",
        lambda options: 1,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "create_collection",
        lambda: new_collection,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "save_collection",
        lambda collection: calls.append(("save", collection)),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "add_artwork_to_collection",
        lambda collection, selected: calls.append(
            ("add", collection, selected)
        ),
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)

    assert calls == [
        ("save", new_collection),
        ("add", new_collection, artwork),
    ]
    assert result is None


def test_handle_selected_artwork_add_no_collections_exit(
    monkeypatch, artwork
):
    entries = iter([3, 7])
    calls = []

    def fake_create_collection():
        raise handle_selected_artwork.ExitInput

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "load_collections",
        lambda: [],
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "add_to_collection_menu",
        lambda options: 1,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "create_collection",
        fake_create_collection,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "save_collection",
        lambda collection: calls.append(collection),
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)

    assert calls == []
    assert result is None


def test_handle_selected_artwork_add_no_collections_back(
    monkeypatch, capsys, artwork
):
    entries = iter([3, 7])
    options_seen = []

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "load_collections",
        lambda: [],
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "add_to_collection_menu",
        lambda options: options_seen.append(options) or 2,
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)
    captured = capsys.readouterr()

    assert "- No collections found." in captured.out
    assert options_seen == [
        ["Create collection and add this artwork", "Back"]
    ]
    assert result is None


def test_handle_selected_artwork_add_existing(monkeypatch, artwork):
    entries = iter([3, 7])
    collection = object()
    collections_list = [collection]
    calls = []

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "load_collections",
        lambda: collections_list,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "add_to_collection_menu",
        lambda options: 1,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "select_collection",
        lambda collections: calls.append(("select", collections))
        or collection,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "add_artwork_to_collection",
        lambda selected_collection, selected: calls.append(
            ("add", selected_collection, selected)
        ) or True,
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)

    assert calls == [
        ("select", collections_list),
        ("add", collection, artwork),
    ]
    assert result is None


def test_handle_selected_artwork_add_existing_none(
    monkeypatch, artwork
):
    entries = iter([3, 7])
    collection = object()
    calls = []

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "load_collections",
        lambda: [collection],
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "add_to_collection_menu",
        lambda options: 1,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "select_collection",
        lambda collections: None,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "add_artwork_to_collection",
        lambda collection, selected: calls.append(
            (collection, selected)
        ),
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)

    assert calls == []
    assert result is None


def test_handle_selected_artwork_add_duplicate(
    monkeypatch, capsys, artwork
):
    entries = iter([3, 7])
    collection = object()
    calls = []

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "load_collections",
        lambda: [collection],
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "add_to_collection_menu",
        lambda options: 1,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "select_collection",
        lambda collections: collection,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "add_artwork_to_collection",
        lambda selected_collection, selected: calls.append(
            (selected_collection, selected)
        ) or None,
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)
    captured = capsys.readouterr()

    assert calls == [(collection, artwork)]
    assert "Artwork already in collection." in captured.out
    assert result is None


def test_handle_selected_artwork_add_new_collection(
    monkeypatch, artwork
):
    entries = iter([3, 7])
    existing_collection = object()
    new_collection = object()
    calls = []

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "load_collections",
        lambda: [existing_collection],
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "add_to_collection_menu",
        lambda options: 2,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "create_collection",
        lambda: new_collection,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "save_collection",
        lambda collection: calls.append(("save", collection)),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "add_artwork_to_collection",
        lambda collection, selected: calls.append(
            ("add", collection, selected)
        ),
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)

    assert calls == [
        ("save", new_collection),
        ("add", new_collection, artwork),
    ]
    assert result is None


def test_handle_selected_artwork_add_new_collection_exit(
    monkeypatch, artwork
):
    entries = iter([3, 7])
    collection = object()
    calls = []

    def fake_create_collection():
        raise handle_selected_artwork.ExitInput

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "load_collections",
        lambda: [collection],
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "add_to_collection_menu",
        lambda options: 2,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "create_collection",
        fake_create_collection,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "save_collection",
        lambda collection: calls.append(collection),
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)

    assert calls == []
    assert result is None


def test_handle_selected_artwork_add_existing_back(
    monkeypatch, artwork
):
    entries = iter([3, 7])
    collection = object()
    options_seen = []

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "load_collections",
        lambda: [collection],
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "add_to_collection_menu",
        lambda options: options_seen.append(options) or 3,
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)

    assert options_seen == [
        [
            "Select existing collection",
            "Create new collection",
            "Back",
        ]
    ]
    assert result is None


def test_handle_selected_artwork_remove_none(monkeypatch, artwork):
    entries = iter([4, 7])
    calls = []

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "select_collection_with_artwork",
        lambda selected: calls.append(("select", selected)) or None,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "remove_from_collection_confirmation",
        lambda collection, selected: calls.append(("confirm",)),
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)

    assert calls == [("select", artwork)]
    assert result is None


def test_handle_selected_artwork_remove_yes(monkeypatch, artwork):
    entries = iter([4, 7])
    collection = object()
    calls = []

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "select_collection_with_artwork",
        lambda selected: collection,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "remove_from_collection_confirmation",
        lambda selected_collection, selected: calls.append(
            ("confirm", selected_collection, selected)
        ) or 1,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "remove_artwork_from_collection",
        lambda selected_collection, selected: calls.append(
            ("remove", selected_collection, selected)
        ),
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)

    assert calls == [
        ("confirm", collection, artwork),
        ("remove", collection, artwork),
    ]
    assert result is None


def test_handle_selected_artwork_remove_no(monkeypatch, artwork):
    entries = iter([4, 7])
    collection = object()
    calls = []

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "select_collection_with_artwork",
        lambda selected: collection,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "remove_from_collection_confirmation",
        lambda selected_collection, selected: 2,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "remove_artwork_from_collection",
        lambda selected_collection, selected: calls.append(
            (selected_collection, selected)
        ),
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)

    assert calls == []
    assert result is None


def test_handle_selected_artwork_export(monkeypatch, artwork):
    entries = iter([5, 7])
    calls = []
    output_path = "test_artwork.pdf"

    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "get_required_input",
        lambda prompt, commands: calls.append(
            ("input", prompt, commands)
        ) or output_path,
    )
    monkeypatch.setattr(
        handle_selected_artwork,
        "export_artwork_pdf",
        lambda selected, path: calls.append(
            ("export", selected, path)
        ),
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)

    assert calls == [
        ("input", "Save as: ", False),
        ("export", artwork, output_path),
    ]
    assert result is None


def test_handle_selected_artwork_back(monkeypatch, artwork):
    monkeypatch.setattr(
        handle_selected_artwork,
        "selected_artwork_menu",
        lambda: 7,
    )

    result = handle_selected_artwork.handle_selected_artwork(artwork)

    assert result is None
