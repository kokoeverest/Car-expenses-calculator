class Engine:
    power_hp: int
    fuel_type: str | None = None
    capacity: float
    oil_capacity: float | None = None
    emissions_category: str

    @classmethod
    def create_engine(cls, power_hp, fuel_type, capacity, oil_capacity, emissions_category):
        return cls(
            power_hp = power_hp,
            fuel_type = fuel_type, 
            capacity = capacity, 
            oil_capacity = oil_capacity, 
            emissions_category = emissions_category)