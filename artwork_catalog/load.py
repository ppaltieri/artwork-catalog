import json
from pathlib import Path

from .artwork import Artwork
from .collection import Collection
from .dimensions import Dimensions


def load_artworks(json_path: str | Path = "artworks.json") -> list[Artwork]:
    p = Path(json_path)

    if not p.is_file():
        return []

    with open(p, "r") as file:
        data = json.load(file)

    artworks: list[Artwork] = []

    for item in data:
        dimensions = Dimensions(
            item["dimensions"]["height"],
            item["dimensions"]["width"],
            item["dimensions"]["depth"],
            item["dimensions"]["unit"],
        )

        artwork = Artwork(
            item["image_path"],
            item["title"],
            item["year"],
            item["medium"],
            item["technique"],
            item["materials"],
            dimensions,
            item.get("notes"),
            item.get("id"),
        )

        artworks.append(artwork)

    return artworks


def load_collections(json_path: str = "collections.json") -> list[Collection]:
    p = Path(json_path)

    if not p.is_file():
        return []
    
    with open(p, "r") as file:
        data = json.load(file)

    collections: list[Collection] = []

    for item in data:
        collection = Collection(
            item["name"],
            item["artwork_ids"],
            item["description"],
            item["id"],
        )

        collections.append(collection)

    return collections