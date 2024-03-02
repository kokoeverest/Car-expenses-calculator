import requests
from bs4 import BeautifulSoup as bs
from data.db_connect import read_query, multiple_insert_queries
from datetime import date
import sys

sys.path.append(".")

FUELS_DICT = {
    "Бензин A95": "gasoline",
    "Дизел": "diesel",
    "Пропан Бутан": "lpg",
    "Метан": "cng",
    "Дизел премиум": "premium",
    "Бензин A98": "gasoline A98",
    "Бензин A100": "gasoline A100",
}


def scrape_fuel_prices(url="https://m.fuelo.net/m/prices"):
    result = requests.get(url)
    soup = bs(result.text, features="lxml").find_all("h4")
    today = date.today()
    prices = {}
    query = []
    for el in soup:
        raw: list[str] = el.text.split(" ")

        if len(raw) == 3:
            fuel_type, temp_price = " ".join((raw[0], raw[1])), raw[2]
        elif len(raw) == 2:
            fuel_type, temp_price = raw
        else:
            continue

        if "цени от" not in temp_price:
            fuel_type = FUELS_DICT.get(fuel_type)
            temp_price = float(temp_price.replace(",", ".").rstrip("лв."))
            prices[fuel_type] = temp_price
            query.append(
                f"CALL `Car Expenses`.`update_fuel_price`('{fuel_type}', {temp_price}, '{today}');"
            )

    return prices, query


def get_fuel_price(f_type) -> float:
    r_query = f"""CALL `Car Expenses`.`get_fuel_price`('{f_type}', '{date.today()}');"""
    price = read_query(r_query)

    if price:
        price = next(iter(price[0]))
        return float(price)

    prices, query = scrape_fuel_prices()

    _ = multiple_insert_queries(query)  # update the fuel prices for today
    return prices[f_type]
