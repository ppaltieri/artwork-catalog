
import pytest

from artwork_catalog.selected_collection_menu import selected_collection_menu


@pytest.mark.parametrize("choice", range(1, 8))
def test_selected_collection_menu_valid_options(
    monkeypatch, capsys, choice
):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: str(choice),
    )

    result = selected_collection_menu()
    captured = capsys.readouterr()

    expected_options = [
        "1. View collection",
        "2. Edit collection",
        "3. Add artworks",
        "4. Remove artworks",
        "5. Export collection",
        "6. Delete collection",
        "7. Back",
    ]

    for option in expected_options:
        assert option in captured.out

    assert result == choice


@pytest.mark.parametrize(
    "invalid",
    ["abc", "0", "8", "-1", "1.5", ""],
)
def test_selected_collection_menu_invalid_options(
    monkeypatch, capsys, invalid
):
    entries = iter([invalid, "2"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(entries),
    )

    result = selected_collection_menu()
    captured = capsys.readouterr()

    assert "Invalid option." in captured.out
    assert result == 2


def test_selected_collection_menu_multiple_invalid(
    monkeypatch, capsys
):
    entries = iter(["abc", "0", "8", "7"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(entries),
    )

    result = selected_collection_menu()
    captured = capsys.readouterr()

    assert captured.out.count("Invalid option.") == 3
    assert result == 7
