def delete_artwork_confirmation() -> int:
    options = ["Yes", "No"]

    while True:
        print()
        for n, option in enumerate(options, start=1):
            print(f"{n}. {option}")
        try:
            choice = int(input(
                "\nAre you sure "
                "you want to delete "
                "the selected artwork? "
                )
            )
            print()
            
            if 0 < choice <= len(options):
                return choice
            
            raise ValueError

        except ValueError:
            print("\nInvalid option.\n")
            continue


def delete_collection_confirmation() -> int:
    options = ["Yes", "No"]

    while True:
        print()
        for n, option in enumerate(options, start=1):
            print(f"{n}. {option}")
        try:
            choice = int(input(
                "\nAre you sure "
                "you want to delete "
                "the selected collection? "
                )
            )
            print()

            if 0 < choice <= len(options):
                return choice

            raise ValueError

        except ValueError:
            print("\nInvalid option.\n")
            continue


def remove_from_collection_confirmation(collection, artwork):
    options = ["Yes", "No"]

    while True:
        print()
        for n, option in enumerate(options, start=1):
            print(f"{n}. {option}")

        try:
            choice = int(input(
                f"\nAre you sure "
                f"you want to remove "
                f"{artwork.title} from {collection.name}? "
            ))
            if 0 < choice <= len(options):
                return choice

            raise ValueError

        except ValueError:
            print("\nInvalid option.\n")


def remove_multiple_artworks_from_collection_confirmation(collection):
    options = ["Yes", "No"]

    while True:
        print()
        for n, option in enumerate(options, start=1):
            print(f"{n}. {option}")

        try:
            choice = int(input(
                f"\nAre you sure "
                f"you want to remove "
                f"these artworks from {collection.name} ?"
            ))

            if 0 < choice <= len(options):
                return choice

            raise ValueError

        except ValueError:
            print("\nInvalid option.\n")