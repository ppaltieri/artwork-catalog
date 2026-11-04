from .collection import Collection
from .input_funcs import get_required_input, get_input, BackInput

def create_collection():
    step = 0
    print()
    print("- Type /exit to cancel creation -")
    print("- Type /back to return to the previous field -\n")

    while step <= 1:
        try:
            if step == 0:
                name = get_required_input("Name: ")

            elif step == 1:
                description = get_input("Description: ") or None

            step += 1
        except BackInput:
            if step > 0:
                step -= 1

    return Collection(
        name=name,
        description=description,
    )
