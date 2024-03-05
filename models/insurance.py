from datetime import datetime
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
    id: int | None = None
    year: str
    engine_size: str
    fuel_type: str
    power: str
    municipality: str
    registration: bool = False
    driver_age: str | None = None
    driving_experience: str = "5"
    min_price: float = 0
    max_price: float = 0
    date: datetime | None = None

    @classmethod
    def from_query(
        cls,
        id,
        year,
        engine_size,
        fuel_type,
        power,
        municipality,
        registration,
        driver_age,
        driving_experience,
        min_price,
        max_price,
        date,
    ):
        return cls(
            id=id,
            year=year,
            engine_size=engine_size,
            fuel_type=fuel_type,
            power=power,
            municipality=municipality,
            registration=registration,
            driver_age=driver_age,
            driving_experience=driving_experience,
            min_price=min_price,
            max_price=max_price,
            date=date,
        )

    @classmethod
    def from_list(
        cls,
        year,
        engine_size,
        fuel_type,
        power,
        municipality,
        registration,
        driver_age,
        driving_experience,
    ):
        return cls(
            year=year,
            engine_size=engine_size,
            fuel_type=fuel_type,
            power=power,
            municipality=municipality,
            registration=registration,
            driver_age=driver_age,
            driving_experience=driving_experience,
        )

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
