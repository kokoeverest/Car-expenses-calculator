from models.car import Car
from models.insurance import Insurance
from models.tax import Tax
from models.engine import Engine
from models.tire import Tire
from services.scrapers.conversions import (
    get_euro_category_from_car_year,
    done,
    kw_to_hp_convertor,
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
import json
from datetime import datetime
from data.db_connect import read_query


def build_car(
    c_brand: str,
    c_model: str,
    c_year: str,
    c_power_hp: str,
    c_power_kw: str,
    f_type: str,
    engine_capacity: str,
    city: str,
    c_price: str | None = None,
    reg: bool = False,
    driver_age: str | None = None,
    driver_experience: str = '5',
):
    engine_capacity = validate_engine_capacity(engine_capacity)
    c_power_hp = kw_to_hp_convertor(c_power_kw) if not c_power_hp else c_power_hp
    c_power_kw = hp_to_kw_converter(c_power_hp) if not c_power_kw else c_power_kw
    
    start = datetime.now()
    car: Car | None = get_car(
        c_brand, c_model, c_year, engine_capacity, c_power_hp, f_type
    )
    if not car:
        raise WrongCarData()

    if not car.engine:  # create a new engine record and update the database
        car.engine = Engine(
            power_hp=c_power_hp,  # user input
            power_kw=c_power_kw,  # user input
            capacity=engine_capacity,  # user input
            emissions_category=get_euro_category_from_car_year(c_year),  # or user input
            fuel_type=f_type,  # user input
            consumption=None,
            oil_capacity=None,
        )
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
    car.tax = Tax(
        city=city,  # user input
        municipality=city,
        car_age=car.year,
        euro_category=car.engine.emissions_category,
        car_power_kw=car.engine.power_kw,
    )
    car.vignette = get_vignette_price()

    insurance = get_insurance_price(car, reg, driver_age, driver_experience)
    fuel_per_liter = get_fuel_price(car.engine.fuel_type)
    
    car.price = c_price

    end = datetime.now()
    diff = end - start
    print(f"Search duration: {diff}")

    return calculate_prices(car, fuel_per_liter, insurance)


def get_car(brand: str, model: str, year: str, e_capacity, e_power, f_type):
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
    car = Car.create_car(*result)

    engine_data = next(
        iter(
            read_query(
                f"""CALL `Car Expenses`.`test_get_engine`({car.id}, '{e_capacity}', {e_power}, '{f_type}');"""
            )
        ),
        None,
    )
    car.engine = Engine.from_query(*engine_data[2:]) if engine_data else None

    return car


def calculate_prices(car: Car, fuel_price, insurance: Insurance):
    if car.engine:
        fuel_per_30000_km = (fuel_price * car.engine.consumption) * 300
        fuel_per_10000_km = (fuel_price * car.engine.consumption) * 100
    else:
        raise ValueError("No engine data")

    if car.tax:
        tax_price = get_tax_price(
            [
                car.tax.city,
                car.tax.municipality,
                car.tax.car_age,
                car.tax.euro_category,
                car.tax.car_power_kw,
            ]
        )
    else:
        raise ValueError("No tax data")

    tires_max_price, tires_min_price = car.calculate_tires_price()

    total_min_price = sum(
        (tax_price, fuel_per_10000_km, tires_min_price, insurance.min_price, car.vignette),
        start=0,
    )
    total_max_price = sum(
        (tax_price, fuel_per_30000_km, tires_max_price, insurance.max_price, car.vignette),
        start=0,
    )
    car_dict = car.to_dict()

    result_min = {
        "Обща минимална цена": f"{total_min_price:.2f} лв",
        "Данък": f"{tax_price:.2f} лв",
        "Гориво за 10000 км годишен пробег": f"{fuel_per_10000_km:.2f} лв ({fuel_per_10000_km/12:.2f} лв/месец)",
        "Най-ниска цена на застраховка ГО": f"{insurance.min_price:.2f} лв (еднократно плащане)",
        "Най-евтини гуми (1 брой)": {
            str(tire): f"{tire.min_price} лв"
            for tire in car.tires
            if isinstance(tire, Tire)
        },
    }

    result_max = {
        "Обща максимална цена": f"{total_max_price:.2f} лв",
        "Данък": f"{tax_price:.2f} лв",
        "Гориво за 30000 км годишен пробег": f"{fuel_per_30000_km:.2f} лв ({fuel_per_30000_km/12:.2f} лв/месец)",
        "Най-висока цена на застраховка ГО": f"{insurance.max_price:.2f} лв (еднократно плащане)",
        "Годишна винетка": f"{car.vignette:.2f} лв",
        "Най-скъпи гуми (1 брой)": {
            str(tire): f"{tire.max_price} лв"
            for tire in car.tires
            if isinstance(tire, Tire)
        },
    }
    final_result = json.dumps(
        (car_dict, result_min, result_max),
        ensure_ascii=False,
        separators=("", " - "),
    )
    print(json.dumps(car_dict, indent=2, ensure_ascii=False, separators=("", " - ")))
    print(json.dumps(result_min, indent=2, ensure_ascii=False, separators=("", " - ")))
    print(json.dumps(result_max, indent=2, ensure_ascii=False, separators=("", " - ")))
    return final_result


