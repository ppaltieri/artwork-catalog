from copy import deepcopy

from .collection import Collection
from .input_funcs import get_required_input, get_input


def edit_collection(collection: Collection) -> Collection | None:
    edited_collection = deepcopy(collection)

    fields = ["Name", "Description"]

    while True:
        for n, field in enumerate(fields, start=1):
            print(f"{n}. {field}")

        save_option = len(fields) + 1
        cancel_option = len(fields) + 2
        print()
        print(f"{save_option}. Save changes")
        print(f"{cancel_option}. Cancel")

        try:
            choice = int(input("\nSelect an option: "))

            if 0 < choice <= len(fields):
                if choice == 1:
                    edited_collection.name = get_required_input("New name: ", commands=False)

                elif choice == 2:
                    edited_collection.description = get_input("New description: ", commands=False) or None

            elif choice == save_option:
                return edited_collection

            elif choice == cancel_option:
                return None

            else:
                raise ValueError

        except ValueError:
            print("\nInvalid option.\n")