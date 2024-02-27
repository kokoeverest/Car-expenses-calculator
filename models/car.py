from models.engine import Engine
from models.tax import Tax
from models.tire import Tire
from pydantic import BaseModel


class Car(BaseModel):
    brand: str
    model: str
    year: str
    engine: Engine | None = None
    tax: Tax | None = None
    tires: list[Tire] = []
    price: str | None = None
    insurance: int | None = None
    fuel_consumption: float | None = None
    vignette: float | None = None
    seats: int = 5

    @classmethod
    def create_car(cls, brand, model, year, engine, tax, tires, price):
        return cls(
            brand=brand,
            model=model,
            year=year,
            engine=engine,
            tax=tax,
            tires=tires,
            price=price,
        )

    def to_dict(self):
        return {
            "Марка": self.brand,
            "Модел": self.model,
            "Година": self.year,
            "Двигател": f"{self.engine.capacity} куб.см." if self.engine else None,
            "Мощност": f"{self.engine.power_hp} кс" if self.engine else None,
            "Гориво": self.engine.fuel_type if self.engine else None,
            "Среден разход": f"{self.fuel_consumption} л/100 км",
            "Цена": f"{self.price}" if self.price else None,
        }

    def calculate_tires_price(self):
        max_price = max(
            (tire.max_price for tire in self.tires if tire.max_price), default=0
        )
        min_price = min(
            (tire.min_price for tire in self.tires if tire.min_price), default=0
        )

        return max_price * 4, min_price * 4
