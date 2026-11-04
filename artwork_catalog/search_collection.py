from .collection import Collection
from .load import load_collections


def search_collection_name(entry: str) -> list[Collection]:
    collections = load_collections()
    results: list[Collection] = []

    if not entry.strip():
        return results

    keyword = entry.lower().split()

    for collection in collections:
        if all(word in collection.name.lower() for word in keyword):
            results.append(collection)

    return results