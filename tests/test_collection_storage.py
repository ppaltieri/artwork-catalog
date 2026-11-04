import json

from artwork_catalog.collection import Collection
from artwork_catalog import collection_storage


# _load_json_list
def test_load_json_list_file_not_found(tmp_path):
    json_path = tmp_path / "collections.json"

    result = collection_storage._load_json_list(json_path)

    assert result == []


def test_load_json_list(tmp_path):
    json_path = tmp_path / "collections.json"

    data = [
        {"id": "collection-1", "name": "Paintings"},
        {"id": "collection-2", "name": "Ceramics"},
    ]

    with open(json_path, "w") as file:
        json.dump(data, file)

    result = collection_storage._load_json_list(json_path)

    assert result == data


# _write_json_list
def test_write_json_list(tmp_path):
    json_path = tmp_path / "collections.json"

    data = [
        {"id": "collection-1", "name": "Paintings"},
        {"id": "collection-2", "name": "Ceramics"},
    ]

    collection_storage._write_json_list(data, json_path)

    with open(json_path, "r") as file:
        result = json.load(file)

    assert result == data


# save_collection
def test_save_collection(tmp_path):
    json_path = tmp_path / "collections.json"

    collection = Collection(
        name="Paintings",
        artwork_ids=["artwork-1", "artwork-2"],
        description="Watercolor paintings",
        id="collection-1",
    )

    collection_storage.save_collection(collection, json_path)

    with open(json_path, "r") as file:
        data = json.load(file)

    assert data == [collection.to_dict()]


def test_save_collection_existing_data(tmp_path):
    json_path = tmp_path / "collections.json"

    existing_collection = Collection(
        name="Paintings",
        id="collection-1",
    )

    new_collection = Collection(
        name="Ceramics",
        id="collection-2",
    )

    with open(json_path, "w") as file:
        json.dump([existing_collection.to_dict()], file)

    collection_storage.save_collection(new_collection, json_path)

    with open(json_path, "r") as file:
        data = json.load(file)

    assert data == [
        existing_collection.to_dict(),
        new_collection.to_dict(),
    ]

# update_collection
def test_update_collection_file_not_found(tmp_path):
    json_path = tmp_path / "collections.json"

    old_collection = Collection(
        name="Paintings",
        id="collection-1",
    )

    new_collection = Collection(
        name="Updated Paintings",
        id="collection-1",
    )

    collection_storage.update_collection(
        old_collection,
        new_collection,
        json_path,
    )

    assert not json_path.exists()


def test_update_collection(tmp_path):
    json_path = tmp_path / "collections.json"

    old_collection = Collection(
        name="Paintings",
        artwork_ids=["artwork-1"],
        description="Original description",
        id="collection-1",
    )

    other_collection = Collection(
        name="Ceramics",
        artwork_ids=["artwork-2"],
        id="collection-2",
    )

    new_collection = Collection(
        name="Updated Paintings",
        artwork_ids=["artwork-1", "artwork-3"],
        description="Updated description",
        id="collection-1",
    )

    with open(json_path, "w") as file:
        json.dump(
            [
                old_collection.to_dict(),
                other_collection.to_dict(),
            ],
            file,
        )

    collection_storage.update_collection(
        old_collection,
        new_collection,
        json_path,
    )

    with open(json_path, "r") as file:
        data = json.load(file)

    assert data == [
        new_collection.to_dict(),
        other_collection.to_dict(),
    ]


def test_update_collection_no_match(tmp_path):
    json_path = tmp_path / "collections.json"

    existing_collection = Collection(
        name="Ceramics",
        id="collection-2",
    )

    old_collection = Collection(
        name="Paintings",
        id="collection-1",
    )

    new_collection = Collection(
        name="Updated Paintings",
        id="collection-1",
    )

    with open(json_path, "w") as file:
        json.dump(
            [existing_collection.to_dict()],
            file,
        )

    collection_storage.update_collection(
        old_collection,
        new_collection,
        json_path,
    )

    with open(json_path, "r") as file:
        data = json.load(file)

    assert data == [
        existing_collection.to_dict(),
    ]


def test_update_collection_only_first_match(tmp_path):
    json_path = tmp_path / "collections.json"

    first_collection = Collection(
        name="Paintings",
        id="collection-1",
    )

    second_collection = Collection(
        name="Duplicate Paintings",
        id="collection-1",
    )

    new_collection = Collection(
        name="Updated Paintings",
        id="collection-1",
    )

    with open(json_path, "w") as file:
        json.dump(
            [
                first_collection.to_dict(),
                second_collection.to_dict(),
            ],
            file,
        )

    collection_storage.update_collection(
        first_collection,
        new_collection,
        json_path,
    )

    with open(json_path, "r") as file:
        data = json.load(file)

    assert data == [
        new_collection.to_dict(),
        second_collection.to_dict(),
    ]


# delete_collection


def test_delete_collection(tmp_path):
    json_path = tmp_path / "collections.json"

    collection = Collection(
        name="Paintings",
        id="collection-1",
    )

    with open(json_path, "w") as file:
        json.dump([collection.to_dict()], file)

    collection_storage.delete_collection(
        collection,
        json_path,
    )

    with open(json_path, "r") as file:
        data = json.load(file)

    assert data == []


def test_delete_collection_file_not_found(tmp_path):
    json_path = tmp_path / "collections.json"

    collection = Collection(
        name="Paintings",
        id="collection-1",
    )

    collection_storage.delete_collection(
        collection,
        json_path,
    )

    assert not json_path.exists()


def test_delete_collection_no_match(tmp_path):
    json_path = tmp_path / "collections.json"

    existing_collection = Collection(
        name="Ceramics",
        id="collection-2",
    )

    collection = Collection(
        name="Paintings",
        id="collection-1",
    )

    with open(json_path, "w") as file:
        json.dump(
            [existing_collection.to_dict()],
            file,
        )

    collection_storage.delete_collection(
        collection,
        json_path,
    )

    with open(json_path, "r") as file:
        data = json.load(file)

    assert data == [
        existing_collection.to_dict(),
    ]