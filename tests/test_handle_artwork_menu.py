import pytest

from artwork_catalog.artwork import Artwork
from artwork_catalog import handle_artwork_menu
from artwork_catalog.input_funcs import ExitInput


@pytest.fixture
def artworks():
    dimensions = (29, 21)
    return [
        Artwork(
            "painting.jpg",
            "Test 1",
            2025,
            "Watercolor on paper",
            "wet-on-wet",
            "paint, paper",
            dimensions,
            None,
            "artwork-1",
        ),
        Artwork(
            "ceramics.jpg",
            "Test 2",
            2026,
            "Ceramics",
            "pinch pot",
            "clay",
            dimensions,
            None,
            "artwork-2",
        ),
    ]


@pytest.fixture
def artwork():
    dimensions = (29, 21)
    return Artwork(
        "sculpture.jpg",
        "Test 3",
        2020,
        "Sculpture in brass",
        "sculpture",
        "brass",
        dimensions,
        None,
        "artwork-3"
    )


def test_handle_artwork_menu_add_artwork(monkeypatch, artworks, artwork):
    saved = []
    entries = iter([1, 4])

    monkeypatch.setattr(
        handle_artwork_menu,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "artworks_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "create_artwork",
        lambda: artwork,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "save_artwork",
        lambda artwork: saved.append(artwork),
    )

    handle_artwork_menu.handle_artwork_menu()

    assert saved == [artwork]

    assert len(artworks) == 3
    assert artworks[0].id == "artwork-1"
    assert artworks[1].id == "artwork-2"
    assert artworks[2] == artwork


def test_handle_artwork_menu_exit_input(monkeypatch):
    artworks_list = []
    saved = []
    entries = iter([1, 4])
    def fake_create_artwork():
        raise ExitInput

    monkeypatch.setattr(
        handle_artwork_menu,
        "load_artworks",
        lambda: artworks_list,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "artworks_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "create_artwork",
        fake_create_artwork,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "save_artwork",
        lambda artwork: saved.append(artwork),
    )

    handle_artwork_menu.handle_artwork_menu()

    assert artworks_list == []
    assert saved == []


def test_handle_artwork_menu_browse_artworks_no_list(
        monkeypatch,
        capsys,
    ):
    entries = iter([2, 4])
    artworks_list = []
    monkeypatch.setattr(
        handle_artwork_menu,
        "load_artworks",
        lambda: artworks_list,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "artworks_menu",
        lambda: next(entries),
    )

    handle_artwork_menu.handle_artwork_menu()
    captured = capsys.readouterr()

    assert "- No artworks found." in captured.out


def test_handle_artwork_menu_browse_artworks_none(monkeypatch, artworks):
    entries = iter([2, 4])
    selected = []
    monkeypatch.setattr(
        handle_artwork_menu,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "artworks_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "select_artwork",
        lambda _: None,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "handle_selected_artwork",
        lambda artwork: selected.append(artwork),
    )
    
    handle_artwork_menu.handle_artwork_menu()

    assert selected == []


def test_handle_artwork_menu_browse_artworks_selected(
        monkeypatch,
        artworks,
    ):
    entries = iter([2, 4])
    selections = iter([artworks[0], None])
    selected_calls = []
    load_calls = []

    def fake_load_artworks():
        load_calls.append(True)
        return artworks

    monkeypatch.setattr(
        handle_artwork_menu,
        "load_artworks",
        fake_load_artworks,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "artworks_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "select_artwork",
        lambda _: next(selections),
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "handle_selected_artwork",
        lambda artwork: selected_calls.append(artwork),
    )

    handle_artwork_menu.handle_artwork_menu()

    assert selected_calls == [artworks[0]]
    assert len(load_calls) == 2


def test_handle_artwork_menu_search_no_result(
        monkeypatch,
        capsys,
        artworks,
    ):
    entries = iter([3, 4])
    monkeypatch.setattr(
        handle_artwork_menu,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "artworks_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "abc",
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "search_artwork_title",
        lambda _: []
    )

    handle_artwork_menu.handle_artwork_menu()
    captured = capsys.readouterr()

    assert '- No artworks found for "abc".' in captured.out


def test_handle_artwork_menu_search_one_result(
        monkeypatch,
        artworks,
):
    entries = iter([3, 4])
    loaded_calls = []
    selected_calls = []

    def fake_load_artworks():
        loaded_calls.append("called")
        return artworks

    monkeypatch.setattr(
        handle_artwork_menu,
        "load_artworks",
        fake_load_artworks,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "artworks_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1"
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "search_artwork_title",
        lambda _: [artworks[0]]
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "handle_selected_artwork",
        lambda artwork: selected_calls.append(artwork)
    )

    handle_artwork_menu.handle_artwork_menu()

    assert selected_calls == [artworks[0]]
    assert len(loaded_calls) == 2


def test_handle_artwork_menu_search_multiple_results(
        monkeypatch,
        artworks,
):
    entries = iter([3, 4])
    selection = iter([artworks[1], None])
    loaded_calls = []
    searched_calls = []
    selected_calls = []

    def fake_load_artworks():
        loaded_calls.append("called")
        return artworks

    def fake_search_artworks(entry):
        searched_calls.append(entry)
        return artworks

    monkeypatch.setattr(
        handle_artwork_menu,
        "load_artworks",
        fake_load_artworks,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "artworks_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "Test"
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "search_artwork_title",
        fake_search_artworks,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "select_artwork",
        lambda _: next(selection),
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "handle_selected_artwork",
        lambda artwork: selected_calls.append(artwork)
    )

    handle_artwork_menu.handle_artwork_menu()
    
    assert selected_calls == [artworks[1]]
    assert searched_calls == ["Test", "Test"]
    assert len(loaded_calls) == 2


def test_handle_artwork_menu_search_multiple_results_none(
        monkeypatch,
        artworks,
):
    entries = iter([3, 4])
    selected_calls = []

    monkeypatch.setattr(
        handle_artwork_menu,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "artworks_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "Test",
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "search_artwork_title",
        lambda _: artworks,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "select_artwork",
        lambda _: None,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "handle_selected_artwork",
        lambda artwork: selected_calls.append(artwork),
    )

    handle_artwork_menu.handle_artwork_menu()

    assert selected_calls == []


def test_handle_artwork_menu_search_multiple_results_then_no_result(
        monkeypatch,
        capsys,
        artworks,
):
    entries = iter([3, 4])
    searches = iter([artworks, []])
    selected_calls = []

    monkeypatch.setattr(
        handle_artwork_menu,
        "load_artworks",
        lambda: artworks,
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "artworks_menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "Test",
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "search_artwork_title",
        lambda _: next(searches),
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "select_artwork",
        lambda _: artworks[0],
    )
    monkeypatch.setattr(
        handle_artwork_menu,
        "handle_selected_artwork",
        lambda artwork: selected_calls.append(artwork),
    )

    handle_artwork_menu.handle_artwork_menu()

    captured = capsys.readouterr()

    assert selected_calls == [artworks[0]]
    assert '- No artworks found for "Test".' in captured.out