
import pytest

from artwork_catalog.selected_artwork_menu import selected_artwork_menu


@pytest.mark.parametrize("choice", range(1, 8))
def test_selected_artwork_menu_valid_options(
    monkeypatch, capsys, choice
):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: str(choice),
    )

    result = selected_artwork_menu()
    captured = capsys.readouterr()

    expected_options = [
        "1. View details",
        "2. Edit artwork",
        "3. Add to collection",
        "4. Remove from collection",
        "5. Export artwork",
        "6. Delete artwork",
        "7. Back",
    ]

    for option in expected_options:
        assert option in captured.out

    assert result == choice


@pytest.mark.parametrize(
    "invalid",
    ["abc", "0", "8", "-1", "1.5", ""],
)
def test_selected_artwork_menu_invalid_options(
    monkeypatch, capsys, invalid
):
    entries = iter([invalid, "2"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(entries),
    )

    result = selected_artwork_menu()
    captured = capsys.readouterr()

    assert "Invalid option." in captured.out
    assert result == 2


def test_selected_artwork_menu_multiple_invalid(
    monkeypatch, capsys
):
    entries = iter(["abc", "0", "8", "7"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(entries),
    )

    result = selected_artwork_menu()
    captured = capsys.readouterr()

    assert captured.out.count("Invalid option.") == 3
    assert result == 7
