from models.car import Car
from models.tax import Tax
from models.engine import Engine


car: Car = Car.create_car(
    brand="Dacia",
    model="Duster",
    year="2021",
    engine="1.5",
    price="30000"
)                                          
tax: Tax = Tax.get_tax_price(
    city="София",
    municipality="Столична",
    car_age=car.year,
    euro_category=car.engine.emissions_category,
    car_power_kw=car.engine.power
)

