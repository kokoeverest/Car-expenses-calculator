from models.car import Car
from models.tax import Tax
from models.engine import Engine
from models.insurance import InsuranceFuelValues as fuel
import scrapers.tires as tires
from scrapers.tax import get_tax_price
from scrapers.fuel_consumption import get_fuel_consumption
from scrapers.insurance import get_insurance_price
from scrapers.vignette import get_vignette_price
import json
from datetime import datetime


start = datetime.now()
car: Car = Car(
    brand="Dacia", # user input
    model="Duster", # user input
    year="2022", # user input
    price="30000", # user input /optional/
)

car.tires = tires.get_tires_prices_from_file([car.brand, car.model, car.year])

car.engine = Engine(
    power_hp="110", # user input
    fuel_type="diesel", # user input
    capacity="1500", # user input
    oil_capacity=None,
    emissions_category="Euro 4" # user input
)
car_dict = car.__dict__()
car.tax = Tax(
    "София", # user input
    "Столична", # to be extracted from the user input
    car.year,
    car.engine.emissions_category,
    car.engine.power_hp
)
car.fuel_consumption = get_fuel_consumption([
    car.brand, 
    car.model, 
    car.year, 
    car.year, 
    car.engine.fuel_type, 
    str(int(car.engine.power_hp) - 10), 
    str(int(car.engine.power_hp) + 10)
])
car.vignette = get_vignette_price()
tax_price = float(get_tax_price([
    car.tax.city, 
    car.tax.municipality, 
    car.tax.car_age, 
    car.tax.euro_category,
    car.tax.car_power_kw]))

fuel_per_liter = car.get_fuel_prices(car.engine.fuel_type)
fuel_per_15000_km = (fuel_per_liter * car.fuel_consumption) * 150
fuel_per_5000_km = (fuel_per_liter * car.fuel_consumption) * 50

tires_max_price, tires_min_price = car.calculate_tires_price()

insurance_dict = {
    'year': car.year,
    'engine_size': car.engine.capacity, # in cubic cm so 2.2 should be multiplied by 1000 -> int(2.2 * 1000)
    'fuel_type': fuel.gasoline.value,
    'power': '110', # power conversion to be implemented
    'municipality': 'София-град', # regex needed to match car.tax.city
    'registration': False,
    'driver age': None,
    'driving experience': None
    }
insurance_min, insurance_max = get_insurance_price(insurance_dict)

total_min_price = tax_price + fuel_per_5000_km + tires_min_price + insurance_min\
                + car.vignette
total_max_price = tax_price + fuel_per_15000_km + tires_max_price + insurance_max\
                + car.vignette


result_min = {
    'Обща минимална цена': f'{total_min_price:.2f} лв',
    'Данък': f'{tax_price:.2f} лв',
    'Гориво за 5000 км годишен пробег': f'{fuel_per_5000_km:.2f} лв',
    'Най-евтини гуми (1 брой)': {str(tire): f'{tire.min_price} лв' for tire in car.tires},
    'Най-ниска цена на застраховка ГО': f'{insurance_min:.2f} лв'
    }

result_max = {
    'Обща максимална цена': f'{total_max_price:.2f} лв',
    'Данък': f'{tax_price:.2f} лв',
    'Гориво за 15000 км годишен пробег': f'{fuel_per_15000_km:.2f} лв',
    'Най-скъпи гуми (1 брой)': {str(tire): f'{tire.max_price} лв' for tire in car.tires},
    'Най-висока цена на застраховка ГО': f'{insurance_max:.2f} лв',
    'Годишна винетка': f'{car.vignette:.2f} лв'
    }

print(json.dumps(car_dict, indent=2, ensure_ascii=False, separators=('', ' - ')))
print(json.dumps(result_min, indent=2, ensure_ascii=False, separators=('', ' - ')))
print(json.dumps(result_max, indent=2, ensure_ascii=False, separators=('', ' - ')))

end = datetime.now()
diff = (end - start)
print(f"Duration: {diff}")