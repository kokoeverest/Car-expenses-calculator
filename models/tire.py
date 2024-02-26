import json
from pydantic import BaseModel


class Tire(BaseModel):
    width: str
    height: str
    size: str
    min_price: float | None = None
    max_price: float | None = None


    # def __init__(self, width, height, size, min_price=None, max_price=None) -> None:
    #     self.width = width
    #     self.height = height
    #     self.size = size
    #     self.min_price = min_price
    #     self.max_price = max_price
    
    def __repr__(self) -> str:
        return f"{self.width}/{self.height}R{self.size}"
    
    def __str__(self) -> str:
        return f"{self.width}/{self.height}R{self.size}"
    
    def __eq__(self, other) -> bool:
        return f"{self.width}/{self.height}R{self.size}" == f"{other.width}/{other.height}R{other.size}"
    
    def __hash__(self) -> int:
        return hash(f"{self.width}/{self.height}R{self.size}")
    
    def get_prices_list(self):
        return [f"{self.min_price} лв", f"{self.max_price} лв"]

    def jsonify(self):
        result = {'Размер': self.__repr__(),
                  'Най-ниска цена': self.min_price,
                  'Най-висока цена': self.max_price}
        return json.dumps(result, indent=2, ensure_ascii=False, separators=('', ' - '))