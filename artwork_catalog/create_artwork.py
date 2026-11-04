from .artwork import Artwork
from .dimensions import Dimensions
from .input_funcs import (
    BackInput,
    get_image_path,
    get_input,
    get_required_input,
    get_year_input,
    get_descriptive_input,
    get_float_input,
    get_depth_input,
    get_unit_input,
)


def create_artwork():
    step = 0
    print()
    print("- Type /exit to cancel creation -")
    print("- Type /back to return to the previous field -\n")
    
    while step <= 10:
        try:
            if step == 0:
                image_path = get_image_path("Image file: ")
              
            elif step == 1:
                title = get_required_input("Title: ")

            elif step == 2:
                year = get_year_input("Year: ")
            
            elif step == 3:
                medium = get_descriptive_input("Medium: ")
            
            elif step == 4:
                technique = get_descriptive_input("Technique: ")
            
            elif step == 5:
                materials = get_descriptive_input("Materials: ")
            
            elif step == 6:
                height = get_float_input("Height: ")
            
            elif step == 7:
                width = get_float_input("Width: ")
            
            elif step == 8:
                depth = get_depth_input("Depth (leave blank if not applicable): ")
            
            elif step == 9:
                unit = get_unit_input("\nList number: ")
            
            elif step == 10:
                notes = get_input("Notes: ") or None

            step += 1
        except BackInput:
            if step > 0:
                step -= 1

    dimensions = Dimensions(height, width, depth, unit)

    return Artwork(
        image_path=image_path,
        title=title,
        year=year,
        medium=medium,
        technique=technique,
        materials=materials,
        dimensions=dimensions,
        notes=notes,
    )