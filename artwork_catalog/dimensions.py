class Dimensions:
    def __init__(
            self,
            height: float,
            width: float,
            depth: float | None = None,
            unit: str = "cm",
        ):

        if height <= 0 or width <= 0:
            raise ValueError("Measures must be positive")
        if depth == 0:
            depth = None
        if depth is not None and depth < 0:
            raise ValueError("Depth cannot be negative")

        self.height = height
        self.width = width
        self.depth = depth
        self.unit = unit

    def __str__(self):
        if self.depth is None:
            return f"{self.height:g} x {self.width:g} {self.unit}"

        return (
            f"{self.height:g} x "
            f"{self.width:g} x "
            f"{self.depth:g} {self.unit}"
        )

    def to_dict(self):
        return {
            "height": self.height,
            "width": self.width,
            "depth": self.depth,
            "unit": self.unit,
        }