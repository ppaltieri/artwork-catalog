
from artwork_catalog import ui


def test_main_exit(monkeypatch):
    monkeypatch.setattr(ui, "menu", lambda: 3)

    ui.main()


def test_main_artworks(monkeypatch):
    entries = iter([1, 3])
    calls = []

    monkeypatch.setattr(
        ui,
        "menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        ui,
        "handle_artwork_menu",
        lambda: calls.append("artworks"),
    )

    ui.main()

    assert calls == ["artworks"]


def test_main_collections(monkeypatch):
    entries = iter([2, 3])
    calls = []

    monkeypatch.setattr(
        ui,
        "menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        ui,
        "handle_collection_menu",
        lambda: calls.append("collections"),
    )

    ui.main()

    assert calls == ["collections"]


def test_main_multiple_operations(monkeypatch):
    entries = iter([1, 2, 1, 3])
    calls = []

    monkeypatch.setattr(
        ui,
        "menu",
        lambda: next(entries),
    )
    monkeypatch.setattr(
        ui,
        "handle_artwork_menu",
        lambda: calls.append("artworks"),
    )
    monkeypatch.setattr(
        ui,
        "handle_collection_menu",
        lambda: calls.append("collections"),
    )

    ui.main()

    assert calls == [
        "artworks",
        "collections",
        "artworks",
    ]
