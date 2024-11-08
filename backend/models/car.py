from models.engine import Engine
from models.insurance import Insurance
from models.tax import Tax
from models.tire import Tire
from pydantic import BaseModel


class Car(BaseModel):
    id: int | None = None
    brand: str
    model: str
    year: str
    engine: Engine | None = None
    tax: Tax | None = None
    tires: list[Tire] | str = [] 
    price: str | float = 0
    insurance: Insurance | None = None
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
        if self.engine is not None:
            return {
                "Марка": self.brand,
                "Модел": self.model,
                "Година": self.year,
                "Двигател": f"{self.engine.capacity} куб.см.",
                "Мощност": f"{self.engine.power_hp} кс",
                "Гориво": self.engine.fuel,
                "Среден разход": f"{self.engine.consumption:.2f} л/100 км",
                "Цена": f"{self.price}" if self.price else None,
            }

    def calculate_tires_price(self):
        max_price = max(
            (tire.max_price for tire in self.tires if tire.max_price), default=0  # type: ignore
        )
        min_price = min(
            (tire.min_price for tire in self.tires if tire.min_price), default=0 # type:ignore
        )

        return max_price * 4, min_price * 4
