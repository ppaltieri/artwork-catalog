from uuid import uuid4


class Artwork:
    def __init__(
        self,
        image_path,
        title,
        year,
        medium,
        technique,
        materials,
        dimensions,
        notes=None,
        id=None,
    ):
        self.image_path = image_path
        self.title = title
        self.year = year
        self.medium = medium
        self.technique = technique
        self.materials = materials
        self.dimensions = dimensions
        self.notes = notes
        self.id = id or str(uuid4())


    def __str__(self):
        return (
            f"\n{self.title}, {self.year}, "
            f"{self.medium}, {self.dimensions}"
        )


    def __repr__(self):
        return f"Artwork({self.title!r}, {self.year!r})"


    def to_dict(self):
        return {
            "image_path": str(self.image_path),
            "title": self.title,
            "year": self.year,
            "medium": self.medium,
            "technique": self.technique,
            "materials": self.materials,
            "dimensions": self.dimensions.to_dict(),
            "notes": self.notes,
            "id": self.id,
        }


    def details(self):
        return (
            f"Image: {self.image_path}\n"
            f"Title: {self.title}\n"
            f"Year: {self.year}\n"
            f"Medium: {self.medium}\n"
            f"Technique: {self.technique}\n"
            f"Materials: {self.materials}\n"
            f"Dimensions:\n"
            f"    Height: {self.dimensions.height}\n"
            f"    Width: {self.dimensions.width}\n"
            f"    Depth: {self.dimensions.depth}\n"
            f"    Unit: {self.dimensions.unit}\n"
            f"Notes: {self.notes}"
        )