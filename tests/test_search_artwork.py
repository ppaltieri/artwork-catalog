
import pytest

from artwork_catalog.artwork import Artwork
from artwork_catalog.dimensions import Dimensions
from artwork_catalog import search_artwork


@pytest.fixture
def artworks():
    dimensions_1 = Dimensions(10, 15, 20, "cm")
    dimensions_2 = Dimensions(21, 29)
    dimensions_3 = Dimensions(1080, 1920, None, "px")

    return [
        Artwork(
            "image1.jpg",
            "Test 1",
            2026,
            "Ceramics",
            "Throwing",
            "clay",
            dimensions_1,
            None,
        ),
        Artwork(
            "image2.jpg",
            "Test 2",
            2020,
            "Watercolor on paper",
            "wet-on-wet",
            "paint, cotton paper",
            dimensions_2,
            None,
        ),
        Artwork(
            "image3.jpg",
            "Flags",
            2023,
            "Digital painting",
            "digital painting",
            "tablet",
            dimensions_3,
            None,
        ),
    ]


@pytest.mark.parametrize("entry", ["", " ", "   ", "\t"])
def test_search_artwork_title_empty_or_whitespace(
    monkeypatch, artworks, entry
):
    monkeypatch.setattr(
        search_artwork,
        "load_artworks",
        lambda: artworks,
    )

    result = search_artwork.search_artwork_title(entry)

    assert result == []


def test_search_artwork_title_no_match(monkeypatch, artworks):
    monkeypatch.setattr(
        search_artwork,
        "load_artworks",
        lambda: artworks,
    )

    result = search_artwork.search_artwork_title("abc")

    assert result == []


def test_search_artwork_title_one_match(monkeypatch, artworks):
    monkeypatch.setattr(
        search_artwork,
        "load_artworks",
        lambda: artworks,
    )

    result = search_artwork.search_artwork_title("fla")

    assert len(result) == 1
    assert result[0].title == "Flags"


def test_search_artwork_title_multiple_matches(monkeypatch, artworks):
    monkeypatch.setattr(
        search_artwork,
        "load_artworks",
        lambda: artworks,
    )

    results = search_artwork.search_artwork_title("tes")

    assert len(results) == 2
    assert results[0].title == "Test 1"
    assert results[0].year == 2026
    assert results[1].title == "Test 2"
    assert results[1].year == 2020


def test_search_artwork_title_case_insensitive_match(
    monkeypatch, artworks
):
    monkeypatch.setattr(
        search_artwork,
        "load_artworks",
        lambda: artworks,
    )

    result = search_artwork.search_artwork_title("FLA")

    assert len(result) == 1
    assert result[0].title == "Flags"


def test_search_artwork_title_multi_word_match(
    monkeypatch, artworks
):
    monkeypatch.setattr(
        search_artwork,
        "load_artworks",
        lambda: artworks,
    )

    result = search_artwork.search_artwork_title("2 test")

    assert len(result) == 1
    assert result[0].title == "Test 2"


def test_search_artwork_title_multi_word_no_match(
    monkeypatch, artworks
):
    monkeypatch.setattr(
        search_artwork,
        "load_artworks",
        lambda: artworks,
    )

    result = search_artwork.search_artwork_title("test flags")

    assert result == []


def test_search_artwork_title_no_artworks(monkeypatch):
    monkeypatch.setattr(
        search_artwork,
        "load_artworks",
        lambda: [],
    )

    result = search_artwork.search_artwork_title("test")

    assert result == []
