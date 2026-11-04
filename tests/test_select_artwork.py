
import pytest
from types import SimpleNamespace

from artwork_catalog.select_artwork import (
    select_artwork,
    select_multiple_artworks,
)


@pytest.fixture
def artworks():
    return [
        SimpleNamespace(title="Test 1", year=2026),
        SimpleNamespace(title="Test 2", year=2025),
        SimpleNamespace(title="Test 3", year=2024),
    ]


def test_select_artwork_list(monkeypatch, capsys, artworks):
    monkeypatch.setattr("builtins.input", lambda _: "4")

    select_artwork(artworks)
    captured = capsys.readouterr()

    assert "1. Test 1, 2026" in captured.out
    assert "2. Test 2, 2025" in captured.out
    assert "3. Test 3, 2024" in captured.out
    assert "4. Back" in captured.out


@pytest.mark.parametrize("choice", ["1", "2", "3"])
def test_select_artwork_valid(monkeypatch, artworks, choice):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: choice,
    )

    result = select_artwork(artworks)

    assert result is artworks[int(choice) - 1]


def test_select_artwork_back(monkeypatch, artworks):
    monkeypatch.setattr("builtins.input", lambda _: "4")

    assert select_artwork(artworks) is None


@pytest.mark.parametrize(
    "invalid",
    ["abc", "0", "5", "-1", "1.5", ""],
)
def test_select_artwork_invalid(
    monkeypatch, capsys, artworks, invalid
):
    entries = iter([invalid, "2"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(entries),
    )

    result = select_artwork(artworks)
    captured = capsys.readouterr()

    assert "Invalid option." in captured.out
    assert result is artworks[1]


def test_select_artwork_empty_list(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")

    assert select_artwork([]) is None


def test_select_multiple_artworks_list(
    monkeypatch, capsys, artworks
):
    monkeypatch.setattr("builtins.input", lambda _: "4")

    select_multiple_artworks(artworks)
    captured = capsys.readouterr()

    assert "1. Test 1" in captured.out
    assert "2. Test 2" in captured.out
    assert "3. Test 3" in captured.out
    assert "4. Back" in captured.out


def test_select_multiple_artworks_one(monkeypatch, artworks):
    monkeypatch.setattr("builtins.input", lambda _: "2")

    result = select_multiple_artworks(artworks)

    assert result == [artworks[1]]


def test_select_multiple_artworks_multiple(
    monkeypatch, artworks
):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1,3",
    )

    result = select_multiple_artworks(artworks)

    assert result == [artworks[0], artworks[2]]


def test_select_multiple_artworks_order(
    monkeypatch, artworks
):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "3,1",
    )

    result = select_multiple_artworks(artworks)

    assert result == [artworks[2], artworks[0]]


def test_select_multiple_artworks_whitespace(
    monkeypatch, artworks
):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: " 1 , 2 ",
    )

    result = select_multiple_artworks(artworks)

    assert result == [artworks[0], artworks[1]]


def test_select_multiple_artworks_back(
    monkeypatch, artworks
):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: " 4 ",
    )

    assert select_multiple_artworks(artworks) is None


@pytest.mark.parametrize(
    "invalid",
    ["0", "5", "-1", "abc", "1,abc", "1,,2", ""],
)
def test_select_multiple_artworks_invalid(
    monkeypatch, capsys, artworks, invalid
):
    entries = iter([invalid, "1,2"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(entries),
    )

    result = select_multiple_artworks(artworks)
    captured = capsys.readouterr()

    assert "Invalid selection." in captured.out
    assert result == [artworks[0], artworks[1]]


@pytest.mark.parametrize(
    "duplicate",
    ["1,1", "1,2,1", "2,2,3"],
)
def test_select_multiple_artworks_duplicates(
    monkeypatch, capsys, artworks, duplicate
):
    entries = iter([duplicate, "1,2"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(entries),
    )

    result = select_multiple_artworks(artworks)
    captured = capsys.readouterr()

    assert "Duplicate selections are not allowed." in captured.out
    assert result == [artworks[0], artworks[1]]


def test_select_multiple_artworks_empty_list(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")

    assert select_multiple_artworks([]) is None
