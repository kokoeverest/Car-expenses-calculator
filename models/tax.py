class Tax:
    city: str | None
    municipality: str | None
    car_age: str | None
    euro_category: str | None
    car_power_kw: str | None


    @classmethod
    def get_tax_price(cls, city, municipality, car_age, euro_category, car_power_kw):
        return cls(city = city,
                   municipality = municipality,
                   car_age = car_age,
                   euro_category = euro_category,
                   car_power_kw = car_power_kw)