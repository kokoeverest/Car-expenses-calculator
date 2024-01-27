from models.engine import Engine
from models.tax import Tax
from models.tire import Tire
import requests
from bs4 import BeautifulSoup as bs
import os
import pickle


class Car:
    # brand: str
    # model: str
    # year: int
    # engine: Engine | None = None
    # tax: Tax | None = None
    # tires: list[Tire]|None = []
    # price: float | None = None
    # insurance: int | None = None

    # @classmethod
    # def create_car(cls, brand, model, year, engine, tax, tires, price):
    #     return cls(brand = brand,
    #                model = model,
    #                year = year,
    #                engine = engine,
    #                tax = tax, 
    #                tires = tires,
    #                price = price)
    
    def __init__(
        self, 
        brand: str,
        model: str, 
        year: str,
        tax: Tax | None = None,
        price: float | str | None = None,
        insurance: int | None = None,
        fuel_consumption: float | None = None
        ):

        self.brand = brand
        self.model = model
        self.year = year
        self.engine: Engine | None = None
        self.tax = tax 
        self.tires: list[Tire] = []
        self.price = price
        self.insurance = insurance
        self.fuel_consumption = fuel_consumption

    @property
    def _tires(self):
        if len(self.tires) > 0:
            return sorted(self.tires, key=lambda t: t.size)
        

    def __dict__(self):
        return {
            'Марка': self.brand,
            'Модел': self.model,
            'Година': self.year,
            'Двигател': self.engine.capacity or "N/A",
            'Мощност': self.engine.power_hp or "N/A",
            'Гориво': self.engine.fuel_type or "N/A",
            'Цена': self.price or 'N/A',
        }

    def get_fuel_prices(self, f_type, url='https://m.fuelo.net/m/prices'):
    
        fuels_dict = {
            'Бензин A95': 'gasoline',
            'Дизел': 'diesel',
            'Пропан Бутан': 'lpg',
            'Метан': 'cng',
            'Дизел премиум': 'premium',
            'Бензин A98': 'gasoline A98',
            'Бензин A100': 'gasoline A100'
        }
        with open(os.getcwd()+"/fuel_prices.txt", "rb") as file:
            try:
                prices = pickle.load(file)
                return prices[f_type]
            except KeyError:
                prices = pickle.load(file)
            except EOFError:
                prices = {}

        result = requests.get(url)
        soup = bs(result.text, features='lxml').find_all('h4')

        for el in soup:
            raw = el.text.split(' ')

            if len(raw) == 3: 
                fuel_type, price = str(raw[0] + ' ' + raw[1]), raw[2]
            elif len(raw) == 2:
                fuel_type, price = raw 
            else: continue

            if 'цени от' not in price:
                new_str = fuels_dict.get(fuel_type)
                fuel_type = fuel_type.replace(f'{fuel_type}', f'{new_str}')
                prices[fuel_type] = float(price.replace(',', '.').rstrip('лв.'))

        with open(os.getcwd()+"/fuel_prices.txt", "wb") as file:
            pickle.dump(prices, file)
            
        return prices[f_type]
    

    def calculate_tires_price(self):
        max_price = max(tire.max_price for tire in self.tires if tire.max_price)
        min_price = min(tire.min_price for tire in self.tires if tire.min_price)

        return max_price * 4, min_price * 4