import pytest

from artwork_catalog.artwork import Artwork
from artwork_catalog.dimensions import Dimensions
from artwork_catalog import edit_artwork


@pytest.fixture
def artwork():
    dimensions = Dimensions(29, 21, 0, "cm")

    return Artwork(
        "image.jpg",
        "Test",
        2026,
        "Ceramics",
        "pinch-pot",
        "clay",
        dimensions,
        None,
    )

@pytest.mark.parametrize(
        "choice, input_func, attribute, old_value, new_value",
        [
            ("1", "get_image_path", "image_path", "image.jpg", "new_image.jpg"),
            ("2", "get_required_input", "title", "Test", "New Title"),
            ("3", "get_year_input", "year", 2026, 2020),
            ("4", "get_descriptive_input", "medium", "Ceramics", "Watercolor"),
            ("5", "get_descriptive_input", "technique", "pinch-pot", "wet-on-wet"),
            ("6", "get_descriptive_input", "materials", "clay", "paint, paper"),
        ],
)
def test_edit_artwork_updates_selected_fields(
    monkeypatch,
    artwork,
    choice,
    input_func,
    attribute,
    old_value,
    new_value,
):
    entries = iter([choice, "9"])

    monkeypatch.setattr("builtins.input", lambda _: next(entries))
    monkeypatch.setattr(edit_artwork, input_func, lambda _, commands=False: new_value)

    result = edit_artwork.edit_artwork(artwork)

    assert result is not None
    assert getattr(result, attribute) == new_value
    assert getattr(artwork, attribute) == old_value


def test_edit_artwork_edit_and_cancel(monkeypatch, artwork):
    entries = iter(["2", "10"])

    monkeypatch.setattr("builtins.input", lambda _: next(entries))
    monkeypatch.setattr(
        edit_artwork,
        "get_required_input",
        lambda _, commands=False: "New title.jpg",
    )

    result = edit_artwork.edit_artwork(artwork)

    assert result is None
    assert artwork.title == "Test"


def test_edit_artwork_menu_bad_entries(monkeypatch, capsys, artwork):
    entries = iter(["abc", "0", "11", "10"])

    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    edit_artwork.edit_artwork(artwork)

    captured = capsys.readouterr()

    assert captured.out.count("Invalid option.") == 3


def test_edit_artwork_dimensions_submenu_bad_entries(
    monkeypatch,
    capsys,
    artwork,
):
    entries = iter(["7", "abc", "0", "7", "6", "10"])

    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    edit_artwork.edit_artwork(artwork)

    captured = capsys.readouterr()

    assert captured.out.count("Invalid option.") == 3


@pytest.mark.parametrize(
        "choice, input_func, attribute, old_value, new_value",
        [
            ("1", "get_float_input", "height", 29, 15),
            ("2", "get_float_input", "width", 21, 10),
            ("3", "get_depth_input", "depth", None, 20),
            ("4", "get_unit_input", "unit", "cm", "in"),
        ],
)
def test_edit_artwork_updates_dimensions_fields(
    monkeypatch,
    artwork,
    choice,
    input_func,
    attribute,
    old_value,
    new_value,
):
    entries = iter(["7", choice, "5", "9"])

    monkeypatch.setattr("builtins.input", lambda _: next(entries))
    monkeypatch.setattr(
        edit_artwork,
        input_func,
        lambda _, commands=False: new_value,
    )

    result = edit_artwork.edit_artwork(artwork)

    assert result is not None
    assert getattr(artwork.dimensions, attribute) == old_value
    assert getattr(result.dimensions, attribute) == new_value


def test_edit_artwork_dimensions_edit_and_cancel_submenu(monkeypatch, artwork):
    entries = iter(["7", "1", "6", "9"])

    monkeypatch.setattr("builtins.input", lambda _: next(entries))
    monkeypatch.setattr(
        edit_artwork,
        "get_float_input",
        lambda _, commands=False: 10,
    )

    result = edit_artwork.edit_artwork(artwork)

    assert result is not None
    assert artwork.dimensions.height == 29
    assert result.dimensions.height == 29


@pytest.mark.parametrize(
        "choice, input_func, attribute, old_value, new_value",
        [
            ("1", "get_float_input", "height", 29, 15),
            ("2", "get_float_input", "width", 21, 10),
            ("3", "get_depth_input", "depth", None, 20),
            ("4", "get_unit_input", "unit", "cm", "in"),
        ],
)
def test_edit_artwork_dimensions_save_then_cancel_all(
    monkeypatch,
    artwork,
    choice,
    input_func,
    attribute,
    old_value,
    new_value,
):
    entries = iter(["7", choice, "5", "10"])

    monkeypatch.setattr("builtins.input", lambda _: next(entries))
    monkeypatch.setattr(
        edit_artwork,
        input_func,
        lambda _, commands=False: new_value,
    )

    result = edit_artwork.edit_artwork(artwork)

    assert result is None
    assert getattr(artwork.dimensions, attribute) == old_value


def test_edit_artwork_updates_notes_none_to_value_stripping(
        monkeypatch,
        artwork,
    ):
    entries = iter(["8", "  New Notes  ", "9"])

    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    result = edit_artwork.edit_artwork(artwork)

    assert result is not None
    assert artwork.notes is None
    assert result.notes == "New Notes"


def test_edit_artwork_updates_notes_value_to_none(monkeypatch, artwork):
    artwork.notes = "Old Notes"
    entries = iter(["8", "", "9"])

    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    result = edit_artwork.edit_artwork(artwork)

    assert result is not None
    assert artwork.notes == "Old Notes"
    assert result.notes is None


def test_edit_artwork_save_without_changes(monkeypatch, artwork):
    monkeypatch.setattr("builtins.input", lambda _: "9")

    result = edit_artwork.edit_artwork(artwork)

    assert result is not None
    assert result is not artwork
    assert result.to_dict() == artwork.to_dict()