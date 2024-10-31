from pydantic import BaseModel


class Tax(BaseModel):
    city: str 
    municipality: str 
    car_age: str | int
    euro_category: str
    car_power_kw: str 
    price: float = 0

    @classmethod
    def get_tax_price(
        cls, city, municipality, car_age, euro_category, car_power_kw, price
    ):
        return cls(
            city=city,
            municipality=municipality,
            car_age=car_age,
            euro_category=euro_category,
            car_power_kw=car_power_kw,
            price=price,
        )
