from copy import deepcopy

from .artwork import Artwork
from .collection_storage import update_collection
from .load import load_collections


def add_artwork_to_collection(collection, artwork):
    if artwork.id in collection.artwork_ids:
        return None
    
    edited_collection = deepcopy(collection)
    edited_collection.artwork_ids.append(artwork.id)

    update_collection(collection, edited_collection)

    return edited_collection


def add_multiple_artworks_to_collection(collection, artworks):
    edited_collection = deepcopy(collection)
    already_added = []

    for artwork in artworks:
        if artwork.id not in edited_collection.artwork_ids:
            edited_collection.artwork_ids.append(artwork.id)
        else:
            already_added.append(artwork.title)

    if edited_collection.artwork_ids != collection.artwork_ids:
        update_collection(collection, edited_collection)

    return edited_collection, already_added


def add_to_collection_menu(options: list[str]) -> int:
    while True:
        try:
            for n, option in enumerate(options, start=1):
                print(f"{n}. {option}")

            choice = int(input("\nSelect an option: "))
            if 0 < choice <= len(options):
                return choice

            raise ValueError
        
        except ValueError:
            print("\nInvalid option.")


def select_collection_with_artwork(artwork):
    collections_list = load_collections()

    artwork_collections = []

    for collection in collections_list:
        if artwork.id in collection.artwork_ids:
            artwork_collections.append(collection)

    if not artwork_collections:
        return None

    while True:
        for n, collection in enumerate(artwork_collections, start=1):
            print(f"{n}. {collection.name}")

        back_option = len(artwork_collections) + 1
        print(f"{back_option}. Back")

        try:
            choice = int(input("\nSelect an option: "))

            if 0 < choice <= len(artwork_collections):
                return artwork_collections[choice - 1]
            
            if choice == back_option:
                return None

            raise ValueError
        
        except ValueError:
            print("\nInvalid option.")


def remove_artwork_from_collection(collection, artwork):
    if artwork.id not in collection.artwork_ids:
        return collection

    edited_collection = deepcopy(collection)
    edited_collection.artwork_ids.remove(artwork.id)

    update_collection(collection, edited_collection)

    return edited_collection


def remove_multiple_artworks_from_collection(collection, artworks):
    edited_collection = deepcopy(collection)

    for artwork in artworks:
        if artwork.id in edited_collection.artwork_ids:
            edited_collection.artwork_ids.remove(artwork.id)

    update_collection(collection, edited_collection)

    return edited_collection


def remove_artwork_from_all_collections(artwork: Artwork) -> None:
    collections_list = load_collections()

    for collection in collections_list:
        if artwork.id in collection.artwork_ids:
            edited_collection = deepcopy(collection)
            edited_collection.artwork_ids.remove(artwork.id)
            update_collection(collection, edited_collection)