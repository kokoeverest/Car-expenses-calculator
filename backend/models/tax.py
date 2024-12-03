from pydantic import BaseModel


class Tax(BaseModel):
    city: str
    municipality: str
    car_age: str | int
    euro_category: str
    car_power_kw: str
    price: float = 0
