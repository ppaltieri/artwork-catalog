def selected_collection_menu() -> int:
    options =[
        "View collection",
        "Edit collection",
        "Add artworks",
        "Remove artworks",
        "Export collection",
        "Delete collection",
        "Back",
    ]

    while True:
        for n, option in enumerate(options, start=1):
            print(f"{n}. {option}")

        try:
            choice = int(input("\nSelect an option: "))
            if 0 < choice <= len(options):
                return choice

            raise ValueError
        
        except ValueError:
            print("Invalid option.")