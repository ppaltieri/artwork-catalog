from datetime import datetime
from math import isfinite
from pathlib import Path

from PIL import Image, UnidentifiedImageError


class ExitInput(Exception):
    pass


class BackInput(Exception):
    pass


def get_input(prompt: str, commands: bool = True) -> str:
    value = input(prompt).strip()

    if commands:
        if value == "/exit":
            raise ExitInput        
        elif value == "/back":
            raise BackInput

    return value


def get_image_path(prompt: str, commands: bool = True) -> Path:
    while True:
        image_path = get_input(prompt, commands=commands)

        if not image_path:
            print("Image path can't be empty.")
            continue
        p = Path(image_path)

        if not p.exists():
            print("Path file not found.")
            continue

        if not p.is_file():
            print("Path must point to a valid file.")
            continue

        try:
            with Image.open(p) as image:
                image.verify()
        except (UnidentifiedImageError, OSError):
            print("File is not a valid image.")
            continue

        return p


def get_required_input(prompt: str, commands: bool = True) -> str:
    while True:
        value = get_input(prompt, commands=commands)

        if not value:
            print("This field can't be empty.")
            continue

        return value


def get_year_input(prompt: str, commands: bool = True) -> int:
    current_year = datetime.now().year

    while True:
        value = get_input(prompt, commands=commands)

        if not value.isdigit():
            print("Only numbers are allowed.")
            continue

        if len(value) != 4:
            print("Please enter a four-digit year.")
            continue

        year = int(value)
        if not 1000 <= year <= current_year:
            print(f"Please enter a year between 1000 and {current_year}.")
            continue

        return year


def get_descriptive_input(prompt: str, commands: bool = True) -> str:
    while True:
        value = get_input(prompt, commands=commands)

        if not value:
            print("This field can't be empty.")
            continue

        if value.isdigit():
            print("This field can't contain only numbers.")
            continue

        return value


def get_float_input(prompt: str, commands: bool = True) -> float:
    while True:
        try:
            value = float(get_input(prompt, commands=commands))

            if not isfinite(value) or value <= 0:
                print("Value must be a finite positive number.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number.")


def get_depth_input(prompt: str, commands: bool = True) -> float | None:
    while True:
        value = get_input(prompt, commands=commands)

        if not value:
            return None

        try:
            value = float(value)
            if not isfinite(value) or value < 0:
                print("Value must be a finite non-negative number.")
                continue

            if value == 0:
                return None

            return value

        except ValueError:
            print("Please enter a valid number.")


def get_unit_input(prompt: str, commands: bool = True) -> str:
    units = [
        ("Millimeters", "mm"),
        ("Centimeters", "cm"),
        ("Meters", "m"),
        ("Inches", "in"),
        ("Feet", "ft"),
        ("Custom", None),
    ]
    print("Select measurement unit\n")
    for n, (name, abbreviation) in enumerate(units, start=1):
        if abbreviation:
            print(f"{n}. {name} ({abbreviation})")
        else:
            print(f"{n}. {name}")

    while True:
        try:
            choice = int(get_input(prompt, commands=commands))
        except ValueError:
            print("Please choose one of the listed numbers.")
            continue

        if not 1 <= choice <= len(units):
            print("Please choose one of the listed numbers.")
            continue

        name, abbreviation = units[choice - 1]

        if abbreviation is None:
            return get_required_input("Custom unit: ", commands=commands)

        return abbreviation