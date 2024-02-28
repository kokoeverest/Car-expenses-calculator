from models.car import Car
from models.tax import Tax
from models.engine import Engine
from models.insurance import Insurance, INSURANCE_FUEL_VALUES as fuel
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
import json
from datetime import datetime


def build_car(
    car_brand: str,
    car_model: str,
    car_year: str,
    car_power_hp: str,
    car_power_kw: str,
    fuel_type: str,
    engine_capacity: str,
    city: str,
    car_price: str | None = None,
    registration: bool = False,
    driver_age: str | None = None,
    driver_experience: str | None = None,
):
    engine_capacity = validate_engine_capacity(engine_capacity)
    car_power_hp = (
        kw_to_hp_convertor(car_power_kw) if not car_power_hp else car_power_hp
    )
    car_power_kw = (
        hp_to_kw_converter(car_power_hp) if not car_power_kw else car_power_kw
    )

    start = datetime.now()
    car: Car = Car(
        brand=car_brand,  # user input
        model=car_model,  # user input
        year=car_year,  # user input
        price=car_price,  # user input /optional/
    )
    car.engine = Engine(
        power_hp=car_power_hp,  # user input
        power_kw=car_power_kw,  # user input
        fuel_type=fuel_type,  # user input
        capacity=engine_capacity,  # user input
        oil_capacity=None,
        emissions_category=get_euro_category_from_car_year(car_year),  # or user input
    )
    try:
        print("Collecting tires prices...")
        car.tires = get_tires_prices([car.brand, car.model, car.year])
        done()
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
    print("Collecting fuel consumption...")
    car.fuel_consumption = get_fuel_consumption(
        [car.brand, car.model, car.year, car.engine.fuel_type, car.engine.power_hp]
    )
    done()
    print("Collecting vignette price...")
    car.vignette = get_vignette_price()
    done()
    print("Collecting tax price...")
    tax_price = get_tax_price(
        [
            car.tax.city,
            car.tax.municipality,
            car.tax.car_age,
            car.tax.euro_category,
            car.tax.car_power_kw,
        ]
    )

    done()

    fuel_per_liter = get_fuel_price(car.engine.fuel_type)
    fuel_per_30000_km = (fuel_per_liter * car.fuel_consumption) * 300
    fuel_per_10000_km = (fuel_per_liter * car.fuel_consumption) * 100

    tires_max_price, tires_min_price = car.calculate_tires_price()

    insurance = Insurance(
        year=car.year,
        engine_size=car.engine.capacity,
        fuel_type=fuel[fuel_type],
        power=car.engine.power_hp,
        municipality="София-град",  # regex needed to match car.tax.city
        registration=False,
        driver_age=None,
        driving_experience=None,
    )
    print("Collecting insurance price...")
    insurance_min, insurance_max = get_insurance_price(insurance.to_dict())
    done()

    total_min_price = sum(
        (tax_price, fuel_per_10000_km, tires_min_price, insurance_min, car.vignette),
        start=0,
    )
    total_max_price = sum(
        (tax_price, fuel_per_30000_km, tires_max_price, insurance_max, car.vignette),
        start=0,
    )

    car_dict = car.to_dict()
    result_min = {
        "Обща минимална цена": f"{total_min_price:.2f} лв",
        "Данък": f"{tax_price:.2f} лв",
        "Гориво за 10000 км годишен пробег": f"{fuel_per_10000_km:.2f} лв ({fuel_per_10000_km/12:.2f} лв/месец)",
        "Най-ниска цена на застраховка ГО": f"{insurance_min:.2f} лв (еднократно плащане)",
        "Най-евтини гуми (1 брой)": {
            str(tire): f"{tire.min_price} лв" for tire in car.tires
        },
    }

    result_max = {
        "Обща максимална цена": f"{total_max_price:.2f} лв",
        "Данък": f"{tax_price:.2f} лв",
        "Гориво за 30000 км годишен пробег": f"{fuel_per_30000_km:.2f} лв ({fuel_per_30000_km/12:.2f} лв/месец)",
        "Най-висока цена на застраховка ГО": f"{insurance_max:.2f} лв (еднократно плащане)",
        "Годишна винетка": f"{car.vignette:.2f} лв",
        "Най-скъпи гуми (1 брой)": {
            str(tire): f"{tire.max_price} лв" for tire in car.tires
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

    end = datetime.now()
    diff = end - start
    print(f"Search duration: {diff}")
    return final_result
