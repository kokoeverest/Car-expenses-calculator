from models.engine import Engine
from models.tax import Tax
from models.tire import Tire
from pydantic import BaseModel


class Car(BaseModel):
    id: int | None = None
    brand: str
    model: str
    year: str | int
    engine: Engine | None = None
    tax: Tax | None = None
    tires: list[Tire] | str = [] 
    price: str | None = None
    insurance: int | None = None
    vignette: float = 87
    seats: int = 5

    @classmethod
    def create_car(cls, id, brand, model, year, tires, vignette, seats):
        return cls(
            id=id,
            brand=brand,
            model=model,
            year=year,
            tires=tires,
            vignette=vignette,
            seats=seats,
        )

    def to_dict(self):
        return {
            "Марка": self.brand,
            "Модел": self.model,
            "Година": self.year,
            "Двигател": f"{self.engine.capacity} куб.см." if self.engine else None,
            "Мощност": f"{self.engine.power_hp} кс" if self.engine else None,
            "Гориво": self.engine.fuel_type if self.engine else None,
            "Среден разход": f"{self.engine.consumption} л/100 км" if self.engine else None,
            "Цена": f"{self.price}" if self.price else None,
        }

    def calculate_tires_price(self):
        max_price = max(
            (tire.max_price for tire in self.tires if tire.max_price), default=0 # type:ignore
        )
        min_price = min(
            (tire.min_price for tire in self.tires if tire.min_price), default=0 # type:ignore
        )

        return max_price * 4, min_price * 4
