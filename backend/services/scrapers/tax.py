from common.helpers import start_driver
from common.WEBSITES import TAXES_WEBSITE
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from data.db_connect import read_query, insert_query
from datetime import date
import sys

sys.path.append(".")
from models.car import Car
from services.scrapers.conversions import (
    tax_age_converter,
    calculate_euro_category,
)


def generate_car_data_dict(
    city: str, municipality: str, age: str, euro: str, power: str
):
    return {
        "obl": city,
        "obs": municipality,
        "old": tax_age_converter(age),
        "euro": calculate_euro_category(euro),
        "kw": power,
    }


def get_tax_price(car: Car):
    if car.tax:
        car_tax_data = [
            car.tax.city,
            car.tax.municipality,
            car.tax.car_age,
            car.tax.euro_category,
            car.tax.car_power_kw,
        ]

        car_tax_data[1] = next(
            iter(
                read_query(f"CALL `Car Expenses`.`get_municipality`('{car.tax.city}');")
            )
        )[0]

        tax_price = next(
            iter(
                read_query(
                    "CALL `Car Expenses`.`get_tax_price`(?, ?, ?, ?, ?);",
                    tuple(car_tax_data),
                )
            ),
            None,
        )
        if tax_price:
            return float(tax_price[0])
        else:
            return scrape_tax_price(car_tax_data)
    return 0


def scrape_tax_price(car_tax_data: list):
    print("Scraping tax price...")
    car_data_dict = generate_car_data_dict(*car_tax_data)
    with start_driver(TAXES_WEBSITE) as driver:
        for k, v in car_data_dict.items():
            try:
                el = Select(
                    driver.find_element(By.XPATH, f"//select[@name='{k}']")
                ).select_by_value(v)
            except Exception:
                # the 'kw' input field
                try:
                    el = driver.find_element(By.XPATH, f"//input[@name='{k}']")
                    el.clear()
                    el.send_keys(v)
                    el.submit()
                except Exception:
                    continue
        try:
            price = driver.find_element(By.CLASS_NAME, "amount").text.split(" ")[0]
        except IndexError:
            price = "0"

    car_tax_data.extend([float(price), date.today()])

    _ = insert_query(
        "CALL `Car Expenses`.`add_tax_price`(?,?,?,?,?,?,?);", tuple(car_tax_data)
    )

    return float(price)
