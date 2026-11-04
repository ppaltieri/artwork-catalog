from datetime import datetime
from pathlib import Path

import pytest
from PIL import Image

from artwork_catalog import input_funcs

from artwork_catalog.input_funcs import (
    ExitInput,
    BackInput,
    get_input,
    get_image_path,
    get_required_input,
    get_year_input,
    get_descriptive_input,
    get_float_input,
    get_depth_input,
    get_unit_input,
)


@pytest.mark.parametrize(
    "entry, expected",
    [
        ("  Sunset  ", "Sunset"),
        ("", ""),
        ("  /exit  ", "/exit"),
    ],
)
def test_get_input_normal(monkeypatch, entry, expected):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: entry,
    )

    result = get_input("Title: ", commands=False)

    assert result == expected


def test_get_input_exit_commands_true(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "/exit")

    with pytest.raises(ExitInput):
        get_input("test", commands=True)


def test_get_input_exit_commands_false(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "/exit")

    result = get_input("test", commands=False)

    assert result == "/exit"


def test_get_input_back_commands_true(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "/back")
    
    with pytest.raises(BackInput):
        get_input("test", commands=True)


def test_get_input_back_commands_false(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "/back")

    result = get_input("test", commands=False)

    assert result == "/back"


@pytest.mark.parametrize(
    "invalid, expected_message",
    [
        ("missing", "Path file not found."),
        ("directory", "Path must point to a valid file."),
        ("empty", "Image path can't be empty."),
    ],
)

def test_get_image_path(
    invalid, expected_message, tmp_path, monkeypatch, capsys
):
    image_path = tmp_path / "painting.jpg"
    image = Image.new("RGB", (10, 10))
    image.save(image_path)

    invalid_paths = {
        "missing": str(tmp_path / "missing.jpg"),
        "directory": str(tmp_path),
        "empty": "",
    }

    inputs = iter([invalid_paths[invalid], str(image_path)])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    result = get_image_path("Image file: ")
    captured = capsys.readouterr()

    assert expected_message in captured.out
    assert result == image_path


def test_get_image_path_non_image_file(tmp_path, monkeypatch, capsys):
    text_path = tmp_path / "test.txt"
    text_path.write_text("This is not an image.")

    image_path = tmp_path / "painting.jpg"
    image = Image.new("RGB", (10, 10))
    image.save(image_path)

    inputs = iter([str(text_path), str(image_path)])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = get_image_path("Image file: ")
    captured = capsys.readouterr()

    assert "File is not a valid image." in captured.out
    assert result == image_path


def test_get_image_path_oserror(tmp_path, monkeypatch, capsys):
    bad_path = tmp_path / "broken.jpg"
    bad_path.write_bytes(b"fake image")

    valid_path = tmp_path / "valid.jpg"
    Image.new("RGB", (10, 10)).save(valid_path)

    real_open = Image.open

    def fake_open(path):
        if Path(path) == bad_path:
            raise OSError("Cannot read image")
        return real_open(path)

    monkeypatch.setattr(input_funcs.Image, "open", fake_open)

    inputs = iter([str(bad_path), str(valid_path)])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    result = get_image_path("Image file: ")
    captured = capsys.readouterr()

    assert "File is not a valid image." in captured.out
    assert result == valid_path


def test_get_required_input(monkeypatch, capsys):
    inputs = iter(["", "test"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = get_required_input("Title: ")
    captured = capsys.readouterr()

    assert "This field can't be empty" in captured.out
    assert result == "test"


@pytest.mark.parametrize(
    "year, expected_message",
    [
        ("abc", "Only numbers are allowed."),
        ("123", "Please enter a four-digit year."),
        ("0999", "Please enter a year between"),
        ("3000", "Please enter a year between"),
    ],
)
def test_get_year_input(
    year, expected_message, monkeypatch, capsys
):
    current_year = datetime.now().year
    inputs = iter([year, str(current_year)])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    result = get_year_input("Year: ")
    captured = capsys.readouterr()

    assert expected_message in captured.out
    assert result == current_year


def test_get_year_input_minimum(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1000",
    )

    assert get_year_input("Year: ") == 1000


@pytest.mark.parametrize(
    "entry, expected_message",
    [
        ("", "This field can't be empty."),
        ("123", "This field can't contain only numbers."),
    ]
)
def test_get_descriptive_input(entry, expected_message, monkeypatch, capsys):
    inputs = iter([entry, "Watercolor"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = get_descriptive_input("Medium, Techniques or Materials: ")
    captured = capsys.readouterr()

    assert expected_message in captured.out
    assert result == "Watercolor"


def test_get_float_input(monkeypatch, capsys):
    inputs = iter(["-1", "abc", "29"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = get_float_input("Height or Width: ")
    captured = capsys.readouterr()

    assert "Value must be a finite positive number." in captured.out
    assert "Please enter a valid number." in captured.out
    assert result == 29.0


def test_get_float_input_zero(monkeypatch, capsys):
    inputs = iter(["0", "10"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    result = get_float_input("Width: ")
    captured = capsys.readouterr()

    assert "Value must be a finite positive number." in captured.out
    assert result == 10.0


@pytest.mark.parametrize("invalid", ["nan", "inf", "-inf"])
def test_get_float_input_nonfinite(
    monkeypatch, capsys, invalid
):
    inputs = iter([invalid, "10"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    result = get_float_input("Width: ")
    captured = capsys.readouterr()

    assert "Value must be a finite positive number." in captured.out
    assert result == 10.0


@pytest.mark.parametrize(
    "entry, expected_message",
    [
        ("-1", "Value must be a finite non-negative number."),
        ("abc", "Please enter a valid number."),
    ]
)

def test_get_depth_input(entry, expected_message, monkeypatch, capsys):
    inputs = iter([entry, "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = get_depth_input("Depth: ")
    captured = capsys.readouterr()

    assert expected_message in captured.out
    assert result == 2.0


@pytest.mark.parametrize("entry", ["", "  ", "0"])
def test_get_depth_input_none(entry, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: entry)
    result = get_depth_input("Depth: ")

    assert result is None


@pytest.mark.parametrize("invalid", ["nan", "inf", "-inf"])
def test_get_depth_input_nonfinite(
    monkeypatch, capsys, invalid
):
    inputs = iter([invalid, "2"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    result = get_depth_input("Depth: ")
    captured = capsys.readouterr()

    assert "Value must be a finite non-negative number." in captured.out
    assert result == 2.0


@pytest.mark.parametrize(
    "entry, expected_message",
    [
        ("abc", "Please choose one of the listed numbers."),
        ("7", "Please choose one of the listed numbers."),
    ]
)
def test_get_unit_input(entry, expected_message, monkeypatch, capsys):
    inputs = iter([entry, "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = get_unit_input("List number: ")
    captured = capsys.readouterr()

    assert expected_message in captured.out
    assert result == "cm"


@pytest.mark.parametrize(
    "entry, expected",
    [
        ("1", "mm"),
        ("2", "cm"),
        ("3", "m"),
        ("4", "in"),
        ("5", "ft"),
    ],
)
def test_get_unit_input_predefined(
    monkeypatch, entry, expected
):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: entry,
    )

    assert get_unit_input("Unit: ") == expected


def test_get_unit_input_custom(monkeypatch):
    inputs = iter(["6", "pixels"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = get_unit_input("List number: ")

    assert result == "pixels"


def test_get_unit_input_custom_empty(monkeypatch, capsys):
    inputs = iter(["6", "", "pixels"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    result = get_unit_input("Unit: ")
    captured = capsys.readouterr()

    assert "This field can't be empty." in captured.out
    assert result == "pixels"