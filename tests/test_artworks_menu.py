from artwork_catalog.artworks_menu import artworks_menu


def test_artworks_menu_valid_option(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 1)

    result = artworks_menu()

    assert result == 1

def test_artworks_menu_invalid_options_then_valid(monkeypatch, capsys):
    options = iter([0, 5, "abc", 4])

    monkeypatch.setattr("builtins.input", lambda _: next(options))

    result = artworks_menu()

    captured = capsys.readouterr()

    assert result == 4
    assert captured.out.count("Invalid option.") == 3
    