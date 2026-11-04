
import pytest

from artwork_catalog.collection import Collection
from artwork_catalog import search_collection


@pytest.fixture
def collections():
    return [
        Collection(
            name="Watercolor Paintings",
            artwork_ids=["artwork-1", "artwork-2"],
            description="My watercolors",
            id="collection-1",
        ),
        Collection(
            name="Oil Paintings",
            artwork_ids=["artwork-3"],
            description="My oil paintings",
            id="collection-2",
        ),
        Collection(
            name="Ceramic Sculptures",
            artwork_ids=[],
            description="My sculptures",
            id="collection-3",
        ),
    ]


@pytest.mark.parametrize("entry", ["", " ", "   ", "\t"])
def test_search_collection_name_empty_or_whitespace(
    monkeypatch, collections, entry
):
    monkeypatch.setattr(
        search_collection,
        "load_collections",
        lambda: collections,
    )

    result = search_collection.search_collection_name(entry)

    assert result == []


def test_search_collection_name_no_match(monkeypatch, collections):
    monkeypatch.setattr(
        search_collection,
        "load_collections",
        lambda: collections,
    )

    result = search_collection.search_collection_name("photography")

    assert result == []


def test_search_collection_name_one_match(monkeypatch, collections):
    monkeypatch.setattr(
        search_collection,
        "load_collections",
        lambda: collections,
    )

    result = search_collection.search_collection_name("ceramic")

    assert len(result) == 1
    assert result[0].name == "Ceramic Sculptures"


def test_search_collection_name_multiple_matches(
    monkeypatch, collections
):
    monkeypatch.setattr(
        search_collection,
        "load_collections",
        lambda: collections,
    )

    result = search_collection.search_collection_name("paintings")

    assert len(result) == 2
    assert result[0].name == "Watercolor Paintings"
    assert result[1].name == "Oil Paintings"


def test_search_collection_name_case_insensitive(
    monkeypatch, collections
):
    monkeypatch.setattr(
        search_collection,
        "load_collections",
        lambda: collections,
    )

    result = search_collection.search_collection_name("WATERCOLOR")

    assert len(result) == 1
    assert result[0].name == "Watercolor Paintings"


def test_search_collection_name_partial_match(
    monkeypatch, collections
):
    monkeypatch.setattr(
        search_collection,
        "load_collections",
        lambda: collections,
    )

    result = search_collection.search_collection_name("sculp")

    assert len(result) == 1
    assert result[0].name == "Ceramic Sculptures"


def test_search_collection_name_multi_word_match(
    monkeypatch, collections
):
    monkeypatch.setattr(
        search_collection,
        "load_collections",
        lambda: collections,
    )

    result = search_collection.search_collection_name("paintings oil")

    assert len(result) == 1
    assert result[0].name == "Oil Paintings"


def test_search_collection_name_multi_word_no_match(
    monkeypatch, collections
):
    monkeypatch.setattr(
        search_collection,
        "load_collections",
        lambda: collections,
    )

    result = search_collection.search_collection_name("oil ceramic")

    assert result == []


def test_search_collection_name_no_collections(monkeypatch):
    monkeypatch.setattr(
        search_collection,
        "load_collections",
        lambda: [],
    )

    result = search_collection.search_collection_name("paintings")

    assert result == []
