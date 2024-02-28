import json
from pydantic import BaseModel


class Tire(BaseModel):
    width: str
    height: str
    prefix: str = "R"
    size: str
    min_price: float | None = None
    max_price: float | None = None

    @classmethod
    def from_query(cls, p, w, h, s, min_price, max_price):
        return cls(
            width=w,
            height=h,
            prefix=p,
            size=s,
            min_price=min_price,
            max_price=max_price,
        )

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

    def get_prices_list(self):
        return [f"{self.min_price} лв", f"{self.max_price} лв"]

    def jsonify(self):
        result = {
            "Размер": self.__repr__(),
            "Най-ниска цена": self.min_price,
            "Най-висока цена": self.max_price,
        }
        return json.dumps(result, indent=2, ensure_ascii=False, separators=("", " - "))
