from .collection import Collection


def select_collection(collections) -> Collection | None:

    while True:
        for n, collection in enumerate(collections, start=1):
            print(f"{n}. {collection.name}")
        back_option = len(collections) + 1
        print(f"\n{back_option}. Back")

        try:
            choice = int(input("\nSelect a collection: "))
            
            if 0 < choice <= len(collections):

                return collections[choice - 1]

            if choice == back_option:

                return None

            raise ValueError

        except ValueError:
            print("\nInvalid option.\n")
            continue