from pydantic import BaseModel


class Tire(BaseModel):
    width: str
    height: str
    prefix: str = "R"
    size: str
    min_price: float = 0
    max_price: float = 0

    def __repr__(self) -> str:
        return f"{self.width}/{self.height}{self.prefix}{self.size}"

    def __str__(self) -> str:
        return f"{self.width}/{self.height}{self.prefix}{self.size}"

    def __eq__(self, other) -> bool:
        return (
            f"{self.width}/{self.height}{self.prefix}{self.size}"
            == f"{other.width}/{other.height}{other.prefix}{other.size}"
        )

    def __hash__(self) -> int:
        return hash(f"{self.width}/{self.height}{self.prefix}{self.size}")
