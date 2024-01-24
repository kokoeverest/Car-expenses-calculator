from models.engine import Engine
from models.tax import Tax
from models.tire import Tire


class Car:
    # brand: str
    # model: str
    # year: int
    # engine: Engine | None = None
    # tax: Tax | None = None
    # tires: list[Tire]|None = []
    # price: float | None = None
    # insurance: int | None = None

    # @classmethod
    # def create_car(cls, brand, model, year, engine, tax, tires, price):
    #     return cls(brand = brand,
    #                model = model,
    #                year = year,
    #                engine = engine,
    #                tax = tax, 
    #                tires = tires,
    #                price = price)
    
    def __init__(
        self, 
        brand: str, 
        model: str, 
        year: str, 
        engine: Engine | None = None, 
        tax: Tax | None = None,
        tires: list[Tire] | None = [],
        price: float | str | None = None,
        insurance: int | None = None
        ):

        self.brand = brand
        self.model = model
        self.year = year
        self.engine = engine
        self.tax = tax 
        self.tires = tires
        self.price = price
        self.insurance = insurance