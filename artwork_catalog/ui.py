from .menu import menu
from .handle_artwork_menu import handle_artwork_menu
from .handle_collection_menu import handle_collection_menu


def main():
    while True:
        option = menu()

# Artworks
        if option == 1:
            handle_artwork_menu()

# Collections
        elif option == 2:
            handle_collection_menu()

# Exit
        elif option == 3:
            return


if __name__ == "__main__": #pragma: no cover
    main()