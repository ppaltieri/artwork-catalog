
from types import SimpleNamespace

import pytest

from artwork_catalog.select_collection import select_collection


@pytest.fixture
def collections():
    return [
        SimpleNamespace(name="Paintings"),
        SimpleNamespace(name="Sculptures"),
        SimpleNamespace(name="Photography"),
    ]


def test_select_collection_list(monkeypatch, capsys, collections):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "4",
    )

    select_collection(collections)
    captured = capsys.readouterr()

    assert "1. Paintings" in captured.out
    assert "2. Sculptures" in captured.out
    assert "3. Photography" in captured.out
    assert "4. Back" in captured.out


@pytest.mark.parametrize("choice", ["1", "2", "3"])
def test_select_collection_valid(monkeypatch, collections, choice):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: choice,
    )

    result = select_collection(collections)

    assert result is collections[int(choice) - 1]


def test_select_collection_back(monkeypatch, collections):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "4",
    )

    result = select_collection(collections)

    assert result is None


@pytest.mark.parametrize(
    "invalid",
    ["abc", "0", "5", "-1", "1.5", ""],
)
def test_select_collection_invalid(
    monkeypatch, capsys, collections, invalid
):
    entries = iter([invalid, "2"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(entries),
    )

    result = select_collection(collections)
    captured = capsys.readouterr()

    assert "Invalid option." in captured.out
    assert result is collections[1]


def test_select_collection_empty_list(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1",
    )

    result = select_collection([])

    assert result is None
