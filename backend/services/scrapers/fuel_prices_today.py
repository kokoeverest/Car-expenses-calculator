import requests
from data.db_connect import read_query, multiple_insert_queries
from datetime import date
from data.api_keys import FUELO_API_KEY
import sys

sys.path.append(".")

FUELS_DICT = {
    "Бензин A95": "gasoline",
    "Дизел": "diesel",
    "Пропан Бутан": "lpg",
    "Метан": "methane",
    # "Метан": "cng",
    # "Дизел премиум": "dieselplus",
    # "Бензин A98": "gasoline98",
    # "Бензин A100": "gasoline98plus",
}

FUELO_URL = f"http://fuelo.net/api/price?key={FUELO_API_KEY}&fuel="


def scrape_fuel_prices(url=FUELO_URL):
    print("Scraping fuel prices for the first time today...")
    prices = {}
    query: list[str] = []

    for fuel in FUELS_DICT.values():
        temp_result: dict[str, str | float] = requests.get(f"{url}{fuel}").json()

        if temp_result.get("status") == "OK":
            prices[fuel] = temp_result.get("price")
            query.append(
                f"CALL `Car Expenses`.`update_fuel_price`('{fuel}', {prices[fuel]}, '{temp_result['date']}');"
            )

    return prices, query


def get_fuel_price(f_type) -> float:
    r_query = f"""CALL `Car Expenses`.`get_fuel_price`('{f_type}', '{date.today()}');"""
    price = read_query(r_query)

    if price:
        price = next(iter(price[0]))
        return float(price)

    prices, query = scrape_fuel_prices()

    if prices:
        _ = multiple_insert_queries(query)  # update the fuel prices for today
        return prices[f_type]
    else:
        last_known_prices = "CALL `Car Expenses`.`get_last_known_fuel_prices`();"
        prices: dict[str, float] = {el[0]: el[1] for el in read_query(last_known_prices)}
        return prices[f_type]
