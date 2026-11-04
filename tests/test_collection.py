from artwork_catalog.collection import Collection


def test_collection_default_values():
    collection = Collection(
        "Paintings",
    )

    assert collection.artwork_ids == []
    assert collection.description is None
    assert collection.id is not None


def test_collection_to_dict():
    collection = Collection(
        name="Paintings",
        artwork_ids=["artwork-1"],
        description="test",
        id="collection-1",
    )

    assert collection.to_dict() == {
        "id": "collection-1",
        "name": "Paintings",
        "artwork_ids": ["artwork-1"],
        "description": "test",
    }


def test_collection_ids_differ():
    collection_one = Collection("Paintings")
    collection_two = Collection("Ceramics")

    assert collection_one.id != collection_two.id