from unittest.mock import MagicMock

import pytest

from artwork_catalog.artwork import Artwork
from artwork_catalog.collection import Collection
from artwork_catalog.dimensions import Dimensions
from artwork_catalog import export_pdf


@pytest.fixture
def artwork():
    dimensions = Dimensions(29, 21)
    return Artwork(
        "painting.jpg",
        "Test",
        2026,
        "Watercolor on paper",
        "wet-on-wet",
        "paint, paper",
        dimensions,
        "Test notes",
        "artwork-1",
    )


@pytest.fixture
def artwork_without_notes():
    dimensions = Dimensions(29, 21)

    return Artwork(
        "painting.jpg",
        "Test",
        2026,
        "Watercolor on paper",
        "wet-on-wet",
        "paint, paper",
        dimensions,
        None,
        "artwork-1",
    )


@pytest.fixture
def collection():
    return Collection(
        "Paintings",
        ["artwork-1"],
        "Test collection",
        "collection-1",
    )


def test_draw_artwork_page_with_notes(monkeypatch, artwork):
    mock_pdf = MagicMock()

    mock_image = MagicMock()
    mock_image.size = (1000, 500)

    mock_image_context = MagicMock()
    mock_image_context.__enter__.return_value = mock_image

    monkeypatch.setattr(
        export_pdf.Image,
        "open",
        MagicMock(return_value=mock_image_context),
    )

    mock_paragraph = MagicMock()
    mock_paragraph.wrap.return_value = (100, 20)

    mock_paragraph_class = MagicMock(
        return_value=mock_paragraph
    )

    monkeypatch.setattr(
        export_pdf,
        "Paragraph",
        mock_paragraph_class,
    )

    export_pdf._draw_artwork_page(
        mock_pdf,
        artwork,
    )

    mock_pdf.drawImage.assert_called_once()

    assert mock_paragraph_class.call_count == 7
    assert mock_paragraph.wrap.call_count == 7
    assert mock_paragraph.drawOn.call_count == 7


def test_draw_artwork_page_without_notes(
    monkeypatch,
    artwork_without_notes,
):
    mock_pdf = MagicMock()

    mock_image = MagicMock()
    mock_image.size = (500, 1000)

    mock_image_context = MagicMock()
    mock_image_context.__enter__.return_value = mock_image

    monkeypatch.setattr(
        export_pdf.Image,
        "open",
        MagicMock(return_value=mock_image_context),
    )

    mock_paragraph = MagicMock()
    mock_paragraph.wrap.return_value = (100, 20)

    mock_paragraph_class = MagicMock(
        return_value=mock_paragraph
    )

    monkeypatch.setattr(
        export_pdf,
        "Paragraph",
        mock_paragraph_class,
    )

    export_pdf._draw_artwork_page(
        mock_pdf,
        artwork_without_notes,
    )

    assert mock_paragraph_class.call_count == 6


def test_draw_collection_cover_with_description(
    monkeypatch,
    collection,
):
    mock_pdf = MagicMock()

    mock_title = MagicMock()
    mock_title.wrap.return_value = (400, 30)

    mock_description = MagicMock()
    mock_description.wrap.return_value = (400, 40)

    mock_paragraph_class = MagicMock(
        side_effect=[
            mock_title,
            mock_description,
        ]
    )

    monkeypatch.setattr(
        export_pdf,
        "Paragraph",
        mock_paragraph_class,
    )

    export_pdf._draw_collection_cover(
        mock_pdf,
        collection,
    )

    assert mock_paragraph_class.call_count == 2

    mock_title.wrap.assert_called_once_with(
        400,
        100,
    )
    mock_title.drawOn.assert_called_once_with(
        mock_pdf,
        100,
        620,
    )

    mock_description.wrap.assert_called_once_with(
        400,
        200,
    )
    mock_description.drawOn.assert_called_once_with(
        mock_pdf,
        100,
        540,
    )


def test_draw_collection_cover_without_description(
    monkeypatch,
):
    collection = Collection(
        "Paintings",
        [],
        None,
        "collection-1",
    )

    mock_pdf = MagicMock()

    mock_title = MagicMock()
    mock_title.wrap.return_value = (400, 30)

    mock_paragraph_class = MagicMock(
        return_value=mock_title
    )

    monkeypatch.setattr(
        export_pdf,
        "Paragraph",
        mock_paragraph_class,
    )

    export_pdf._draw_collection_cover(
        mock_pdf,
        collection,
    )

    assert mock_paragraph_class.call_count == 1
    mock_title.drawOn.assert_called_once()


def test_export_artwork_pdf(
    monkeypatch,
    artwork,
    tmp_path,
):
    mock_pdf = MagicMock()
    mock_canvas = MagicMock(
        return_value=mock_pdf
    )
    mock_draw = MagicMock()

    monkeypatch.setattr(
        export_pdf.canvas,
        "Canvas",
        mock_canvas,
    )

    monkeypatch.setattr(
        export_pdf,
        "_draw_artwork_page",
        mock_draw,
    )

    output_path = tmp_path / "artwork"

    export_pdf.export_artwork_pdf(
        artwork,
        output_path,
    )

    mock_canvas.assert_called_once_with(
        str(output_path.with_suffix(".pdf")),
        pagesize=(
            export_pdf.PAGE_WIDTH,
            export_pdf.PAGE_HEIGHT,
        ),
    )

    mock_draw.assert_called_once_with(
        mock_pdf,
        artwork,
    )

    mock_pdf.save.assert_called_once()


def test_export_collection_pdf(
    monkeypatch,
    artwork,
    collection,
    tmp_path,
):
    mock_pdf = MagicMock()

    mock_canvas = MagicMock(
        return_value=mock_pdf
    )

    mock_cover = MagicMock()
    mock_draw_artwork = MagicMock()

    monkeypatch.setattr(
        export_pdf.canvas,
        "Canvas",
        mock_canvas,
    )

    monkeypatch.setattr(
        export_pdf,
        "_draw_collection_cover",
        mock_cover,
    )

    monkeypatch.setattr(
        export_pdf,
        "_draw_artwork_page",
        mock_draw_artwork,
    )

    output_path = tmp_path / "collection"

    artworks = [
        artwork,
        artwork,
    ]

    export_pdf.export_collection_pdf(
        collection,
        artworks,
        output_path,
    )

    mock_canvas.assert_called_once_with(
        str(output_path.with_suffix(".pdf")),
        pagesize=(
            export_pdf.PAGE_WIDTH,
            export_pdf.PAGE_HEIGHT,
        ),
    )

    mock_cover.assert_called_once_with(
        mock_pdf,
        collection,
    )

    assert mock_draw_artwork.call_count == 2

    mock_pdf.showPage.assert_called()
    assert mock_pdf.showPage.call_count == 3

    mock_pdf.save.assert_called_once()