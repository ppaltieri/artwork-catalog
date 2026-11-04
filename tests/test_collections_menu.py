from artwork_catalog.collections_menu import collections_menu


def test_collections_menu_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 1)

    result = collections_menu()

    assert result == 1


def test_collections_menu_invalid_then_valid(monkeypatch, capsys):
    options = iter([0, 5, "abc", 4])

    monkeypatch.setattr("builtins.input", lambda _: next(options))

    result = collections_menu()

    captured = capsys.readouterr()

    assert result == 4
    assert captured.out.count("Invalid option.") == 3
