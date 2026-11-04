import pytest

from artwork_catalog.artwork import Artwork
from artwork_catalog import artwork_to_collection
from artwork_catalog.collection import Collection



@pytest.fixture
def artworks():
    dimensions = (29, 21)
    return [Artwork(
        "test.json",
        "Test 1",
        2026,
        "Watercolor",
        "wet-on-wet",
        "paint, paper",
        dimensions,
        None,
        "artwork-1",
    ),
        Artwork(
            "test2.json",
            "Test 2",
            2025,
            "Ceramics",
            "pinch-pot",
            "clay",
            dimensions,
            None,
            "artwork-2"
        ),
    ]


@pytest.fixture
def artwork_three():
    dimensions = (29, 21)
    return Artwork(
        "test3.json",
        "Test 3",
        2020,
        "Painting",
        "Oil on cavas",
        "paint, canvas",
        dimensions,
        None,
        "artwork-3"
    )

@pytest.fixture
def collections():
    return [Collection(
        "Painting",
        ["artwork-1"],
        None,
        "collection-1",
    ),
        Collection(
            "Pottery",
            ["artwork-2"],
            None,
            "collection-2",
        ),
        Collection(
            "Mix",
            ["artwork-1", "artwork-2"],
            None,
            "collection-3",
        ),
]

@pytest.fixture
def empty_collection():
    return Collection(
        "Test",
        None,
        None,
        "collection-test",
    )


@pytest.fixture
def mock_update_collection(monkeypatch):
    updated = []

    def fake_update_collection(original, edited):
        updated.append((original, edited))

    monkeypatch.setattr(
        artwork_to_collection,
        "update_collection",
        fake_update_collection,
    )

    return updated


# add_artwork_to_collection
def test_add_artwork_to_collection_new(
        artworks,
        collections,
        mock_update_collection,
    ):
    
    result = artwork_to_collection.add_artwork_to_collection(
        collections[0], artworks[1]
    )

    assert result is not None
    assert result.artwork_ids == ["artwork-1", "artwork-2"]
    assert collections[0].artwork_ids == ["artwork-1"]

    assert len(mock_update_collection) == 1
    assert mock_update_collection[0][0] is collections[0]
    assert mock_update_collection[0][1] is result


def test_add_artwork_to_collection_existing(
        artworks,
        collections,
        mock_update_collection,
    ):

    result = artwork_to_collection.add_artwork_to_collection(
        collections[0], artworks[0]
    )

    assert result is None
    assert mock_update_collection == []


# add_multiple_artworks_to_collection
def test_add_multiple_artworks_to_collection_new(
        artworks,
        empty_collection,
        mock_update_collection,
    ):

    edited_collection, already_added = (
        artwork_to_collection.add_multiple_artworks_to_collection(
            empty_collection,
            artworks,
        )
    )

    assert empty_collection.artwork_ids == []
    assert edited_collection.artwork_ids == ["artwork-1", "artwork-2"]
    assert already_added == []

    assert len(mock_update_collection) == 1
    assert mock_update_collection[0][0] is empty_collection
    assert mock_update_collection[0][1] is edited_collection


def test_add_multiple_artworks_to_collection_some_already_added(
        artworks,
        collections,
        mock_update_collection,
    ):

    edited_collection, already_added = (
        artwork_to_collection.add_multiple_artworks_to_collection(
            collections[0],
            artworks
        )
    )

    assert collections[0].artwork_ids == ["artwork-1"]
    assert edited_collection.artwork_ids == ["artwork-1", "artwork-2"]
    assert already_added == ["Test 1"]

    assert len(mock_update_collection) == 1
    assert mock_update_collection[0][0] is collections[0]
    assert mock_update_collection[0][1] is edited_collection


def test_add_multiple_artworks_to_collection_all_already_added(
        artworks,
        collections,
        mock_update_collection
    ):

    edited_collection, already_added = (
        artwork_to_collection.add_multiple_artworks_to_collection(
            collections[2],
            artworks,
        )
    )

    assert collections[2].artwork_ids == ["artwork-1", "artwork-2"]
    assert mock_update_collection == []
    assert edited_collection.artwork_ids == collections[2].artwork_ids
    assert already_added == ["Test 1", "Test 2"]


# add_to_collection_menu
def test_add_to_collection_menu_invalid_options_then_valid(monkeypatch, capsys):
    options = ["option 1", "option 2", "back"]
    choice = iter([0, 4, "abc", 3])
    monkeypatch.setattr("builtins.input", lambda _: next(choice))

    result = artwork_to_collection.add_to_collection_menu(options)

    captured = capsys.readouterr()

    assert result == 3
    assert captured.out.count("Invalid option.") == 3


@pytest.mark.parametrize("choice", [1, 2, 3])
def test_add_to_collection_menu_valid_options(monkeypatch, choice):
    options = ["option 1", "option 2", "back"]
    monkeypatch.setattr("builtins.input", lambda _: choice)

    result = artwork_to_collection.add_to_collection_menu(options)

    assert result == choice


