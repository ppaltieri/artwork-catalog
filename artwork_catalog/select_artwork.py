from .artwork import Artwork


class DuplicateSelectionError(Exception):
    pass


def select_artwork(artworks) -> Artwork | None:

    while True:
        for n, artwork in enumerate(artworks, start=1):
            print(f"{n}. {artwork.title}, {artwork.year}")
        back_option = len(artworks) + 1
        print(f"\n{back_option}. Back")
        
        try:
            choice = int(input("\nSelect an artwork: "))

            if 0 < choice <= len(artworks):

                return artworks[choice - 1]
            
            if choice == back_option:

                return None

            raise ValueError
        
        except ValueError:
            print("\nInvalid option.\n")
            continue


def select_multiple_artworks(artworks) -> list[Artwork] | None:
    while True:
        for n, artwork in enumerate(artworks, start=1):
            print(f"{n}. {artwork.title}")
        back_option = len(artworks) + 1
        print(f"\n{back_option}. Back")

        entry = input("\nSelect artworks separated by commas: ")

        if entry.strip() == str(back_option):
            return None

        try:
            choices = [
                int(choice.strip())
                for choice in entry.split(",")
            ]

            if len(choices) != len(set(choices)):
                raise DuplicateSelectionError

            if all(
                0 < choice <= len(artworks)
                for choice in choices
            ):
                return [
                    artworks[choice - 1]
                    for choice in choices
                ]

            raise ValueError

        except DuplicateSelectionError:
            print("\nDuplicate selections are not allowed.\n")

        except ValueError:
            print("\nInvalid selection.\n")