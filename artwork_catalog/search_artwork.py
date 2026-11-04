from .artwork import Artwork
from .load import load_artworks


def search_artwork_title(entry: str) -> list[Artwork]:
    artworks = load_artworks()
    results: list[Artwork] = []

    if not entry.strip():
        return results

    keyword = entry.lower().split()

    for artwork in artworks:
        if all(word in artwork.title.lower() for word in keyword):
            results.append(artwork)

    return results