# select_collection_with_artwork_selected
def test_select_collection_with_artwork_selected(
        monkeypatch,
        artworks,
        collections,
    ):
    artwork = artworks[0]

    collections[0].artwork_ids = []
    collections[1].artwork_ids = [artwork.id]

    monkeypatch.setattr(
        artwork_to_collection,
        "load_collections",
        lambda: collections,
    )

    monkeypatch.setattr("builtins.input", lambda _: 1)

    result = artwork_to_collection.select_collection_with_artwork(
        artwork
    )

    assert result == collections[1]


def test_select_collection_with_artwork_no_matches(
        monkeypatch,
        artwork_three,
        collections,
):

    monkeypatch.setattr(
        artwork_to_collection,
        "load_collections",
        lambda: collections,
    )

    result = artwork_to_collection.select_collection_with_artwork(
        artwork_three
    )

    assert result is None


def test_select_collection_with_artwork_back(
        monkeypatch,
        artworks,
        collections,
):
    artwork = artworks[0]

    monkeypatch.setattr(
    artwork_to_collection,
    "load_collections",
    lambda: collections,
    )

    monkeypatch.setattr("builtins.input", lambda _: 3)

    result = artwork_to_collection.select_collection_with_artwork(
        artwork
    )

    assert result is None


def test_select_collection_with_artwork_invalid_options_then_valid(
        monkeypatch,
        capsys,
        artworks,
        collections,
    ):
    artwork = artworks[0]
    choice = iter([0, 4, "abc", 1])

    monkeypatch.setattr(
        artwork_to_collection,
        "load_collections",
        lambda: collections,
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(choice)
    )

    result = artwork_to_collection.select_collection_with_artwork(
        artwork
    )

    captured = capsys.readouterr()

    assert result == collections[0]
    assert captured.out.count("Invalid option.") == 3


# remove_artwork_from_collection
def test_remove_artwork_from_collection(
        artworks,
        collections,
        mock_update_collection,
    ):
    artwork = artworks[0]
    collection = collections[0]

    result = artwork_to_collection.remove_artwork_from_collection(
        collection,
        artwork
    )

    assert collection.artwork_ids == [artwork.id]
    assert result.artwork_ids == []
    assert mock_update_collection[0][0] == collection
    assert mock_update_collection[0][1] == result


def test_remove_artwork_from_collection_no_match(
        artwork_three,
        collections,
        mock_update_collection,
):
    collection = collections[0]

    result = artwork_to_collection.remove_artwork_from_collection(
        collection,
        artwork_three
    )

    assert result == collection
    assert mock_update_collection == []


# remove_multiple_artworks_from_collection
def test_remove_multiple_artworks_from_collection(
        collections,
        artworks,
        mock_update_collection,
    ):
    collection = collections[2]

    result = artwork_to_collection.remove_multiple_artworks_from_collection(
        collection,
        artworks
    )

    assert result.artwork_ids == []
    assert collection.artwork_ids == ["artwork-1", "artwork-2"]
    assert mock_update_collection[0][0] == collection
    assert mock_update_collection[0][1] == result


def test_remove_multiple_artworks_from_collection_with_nonexistent_artwork(
        collections,
        artworks,
        artwork_three,
        mock_update_collection,
    ):
    collection = collections[2]
    artworks_to_remove = [*artworks, artwork_three]

    result = artwork_to_collection.remove_multiple_artworks_from_collection(
        collection,
        artworks_to_remove
    )

    assert result.artwork_ids == []
    assert collection.artwork_ids == ["artwork-1", "artwork-2"]
    assert mock_update_collection[0][0] == collection
    assert mock_update_collection[0][1] == result


def test_remove_multiple_artworks_from_collection_partial_removal(
        collections,
        artworks,
        mock_update_collection,
    ):
    collection = collections[2]
    collection.artwork_ids.append("artwork-3")

    result = artwork_to_collection.remove_multiple_artworks_from_collection(
        collection,
        artworks
    )

    assert result.artwork_ids == ["artwork-3"]
    assert collection.artwork_ids == [
        "artwork-1",
        "artwork-2",
        "artwork-3",
    ]
    assert mock_update_collection[0][0] == collection
    assert mock_update_collection[0][1] == result


# remove_artwork_from_all_collections
def test_remove_artwork_from_all_collections(
        monkeypatch,
        artworks,
        collections,
        mock_update_collection,
    ):
    artwork = artworks[0]
    
    monkeypatch.setattr(
        artwork_to_collection,
        "load_collections",
        lambda: collections
    )

    artwork_to_collection.remove_artwork_from_all_collections(artwork)

    assert collections[0].artwork_ids == ["artwork-1"]
    assert collections[2].artwork_ids == ["artwork-1", "artwork-2"]

    assert len(mock_update_collection) == 2

    assert mock_update_collection[0][0] == collections[0]
    assert mock_update_collection[0][1].artwork_ids == []

    assert mock_update_collection[1][0] == collections[2]
    assert mock_update_collection[1][1].artwork_ids == ["artwork-2"]


def test_remove_artwork_from_all_collections_no_match(
        monkeypatch,
        artwork_three,
        collections,
        mock_update_collection,
    ):
    monkeypatch.setattr(
        artwork_to_collection,
        "load_collections",
        lambda: collections
    )

    artwork_to_collection.remove_artwork_from_all_collections(
        artwork_three
    )

    assert mock_update_collection == []