from models.car import Car
from models.tax import Tax
from models.engine import Engine


car: Car = Car.create_car(
    brand="Dacia",
    model="Duster",
    year="2021",
    engine=None,
    tax= None,
    tires=None,
    price="30000"
)

engine: Engine = Engine.create_engine(
    power_hp="115",
    fuel_type="petrol",
    capacity="1.5",
    oil_capacity=None,
    emissions_category="Euro 4")

car.engine = engine

tax: Tax = Tax.get_tax_price(
    city="София",
    municipality="Столична",
    car_age=car.year,
    euro_category=car.engine.emissions_category,
    car_power_kw=car.engine.power_hp
)

# calculate fuel expenses based on the fuel consumption