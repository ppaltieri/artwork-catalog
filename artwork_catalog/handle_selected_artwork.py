from .artwork_to_collection import (
    add_artwork_to_collection,
    add_to_collection_menu,
    select_collection_with_artwork,
    remove_artwork_from_collection,
    remove_artwork_from_all_collections,
)
from .artwork_storage import update_artwork, delete_artwork
from .create_collection import create_collection
from .collection_storage import save_collection
from .delete_confirmation import (
    delete_artwork_confirmation,
    remove_from_collection_confirmation
)
from .edit_artwork import edit_artwork
from .export_pdf import export_artwork_pdf
from .input_funcs import get_required_input, ExitInput
from .load import load_collections
from .select_collection import select_collection
from .selected_artwork_menu import selected_artwork_menu


def handle_selected_artwork(selected):
    while True:
        print(f"{selected.title}, {selected.year}")
        print()

        selected_option = selected_artwork_menu()


# View details
        if selected_option == 1:
            print()
            print(selected.details())
            print()


# Edit artwork
        elif selected_option == 2:
            edited_artwork = edit_artwork(selected)

            if edited_artwork is None:
                continue

            update_artwork(selected, edited_artwork)
            selected = edited_artwork


# Add to collection
        elif selected_option == 3:
            collections_list = load_collections()

            if not collections_list:
                print("\n- No collections found.\n")
            
                options = ["Create collection and add this artwork", "Back"]
                choice = add_to_collection_menu(options)

                if choice == 1:
                    try:
                        new_collection = create_collection()
                    except ExitInput:
                        continue
                    save_collection(new_collection)
                    add_artwork_to_collection(new_collection, selected)
                    
                    continue

                elif choice == 2:
                    continue
           
            options = [
                "Select existing collection",
                "Create new collection",
                "Back"
            ]
            choice = add_to_collection_menu(options)

            if choice == 1:
                collection = select_collection(collections_list)

                if collection is not None:
                    added = add_artwork_to_collection(collection, selected)
                    
                    if added is None:
                        print("\nArtwork already in collection.\n")
                        continue

            elif choice == 2:
                try:
                    collection = create_collection()
                except ExitInput:
                    continue
                save_collection(collection)
                add_artwork_to_collection(collection, selected)

            elif choice == 3:
                continue


# Remove from collection
        elif selected_option == 4:
            collection = select_collection_with_artwork(selected)

            if collection is None:
                continue

            choice = remove_from_collection_confirmation(collection, selected)

            if choice == 1:
                remove_artwork_from_collection(
                    collection,
                    selected
                )


# Export artwork
        elif selected_option == 5:
            output_path = get_required_input("Save as: ", commands=False)
            export_artwork_pdf(selected, output_path)


# Delete artwork
        elif selected_option == 6:
            option = delete_artwork_confirmation()
            if option == 1:
                remove_artwork_from_all_collections(selected)
                delete_artwork(selected)
                return None


# Back
        elif selected_option == 7:
            return None