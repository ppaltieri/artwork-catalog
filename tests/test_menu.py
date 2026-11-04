
import pytest

from artwork_catalog.menu import menu


@pytest.mark.parametrize("choice", ["1", "2", "3"])
def test_menu_valid_option(monkeypatch, choice):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: choice,
    )

    result = menu()

    assert result == int(choice)


@pytest.mark.parametrize("invalid", ["0", "4", "-1", "abc", "1.5", ""])
def test_menu_invalid_option(monkeypatch, capsys, invalid):
    entries = iter([invalid, "2"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(entries),
    )

    result = menu()
    captured = capsys.readouterr()

    assert "Invalid option." in captured.out
    assert result == 2
