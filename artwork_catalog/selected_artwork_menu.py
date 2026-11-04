def selected_artwork_menu() -> int:
    options = [
        "View details",
        "Edit artwork",
        "Add to collection",
        "Remove from collection",
        "Export artwork",
        "Delete artwork",
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
            print("\nInvalid option.\n")