from .create_collection import create_collection
from .collections_menu import collections_menu
from .collection_storage import save_collection
from .handle_selected_collection import handle_selected_collection
from .input_funcs import ExitInput
from .load import load_collections
from .search_collection import search_collection_name
from .select_collection import select_collection


def handle_collection_menu():
    collections_list = load_collections()

    while True:
        selected_option = collections_menu()
# Create collection
        if selected_option == 1:
            try:
                collection = create_collection()
            except ExitInput:
                continue
            save_collection(collection)
            collections_list.append(collection)

# Browse collections
        elif selected_option == 2:
            if not collections_list:
                print()
                print("- No collections found.")
            else:
                while True:
                    print()
                    select = select_collection(collections_list)

                    if select is None:
                        break

                    handle_selected_collection(select)
                    collections_list = load_collections()



# Search collections
        elif selected_option == 3:
            search_entry = input("\nType your search: ")
            results = search_collection_name(search_entry)
            print()

            if not results:
                print(f'- No collections found for "{search_entry}".')

            elif len(results) == 1:
                handle_selected_collection(results[0])
                collections_list = load_collections()

            else:
                while True:
                    select = select_collection(results)
                    if select is None:
                        break

                    handle_selected_collection(select)
                    
                    collections_list = load_collections()
                    results = search_collection_name(search_entry)

                    if not results:
                        print(f'\n- No collections found for "{search_entry}".')
                        break
# Back
        elif selected_option == 4:
            return None
            