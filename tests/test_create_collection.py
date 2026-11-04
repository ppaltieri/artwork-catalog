from artwork_catalog import create_collection
from artwork_catalog.input_funcs import BackInput


def test_create_collection(monkeypatch):
    monkeypatch.setattr(
        create_collection,
        "get_required_input",
        lambda _: "Paintings"
    )
    monkeypatch.setattr(
        create_collection,
        "get_input",
        lambda _: "",
    )

    result = create_collection.create_collection()

    assert result.id is not None
    assert result.name == "Paintings"
    assert result.artwork_ids == []
    assert result.description is None


def test_create_collection_with_description(monkeypatch):
    monkeypatch.setattr(
        create_collection,
        "get_required_input",
        lambda _: "Paintings"
    )
    monkeypatch.setattr(
        create_collection,
        "get_input",
        lambda _: "Landscape study",
    )

    result = create_collection.create_collection()

    assert result.id is not None
    assert result.name == "Paintings"
    assert result.artwork_ids == []
    assert result.description == "Landscape study"


def test_create_collection_back_at_first_step(monkeypatch):
    name_entries = iter([BackInput, "Paintings"])

    def fake_get_required_input(_):
        value = next(name_entries)

        if value is BackInput:
            raise BackInput

        return value
    
    monkeypatch.setattr(
        create_collection,
        "get_required_input",
        fake_get_required_input,
    )
    monkeypatch.setattr(
        create_collection,
        "get_input",
        lambda _: "Landscape study",
    )

    result = create_collection.create_collection()

    assert result.name == "Paintings"
    assert result.description == "Landscape study"


def test_create_collection_back(monkeypatch):
    name_entries = iter(["Paintings", "New Paintings"])
    description_entries = iter([BackInput, "Landscape study"])

    def fake_get_input(_):
        value = next(description_entries)

        if value is BackInput:
            raise BackInput

        return value

    monkeypatch.setattr(
        create_collection,
        "get_required_input",
        lambda _: next(name_entries),
    )
    monkeypatch.setattr(
        create_collection,
        "get_input",
        fake_get_input,
    )

    result = create_collection.create_collection()

    assert result.name == "New Paintings"
    assert result.description == "Landscape study"