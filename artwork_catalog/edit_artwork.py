from copy import deepcopy

from .artwork import Artwork
from .input_funcs import (
    get_image_path,
    get_required_input,
    get_year_input,
    get_descriptive_input,
    get_float_input,
    get_depth_input,
    get_unit_input,
)


def edit_artwork(artwork: Artwork) -> Artwork | None:
    edited_artwork = deepcopy(artwork)
    dimensions = ["Height", "Width", "Depth", "Unit"]
    fields = [
        "Image",
        "Title",
        "Year",
        "Medium",
        "Technique",
        "Materials",
        "Dimensions",
        "Notes",
    ]

    while True:
        for n, field in enumerate(fields, start=1):
            print(f"{n}. {field}")

        save_option = len(fields) + 1
        cancel_option = len(fields) + 2
        print()
        print(f"{save_option}. Save changes")
        print(f"{cancel_option}. Cancel")

        try:
            choice = int(input("Select a field: "))
            if 0 < choice <= len(fields):
                if choice == 1:
                    edited_artwork.image_path = get_image_path("New image file: ", commands=False)
                elif choice == 2:
                    edited_artwork.title = get_required_input("New title: ", commands=False)
                elif choice == 3:
                    edited_artwork.year = get_year_input("New year: ", commands=False)
                elif choice == 4:
                    edited_artwork.medium = get_descriptive_input("New medium: ", commands=False)
                elif choice == 5:
                    edited_artwork.technique = get_descriptive_input("New technique: ", commands=False)
                elif choice == 6:
                    edited_artwork.materials = get_descriptive_input("New materials: ", commands=False)
                elif choice == 7:
                    edited_dimensions = deepcopy(edited_artwork.dimensions)
                    while True:
                        for n_2, field_2 in enumerate(dimensions, start=1):
                            print(f"{n_2}. {field_2}")

                        save_option_2 = len(dimensions) + 1
                        cancel_option_2 = len(dimensions) + 2

                        print()
                        print(f"{save_option_2}. Save and go back")
                        print(f"{cancel_option_2}. Cancel")

                        try:
                            d_choice = int(input("Select a field: "))
                            if 0 < d_choice <= len(dimensions):
                                if d_choice == 1:
                                    edited_dimensions.height = get_float_input("New height: ", commands=False)
                                elif d_choice == 2:
                                    edited_dimensions.width = get_float_input("New width: ", commands=False)                                    
                                elif d_choice == 3:
                                    edited_dimensions.depth = get_depth_input("New depth: ", commands=False)
                                elif d_choice == 4:
                                    edited_dimensions.unit = get_unit_input("New unit: ", commands=False)

                            elif d_choice == save_option_2:
                                edited_artwork.dimensions = edited_dimensions
                                break

                            elif d_choice == cancel_option_2:
                                break

                            else:
                                raise ValueError

                        except ValueError:
                            print("Invalid option.")
                            continue                

                elif choice == 8:
                    edited_artwork.notes = input("New notes: ").strip() or None

            elif choice == save_option:
                return edited_artwork

            elif choice == cancel_option:
                return None

            else:
                raise ValueError
            
        except ValueError:
            print("Invalid option.")