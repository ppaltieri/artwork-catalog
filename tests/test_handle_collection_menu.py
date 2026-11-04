import pytest

from artwork_catalog.collection import Collection
from artwork_catalog import handle_collection_menu
from artwork_catalog.input_funcs import ExitInput


@pytest.fixture
def collection():
    return Collection(
        name="Collection 1",
        artwork_ids=[],
        description=None,
        id="collection-1",
    )

@pytest.fixture
def collections():
    return [
        Collection(
            name="Paintings",
            artwork_ids=[],
            description=None,
            id="collection-1",
        ),
        Collection(
            name="Ceramics",
            artwork_ids=[],
            description=None,
            id="collection-2",
        )
    ]


def test_handle_collection_menu_create_collection(monkeypatch, collection):
    entries = iter([1, 4])
    collections_list = []
    saved = []

    def fake_save_collection(seen):
        saved.append(seen)

    monkeypatch.setattr(
        handle_collection_menu,
        "load_collections",
        lambda: collections_list,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "collections_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "create_collection",
        lambda: collection,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "save_collection",
        fake_save_collection,
    )

    handle_collection_menu.handle_collection_menu()

    assert saved == [collection]
    assert collections_list == [collection]


def test_handle_collection_menu_create_exit_input(monkeypatch):
    entries = iter([1, 4])
    collections_list = []
    saved = []

    def fake_create_collection():
        raise ExitInput

    def fake_save_collection(collection):
        saved.append(collection)

    monkeypatch.setattr(
        handle_collection_menu,
        "load_collections",
        lambda: collections_list,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "collections_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "create_collection",
        fake_create_collection,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "save_collection",
        fake_save_collection,
    )

    handle_collection_menu.handle_collection_menu()

    assert collections_list == []
    assert saved == []


def test_handle_collection_menu_browse_no_list(monkeypatch, capsys):
    entries = iter([2, 4])
    collections_list = []

    monkeypatch.setattr(
        handle_collection_menu,
        "load_collections",
        lambda: collections_list,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "collections_menu",
        lambda: next(entries),
    )

    handle_collection_menu.handle_collection_menu()

    captured = capsys.readouterr()

    assert "- No collections found." in captured.out


def test_handle_collection_menu_browse_select_is_none(
        monkeypatch,
        collections,
    ):
    entries = iter([2, 4])
    seen_collections = []
    load_calls = []

    def fake_load_collections():
        load_calls.append(1)
        return collections

    def fake_select_collection(collections_list):
        seen_collections.append(collections_list)
        return None

    monkeypatch.setattr(
        handle_collection_menu,
        "load_collections",
        fake_load_collections,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "collections_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "select_collection",
        fake_select_collection,
    )

    handle_collection_menu.handle_collection_menu()

    assert seen_collections == [collections]
    assert len(load_calls) == 1


def test_handle_collection_menu_browse_selected(
        monkeypatch,
        collections,
):
    entries = iter([2, 4])
    selections = iter([collections[0], None])

    handled = []
    load_calls = []

    def fake_load_collections():
        load_calls.append(1)
        return collections

    def fake_select_collection(_):
        return next(selections)

    def fake_handle_selected_collection(collection):
        handled.append(collection)

    monkeypatch.setattr(
        handle_collection_menu,
        "load_collections",
        fake_load_collections,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "collections_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "select_collection",
        fake_select_collection,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "handle_selected_collection",
        fake_handle_selected_collection,
    )

    handle_collection_menu.handle_collection_menu()

    assert handled == [collections[0]]
    assert len(load_calls) == 2


def test_handle_collection_menu_search_no_results(
        monkeypatch,
        capsys,
    ):
    entries = iter([3, 4])

    monkeypatch.setattr(
        handle_collection_menu,
        "load_collections",
        lambda: [],
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "collections_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "paintings",
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "search_collection_name",
        lambda _: [],
    )

    handle_collection_menu.handle_collection_menu()

    captured = capsys.readouterr()

    assert '- No collections found for "paintings".' in captured.out


def test_handle_collection_menu_search_one_result(
        monkeypatch,
        collections,
    ):
    entries = iter([3, 4])
    handled = []
    load_calls = []

    def fake_load_collections():
        load_calls.append(1)
        return collections

    def fake_handle_selected_collection(collection):
        handled.append(collection)

    monkeypatch.setattr(
        handle_collection_menu,
        "load_collections",
        fake_load_collections,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "collections_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "paintings",
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "search_collection_name",
        lambda _: [collections[0]],
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "handle_selected_collection",
        fake_handle_selected_collection,
    )

    handle_collection_menu.handle_collection_menu()

    assert handled == [collections[0]]
    assert len(load_calls) == 2


def test_handle_collection_menu_search_multiple_select_none(
        monkeypatch,
        collections,
    ):
    entries = iter([3, 4])
    seen_results = []
    load_calls = []

    def fake_load_collections():
        load_calls.append(1)
        return collections

    def fake_select_collection(results):
        seen_results.append(results)
        return None

    monkeypatch.setattr(
        handle_collection_menu,
        "load_collections",
        fake_load_collections,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "collections_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "paintings",
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "search_collection_name",
        lambda _: collections,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "select_collection",
        fake_select_collection,
    )

    handle_collection_menu.handle_collection_menu()

    assert seen_results == [collections]
    assert len(load_calls) == 1


def test_handle_collection_menu_search_multiple_select_collection(
        monkeypatch,
        collections,
    ):
    entries = iter([3, 4])
    selections = iter([collections[0], None])

    handled = []
    load_calls = []
    search_calls = []

    def fake_load_collections():
        load_calls.append(1)
        return collections

    def fake_search_collection_name(search_entry):
        search_calls.append(search_entry)
        return collections

    def fake_select_collection(_):
        return next(selections)

    def fake_handle_selected_collection(collection):
        handled.append(collection)

    monkeypatch.setattr(
        handle_collection_menu,
        "load_collections",
        fake_load_collections,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "collections_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "paintings",
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "search_collection_name",
        fake_search_collection_name,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "select_collection",
        fake_select_collection,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "handle_selected_collection",
        fake_handle_selected_collection,
    )

    handle_collection_menu.handle_collection_menu()

    assert handled == [collections[0]]
    assert len(load_calls) == 2
    assert search_calls == ["paintings", "paintings"]


def test_handle_collection_menu_search_multiple_results_become_empty(
        monkeypatch,
        collections,
        capsys,
    ):
    entries = iter([3, 4])
    search_results = iter([collections, []])

    handled = []
    load_calls = []

    def fake_load_collections():
        load_calls.append(1)
        return collections

    def fake_search_collection_name(_):
        return next(search_results)

    def fake_handle_selected_collection(collection):
        handled.append(collection)

    monkeypatch.setattr(
        handle_collection_menu,
        "load_collections",
        fake_load_collections,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "collections_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "paintings",
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "search_collection_name",
        fake_search_collection_name,
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "select_collection",
        lambda _: collections[0],
    )
    monkeypatch.setattr(
        handle_collection_menu,
        "handle_selected_collection",
        fake_handle_selected_collection,
    )

    handle_collection_menu.handle_collection_menu()

    captured = capsys.readouterr()

    assert handled == [collections[0]]
    assert len(load_calls) == 2
    assert '- No collections found for "paintings".' in captured.out