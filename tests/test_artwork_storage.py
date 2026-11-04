import json
import pytest
from copy import deepcopy

from artwork_catalog.artwork import Artwork
from artwork_catalog.dimensions import Dimensions
from artwork_catalog.artwork_storage import save_artwork, delete_artwork, update_artwork


@pytest.fixture
def artworks():
    dimensions_1 = Dimensions(29, 21)
    dimensions_2 = Dimensions(10, 10, 10)

    return [
        Artwork(
            "test1.jpg",
            "Test 1",
            2025,
            "Watercolor on paper",
            "wet-on-wet",
            "paint, paper",
            dimensions_1,
            id="artwork-1",
        ),

        Artwork(
            "test2.jpg",
            "Test 2",
            2026,
            "Ceramics",
            "pinch pot",
            "clay",
            dimensions_2,
            id="artwork-2",
        )
    ]


# save_artwork
def test_save_artwork_new(tmp_path, artworks):
    json_path = tmp_path / "test.json"

    save_artwork(artworks[0], json_path)

    assert json_path.is_file()

    with open(json_path, "r") as file:
        data = json.load(file)

    assert len(data) == 1
    assert data[0]["title"] == "Test 1"
    assert data[0]["year"] == 2025
    assert data[0]["medium"] == "Watercolor on paper"


def test_save_artwork_append(tmp_path, artworks):
    json_path = tmp_path / "test.json"

    save_artwork(artworks[0], json_path)
    save_artwork(artworks[1], json_path)

    with open(json_path, "r") as file:
        data = json.load(file)

    assert len(data) == 2
    assert data[0]["title"] == "Test 1"
    assert data[1]["title"] == "Test 2"


# update_artwork
def test_update_artwork(tmp_path, artworks):
    json_path = tmp_path / "test.json"

    save_artwork(artworks[0], json_path)
    save_artwork(artworks[1], json_path)

    edited_artwork = deepcopy(artworks[0])
    edited_artwork.title = "New Title"

    update_artwork(artworks[0], edited_artwork, json_path)

    with open(json_path, "r") as file:
        data = json.load(file)

    assert data[0] == edited_artwork.to_dict()
    assert data[1] == artworks[1].to_dict()


def test_update_artwork_missing_file(tmp_path, artworks):
    json_path = tmp_path / "missing.json"

    result = update_artwork(
        artworks[0],
        artworks[1],
        json_path,
    )

    assert not json_path.exists()


# delete_artwork
def test_delete_artwork(tmp_path, artworks):
    json_path = tmp_path / "test.json"

    save_artwork(artworks[0], json_path)
    save_artwork(artworks[1], json_path)

    with open(json_path, "r") as file:
        data = json.load(file)

    assert len(data) == 2

    delete_artwork(artworks[0], json_path)
    with open(json_path, "r") as file:
        data = json.load(file)

    assert len(data) == 1
    assert data[0]["title"] == "Test 2"


def test_delete_artwork_missing_file(tmp_path, artworks):
    json_path = tmp_path / "missing.json"

    result = delete_artwork(artworks[0], json_path)

    assert result is None
    assert not json_path.exists()