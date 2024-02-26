from pydantic import BaseModel


class Engine(BaseModel):
# class Engine:
    power_hp: str
    power_kw: str
    capacity: str
    emissions_category: str
    fuel_type: str
    oil_capacity: str | None = None

    @classmethod
    def create_engine(cls, power_hp, power_kw, fuel_type, capacity, oil_capacity, emissions_category):
        return cls(
            power_hp = power_hp,
            power_kw = power_kw,
            fuel_type = fuel_type, 
            capacity = capacity, 
            oil_capacity = oil_capacity, 
            emissions_category = emissions_category)
    
    # def __init__(self, 
    #     power_hp: str, 
    #     capacity: str, 
    #     emissions_category: str, 
    #     fuel_type: str,  
    #     oil_capacity: str | None
    #     ):

        # self.power_hp = power_hp
        # self.fuel_type = fuel_type 
        # self.capacity = capacity
        # self.oil_capacity = oil_capacity
        # self.emissions_category = emissions_category