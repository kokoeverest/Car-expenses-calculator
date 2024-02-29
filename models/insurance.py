from enum import Enum
from pydantic import BaseModel

INSURANCE_FUEL_VALUES = {
    "gasoline": "1",
    "diesel": "2",
    "hybrid_gasoline": "3",
    "hybrid_diesel": "4",
    "gasoline_lpg_cng": "5",
    "diesel_lpg_cng": "6",
    "eev": "7",
    "lpg_cng_only": "8",
}

class Insurance(BaseModel):
    year: str | int
    engine_size: str
    fuel_type: str
    power: str
    municipality: str  # regex needed to match car.tax.city
    registration: bool = False
    driver_age: str | None = None
    driving_experience: str | None = None

    def to_dict(self):
        return {
            "year": self.year,
            "engine_size": self.engine_size,
            "fuel_type": self.fuel_type,
            "power": self.power,
            "municipality": self.municipality,
            "registration": self.registration,
            "driver age": self.driver_age,
            "driving experience": self.driving_experience,
        }


class FuelsDictionary(Enum):
    gasoline = "Бензин"
    diesel = "Дизел"
    lpg = "Пропан Бутан"
    cng = "Метан"
    premium = "Премиум"
