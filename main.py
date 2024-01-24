from models.car import Car
from models.tax import Tax
from models.engine import Engine
import scrapers.tires as tires 

car: Car = Car(
    brand="Dacia",
    model="Duster",
    year="2022",
    engine=None,
    tax= None,
    tires=None,
    price="30000",
    insurance=None
)
car.tires = tires.get_tires_prices_from_file([car.brand, car.model, car.year])

engine: Engine = Engine(
    power_hp="115",
    fuel_type="petrol",
    capacity="1.5",
    oil_capacity=None,
    emissions_category="Euro 4")

car.engine = engine

tax: Tax = Tax(
    city="София",
    municipality="Столична",
    car_age=car.year,
    euro_category=car.engine.emissions_category,
    car_power_kw=car.engine.power_hp
)

# calculate fuel expenses based on the fuel consumption