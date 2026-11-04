import pytest

from artwork_catalog.artwork import Artwork
from artwork_catalog.collection import Collection
from artwork_catalog.delete_confirmation import (
    delete_artwork_confirmation,
    delete_collection_confirmation,
    remove_from_collection_confirmation,
    remove_multiple_artworks_from_collection_confirmation,
)

@pytest.fixture
def collection():
    return Collection(
        "Paintings",
    )


def test_delete_artwork_confirmation_invalid_then_valid(monkeypatch, capsys):
    entries = iter(["abc", 3, 2])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    result = delete_artwork_confirmation()
    captured = capsys.readouterr()

    assert "1. Yes\n2. No" in captured.out
    assert captured.out.count("Invalid option.") == 2
    assert result == 2


def test_delete_collection_confirmation_invalid_then_valid(monkeypatch, capsys):
    entries = iter(["abc", 3, 2])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    result = delete_collection_confirmation()
    captured = capsys.readouterr()

    assert "1. Yes\n2. No" in captured.out
    assert captured.out.count("Invalid option.") == 2
    assert result == 2


def test_remove_from_collection_confirmation_invalid_then_valid(
        monkeypatch,
        capsys,
        collection,
    ):
    entries = iter(["abc", 3, 2])
    dimensions = (29, 21)
    artwork = Artwork(
        "painting.jpg",
        "Test",
        2026,
        "Watercolor",
        "wet-on-wet",
        "paint, paper",
        dimensions,
    )
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    result = remove_from_collection_confirmation(collection, artwork)
    captured = capsys.readouterr()

    assert "1. Yes\n2. No" in captured.out
    assert result == 2
    assert captured.out.count("Invalid option.") == 2


def test_remove_multiple_artworks_from_collection_confirmation_invalid_then_valid(
        monkeypatch,
        capsys,
        collection,
):
    entries = iter(["abc", 3, 2])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    result = remove_multiple_artworks_from_collection_confirmation(collection)
    captured = capsys.readouterr()

    assert "1. Yes\n2. No" in captured.out
    assert result == 2
    assert captured.out.count("Invalid option.") == 2