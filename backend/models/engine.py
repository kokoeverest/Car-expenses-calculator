from pydantic import BaseModel


class Engine(BaseModel):
    # class Engine:
    id: int | None = None
    capacity: str
    power_hp: str
    power_kw: str
    fuel_type: str
    emissions_category: str
    consumption: float | None = None
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
            fuel_type=f_type,
            capacity=cap,
            oil_capacity=oil_cap,
            consumption=cons,
            emissions_category=eur_category,
            oil_type=type_oil,
        )

    def __repr__(self) -> str:
        return (
            f"{__class__}, capacity: {self.capacity}, {self.fuel_type}, {self.power_hp}"
        )
