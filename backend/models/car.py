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
    def from_query(cls, id, brand, model, year, tires, vignette, seats):
        return cls(
            id=id,
            brand=brand,
            model=model,
            year=year,
            tires=tires,
            vignette=vignette,
            seats=seats,
        )
