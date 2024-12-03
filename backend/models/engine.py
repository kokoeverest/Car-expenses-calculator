from pydantic import BaseModel

from models.fuel import Fuel


class Engine(BaseModel):
    id: int | None = None
    capacity: str
    power_hp: str
    power_kw: str
    fuel: Fuel
    emissions_category: str
    consumption: float = 0
    oil_capacity: float = 0
    oil_type: str | None = None

    def __repr__(self) -> str:
        return f"{__class__}, capacity: {self.capacity}, {self.fuel}, {self.power_hp}"
