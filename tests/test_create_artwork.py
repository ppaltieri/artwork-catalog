from artwork_catalog import create_artwork
from artwork_catalog.input_funcs import BackInput


def test_create_artwork(monkeypatch):
    descriptions = iter([
        "Watercolor on paper",
        "wet-on-wet",
        "paint, paper",
    ])

    floats = iter([29, 21])

    monkeypatch.setattr(create_artwork, "get_image_path", lambda _: "painting.jpg")
    monkeypatch.setattr(create_artwork, "get_required_input", lambda _: "Test")
    monkeypatch.setattr(create_artwork, "get_year_input", lambda _: 2026)
    monkeypatch.setattr(
        create_artwork,
        "get_descriptive_input",
        lambda _: next(descriptions),
    )
    monkeypatch.setattr(create_artwork, "get_float_input", lambda _: next(floats))
    monkeypatch.setattr(create_artwork, "get_depth_input", lambda _: None)
    monkeypatch.setattr(create_artwork, "get_unit_input", lambda _: "cm")
    monkeypatch.setattr(create_artwork, "get_input", lambda _: "")

    result = create_artwork.create_artwork()

    assert result.image_path == "painting.jpg"
    assert result.title == "Test"
    assert result.year == 2026
    assert result.medium == "Watercolor on paper"
    assert result.technique == "wet-on-wet"
    assert result.materials == "paint, paper"
    assert result.dimensions.height == 29
    assert result.dimensions.width == 21
    assert result.dimensions.depth is None
    assert result.dimensions.unit == "cm"
    assert result.notes is None


def test_create_artwork_with_notes(monkeypatch):
    descriptions = iter([
        "Watercolor on paper",
        "wet-on-wet",
        "paint, paper",
    ])

    floats = iter([29, 21])

    monkeypatch.setattr(create_artwork, "get_image_path", lambda _: "painting.jpg")
    monkeypatch.setattr(create_artwork, "get_required_input", lambda _: "Test")
    monkeypatch.setattr(create_artwork, "get_year_input", lambda _: 2026)
    monkeypatch.setattr(
        create_artwork,
        "get_descriptive_input",
        lambda _: next(descriptions),
    )
    monkeypatch.setattr(create_artwork, "get_float_input", lambda _: next(floats))
    monkeypatch.setattr(create_artwork, "get_depth_input", lambda _: None)
    monkeypatch.setattr(create_artwork, "get_unit_input", lambda _: "cm")
    monkeypatch.setattr(create_artwork, "get_input", lambda _: "Landscape study")

    result = create_artwork.create_artwork()

    assert result.notes == "Landscape study"


def test_create_artwork_back(monkeypatch):
    descriptions = iter([
        "Watercolor on paper",
        "wet-on-wet",
        "paint, paper",
    ])

    floats = iter([21, 29])
    title_entries = iter(["Test", "New Title"])
    year_entries = iter([BackInput, 2026])

    def fake_get_year_input(_):
        value = next(year_entries)

        if value is BackInput:
            raise BackInput

        return value

    monkeypatch.setattr(create_artwork, "get_image_path", lambda _: "painting.jpg")
    monkeypatch.setattr(create_artwork, "get_required_input", lambda _: next(title_entries))
    monkeypatch.setattr(create_artwork, "get_year_input", fake_get_year_input)
    monkeypatch.setattr(
        create_artwork,
        "get_descriptive_input",
        lambda _: next(descriptions),
    )
    monkeypatch.setattr(create_artwork, "get_float_input", lambda _: next(floats))
    monkeypatch.setattr(create_artwork, "get_depth_input", lambda _: None)
    monkeypatch.setattr(create_artwork, "get_unit_input", lambda _: "cm")
    monkeypatch.setattr(create_artwork, "get_input", lambda _: "")

    result = create_artwork.create_artwork()

    assert result.title == "New Title"
    assert result.year == 2026


def test_create_artwork_back_at_first_step(monkeypatch):
    image_entries = iter([BackInput, "painting.jpg"])
    descriptions = iter([
        "Watercolor on paper",
        "wet-on-wet",
        "paint, paper",
    ])
    
    floats = iter([29, 21])

    def fake_get_image_path(_):
        value = next(image_entries)

        if value is BackInput:
            raise BackInput

        return value

    monkeypatch.setattr(create_artwork, "get_image_path", fake_get_image_path)
    monkeypatch.setattr(create_artwork, "get_required_input", lambda _: "Test")
    monkeypatch.setattr(create_artwork, "get_year_input", lambda _: 2026)
    monkeypatch.setattr(
        create_artwork,
        "get_descriptive_input",
        lambda _: next(descriptions),
    )
    monkeypatch.setattr(create_artwork, "get_float_input", lambda _: next(floats))
    monkeypatch.setattr(create_artwork, "get_depth_input", lambda _: None)
    monkeypatch.setattr(create_artwork, "get_unit_input", lambda _: "cm")
    monkeypatch.setattr(create_artwork, "get_input", lambda _: "")

    result = create_artwork.create_artwork()

    assert result.image_path == "painting.jpg"
    assert result.title == "Test"