from models.car import Car
from models.fuel import Fuel
from models.tax import Tax
from models.engine import Engine
from services.scrapers.conversions import (
    tax_get_euro_category_from_car_year,
    done,
    kw_to_hp_converter,
    hp_to_kw_converter,
    validate_engine_capacity,
)
from services.scrapers.tires import get_tires_prices
from services.scrapers.tax import get_tax_price
from services.scrapers.fuel_consumption import get_fuel_consumption
from services.scrapers.fuel_prices_today import get_fuel_price
from services.scrapers.insurance import get_insurance_price
from services.scrapers.vignette import get_vignette_price
from common.exceptions import WrongCarData
from common.helpers import collection_to_dict
from datetime import datetime
from data.db_connect import read_query


def build_car(
    car_brand: str,
    car_model: str,
    car_year: str,
    car_power_hp: str,
    car_power_kw: str,
    type_fuel: str,
    engine_capacity: str,
    city: str,
    car_price: str | float = 0,
    registration: int = 0,
    driver_age: str | None = "35",
    driver_experience: str = "5",
):
    if not engine_capacity == "eev":
        engine_capacity = validate_engine_capacity(engine_capacity)
    car_power_hp = (
        kw_to_hp_converter(car_power_kw) if not car_power_hp else car_power_hp
    )
    car_power_kw = (
        hp_to_kw_converter(car_power_hp) if not car_power_kw else car_power_kw
    )

    start = datetime.now()
    car: Car | None = get_car(
        car_brand, car_model, car_year, engine_capacity, car_power_hp, type_fuel
    )
    if not car:
        raise WrongCarData()

    if not car.engine:  # create a new engine record and update the database
        new_fuel = Fuel(**collection_to_dict((type_fuel, float(0), None), Fuel))  # type: ignore
        engine_data = (
            None,
            engine_capacity,
            car_power_hp,
            car_power_kw,
            new_fuel,
            tax_get_euro_category_from_car_year(car_year),
            0,
            0,
            None,
        )
        car.engine = Engine(**collection_to_dict(engine_data, Engine))  # type: ignore

        if car.engine is not None:
            car.engine.consumption = get_fuel_consumption(car)

    if not car.engine.consumption:
        raise WrongCarData("Data for engine not found!")
    try:
        car.tires = get_tires_prices(car)
    except Exception as e:
        # return the prices of the most common tire sizes instead of *No info*
        done(str(e))
        car.tires = []

    tax_data = (
        city,
        city,
        car.year,
        car.engine.emissions_category,
        car.engine.power_kw,
        float(car.price),
    )
    car.tax = Tax(**collection_to_dict(tax_data, Tax))  # type: ignore
    if car.tax:
        car.tax.price = get_tax_price(car)
    else:
        raise ValueError("No tax data")

    car.vignette = get_vignette_price()

    car.insurance = get_insurance_price(
        car, registration, driver_age, driver_experience
    )
    if car.engine.fuel.fuel_type != "eev":
        car.engine.fuel.price = get_fuel_price(car.engine.fuel.fuel_type)
    else:
        car.engine.fuel.price = 0

    car.price = car_price

    end = datetime.now()
    diff = end - start
    print(f"Search duration: {diff}")

    return car


def get_car(
    brand: str, model: str, year: str, e_capacity: str, e_power: str, f_type: str
):
    result = next(
        iter(
            read_query(
                f"CALL `Car Expenses`.`get_car`('{brand}', '{model}', '{year}');"
            )
        ),
        None,
    )

    if not result:
        return

    car = Car.from_query(*result)

    engine_data = next(
        iter(
            read_query(
                f"""CALL `Car Expenses`.`test_get_engine`({car.id}, '{e_capacity}', {e_power}, '{f_type}');"""
            )
        ),
        None,
    )
    if engine_data:
        new_fuel = Fuel(**collection_to_dict((f_type, float(0), None), Fuel))  # type: ignore
        engine_data = list(engine_data)
        engine_data[6] = new_fuel

    car.engine = (
        Engine(**collection_to_dict(engine_data[2:], Engine)) if engine_data else None  # type: ignore
    )

    return car


async def get_car_brands():
    query = "SELECT DISTINCT brand FROM `Car Expenses`.`cars`;"
    data = [next(iter(x), "").capitalize() for x in read_query(query)]
    return data


async def get_models_by_car_brand(brand: str):
    query = f"SELECT DISTINCT model FROM `Car Expenses`.`cars` WHERE brand = '{brand}';"
    data = [next(iter(x), "") for x in read_query(query)]
    return data


async def get_years_by_car_model(brand: str, model: str):
    query = f"SELECT year FROM `car expenses`.cars WHERE brand = '{brand}' AND model = '{model}';"
    data = [next(iter(x), "") for x in read_query(query)]
    return data


async def get_cities():
    query = "SELECT name FROM `car expenses`.cities ORDER BY name ASC;"
    data = [next(iter(x), "") for x in read_query(query)]
    return data
