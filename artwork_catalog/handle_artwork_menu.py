from .artworks_menu import artworks_menu
from .artwork_storage import save_artwork
from .create_artwork import create_artwork
from .handle_selected_artwork import handle_selected_artwork
from .input_funcs import ExitInput
from .load import load_artworks
from .search_artwork import search_artwork_title
from .select_artwork import select_artwork


def handle_artwork_menu():
    artworks_list = load_artworks()

    while True:
        selected_option = artworks_menu()
# Add artwork
        if selected_option == 1:
            try:
                artwork = create_artwork()
            except ExitInput:
                continue
            save_artwork(artwork)
            artworks_list.append(artwork)

# Browse artworks
        elif selected_option == 2:
            if not artworks_list:
                print()
                print("- No artworks found.")
            else:
                while True:
                    print()
                    select = select_artwork(artworks_list)

                    if select is None:
                        break

                    handle_selected_artwork(select)
                    artworks_list = load_artworks()

# Search artworks
        elif selected_option == 3:
            search_entry = input("\nType your search: ")
            results = search_artwork_title(search_entry)
            print()

            if not results:
                print(f'- No artworks found for "{search_entry}".')

            elif len(results) == 1:
                handle_selected_artwork(results[0])

                artworks_list = load_artworks()

            else:
                while True:
                    select = select_artwork(results)
                    if select is None:
                        break
                    handle_selected_artwork(select)
                    artworks_list = load_artworks()
                    results = search_artwork_title(search_entry)
                    if not results:
                        print(f'\n- No artworks found for "{search_entry}".')
                        break

# Back
        elif selected_option == 4:
            return None