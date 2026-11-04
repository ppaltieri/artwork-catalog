from .artwork import Artwork
from .artwork_to_collection import (
    add_multiple_artworks_to_collection,
    remove_multiple_artworks_from_collection,
)
from .collection_storage import (
    update_collection,
    delete_collection,
)
from .delete_confirmation import (
    remove_multiple_artworks_from_collection_confirmation,
    delete_collection_confirmation,
    )
from .edit_collection import edit_collection
from .export_pdf import export_collection_pdf
from .input_funcs import get_required_input
from .load import load_artworks
from .select_artwork import select_multiple_artworks
from .selected_collection_menu import selected_collection_menu


def handle_selected_collection(selected):
    while True:
        print()
        print(f"{selected.name}")
        print()

        selected_option = selected_collection_menu()


# View collection
        if selected_option == 1:
            artworks_list = load_artworks()
            artworks = selected.artwork_ids
            loaded = []

            for artwork in artworks_list:
                if artwork.id in artworks:
                    loaded.append(artwork)

            if selected.description is not None:
                print()
                print(selected.description)

            if not loaded:
                print()
                print("Empty collection")
            else:
                print()
                for appended in loaded:
                    print(f"{appended.title}, {appended.year}")


# Edit collection
        elif selected_option == 2:
            edited_collection = edit_collection(selected)

            if edited_collection is None:
                continue

            update_collection(selected, edited_collection)
            selected = edited_collection


# Add artworks
        elif selected_option == 3:
            artworks_list = load_artworks()

            if not artworks_list:
                print("\nNo artworks found.")
                continue

            selected_artworks = select_multiple_artworks(artworks_list)

            if selected_artworks is None:
                continue

            edited_collection, already_added = add_multiple_artworks_to_collection(
                selected,
                selected_artworks
            )

            if len(already_added) == len(selected_artworks):
                print("\nAll selected artworks are already in this collection.\n")
                continue

            selected = edited_collection

            if already_added:
                print(
                    f"\nAlready in collection: {', '.join(already_added)}\n"
                )


# Remove artworks
        elif selected_option == 4:
            artworks_list = load_artworks()
            added_artworks = [
                artwork
                for artwork in artworks_list
                if artwork.id in selected.artwork_ids
            ]

            if not added_artworks:
                print("No artworks in this collection.\n")
                continue

            selected_artworks = select_multiple_artworks(added_artworks)

            if selected_artworks is None:
                continue

            choice = remove_multiple_artworks_from_collection_confirmation(
                selected
            )

            if choice == 1:
                edited_collection = remove_multiple_artworks_from_collection(
                    selected,
                    selected_artworks
                )
                selected = edited_collection


# Export collection
        elif selected_option == 5:
            artworks_list = load_artworks()

            collection_artworks = [
                artwork
                for artwork in artworks_list
                if artwork.id in selected.artwork_ids
            ]

            if not collection_artworks:
                print("\nNo artworks in this collection.\n")
                continue

            output_path = get_required_input("Save as: ", commands=False)

            export_collection_pdf(
                selected,
                collection_artworks,
                output_path,
            )


# Delete collection
        elif selected_option == 6:
            choice = delete_collection_confirmation()
            
            if choice == 1:
                delete_collection(selected)
                break


# Back
        elif selected_option == 7:
            return None