from uuid import uuid4


class Collection:
    def __init__(
            self,
            name: str,
            artwork_ids: list[str] | None = None,
            description: str | None = None,
            id: str | None = None,
    ):
        self.id = id or str(uuid4())
        self.name = name
        self.artwork_ids = artwork_ids or []
        self.description = description


    def to_dict(self) -> dict[str, str | list[str] | None]:
        return {
            "id": self.id,
            "name": self.name,
            "artwork_ids": self.artwork_ids,
            "description": self.description,
        }