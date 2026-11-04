
import json

from artwork_catalog.artwork import Artwork
from artwork_catalog.collection import Collection
from artwork_catalog.dimensions import Dimensions
from artwork_catalog.load import load_artworks, load_collections


def test_load_artworks_missing_file(tmp_path):
    p = tmp_path / "missing.json"

    result = load_artworks(p)

    assert result == []


def test_load_artworks_empty_file(tmp_path):
    p = tmp_path / "artworks.json"
    p.write_text("[]")

    result = load_artworks(p)

    assert result == []


def test_load_artworks_one_valid_artwork(tmp_path):
    p = tmp_path / "artworks.json"

    data = [
        {
            "id": "artwork-1",
            "image_path": "painting.jpg",
            "title": "Sunset",
            "year": 2026,
            "medium": "Watercolor on paper",
            "technique": "Wet-on-wet",
            "materials": "Paint, paper",
            "dimensions": {
                "height": 29,
                "width": 21,
                "depth": None,
                "unit": "cm",
            },
            "notes": "First artwork",
        }
    ]

    p.write_text(json.dumps(data))

    result = load_artworks(p)

    assert len(result) == 1

    artwork = result[0]

    assert isinstance(artwork, Artwork)
    assert isinstance(artwork.dimensions, Dimensions)

    assert artwork.id == "artwork-1"
    assert artwork.image_path == "painting.jpg"
    assert artwork.title == "Sunset"
    assert artwork.year == 2026
    assert artwork.medium == "Watercolor on paper"
    assert artwork.technique == "Wet-on-wet"
    assert artwork.materials == "Paint, paper"
    assert artwork.notes == "First artwork"

    assert artwork.dimensions.height == 29
    assert artwork.dimensions.width == 21
    assert artwork.dimensions.depth is None
    assert artwork.dimensions.unit == "cm"


def test_load_artworks_two_valid_artworks(tmp_path):
    p = tmp_path / "artworks.json"

    data = [
        {
            "id": "artwork-1",
            "image_path": "painting.jpg",
            "title": "Painting",
            "year": 2026,
            "medium": "Watercolor",
            "technique": "Wet-on-wet",
            "materials": "Paint, paper",
            "dimensions": {
                "height": 29,
                "width": 21,
                "depth": None,
                "unit": "cm",
            },
            "notes": None,
        },
        {
            "id": "artwork-2",
            "image_path": "pot.jpg",
            "title": "Ceramic Pot",
            "year": 2020,
            "medium": "Ceramics",
            "technique": "Pinch pot",
            "materials": "Clay",
            "dimensions": {
                "height": 15,
                "width": 10,
                "depth": 20,
                "unit": "in",
            },
            "notes": "Second artwork",
        },
    ]

    p.write_text(json.dumps(data))

    result = load_artworks(p)

    assert len(result) == 2

    assert result[0].id == "artwork-1"
    assert result[0].title == "Painting"
    assert result[0].dimensions.depth is None

    assert result[1].id == "artwork-2"
    assert result[1].title == "Ceramic Pot"
    assert result[1].dimensions.height == 15
    assert result[1].dimensions.width == 10
    assert result[1].dimensions.depth == 20
    assert result[1].dimensions.unit == "in"
    assert result[1].notes == "Second artwork"


def test_load_artworks_missing_optional_fields(tmp_path):
    p = tmp_path / "artworks.json"

    data = [
        {
            "image_path": "painting.jpg",
            "title": "Untitled",
            "year": 2025,
            "medium": "Painting",
            "technique": "Oil",
            "materials": "Canvas",
            "dimensions": {
                "height": 30,
                "width": 40,
                "depth": None,
                "unit": "cm",
            },
        }
    ]

    p.write_text(json.dumps(data))

    result = load_artworks(p)

    assert len(result) == 1
    assert result[0].notes is None
    assert result[0].id is not None


def test_load_collections_missing_file(tmp_path):
    p = tmp_path / "missing.json"

    result = load_collections(p)

    assert result == []


def test_load_collections_empty_file(tmp_path):
    p = tmp_path / "collections.json"
    p.write_text("[]")

    result = load_collections(p)

    assert result == []


def test_load_collections_one_valid_collection(tmp_path):
    p = tmp_path / "collections.json"

    data = [
        {
            "id": "collection-1",
            "name": "Paintings",
            "artwork_ids": ["artwork-1", "artwork-2"],
            "description": "My paintings",
        }
    ]

    p.write_text(json.dumps(data))

    result = load_collections(p)

    assert len(result) == 1

    collection = result[0]

    assert isinstance(collection, Collection)
    assert collection.id == "collection-1"
    assert collection.name == "Paintings"
    assert collection.artwork_ids == [
        "artwork-1",
        "artwork-2",
    ]
    assert collection.description == "My paintings"


def test_load_collections_two_valid_collections(tmp_path):
    p = tmp_path / "collections.json"

    data = [
        {
            "id": "collection-1",
            "name": "Paintings",
            "artwork_ids": ["artwork-1"],
            "description": "Watercolors",
        },
        {
            "id": "collection-2",
            "name": "Sculptures",
            "artwork_ids": [],
            "description": None,
        },
    ]

    p.write_text(json.dumps(data))

    result = load_collections(p)

    assert len(result) == 2

    assert result[0].id == "collection-1"
    assert result[0].name == "Paintings"
    assert result[0].artwork_ids == ["artwork-1"]
    assert result[0].description == "Watercolors"

    assert result[1].id == "collection-2"
    assert result[1].name == "Sculptures"
    assert result[1].artwork_ids == []
    assert result[1].description is None
