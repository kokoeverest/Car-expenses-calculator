from models.car import Car
from models.tax import Tax
from models.engine import Engine
from models.insurance import InsuranceFuelValues as fuel
from scrapers.conversions import get_euro_category_from_car_year, done
from scrapers.tires import get_tires_prices
from scrapers.tax import get_tax_price
from scrapers.fuel_consumption import get_fuel_consumption
from scrapers.insurance import get_insurance_price
from scrapers.vignette import get_vignette_price
import json
from datetime import datetime


start = datetime.now()
car: Car = Car(
    brand="Mazda",  # user input
    model="cx-5",  # user input
    year="2016",  # user input
    price="24800",  # user input /optional/
)
car.engine = Engine(
    power_hp="150",  # user input
    fuel_type="diesel",  # user input
    capacity="2191",  # user input
    oil_capacity=None,
    emissions_category=get_euro_category_from_car_year(car.year),  # or user input
)
try:
    print("Collecting tires prices...")
    car.tires = get_tires_prices([car.brand, car.model, car.year])
    done()
except Exception:
    # return the prices of the most common tire sizes instead of *No info*
    done("***Error while collecting tires prices***")
    car.tires = []

car.tax = Tax(
    "София",  # user input
    "Столична",  # to be extracted from the user input
    car.year,
    car.engine.emissions_category,
    car.engine.power_hp,
)
print("Collecting fuel consumption...")
car.fuel_consumption = get_fuel_consumption(
    [
        car.brand,
        car.model,
        car.year,
        car.year,
        car.engine.fuel_type,
        car.engine.power_hp,
        car.engine.power_hp,
    ]
)
done()
print("Collecting vignette price...")
car.vignette = get_vignette_price()
done()
print("Collecting tax price...")
tax_price = float(
    get_tax_price(
        [
            car.tax.city,
            car.tax.municipality,
            car.tax.car_age,
            car.tax.euro_category,
            car.tax.car_power_kw,
        ]
    )
)
done()

fuel_per_liter = car.get_fuel_prices(car.engine.fuel_type)
fuel_per_30000_km = (fuel_per_liter * car.fuel_consumption) * 300
fuel_per_10000_km = (fuel_per_liter * car.fuel_consumption) * 100

tires_max_price, tires_min_price = car.calculate_tires_price()

insurance_dict = {
    "year": car.year,
    "engine_size": car.engine.capacity,  # in cubic cm so 2.2 should be multiplied by 1000 -> int(2.2 * 1000)
    "fuel_type": fuel.gasoline.value,
    "power": car.engine.power_hp,  # power conversion to be implemented
    "municipality": "София-град",  # regex needed to match car.tax.city
    "registration": False,
    "driver age": None,
    "driving experience": None,
}
print("Collecting insurance price...")
insurance_min, insurance_max = get_insurance_price(insurance_dict)
done()

total_min_price = sum(
    (tax_price, fuel_per_10000_km, tires_min_price, insurance_min, car.vignette), start=0
)
total_max_price = sum(
    (tax_price, fuel_per_30000_km, tires_max_price, insurance_max, car.vignette), start=0
)


car_dict = car.__dict__()
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

print(json.dumps(car_dict, indent=2, ensure_ascii=False, separators=("", " - ")))
print(json.dumps(result_min, indent=2, ensure_ascii=False, separators=("", " - ")))
print(json.dumps(result_max, indent=2, ensure_ascii=False, separators=("", " - ")))

end = datetime.now()
diff = end - start
print(f"Search duration: {diff}")