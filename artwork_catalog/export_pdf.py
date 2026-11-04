from html import escape
from pathlib import Path

from PIL import Image
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from .artwork import Artwork
from .collection import Collection


PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)

def _draw_artwork_page(pdf: canvas.Canvas, artwork: Artwork) -> None:

    with Image.open(artwork.image_path) as image:
        original_width, original_height = image.size

# Image handling
    max_width = 160 * mm
    max_height = 105 * mm

    scale = min(
        max_width / original_width,
        max_height / original_height,
    )

    draw_width = original_width * scale
    draw_height = original_height * scale

    image_x = (PAGE_WIDTH - draw_width) / 2
    image_y = PAGE_HEIGHT - 20 * mm - draw_height

    pdf.drawImage(
        str(artwork.image_path),
        image_x,
        image_y,
        width=draw_width,
        height=draw_height,
    )


# Text handling
    styles = getSampleStyleSheet()
    body_style = styles["BodyText"]
    body_style.fontName = "Helvetica"
    body_style.fontSize = 11
    body_style.leading = 14
    body_style.alignment = TA_CENTER

    paragraph_width = 180 * mm
    text_x = (PAGE_WIDTH - paragraph_width) / 2
    text_y = image_y - 8 * mm

    details = [
        ("Title", artwork.title),
        ("Year", str(artwork.year)),
        ("Medium", artwork.medium),
        ("Technique", artwork.technique),
        ("Materials", artwork.materials),
        ("Dimensions", str(artwork.dimensions)),
    ]

    if artwork.notes:
        details.append(("Notes", artwork.notes))

    for label, value in details:
        paragraph = Paragraph(
            f"<b>{label}:</b> {escape(value)}",
            body_style,
        )

        _, height = paragraph.wrap(
            paragraph_width,
            PAGE_HEIGHT,
        )

        text_y -= height

        paragraph.drawOn(
            pdf,
            text_x,
            text_y,
        )

        text_y -= 2 * mm


def _draw_collection_cover(pdf: canvas.Canvas, collection: Collection) -> None:
    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    body_style = styles["BodyText"]

    title = Paragraph(
        escape(collection.name),
        title_style,
    )

    _, height = title.wrap(400, 100)
    title.drawOn(pdf, 100, 650 - height)

    if collection.description:
        description = Paragraph(
            escape(collection.description),
            body_style,
        )

        _, height = description.wrap(400, 200)
        description.drawOn(pdf, 100, 580 - height)


def export_artwork_pdf(artwork: Artwork, output_path: str | Path) -> None:
    output_path = Path(output_path).with_suffix(".pdf")
    pdf = canvas.Canvas(
        str(output_path),
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
    )

    _draw_artwork_page(pdf, artwork)

    pdf.save()


def export_collection_pdf(
        collection: Collection,
        artworks: list[Artwork],
        output_path: str | Path,
    ) -> None:
    output_path = Path(output_path).with_suffix(".pdf")
    pdf = canvas.Canvas(
        str(output_path),
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
    )

    _draw_collection_cover(pdf, collection)
    pdf.showPage()

    for artwork in artworks:
        _draw_artwork_page(pdf, artwork)
        pdf.showPage()

    pdf.save()