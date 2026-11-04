from pathlib import Path

from artwork_catalog.artwork import Artwork
from artwork_catalog.dimensions import Dimensions


def test_artwork_str():
    dimensions = Dimensions(29, 21)
    artwork = Artwork(
        Path("painting.jpg"),
        "Test title",
        2026,
        "Watercolor on paper",
        "watercolor",
        "paint",
        dimensions,
        "fifth version",
        "artwork-1"
    )

    assert str(artwork) == (
        "\nTest title, 2026, "
        "Watercolor on paper, 29 x 21 cm"
    )


def test_artwork_repr():
    dimensions = Dimensions(29, 21)
    artwork = Artwork(
        "painting.jpg",
        "Test",
        2026,
        "Watercolor on paper",
        "wet-on-wet",
        "paint, paper",
        dimensions,
        None,
        "artwork-1"
    )

    assert repr(artwork) == "Artwork('Test', 2026)"


def test_artwork_default_notes():
    dimensions = Dimensions(29, 21)
    artwork = Artwork(
        Path("painting.jpg"),
        "Test title",
        2026,
        "Watercolor on paper",
        "watercolor",
        "paint",
        dimensions,
        id="artwork-1"
    )

    assert artwork.notes is None


def test_artwork_to_dict():
    dimensions = Dimensions(29, 21, 2, "cm")

    artwork = Artwork(
        Path("painting.jpg"),
        "Test title",
        2026,
        "Watercolor on paper",
        "watercolor",
        "paint",
        dimensions,
        "fifth version",
        "artwork-1",
    )

    assert artwork.to_dict() == {
        "image_path": "painting.jpg",
        "title": "Test title",
        "year": 2026,
        "medium": "Watercolor on paper",
        "technique": "watercolor",
        "materials": "paint",
        "dimensions": {
            "height": 29,
            "width": 21,
            "depth": 2,
            "unit": "cm",
        },
        "notes": "fifth version",
        "id": "artwork-1",
    }


def test_artwork_to_dict_none_notes():
    dimensions = Dimensions(29, 21, 2, "cm")

    artwork = Artwork(
        Path("painting.jpg"),
        "Test title",
        2026,
        "Watercolor on paper",
        "watercolor",
        "paint",
        dimensions,
        id="artwork-1",
    )

    assert artwork.to_dict() == {
        "image_path": "painting.jpg",
        "title": "Test title",
        "year": 2026,
        "medium": "Watercolor on paper",
        "technique": "watercolor",
        "materials": "paint",
        "dimensions": {
            "height": 29,
            "width": 21,
            "depth": 2,
            "unit": "cm",
        },
        "notes": None,
        "id": "artwork-1",
    }


def test_artwork_details():
    dimensions = Dimensions(29, 21)
    artwork = Artwork(
        "painting.jpg",
        "Test",
        2026,
        "Watercolor on paper",
        "wet-on-wet",
        "paint, paper",
        dimensions,
        None,
        "artwork-1"
    )

    assert artwork.details() == (
        "Image: painting.jpg\n"
        "Title: Test\n"
        "Year: 2026\n"
        "Medium: Watercolor on paper\n"
        "Technique: wet-on-wet\n"
        "Materials: paint, paper\n"
        "Dimensions:\n"
        "    Height: 29\n"
        "    Width: 21\n"
        "    Depth: None\n"
        "    Unit: cm\n"
        "Notes: None"
    )


def test_artwork_unique_ids():
    dimensions = Dimensions(29, 21)
    artwork_1 = Artwork(
        "painting.jpg",
        "Test 1",
        2026,
        "Watercolor on paper",
        "wet-on-wet",
        "paint, paper",
        dimensions,
    )

    artwork_2 = Artwork(
        "ceramics.jpg",
        "Test 2",
        2025,
        "Ceramics",
        "pinch pot",
        "clay",
        dimensions,
    )

    assert artwork_1.id is not None
    assert artwork_2.id is not None
    assert artwork_1.id != artwork_2.id