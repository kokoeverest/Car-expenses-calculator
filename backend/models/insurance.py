from datetime import datetime
from enum import Enum  # YAGNI
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
    driver_experience: str = "5"
    min_price: float = 0
    max_price: float = 0
    date: datetime | None = None

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
        driver_experience,
    ):
        return cls(
            year=year,
            engine_size=engine_size,
            fuel_type=fuel_type,
            power=power,
            municipality=municipality,
            registration=registration,
            driver_age=driver_age,
            driver_experience=driver_experience,
        )
