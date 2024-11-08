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
    oil_capacity: str | None = None
    oil_type: str | None = None

    @classmethod
    def from_query(
        cls, id, cap, pow_hp, pow_kw, f_type, eur_category, cons, oil_cap, type_oil
    ):
        return cls(
            id=id,
            power_hp=pow_hp,
            power_kw=pow_kw,
            fuel=f_type,
            capacity=cap,
            oil_capacity=oil_cap,
            consumption=cons,
            emissions_category=eur_category,
            oil_type=type_oil,
        )

    def __repr__(self) -> str:
        return (
            f"{__class__}, capacity: {self.capacity}, {self.fuel}, {self.power_hp}"
        )
