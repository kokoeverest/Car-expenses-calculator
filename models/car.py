from models.engine import Engine
from models.tax import Tax
from models.tire import Tire


class Car:
    brand: str
    model: str
    year: int
    engine: Engine | None = None
    tax: Tax | None = None
    tires: Tire | None = None
    price: float | None = None
    insurance: int | None = None

    @classmethod
    def create_car(cls, brand, model, year, engine, tax, tires, price):
        return cls(brand = brand,
                   model = model,
                   year = year,
                   engine = engine,
                   tax = tax, 
                   tires = tires,
                   price = price)