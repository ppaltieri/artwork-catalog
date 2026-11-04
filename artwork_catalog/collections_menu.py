def collections_menu() -> int:
    options = [
        "Create collection",
        "Browse collections",
        "Search collections",
        "Back",
    ]

    while True:
        print()
        for n, option in enumerate(options, start=1):
            print(f"{n}. {option}")

        try:
            choice = int(input("\nSelect an option: "))
            if 0 < choice <= len(options):
                return choice

            raise ValueError
        except ValueError:
            print("\nInvalid option.\n")