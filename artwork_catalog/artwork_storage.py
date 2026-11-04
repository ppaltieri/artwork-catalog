import json
from pathlib import Path

from .artwork import Artwork


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


def save_artwork(
    artwork: Artwork,
    json_path: str | Path = "artworks.json",
) -> None:
    p = Path(json_path)

    data = _load_json_list(p)

    data.append(artwork.to_dict())

    _write_json_list(data, p)


def update_artwork(
    selected: Artwork,
    edited_artwork: Artwork,
    json_path: str | Path = "artworks.json",
) -> None:
    p = Path(json_path)

    if not p.is_file():    
        return

    data = _load_json_list(p)

    for index, artwork_data in enumerate(data):
        if artwork_data.get("id") == selected.id:
            data[index] = edited_artwork.to_dict()
            break

    _write_json_list(data, p)


def delete_artwork(
    artwork: Artwork,
    json_path: str | Path = "artworks.json",
) -> None: 
    p = Path(json_path)
    
    if not p.is_file():
        return

    data = _load_json_list(p)

    for index, artwork_data in enumerate(data):
        if artwork_data.get("id") == artwork.id:
            del data[index]
            break

    _write_json_list(data, p)