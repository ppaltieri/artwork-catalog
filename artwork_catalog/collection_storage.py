import json
from pathlib import Path

from .collection import Collection


def _load_json_list(json_path: str | Path) -> list[dict]:
    p = Path(json_path)

    if not p.is_file():
        return []

    with open(p, "r") as file:
        return json.load(file)


def _write_json_list(
    data: list[dict],
    json_path: str | Path,
) -> None:
    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)
    

def save_collection(
    collection: Collection,
    json_path: str | Path = "collections.json",
) -> None:
    p = Path(json_path)
    data = _load_json_list(p)

    data.append(collection.to_dict())

    _write_json_list(data, p)


def update_collection(
    old_collection: Collection,
    new_collection: Collection,
    json_path: str | Path = "collections.json",
) -> None:
    p = Path(json_path)

    if not p.is_file():
        return

    data = _load_json_list(p)

    for index, collection_data in enumerate(data):
        if collection_data.get("id") == old_collection.id:
            data[index] = new_collection.to_dict()
            break

    _write_json_list(data, p)


def delete_collection(
    collection: Collection,
    json_path: str | Path = "collections.json",
) -> None:
    p = Path(json_path)

    if not p.is_file():
        return

    data = _load_json_list(p)

    for index, collection_data in enumerate(data):
        if collection_data.get("id") == collection.id:
            del data[index]
            break

    _write_json_list(data, p)